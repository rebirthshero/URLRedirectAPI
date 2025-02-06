# URLRedirectAPI

## API Documentation

### 1. Create Short URL

URL: /shorten
Method: POST

Request Body:
JSON: { "original_url": "https://irisho0128.pixnet.net/blog/post/74854062" }

* Response(success):
{
    "expiration_date": "2025-03-08",
    "reason": "URL successfully shortened",
    "short_url": "http://127.0.0.1:8000/361f7f28e539",
    "success": true
}

or 
 *(if url was shorten and expiration date is valid.)
{
    "expiration_date": "2025-03-08",
    "short_url": "http://127.0.0.1:8000/361f7f28e539",
    "success": true
}



*Response(error 400):
{
    "reason": "Missing 'original_url' field.",
    "success": false
}


 
*Response(error 400):
{
    "reason": "Missing 'URL should be less than 2048.",
    "success": false
}



*Response(error 400):
{
    "reason": "Invalid URL.",
    "success": false
}




### 2. Redirect Using Short URL

URL: /<short_url>
Method: GET
Response:
Sample: http://127.0.0.1:8000/361f7f28e539
*Success: Redirects to the original URL.

*Response(error 404):
{
    "reason": "Short URL is missing",
    "success": false

}

*Response(error 410):
{
    "reason": "Short URL has expired.",
    "success": false

}
