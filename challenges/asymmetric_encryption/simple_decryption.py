import re

import pwn
import parse
import hashlib

r = pwn.remote('35.195.130.106',
               17021,
               # ssl=True,
               )

instructions = []
for i in range(2):
    instructions.append(r.readline().decode().strip())
    print(instructions[-1])


from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.exceptions import InvalidSignature

my_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
my_public_key = my_private_key.public_key()
readable_key = my_public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
# to_send = ''.join(readable_key.decode().split('\n')[1:-2])
# to_send = to_send.encode().hex()
to_send=readable_key.hex()

r.sendline(to_send)

for i in range(2):
    instructions.append(r.readline().decode().strip())
    print(instructions[-1])

cipher = parse.parse('{}"{}"', instructions[-2])[1]
b_cipher = bytes.fromhex(cipher)
msg = my_private_key.decrypt(b_cipher,
                       padding.OAEP(
                           mgf=padding.MGF1(algorithm=hashes.SHA256()),
                           algorithm=hashes.SHA256(),
                           label=None
                       ))

r.sendline(msg)

print(r.recvall())