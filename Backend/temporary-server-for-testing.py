import socket, threading


TEMP_SERVER_IP="localhost"
TEMP_SERVER_PORT=8080
MAX_CLIENTS=5


clients=[]


def handle_client(client_socket):
    try:
        while True:
            message=client_socket.recv(1024).decode()
            if not message:
                break
            print(f"Recieved message: {message}")
            client_socket.send(f"Message recieved: {message}".encode())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        if client_socket in clients:
            clients.remove(client_socket)


def start_temp_server():
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((TEMP_SERVER_IP,TEMP_SERVER_PORT))
    server.listen()
    print(f"Temporary server listening on {TEMP_SERVER_IP}:{TEMP_SERVER_PORT}")

    while True:
        if len(clients)<MAX_CLIENTS:
            client_socket,addr=server.accept()
            print(f"Accepted connection from {addr}")
            clients.append(client_socket)
            threading.Thread(target=handle_client,args=(client_socket,)).start()
        else:
            print("Server is full. Can not accept more clients.")


if __name__=="__main__":
    start_temp_server()