import re

import pwn
import parse
import hashlib

r = pwn.remote('35.195.130.106',
               17005,
               # ssl=True,
               )

instructions = [r.readline().decode() for i in range(2)]

for i in range(2):
    print(instructions[i])

for i in range(100):
    ans = input('Enter the primitive > ')
    r.sendline(ans.encode())
    rans = r.readline().decode()
    if re.search("What", rans):
        pass
    else:
        break
    print(rans)

print(r.recvall())