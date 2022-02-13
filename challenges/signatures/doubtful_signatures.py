import re

import pwn
import parse
import hashlib

r = pwn.remote('35.195.130.106',
               17018,
               # ssl=True,
               )

instructions = []
for i in range(5):
    instructions.append(r.readline().decode().strip())
    print(instructions[-1])

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding, utils
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.exceptions import InvalidSignature

server_pub_key_repr = parse.parse('{}: "{}"', instructions[1])[1]
serv_pub_key = load_pem_public_key(bytes.fromhex(server_pub_key_repr))

_, text_src, _, sig_src = parse.parse('{}"{}"{}"{}"', instructions[3])

def get_modified_digest(txt):
    hex_txt_dgst = hashlib.sha256(txt.encode()).digest()
    return bytes.fromhex(hex_txt_dgst[:2].hex() + 60*'0')

serv_pub_key.verify(
    bytes.fromhex(sig_src),
    get_modified_digest(text_src),
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    utils.Prehashed(hashes.SHA256())
)

def test_text(txt):
    try:
        serv_pub_key.verify(
            bytes.fromhex(sig_src),
            get_modified_digest(txt),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            utils.Prehashed(hashes.SHA256())
        )
    except:
        return False
    return True

import random as rd

txt = str(rd.random())
while not test_text(txt):
    txt = str(rd.random())

r.sendline(txt)
print(r.recvall())