import socket
import threading
import os
import tkinter as tk
from tkinter import scrolledtext, filedialog

HOST = '127.0.0.1'
PORT = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# 🔹 GUI setup
root = tk.Tk()
root.title("Chat App")
root.geometry("500x600")
root.configure(bg="#1e1e1e")

chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg="#2b2b2b", fg="white", font=("Arial", 12))
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_area.config(state='disabled')

input_frame = tk.Frame(root, bg="#1e1e1e")
input_frame.pack(fill=tk.X, padx=10, pady=10)

msg_entry = tk.Entry(input_frame, font=("Arial", 12), bg="#3c3f41", fg="white")
msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

# 🔹 Display message in chat
def display(msg):
    chat_area.config(state='normal')
    chat_area.insert(tk.END, msg + "\n")
    chat_area.yview(tk.END)
    chat_area.config(state='disabled')

# 🔹 Receive messages / files
def receive():
    while True:
        try:
            data = client.recv(4096)

            if data.startswith(b"FILE"):
                header = data.decode(errors='ignore')
                parts = header.split("|")

                filename = parts[1]
                filesize = int(parts[2])

                file_data = b''
                while len(file_data) < filesize:
                    chunk = client.recv(4096)
                    file_data += chunk

                with open("received_" + filename, "wb") as f:
                    f.write(file_data)

                display(f"📂 File received: {filename}")

            else:
                display(data.decode())

        except:
            display("❌ Disconnected from server")
            client.close()
            break

# 🔹 Send message
def send_message():
    msg = msg_entry.get()
    if msg:
        client.send(f"MSG|{msg}".encode())
        msg_entry.delete(0, tk.END)

# 🔹 Send file
def send_file():
    filepath = filedialog.askopenfilename()
    if filepath:
        filesize = os.path.getsize(filepath)
        filename = os.path.basename(filepath)

        client.send(f"FILE|{filename}|{filesize}".encode())

        with open(filepath, "rb") as f:
            client.sendall(f.read())

        display(f"📤 File sent: {filename}")

# 🔹 Buttons
send_btn = tk.Button(input_frame, text="Send", command=send_message, bg="#4CAF50", fg="white")
send_btn.pack(side=tk.RIGHT)

file_btn = tk.Button(root, text="Send File", command=send_file, bg="#2196F3", fg="white")
file_btn.pack(pady=5)

# 🔹 Handshake
def start():
    username = input("Enter username: ")
    room = input("Enter room: ")

    while True:
        msg = client.recv(1024).decode()

        if msg == "USERNAME":
            client.send(username.encode())

        elif msg == "ROOM":
            client.send(room.encode())
            break

start()

# 🔹 Threads
threading.Thread(target=receive, daemon=True).start()

# 🔹 Run GUI
root.mainloop()