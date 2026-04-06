from cryptography.fernet import Fernet

# Generate once and keep constant
key = b'0vQ5m8kH8pYxZxX3gS8u5r1Y7Kjv3G9m8Xc4wQ2L1A='
cipher = Fernet(key)

def encrypt_message(msg):
    return cipher.encrypt(msg.encode())

def decrypt_message(msg):
    return cipher.decrypt(msg).decode()