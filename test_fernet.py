

from base64 import encode
from cryptography.fernet import Fernet

key = Fernet.generate_key()
passwd = "mitesh"
print(passwd.encode())
key2 = key + passwd.encode()
print(key2)
print(key)
f = Fernet(key)
f2 = Fernet(key2)
token = f.encrypt(b"my deep dark secret")
print(token)

token = token + passwd.encode()
print(token)
data = f.decrypt(token)
print(data)

data = f2.decrypt(token)
print(data)