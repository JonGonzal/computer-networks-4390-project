# ComputerNetworks-4390-Project

Website to view Yu-Gi-Oh! cards using python's sockets library, some html with inline JS, and sqlite3.


# How to access the application


1. Clone the directory: `git@github.com:JonGonzal/computer-networks-4390-project.git`

## Server side:

2. In the root folder: `python3 -m server.main`
- You will see listening on 127.0.0.1:8080


## Client side:

1. `python3 client/src/client.py 127.0.0.1 8080 index.jpg GET`

2. `python3 client/src/client.py 127.0.0.1 8080 index.jpg POST`

3. `python3 client/src/client.py 127.0.0.1 8080 index.jpg PUT`

4. `python client/src/client.py 127.0.0.1 8080 index.html GET -d 200`
    - This will run the DoS attack

## Web UI 

While the server is running, go to this site via a webbrowser `http://127.0.0.1:8080`. Here you will find the webpage allowing you to search cards by name.

<img width="1382" height="1470" alt="image" src="https://github.com/user-attachments/assets/0787294c-9472-4812-bbd6-a7aa627faf84" />
