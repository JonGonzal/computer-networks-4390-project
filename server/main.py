import sys
import os

# Allows us to get all the import modules we need
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from server.sockets import server_sockets

if __name__ == "__main__":
    server_sockets.start()


