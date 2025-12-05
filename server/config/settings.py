import os 

HOST = "127.0.0.1"
PORT = 8080


BASE_DIRECTORY = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UPLOAD_DIRECTORY = os.path.join(BASE_DIRECTORY, 'upload')
VISITORS_DOC = os.path.join(BASE_DIRECTORY, 'server', 'models', 'visitors.json')


# DoS Prevention - #6 in requirements doc.
DDOS_LIMIT = 30
DDOS_WINDOW = 60

