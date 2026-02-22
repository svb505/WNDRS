from cryptography.fernet import Fernet

def load_key():
    try:
        return open("syst_comp/syst.key", "rb").read()
    except:
        return None
def decrypt_message(encrypted_message, key):
    f = Fernet(key)
    return f.decrypt(encrypted_message).decode()
def generate_key():
    key = Fernet.generate_key()
    with open("syst_comp/syst.key", "wb") as key_file:
        key_file.write(key)
def encrypt_message(message, key):
    f = Fernet(key)
    return f.encrypt(message.encode())
def read_encrypted_file(path):
    key = load_key()
    with open(path, "rb") as f:
        return decrypt_message(f.read(), key).strip()
def write_encrypted_file(filepath, data, key=None, backup=False):
    if not key:
        key = load_key()

    encrypted = encrypt_message(data, key)
    with open(filepath, "wb") as f:
        f.write(encrypted)
