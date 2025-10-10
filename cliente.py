import tkinter as tk
from tkinter import messagebox
import socket
import threading

HOST = '127.0.0.1'
PORT = 5000

class ChatClientGUI:
    def __init__(self, master):
        self.master = master
        master.title("Chat - Login")

        self.client_socket = None
        self.current_username = None

        self.frame = tk.Frame(master, padx=10, pady=10)
        self.frame.pack(padx=10, pady=10)

        self.label_username = tk.Label(self.frame, text="Nome de Usuário:")
        self.label_username.grid(row=0, column=0, pady=5, sticky="w")
        self.entry_username = tk.Entry(self.frame)
        self.entry_username.grid(row=0, column=1, pady=5)

        self.label_password = tk.Label(self.frame, text="Senha:")
        self.label_password.grid(row=1, column=0, pady=5, sticky="w")
        self.entry_password = tk.Entry(self.frame, show="*")
        self.entry_password.grid(row=1, column=1, pady=5)

        self.login_button = tk.Button(self.frame, text="Login", command=self.handle_login)
        self.login_button.grid(row=2, column=0, pady=10)

        self.register_button = tk.Button(self.frame, text="Registrar", command=self.handle_register)
        self.register_button.grid(row=2, column=1, pady=10)

    def connect_to_server(self):
        """Estabelece a conexão com o servidor."""
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((HOST, PORT))
            return True
        except socket.error as e:
            messagebox.showerror("Erro de Conexão", f"Não foi possível conectar ao servidor: {e}")
            return False

    def handle_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if self.connect_to_server():
            message = f"LOGIN|{username}|{password}"
            self.client_socket.sendall(message.encode('utf-8'))

            response = self.client_socket.recv(1024).decode('utf-8')

            if response.startswith("LOGIN_OK"):
                messagebox.showinfo("Login", "Login realizado com sucesso.")
                self.current_username = username
                # Inicia a thread para receber mensagens do servidor
                threading.Thread(target=self.receive_messages, daemon=True).start()
                self.show_chat_window()
            else:
                messagebox.showerror("Login Falhou", response)
                self.client_socket.close()

    def handle_register(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if self.connect_to_server():
            message = f"REGISTER|{username}|{password}"
            self.client_socket.sendall(message.encode('utf-8'))

            response = self.client_socket.recv(1024).decode('utf-8')
            messagebox.showinfo("Registro", response)
            self.client_socket.close()

    def receive_messages(self):
        """Função para receber mensagens do servidor em uma thread separada."""
        while True:
            try:
                data = self.client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                print(f"Mensagem recebida do servidor: {data}")
            except socket.error:
                break
        self.client_socket.close()

    def show_chat_window(self):
        """Muda para a janela de chat (placeholder)."""
        self.frame.destroy()
        chat_frame = tk.Frame(self.master, padx=10, pady=10)
        chat_frame.pack()
        tk.Label(chat_frame, text=f"Bem-vindo, {self.current_username}!").pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClientGUI(root)
    root.mainloop()