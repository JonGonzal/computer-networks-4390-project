import os
from server.config import settings
from server.models import visitor_model


def handle_reqs(raw_reqs, ip):
    try:
        header_split, body = raw_reqs.split('\r\n\r\n', 1)
    except ValueError:
        return "HTTP/1.0 400 Bad Request\r\n\r\n".encode()
    
    lines = header_split.split('\r\n')
    request_lines = lines[0].split()

    if len(request_lines) < 2:
        return "HTTP/1.0 400 Bad Request\r\n\r\n".encode()
    
    method, path = request_lines[0], request_lines[1]

    user_agent = "Anonymous"
    for line in lines:
        if line.lower().startswith("user-agent:"):
            user_agent = line.split(":", 1)[1].strip()

    
    visitor_model.track_visitors(ip, user_agent)

    fileName = path.lstrip('/')
    if fileName == "":
        fileName = "index.html"

    filePath = os.path.join(settings.UPLOAD_DIRECTORY, fileName)

    # GET and HEAD 

    if method in ['GET', 'HEAD']:
        if os.path.exists(fileName) and os.path.isfile(fileName):
            with open(fileName, 'rb') as f:
                content = f.read()

            response = "HTTP/1.0 200 OK\r\n"
            response = f"Content-Length: {len(content)}\r\n\r\n"

            if method = 'GET':
                return response.encode() + content
            else:
                return response.encode()
        else:
            return "HTTP/1.0 404 NOT FOUND\r\n\r\n".encode()

    elif method in ['POST', 'PUT']:
        try:
            if not os.path.exists(settings.UPLOAD_DIRECTORY):
                os.makedirs(settings.UPLOAD_DIRECTORY)

            with open(filePath, 'wb') as f:
                f.write(body.encode('utf-8'))

            return "HTTP/1.0 200 OK\r\n\r\n File Uploaded!".encode()
        except Exception as e:
            return f"HTTP/1.0 500 Internal ERROR\r\n\r\n{str(e)}".encode()

    return f"HTTP/1.0 501 NOT Implemented\r\n\r\n".encode()
