import hashlib

import pwn
import parse
import hmac

login = 'gandalfini'.encode()
shared_secret = bytes.fromhex('23fb0c2087b7a315603464a695941a37ff7a03066d4f9ecebeda237e8a74be9e')




r = pwn.remote('35.195.130.106',
               17015,
               # ssl=True,
               )

instructions = [r.readline().decode() for i in range(3)]

for line in instructions:
    print(line)

key = parse.parse('{}"{}"{}', instructions[1])[1]
print(f"key is {bytes.fromhex(key)}")
msg = parse.parse('{}"{}"{}', instructions[2])[1]
print(f"msg is {msg.encode()}")

from cryptography.hazmat.primitives.cmac import CMAC
from cryptography.hazmat.primitives.ciphers import algorithms

c = CMAC(algorithms.AES(bytes.fromhex(key)))
c.update(msg.encode())
answer = c.finalize().hex()

print(answer)

r.sendline(answer)
print(r.recvall())