import socket
import threading
import os

HOST = "127.0.0.1"
PORT = 5000
BUFFER_SIZE = 1024

def start_server():
    # Create socket object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Set socket option to allow address reuse
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind server to HOST and PORT
    server.bind((HOST, PORT))
    # Allows for <=5 clients waiting in queue
    server.listen(5)
    print("Server is live and waiting for connections...")
    # Accept a connection
    client_socket, client_address = server.accept()
    print(f"Connection from {client_address}")
    # Start a thread with target recieve from the client
    threading.Thread(target=receive, args=(client_socket,)).start()
    # Send message from server to client
    send(client_socket, "Server")

def receive(client_socket):
    while True:
        try:
            m = client_socket.recv(BUFFER_SIZE).decode('utf-8')
            if m.startswith("FT"):
                _, fname, fsize = m.split(':')
                fsize = int(fsize)
                with open(fname, 'wb') as file:
                    while fsize > 0:
                        chunk = client_socket.recv(min(BUFFER_SIZE, fsize))
                        file.write(chunk)
                        fsize -= len(chunk)
                print(f"Received file: {fname}")
                if fname.endswith('.txt'):
                    with open(fname, 'r') as file:
                        print(file.read())
            else:
                print(m)
        except:
            print("Error recieve() in server.py")
            break

def send(client_socket, app_name):
    while True:
        m = input(f"{app_name}: ")
        if m.startswith("SEND"):
            fpath = m.split(' ')[1]
            if os.path.exists(fpath):
                fsize = os.path.getsize(fpath)
                client_socket.send(f"FT:{os.path.basename(fpath)}:{fsize}".encode('utf-8'))                
                with open(fpath, 'rb') as file:
                    while (chunk := file.read(BUFFER_SIZE)):
                        client_socket.send(chunk)
                print(f"Sent file: {fpath}")
            else:
                print("File not found...")
        else:
            client_socket.send(m.encode('utf-8'))

if __name__ == "__main__":
    start_server()