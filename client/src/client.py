import socket 
import sys
import os
import time


# Constants for the files we will be accessing
CURR_DIR = os.path.dirname(os.path.abspath(__file__))
PROJ_ROOT = os.path.dirname(os.path.dirname(CURR_DIR))
DOWN_DIR = os.path.join(PROJ_ROOT, 'downloads')


def send_request(host, port, filename, method, dos_mode=False):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))


        body = ""
        if method in ['POST', 'PUT']:
            file_path = os.path.join(DOWN_DIR, filename)
            if not os.path.exists(file_path):
                print(f"ERROR - File is not found: {file_path}")
                client_socket.close()
                return

            with open(file_path, 'r') as f:
                body = f.read()


        request =  f"{method} / {filename} HTTP/1.0\r\n"
        request += f"Host: {host}\r\n"
        request += f"User-Agent: TerminalClient/1.0\r\n"
        request += f"Content-Length: {len(body)}\r\n"
        request += "\r\n"
        request += body

        client_socket.sendall(request.encode())

        if dos_mode:
            client_socket.close()
            return

        response_data = b""
        while True:
            chunk = client_socket.recv(4096)
            if not chunk:
                break
            response_data += chunk

        
        response_str = response_data.decode('utf-8', errors='ignore')

        if "\r\n\r\n" in response_str:
            headers, content = response_str.split("\r\n\r\n", 1)
        else:
            headers, content = response_str, ""
        
        print("\n Server Headers ")
        print(headers)

        if method == 'GET' and "200 OK" in headers:
            if not os.path.exists(DOWN_DIR):
                os.makedirs(DOWN_DIR)

            save_path = os.path.join(DOWN_DIR, filename)

            header_end_index = response_data.find(b'\r\n\r\n') + 4
            file_bytes = response_data[header_end_index:]
    
            with open(save_path, 'wb') as f:
                f.write(file_bytes)

            print(f"\n SUCCESS - File saved to: {save_path}")
    
    except Exception as e:
        print(f'ERROR - Connection failed: {e}')
    finally:
        client_socket.close()



if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("How to use:\n python3 client.py <host> <port> <filename> <command> [-d <count>]")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    filename = sys.argv[3]
    command = sys.argv[4].upper()

    dos_count = 0 
    if '-d' in sys.argv:
        try:
            d_index = sys.argv.index('-d')
            if d_index + 1 < len(sys.argv):
                dos_count = int(sys.argv[d_index + 1])
            else:
                # this is the default for fast testing
                dos_count  = 200
        except ValueError as e:
            print(e)
            dos_count = 0

    if dos_count > 0:
        print(f" ~~~~ DOS ATTACK INCOMING!!! {dos_count} requests ~~~~ ")
        start_time = time.time()
        for i in range(dos_count):
            print(f"Sending request {i+1}/{dos_count}....", end='\r')
            send_request(host, port, filename, command, dos_mode=True)
        print(f"\n ~~~~ DOS ATTACK COMPLETED in {time.time() - start_time:.2f}s ~~~~ ")
    else:
        send_request(host, port, filename, command)
