import socket
import os
import threading
from server.config import settings
from server.middleware import security
from server.controllers import main_controller
from server.models import visitor_model


def handle_client(conn, addr):
    ip = addr[0]
    print(f"Incoming connection from {ip}")

    conn.settimeout(5)

    if not security.check_dos(ip):
        conn.close()
        return

    try:
        request_data = conn.recv(8192).decode('utf-8', errors='ignore')
        if not request_data:
            return

        response_bytes = main_controller.handle_reqs(request_data, ip)
        conn.sendall(response_bytes)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Makes sure the connection is closed regardless of failure or success.
        conn.close()


def start():
    visitor_model.load_data()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((settings.HOST, settings.PORT))
    server.listen(5)
    print(f"Server is listening on {settings.HOST}:{settings.PORT}")
    print(f"Servering files from {settings.UPLOAD_DIRECTORY}")

    try:
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.daemon = True
            thread.start()
    except KeyboardInterrupt:
        print("\n Closing down...")
        visitor_model.save_data()
        server.close()
