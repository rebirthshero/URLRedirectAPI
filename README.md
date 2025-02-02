# URLRedirectAPI

activate virtual env: URLRedirectAPI\venv\Scripts\activate.bat

API Documentation
1. Create Short URL

URL: /shorten
Method: POST
Request: (key= original_url)
JSON: { "original_url": "https://irisho0128.pixnet.net/blog/post/74854062" }
Response:
{
    "expiration_date": "2025-03-05",
    "reason": "URL successfully shortened",
    "short_url": "http://localhost:5000/361f7f28e539",
    "success": true
}

2. Redirect Using Short URL

URL: /<short_url>
Method: GET
Response:
Sample: http://localhost:5000/bb1a9f65e0af
Success: Redirects to the original URL. ()
Error (404): { "error": "Short URL not found" }
Error (410): { "error": "URL expired" }