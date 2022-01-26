import hashlib

import pwn
import parse
import hmac
import random as rd
import time

VERBOSE_EVERY = 10      # s

r = pwn.remote('35.195.130.106',
               17003,
               # ssl=True,
               )

instructions = [r.readline().decode() for i in range(3)]

for line in instructions:
    print(line)

m = parse.parse('{}"{}"{}', instructions[-1])[1].encode()

index = str(rd.random()).encode()

hasher = hashlib.new('sha256')
hasher.update(m+index)
hash = hasher.hexdigest()

strt = time.time()
tries_count = 1
while hash[0:4]!='0000':

    index = str(rd.random()).encode()

    hasher = hashlib.new('sha256')
    hasher.update(m + index)
    hash = hasher.hexdigest()
    if time.time()-strt > VERBOSE_EVERY:
        print(f'{time.time()-strt} s ellapsed since beginning. Performed {tries_count} tries')
    tries_count += 1

r.sendline(index)

print(r.recvall())
