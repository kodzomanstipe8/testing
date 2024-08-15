from tkinter import *
from tkinter import messagebox, ttk
import json, socket


SERVER_IP="localhost"
SERVER_PORT=8080


class Login:
    def __init__(self,root):
        self.root=root
        self.root.geometry("400x500")
        self.root.resizable(0,0)
        self.root.title("PassLock Testing")

        self.username_l=Label(self.root,bd=0,relief=RIDGE,text="USERNAME",justify=CENTER)
        self.username_l.place(x=10,y=10,width=380,height=15)

        self.username_e=Entry(self.root,bd=1,relief=RIDGE,justify=CENTER)
        self.username_e.place(x=30,y=30,width=340,height=30)


        self.password_l=Label(self.root,bd=0,relief=RIDGE,text="PASSWORD",justify=CENTER)
        self.password_l.place(x=10,y=80,width=380,height=15)

        self.password_e=Entry(self.root,bd=1,relief=RIDGE,justify=CENTER)
        self.password_e.place(x=30,y=100,width=340,height=30)


        self.login_b=Button(self.root,bd=1,relief=RIDGE,text="LOGIN",justify=CENTER,command=self.login)
        self.login_b.place(x=100,y=150,width=200,height=25)

        self.register_b=Button(self.root,bd=1,relief=RIDGE,text="REGISTER",justify=CENTER,command=self.open_registration_page)
        self.register_b.place(x=100,y=200,width=200,height=25)

    
    def send_to_server(self,message):
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as client_socket:
            client_socket.connect((SERVER_IP,SERVER_PORT))
            client_socket.send(message.encode())
            response=client_socket.recv(1024).decode()

    
    def login(self):
        username=self.username_e.get()
        password=self.password_e.get()
        if not username or not password:
            messagebox.showerror("PassLock Testing","Please enter your username and password.")
            return
        
        message=f"LOGIN|{username}|{password}"
        response=self.send_to_server(message)
        if response.startswith("LOGIN_SUCCESS"):
            _, user_db, temp_server_ip, temp_server_port=response.split("|")
            messagebox.showinfo("PassLock Testing","Login Successful.")
            self.root.destroy()
        else:
            messagebox.showerror("Login error.",response)
            self.open_user_app(user_db, temp_server_ip, temp_server_port)


    def open_user_app(self,user_db,temp_server_ip,temp_server_port):
        user_app=Tk()
        PassLock_Testing(user_app,user_db,temp_server_ip,temp_server_port)
        user_app.mainloop()

    
    def open_registration_page(self):
        self.root.destroy()
        register_page=Tk()
        Register(register_page)



class Register:
    def __init__(self,root):
        self.root=root
        self.root.geometry("630x500")
        self.root.resizable(0,0)
        self.root.title("PassLock Testing")

        self.firstname_l=Label(self.root,bd=0,relief=RIDGE,anchor=W,text="FIRST NAME")
        self.firstname_l.place(x=10,y=10,width=300,height=15)

        self.firstname_e=Entry(self.root,bd=1,relief=RIDGE)
        self.firstname_e.place(x=10,y=30,width=300,height=30)


        self.lastname_l=Label(self.root,bd=0,relief=RIDGE,anchor=W,text="LAST NAME")
        self.lastname_l.place(x=10,y=80,width=300,height=15)

        self.lastname_e=Entry(self.root,bd=1,relief=RIDGE)
        self.lastname_e.place(x=10,y=100,width=300,height=30)


        self.username_l=Label(self.root,bd=0,relief=RIDGE,anchor=W,text="USERNAME")
        self.username_l.place(x=10,y=150,width=300,height=15)

        self.username_e=Entry(self.root,bd=1,relief=RIDGE)
        self.username_e.place(x=10,y=170,width=300,height=30)


        self.email_l=Label(self.root,bd=0,relief=RIDGE,anchor=W,text="EMAIL")
        self.email_l.place(x=10,y=220,width=300,height=15)

        self.email_e=Entry(self.root,bd=1,relief=RIDGE)
        self.email_e.place(x=10,y=240,width=300,height=30)


        self.password_l=Label(self.root,bd=0,relief=RIDGE,anchor=W,text="PASSWORD")
        self.password_l.place(x=320,y=10,width=300,height=15)

        self.password_e=Entry(self.root,bd=1,relief=RIDGE)
        self.password_e.place(x=320,y=30,width=300,height=30)

        
        self.confirm_password_l=Label(self.root,bd=0,relief=RIDGE,anchor=W,text="CONFIRM PASSWORD")
        self.confirm_password_l.place(x=320,y=80,width=300,height=15)

        self.confirm_password_e=Entry(self.root,bd=1,relief=RIDGE)
        self.confirm_password_e.place(x=320,y=100,width=300,height=30)


        self.security_code_l=Label(self.root,bd=0,relief=RIDGE,anchor=W,text="SECURITY CODE")
        self.security_code_l.place(x=320,y=150,width=300,height=15)
        
        self.security_code_e=Entry(self.root,bd=1,relief=RIDGE)
        self.security_code_e.place(x=320,y=170,width=300,height=30)


        self.confirm_security_code_l=Label(self.root,bd=0,relief=RIDGE,anchor=W,text="CONFIRM SECURITY CODE")
        self.confirm_security_code_l.place(x=320,y=220,width=300,height=15)

        self.confirm_security_code_e=Entry(self.root,bd=1,relief=RIDGE)
        self.confirm_security_code_e.place(x=320,y=240,width=300,height=30)


        self.register_b=Button(self.root,bd=1,relief=RIDGE,text="REGISTER",command=self.register)
        self.register_b.place(x=215,y=360,width=200,height=25)

        self.back_to_login_b=Button(self.root,bd=1,relief=RIDGE,text="BACK TO LOGIN",command=self.open_login_page)
        self.back_to_login_b.place(x=215,y=405,width=200,height=25)


    def send_to_server(self,message):
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as client_socket:
            client_socket.connect((SERVER_IP,SERVER_PORT))
            client_socket.send(message.encode())
            response=client_socket.recv(1024).decode()
        return response
    

    def register(self):
        first_name=self.firstname_e.get()
        last_name=self.lastname_e.get()
        username=self.username_e.get()
        email=self.email_e.get()
        password=self.password_e.get()
        confirm_password=self.confirm_password_e.get()
        security_code=self.security_code_e.get()
        confirm_security_code=self.confirm_security_code_e.get()

        if not all([first_name,last_name,username,email,password,confirm_password,security_code,confirm_security_code]):
            messagebox.showerror("PassLock Testing","Please fill in all details.")
            return
        
        if password != confirm_password:
            messagebox.showerror("PassLock Testing","Passwords do not match.")

        if security_code != confirm_security_code:
            print(security_code,confirm_security_code)
            messagebox.showerror("PassLock Testing","Security codes do not match.")

        message=f"REGISTER|{first_name}|{last_name}|{username}|{email}|{password}|{confirm_password}|{security_code}|{confirm_security_code}"
        response=self.send_to_server(message)
        messagebox.showinfo("Registration",response)

    
    def open_login_page(self):
        self.root.destroy()
        login_page=Tk()
        Login(login_page)



class PassLock_Testing:
    def __init__(self,root):
        self.root=root
        self.root.geometry("600x800")
        # self.user_db=user_db
        # self.temp_server_ip=temp_server_ip
        # self.temp_server_port=temp_server_port

        # self.temp_client_sokcet=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # self.temp_client_sokcet.connect((self.temp_server_ip,self.temp_server_port))








root=Tk()
obj=Register(root)
root.mainloop()