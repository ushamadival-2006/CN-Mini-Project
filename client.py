import socket
import threading
import os

from security import encrypt_message, decrypt_message

HOST = '127.0.0.1'
PORT = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

username = input("Enter username: ")
room = input("Enter room: ")

print("""
📌 Commands:
- Type message → send chat
- sendfile <path> → send file
""")

# 🔹 Receive messages / files
def receive():
    while True:
        try:
            data = client.recv(4096)

            # ---------------- FILE ----------------
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

                print(f"\n📂 File received: {filename}")

            # ---------------- MESSAGE ----------------
            else:
                # 🔐 Convert to bytes → decrypt
                decrypted_msg = decrypt_message(data.decode().encode())
                print(f"\n💬 {decrypted_msg}")

        except:
            print("\n❌ Disconnected from server")
            client.close()
            break


# 🔹 Send messages / files
def write():
    while True:
        msg = input()

        # ---------------- FILE SEND ----------------
        if msg.startswith("sendfile"):
            try:
                _, filepath = msg.split(" ", 1)

                if not os.path.exists(filepath):
                    print("❌ File not found!")
                    continue

                filesize = os.path.getsize(filepath)
                filename = os.path.basename(filepath)

                # Send header
                client.send(f"FILE|{filename}|{filesize}".encode())

                # Send file data
                with open(filepath, "rb") as f:
                    client.sendall(f.read())

                print(f"📤 File sent: {filename}")

            except Exception as e:
                print("❌ Error sending file:", e)

        # ---------------- NORMAL MESSAGE ----------------
        else:
            # 🔐 Encrypt before sending
            encrypted_msg = encrypt_message(msg).decode()
            client.send(f"MSG|{encrypted_msg}".encode())


# 🔹 Initial handshake
def start():
    while True:
        msg = client.recv(1024).decode()

        if msg == "USERNAME":
            client.send(username.encode())

        elif msg == "ROOM":
            client.send(room.encode())
            break


start()

# 🔹 Start threads
threading.Thread(target=receive).start()
threading.Thread(target=write).start()