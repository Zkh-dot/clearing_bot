import pickle
from cryptography.fernet import Fernet
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

def generate_fernet_key(password):
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256,
        iterations=100000,
        salt=salt,
        length=32,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def get_fernet(key):
    return Fernet(key)


def save(data, filename, password):
    try:
        password = get_fernet(password)
    except:
        password = generate_fernet_key(password)
    # Serialize the dictionary using pickle
    pickled_data = pickle.dumps(data)

    # Encrypt the data using Fernet
    fernet = Fernet(password)
    encrypted_data = fernet.encrypt(pickled_data)

    # Write the encrypted data to a file
    with open(filename, 'wb') as file:
        file.write(encrypted_data)

def get(filename, password):
    try:
        password = get_fernet(password)
    except:
        password = generate_fernet_key(password)
    # Read the encrypted data from a file
    with open(filename, 'rb') as file:
        encrypted_data = file.read()

    # Decrypt the data using Fernet
    fernet = Fernet(password)
    pickled_data = fernet.decrypt(encrypted_data)

    # Deserialize the data using pickle
    data = pickle.loads(pickled_data)

    return data

def save_users(data, file_path):
    with open(file_path, 'wb') as file:
        pickle.dump(data, file)

def get_user(file_path):
    try:
        with open(file_path, 'rb') as file:
            return pickle.load(file)
    except:
        return []
