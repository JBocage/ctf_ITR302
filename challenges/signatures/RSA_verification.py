import re

import pwn
import parse
import hashlib

r = pwn.remote('35.195.130.106',
               17017,
               # ssl=True,
               )

instructions = []
for i in range(4):
    instructions.append(r.readline().decode().strip())
    print(instructions[-1])

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.exceptions import InvalidSignature

server_pub_key_repr = parse.parse('{}: "{}"', instructions[1])[1]
serv_pub_key = load_pem_public_key(server_pub_key_repr)


for i in range(30):
    pass
