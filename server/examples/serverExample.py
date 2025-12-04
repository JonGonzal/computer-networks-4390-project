import socket

HOST = '127.0.0.1'
PORT = 4005

s = socket.socket()


s.bind((HOST, PORT))

s.listen(5)

c, addr = s.accept()
print("Got connectino from" , addr)

c.close()
