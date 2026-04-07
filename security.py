from cryptography.fernet import Fernet

# ✅ Valid Fernet key
key = b'X6vVnZ4r2l0l3F8xJv9qY3c5T8p2K6mN4Q1W7E9R2TY='

cipher = Fernet(key)

def encrypt_message(msg):
    return cipher.encrypt(msg.encode())

def decrypt_message(msg):
    return cipher.decrypt(msg).decode()