import time
import threading
from server.config import settings


# Variables to store, see, and for future handling of banned IPs.
request_log = {}
banned_ips = set()
lock = threading.Lock()


def check_dos(ip):
    curr_time = time.time()
    with lock:
        if ip in banned_ips:
            # Rejects banned IP's from connecting
            return False

        if ip not in request_log:
            request_log[ip] = []
        
        request_log[ip].append(curr_time)
        
        # Excludes old requests based on the window - see 'DDOS_WINDOW' variable for time.
        request_log[ip] = [con for con in request_log[ip] if curr_time - con <= settings.DDOS_WINDOW]
    
        if len(request_log[ip]) > settings.DDOS_LIMIT:
            print(f"[DDOS prevention->] This IP will be banned: {ip}" )
            banned_ips.add(ip)
            return False

    # If the above don't pertain, allow the connection.
    return True
