import os
import json
import sqlite3 
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

    if path.startswith("/api/search"):
        try:
            if '?q=' not in path:
                return "HTTP/1.0 400 Bad Request\r\n\r\nMissing query".encode()

            query_parts = path.split('?q=')
            search_term = query_parts[1].replace('%20', ' ').replace('+', ' ')

            db_path = os.path.join(settings.BASE_DIRECTORY, 'server', 'models', 'yugioh.db')

            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT Card_name, \"Other names\", Image_name FROM yugioh WHERE Card_name LIKE ? LIMIT 10", (f"%{search_term}%",))
                rows = cursor.fetchall()

            results = [{"name": r[0], "desc": r[1], "image": r[2]} for r in rows]
            json_resp = json.dumps(results)
            print(json_resp)

            return (f"HTTP/1.0 200 OK\r\nContent-Type: application/json\r\nContent-Length: {len(json_resp)}\r\n\r\n{json_resp}").encode()
        except Exception as e:
            print(f"ERROR - {e}")
            return f"HTTP/1.0 500 Error\r\n\r\n{str(e)}".encode()


    if path.startswith("/card_images/"):
        image_name = path.split("/")[-1]
        
        image_path = os.path.join(settings.BASE_DIRECTORY, 'database', 'Yugi_images', image_name)
        print(image_path)
        
        if os.path.exists(image_path):
            with open(image_path, 'rb') as f:
                img_data = f.read()
            header = f"HTTP/1.0 200 OK\r\nContent-Type: image/jpeg\r\nContent-Length: {len(img_data)}\r\n\r\n"
            return header.encode() + img_data
        else:
            return "HTTP/1.0 404 Not Found\r\n\r\nImage Not Found".encode()

    fileName = path.lstrip('/')

    if fileName == "" or fileName is None:
        fileName = "index.html"

    filePath = os.path.join(settings.UPLOAD_DIRECTORY, fileName)

    # GET and HEAD 
    if method in ['GET', 'HEAD']:
        if os.path.exists(filePath) and os.path.isfile(filePath):
            with open(filePath, 'rb') as f:
                content = f.read()

            response = "HTTP/1.0 200 OK\r\n"
            response += f"Content-Length: {len(content)}\r\n\r\n"

            if method == 'GET':
                return response.encode() + content
            else:
                return response.encode()
        else:
            error_body = """
            <html>
                <head><title>404 Not Found</title></head>
                <body style="font-family:sans-serif; text-align:center; padding:50px;">
                    <h1 style="color:red;">404 Not Found</h1>
                    <p>File: <b>{}</b> could not be found on this server.</p>
                </body>
            </html>
            """.format(fileName)

            response = "HTTP/1.0 404 Not Found\r\n"
            response += "Content-Type: text/html\r\n"
            response += f"Content-Length: {len(error_body)}\r\n"
            response += "\r\n"

            return response.encode() + error_body.encode()

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
