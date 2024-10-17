import socket
import threading
import os

HOST = "127.0.0.1"
PORT = 5000
BUFFER_SIZE = 1024

def start_client():
    # Create socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to server using HOST and PORT
    client.connect((HOST, PORT))
    # Start a thread with target receive from the server
    threading.Thread(target=receive, args=(client,)).start()
    # Send message from client to server
    send(client, "Client")

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
            print("Error recieve() in client.py")
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
    start_client()