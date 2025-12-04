import os
from server.config import settings
from server.models import visitor_model


def handle_reqs(raw_reqs, ip):
    try:
        header_split, body = raw_reqs.split('\r\n\r\n', 1)
    except ValueError:
        return "HTTTP/1.0 400 Bad Request\r\n\r\n".encode()
    
    lines = header_split.split('\r\n')
    request_lines = lines[0].split()

    if len(request_lines) < 2:
        return "HTTTP/1.0 400 Bad Request\r\n\r\n".encode()
    
    method, path = request_lines[0], request_lines[1]

    user_agent = "Anonymous"
    for line in lines:
        if line.lower().startswith("user-agent:"):
            user_agent = line.split(":", 1)[1].strip()

    
    visitor_model.track_visitors(ip, user_agent)

    fileName = path.lstrip('/')
    if fileName == "":
        fileName = "index.html"

    fileName = os.path.join(settings.UPLOAD_DIRECTORY, fileName)

    # GET and HEAD 

    if method in ['GET', 'HEAD']:
        if os.path.exists(fileName) and os.path.isfile(fileName)




