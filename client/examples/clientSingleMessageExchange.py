import socket


HOST = '127.0.0.1'
PORT = 4005

#What do ?
s = socket.socket()
s.connect((HOST,PORT))

# What is recv and 1024? Is 1024 the max size of the message in bit?
print(s.recv(1024).decode())

s.send("Okay, bye!".encode())

s.close()




