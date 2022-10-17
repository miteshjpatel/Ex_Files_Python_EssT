
import base64
import os
from hashlib import sha256
from importlib import invalidate_caches
from xmlrpc.client import boolean
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def salt_key():

    if os.path.exists("salt_file.key") == True:
        with open("salt_file.key", "rb") as salt_key:
            salt = salt_key.read()
    else:
        with open("salt_file.key", "wb") as salt_key:
            salt = os.urandom(16)
            salt_key.write(salt)
    return salt


def load_key(pass_word, salt):
    #salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=sha256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(pass_word.encode()))
    return key


def view():
    invalid_pwd = False
    with open('passwords2.txt', 'r') as f:
        for line in f.readlines():
            f_data = line.rstrip()
            user_id, user_pwd = f_data.split("|")
            try:
                print("User ID:", user_id,  " | Password: ",
                      fer.decrypt(user_pwd.encode()).decode())
            except InvalidToken:
                print("Invalid Password!!")
                invalid_pwd = True
                break
    return invalid_pwd


def add():
    user_id = input("Account user ID: ")
    user_pwd = input("Enter password:")
    with open('passwords2.txt', 'a') as f:
        f.write(user_id + "|" + fer.encrypt(user_pwd.encode()).decode() + "\n")


master_pwd = input("What is the master password?")

salt = salt_key()
key = load_key(master_pwd, salt)
fer = Fernet(key)
invalid_pwd = False

while True:
    if invalid_pwd == True:
        invalid_pwd == False
        master_pwd = input("Enter valid master password: ")
        key = load_key(master_pwd, salt)
        fer = Fernet(key)
    mode = input(
        "Would you like to add a new password or view existing ones (view, add), press q to quit?").lower()

    if mode == 'q':
        break
    if mode == 'view':
        invalid_pwd = view()
    elif mode == 'add':
        add()
    else:
        print("Invalide mode.")
        continue
