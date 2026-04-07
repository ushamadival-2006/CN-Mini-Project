# CN-Mini-Project

# Multi-Room Secure Chat System with File Transfer

## Introduction
This project implements a multi-room secure chat system using socket programming. It allows multiple users to communicate in different chat rooms and supports secure messaging and file transfer. A WebSocket-based frontend is also provided for real-time browser interaction.

---

## Features
- Multi-user chat system
- Multiple chat rooms
- Secure messaging using encryption
- File transfer between users
- GUI-based client (Tkinter)
- Web-based frontend using WebSockets

---

## Technologies Used
- Python
- Socket Programming (TCP)
- WebSockets
- HTML, CSS, JavaScript
- Cryptography (Fernet encryption)

---

## Project Structure
- server.py          → Main backend server
- client.py          → Terminal client
- client_gui.py      → GUI client using Tkinter
- ws_server.py       → WebSocket server for frontend
- index.html         → Web frontend
- security.py        → Encryption logic
- file_transfer.py   → File handling

---

## How to Run

### Backend (Socket Version)
1. Run server:
   python server.py

2. Run client:
   python client.py

### GUI Client
python client_gui.py

### Web Version
1. Run WebSocket server:
   python ws_server.py

2. Open index.html in browser

---

## How It Works
- Clients connect to a central server using TCP sockets
- Server manages chat rooms and broadcasts messages
- Messages are encrypted before transmission and decrypted at the receiver
- Files are transferred as binary data
- WebSocket is used for real-time communication in browser

---

## Security
- Messages are encrypted using Fernet symmetric encryption
- Data is decrypted at the receiver side
- Ensures confidentiality during transmission

---

## Computer Network Concepts Used
- Client-Server Architecture
- TCP Socket Programming
- Multithreading
- Application Layer Protocol Design
- Data Transmission
- Encryption
- WebSocket (Persistent communication)

---

## Contributors
- Usha Suresh Madival
- Sneha N
- Snidhi Prasad

---

## Future Improvements
- Add advanced encryption
- Improve UI design
- Add database for user management
- Enable file transfer in web version
