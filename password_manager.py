
import base64
from hashlib import sha256
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC




## This function generates key for encryption and run only once and see if key.key is generated
#   once key.key is generated comment out  this code
""" def write_key():
    key = fernet.Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)


write_key() """
###  End of key.key generateion

def salt_key():
    
    if os.path.exists("salt_file.key") == True:
        with open("salt_file.key", "rb") as salt_key:
            print("salt.key")
            salt = salt_key.read()
            print("Salt Key Read:", salt)
    else:
        with open("salt_file.key", "wb") as salt_key:
                salt = os.urandom(16)
                salt_key.write(salt)
                print("Salt Key New:",  salt)
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
    print(key)
    return key


def view():
    with open('passwords2.txt', 'r') as f:
        for line in f.readlines():
            f_data = line.rstrip()
            user_id, user_pwd = f_data.split("|")
            print(user_pwd)
            print("User ID:", user_id,  " | Password: " , fer.decrypt(user_pwd.encode())  )

        """     try:
                user_pwd = fer.decrypt(user_pwd)
            except InvalidToken:
                pass
 """

def add():
    user_id = input("Account user ID: ")
    user_pwd = input("Enter password:")
    with open('passwords2.txt', 'a') as f:
        f.write(user_id + "|" +  fer.encrypt(user_pwd.encode()).decode() + "\n")

        

master_pwd = input("What is the master password?")

salt = salt_key()
key = load_key(master_pwd,salt)
fer = Fernet(key)

while True:
    mode = input("Would you like to add a new password or view existing ones (view, add), press q to quit?").lower()

    if mode == 'q':
        break

    if mode == 'view':
        view()
    elif mode == 'add':
        add()
    else:
        print("Invalide mode.")
        continue