import json
import os
import threading
from datetime import datetime
# Importing code from settings.py 
from server.config import settings


visitors = {}
lock = threading.Lock()


def load_data():
    global visitors
    if os.path.exists(settings.VISITORS_DOC):
        with open(settings.VISITORS_DOC, 'r') as f:
            try: 
                visitors = json.load(f)
            except json.JSONDecodeError:
                visitors = {}

def save_data():
    with lock:
        with open(settings.VISITORS_DOC, 'w') as f:
            json.dump(visitors, f, indent=4)

# Using this to track visitors by IP
def track_visitors(ip, user_agent):
    key= f"{ip}_{user_agent}"
    with lock:
        if key not in visitors:
            visitors[key] = {'count': 0, 'lasttime_visited': ''}
        visitors[key]['count'] += 1
        visitors[key]['lasttime_visited']= str(datetime.now())

        with open(settings.VISITORS_DOC, 'w') as f:
            json.dump(visitors, f, indent=4)
