from flask_sqlalchemy import SQLAlchemy
from flask import Flask, globals, request, jsonify, redirect, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import date, timedelta, datetime
import hashlib
import os
import re

db_path = os.path.join(os.path.abspath(os.getcwd()), "tmp_test.db")


app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + db_path
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_pre_ping": True,
    "pool_recycle": 30,
    'pool_timeout': 60,
    'pool_size': 10,
    'max_overflow': 5,
}

db = SQLAlchemy(app)
limiter = Limiter(get_remote_address, app=app)


class URLMapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(2048), nullable=False)
    short_url = db.Column(db.String(20), unique=True, nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=False)


def is_valid_url(url):
    url_regex = re.compile(r'^(https?://)?([a-zA-Z0-9.-]+)(:[0-9]+)?(/.*)?$')
    return re.match(url_regex, url) is not None


# API 1: Create short URL
@app.route('/shorten', methods=['POST'])
@limiter.limit("5/minute")
def shorten_url():

    data = globals.request.get_json()
    if not data or 'original_url' not in data:
        return jsonify({"success": False, "reason": "Missing 'original_url' field."}), 400

    original_url = data['original_url']

    if len(original_url) > 2048:
        return jsonify({"success": False, "reason": "URL should be less than 2048."}), 400

    if not is_valid_url(original_url):
        return jsonify({"success": False, "reason": "Invalid URL."}), 400

    existing_mapping = URLMapping.query.filter_by(original_url=original_url).first()

    if existing_mapping:
        expiration_date = existing_mapping.expiration_date.date()
        delta = expiration_date - date.today()
        if delta.days >= 0:
            return jsonify({
                "success": True,
                "short_url": f"http://127.0.0.1:8000/{existing_mapping.short_url}",
                "expiration_date": existing_mapping.expiration_date.isoformat()
            }), 200

    short_url = hashlib.md5(original_url.encode()).hexdigest()[:12]
    expiration_date = date.today() + timedelta(days=30)
    url_mapping = URLMapping(original_url=original_url, short_url=short_url, expiration_date=expiration_date)
    db.session.add(url_mapping)
    db.session.commit()

    return jsonify({
        "success": True,
        "short_url": f"http://127.0.0.1:8000/{short_url}",
        "expiration_date": expiration_date.isoformat(),
        "reason": "URL successfully shortened"
    }), 201


# API 2: Redirect Using Short URL (GET /<short_url>)
@app.route('/<short_url>', methods=['GET'])
def redirect_url(short_url):

    url_mapping = URLMapping.query.filter_by(short_url=short_url).first()

    if not url_mapping:
        return jsonify({"success": False, "reason": "Short URL is missing"}), 404

    if url_mapping:
        expiration_date = url_mapping.expiration_date.date()
        delta = expiration_date - date.today()
        if delta.days < 0:
            return jsonify({"success": False, "reason": "Short URL has expired."}), 410

    return redirect(url_mapping.original_url)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=8000, debug=True)

