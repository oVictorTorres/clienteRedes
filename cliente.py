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
        self.contacts = {} # Dicionário para armazenar contatos
        self.login_frame = self.create_login_frame()

    def create_login_frame(self):
        """Cria o frame da tela de login."""
        frame = tk.Frame(self.master, padx=10, pady=10)
        frame.pack(padx=10, pady=10)

        tk.Label(frame, text="Nome de Usuário:").grid(row=0, column=0, pady=5, sticky="w")
        self.entry_username = tk.Entry(frame)
        self.entry_username.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Senha:").grid(row=1, column=0, pady=5, sticky="w")
        self.entry_password = tk.Entry(frame, show="*")
        self.entry_password.grid(row=1, column=1, pady=5)

        tk.Button(frame, text="Login", command=self.handle_login).grid(row=2, column=0, pady=10)
        tk.Button(frame, text="Registrar", command=self.handle_register).grid(row=2, column=1, pady=10)
        return frame

    def handle_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if self.connect_to_server():
            message = f"LOGIN|{username}|{password}"
            self.client_socket.sendall(message.encode('utf-8'))
            response = self.client_socket.recv(1024).decode('utf-8')

            if response.startswith("LOGIN_OK"):
                self.current_username = username
                self.login_frame.destroy()
                self.create_chat_window()
                threading.Thread(target=self.receive_messages, daemon=True).start()
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

    def connect_to_server(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((HOST, PORT))
            return True
        except socket.error as e:
            messagebox.showerror("Erro de Conexão", f"Não foi possível conectar ao servidor: {e}")
            return False

    def create_chat_window(self):
        """Cria a janela principal do chat."""
        self.master.title(f"Chat - {self.current_username}")
        self.master.geometry("800x600")

        main_frame = tk.Frame(self.master)
        main_frame.pack(fill=tk.BOTH, expand=True)

        contacts_frame = tk.Frame(main_frame, width=200, bg="lightgray")
        contacts_frame.pack(side=tk.LEFT, fill=tk.Y)
        contacts_frame.pack_propagate(False)

        tk.Label(contacts_frame, text="Contatos", bg="gray", fg="white", font=("Arial", 12)).pack(fill=tk.X)
        self.contacts_listbox = tk.Listbox(contacts_frame)
        self.contacts_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.contacts_listbox.bind("<<ListboxSelect>>", self.on_contact_select)

        self.chat_history = tk.Text(main_frame, state='disabled', wrap='word')
        self.chat_history.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        message_frame = tk.Frame(self.master)
        message_frame.pack(fill=tk.X, padx=5, pady=5)

        self.message_entry = tk.Entry(message_frame, font=("Arial", 12))
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.message_entry.bind("<Return>", lambda event: self.send_message())

        self.send_button = tk.Button(message_frame, text="Enviar", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)

        self.master.bind("<Destroy>", self.on_closing)

    def on_contact_select(self, event):
        # Lógica para carregar o histórico de conversa
        pass

    def send_message(self):
        """Função para enviar uma mensagem ao servidor."""
        message = self.message_entry.get()
        if message and self.client_socket:
            selected_contact = self.contacts_listbox.get(self.contacts_listbox.curselection())
            if selected_contact:
                # Formato da mensagem: MESSAGE|destinatario|mensagem
                message_to_send = f"MESSAGE|{selected_contact}|{message}"
                self.client_socket.sendall(message_to_send.encode('utf-8'))
                self.message_entry.delete(0, tk.END)
                self.update_chat_history(f"Você: {message}")

    def update_chat_history(self, message):
        self.chat_history.config(state='normal')
        self.chat_history.insert(tk.END, message + "\n")
        self.chat_history.config(state='disabled')
        self.chat_history.see(tk.END)

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

    def on_closing(self, event):
        if self.client_socket:
            self.client_socket.close()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClientGUI(root)
    root.mainloop()