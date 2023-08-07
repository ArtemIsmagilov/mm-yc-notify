from cryptography.fernet import Fernet


def generate_key():
    key = Fernet.generate_key()
    return key


def create_fernet(key):
    return Fernet(key)
