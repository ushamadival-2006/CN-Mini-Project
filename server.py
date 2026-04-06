import socket
import threading

from security import encrypt_message, decrypt_message

HOST = '127.0.0.1'
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Server started...")

clients = []
usernames = []
client_rooms = {}   # client : room
rooms = {}          # room : [clients]

# 🔹 Broadcast message to room
def broadcast(message, room, sender=None):
    for client in rooms.get(room, []):
        if client != sender:
            try:
                client.send(message.encode())
            except:
                remove_client(client)

# 🔹 Remove client safely
def remove_client(client):
    if client in clients:
        username = usernames[clients.index(client)]
        room = client_rooms.get(client)

        print(f"{username} disconnected")

        if room and client in rooms.get(room, []):
            rooms[room].remove(client)

        clients.remove(client)
        usernames.remove(username)
        client_rooms.pop(client, None)
        client.close()

# 🔹 Handle each client
def handle_client(client):
    while True:
        try:
            data = client.recv(4096)

            if not data:
                break

            data = data.decode()

            # ---------------- MESSAGE ----------------
            if data.startswith("MSG"):
                _, encrypted_msg = data.split("|", 1)

                # 🔐 Convert string → bytes
                encrypted_msg = encrypted_msg.encode()

                # 🔐 Decrypt message
                message = decrypt_message(encrypted_msg)

                username = usernames[clients.index(client)]
                room = client_rooms[client]

                formatted_msg = f"[{room}] {username}: {message}"
                print(formatted_msg)

                # 🔐 Encrypt before sending
                encrypted_send = encrypt_message(formatted_msg)

                # Send encrypted message
                broadcast(encrypted_send.decode(), room, client)

            # ---------------- FILE ----------------
            elif data.startswith("FILE"):
                _, filename, filesize = data.split("|")
                filesize = int(filesize)

                file_data = b''
                while len(file_data) < filesize:
                    chunk = client.recv(4096)
                    file_data += chunk

                room = client_rooms[client]
                username = usernames[clients.index(client)]

                print(f"{username} sent file {filename} in {room}")

                for c in rooms[room]:
                    if c != client:
                        try:
                            c.send(f"FILE|{filename}|{filesize}".encode())
                            c.send(file_data)
                        except:
                            remove_client(c)

        except:
            break

    remove_client(client)

# 🔹 Accept clients
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {address}")

        # Get username
        client.send("USERNAME".encode())
        username = client.recv(1024).decode()

        # Get room
        client.send("ROOM".encode())
        room = client.recv(1024).decode()

        clients.append(client)
        usernames.append(username)
        client_rooms[client] = room

        if room not in rooms:
            rooms[room] = []

        rooms[room].append(client)

        print(f"{username} joined {room}")

        client.send("Connected to server!".encode())

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

receive()