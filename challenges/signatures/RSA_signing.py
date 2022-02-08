import re

import pwn
import parse
import hashlib

r = pwn.remote('35.195.130.106',
               17016,
               # ssl=True,
               )

instructions = []
for i in range(2):
    instructions.append(r.readline().decode())
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

for i in range(1):
    print(r.readline())

message = 'this is a really simple message'.encode()

r.sendline(message)

for i in range(1):
    print(r.readline())

signature = my_private_key.sign(
    message,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
).hex()

r.sendline(signature)

for i in range(10):
    print(r.readline())