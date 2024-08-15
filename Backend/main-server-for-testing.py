from cryptography.fernet import Fernet
import os, socket, sqlite3


def generate_key():
    return Fernet.generate_key()

def save_key(user_name,key):
    user_folder=f"{user_name}"
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
    key_file_path=os.path.join(user_folder,f"{user_name}_key.key")
    with open(key_file_path,"wb") as key_file:
        key_file.write(key)

def load_key(user_name):
    key_file_path=os.path.join(user_name,f"{user_name}_key.key")
    if os.path.exists(key_file_path):
        with open(key_file_path,"rb") as key_file:
            return key_file.read()
    else:
        key=generate_key()
        save_key(user_name,key)
        return key


def encrypt_data(user_name,data):
    key=load_key(user_name)
    cipher_suite=Fernet(key)
    return cipher_suite.encrypt(data.encode()).decode()

def decrypt_data(user_name,encrypted_data):
    key=load_key(user_name)
    cipher_suite=Fernet(key)
    try:
        return cipher_suite.decrypt(encrypted_data.encode()).decode()
    except Exception as e:
        return ""
    

SERVER_IP="localhost"
SERVER_PORT=8080
TEMP_SERVER_IPS=[
    
]
#add temp server ip and ports when ready

active_temp_servers={ip:[] for ip in TEMP_SERVER_IPS}


def create_user_db(user_name):
    user_folder=f"{user_name}"
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
    user_db_path=os.path.join(user_folder,f"{user_name}.db")
    conn_user_db=sqlite3.connect(user_db_path)
    cursor_user_db=conn_user_db.cursor()
    #add info tables when ready


def create_server_db():
    conn=sqlite3.connect("server_db.db")
    cursor=conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   first_name TEXT NOT NULL,
                   last_name TEXT NOT NULL,
                   username TEXT UNIQUE NOT NULL,
                   email TEXT UNIQUE NOT NULL,
                   password TEXT NOT NULL,
                   security_code TEXT NOT NULL
                   )""")
    conn.commit()
    conn.close()


def find_available_temp_server():
    for ip,port in TEMP_SERVER_IPS:
        if len(active_temp_servers[(ip,port)])<5:
            return ip,port
    return None


def handle_client(client_socket):
    conn=sqlite3.connect("server_db.db")
    cursor=conn.cursor()

    try:
        while True:
            request=client_socket.recv(1024).decode()
            if not request:
                break

            command,*args=request.split("|")

            if command=="REGISTER":
                first_name, last_name, username, email, password, confirm_password, security_code, confirm_security_code=args
                if password != confirm_password:
                    client_socket.send("Passwords do not match.".encode())
                    continue
                if security_code != confirm_security_code:
                    client_socket.send("Security codes do not match.".encode())
                
                cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?",(username,email))
                if cursor.fetchone():
                    client_socket.send("Username or email already exists.".encode())
                else:
                    user_name=f"{first_name}_{last_name}"
                    cursor.execute("INSERT INTO users (first_name, last_name, username, email, password, security_code) VALUES (?, ?, ?, ?, ?, ?)", (first_name, last_name, username, email, encrypt_data(user_name, password),encrypt_data(user_name,security_code)))
                    conn.commit()

                    create_user_db(user_name)
                    client_socket.send(f"Registration successful.")

            elif command=="LOGIN":
                username,password=args
                cursor.execute("SELECT password, first_name, last_name FROM users WHERE username = ?",(username,))
                record=cursor.fetchone()
                if record:
                    stored_password,first_name,last_name=record
                    user_name=f"{first_name}_{last_name}"
                    if decrypt_data(user_name,stored_password)==password:
                        user_db=os.path.join(user_name,f"{user_name}.db")
                        temp_server=find_available_temp_server()
                        if temp_server:
                            ip,port=temp_server
                            active_temp_servers[temp_server].append(client_socket)
                            client_socket.send(f"LOGIN_SUCCESS|{user_db}|{ip}|{port}".encode())
                        else:
                            client_socket.send("No temporary servers available.".encode())
                    else:
                        client_socket.send("Invalid password".encode())
                else:
                    client_socket.send("Username not found.".encode())
    
    except Exception as e:
        client_socket.send(f"Error: {str(e)}".encode())
    finally:
        conn.close()
        client_socket.close()


def start_server():
    server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP,SERVER_PORT))
    server_socket.listen(5)
    print(f"Sever listening on {SERVER_IP}:{SERVER_PORT}")

    while True:
        client_socket,addr=server_socket.accept()
        print(f"Connection from {addr}")
        handle_client(client_socket)


if __name__=="__main__":
    create_server_db()
    start_server()