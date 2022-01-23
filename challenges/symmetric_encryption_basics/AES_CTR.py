import hashlib

import pwn
import parse
import hmac

r = pwn.remote('35.195.130.106',
               17011,
               # ssl=True,
               )

instructions = [r.readline().decode() for i in range(3)]

for line in instructions:
    print(line)

key = "b4cf7094f32b8551ac39e841216e2c36cf3c63d4b6376aa5af025391c41c5979"
nonce = "dd74f4335777bc4333e25fc7f8fe1a81"

message = parse.parse('{}"{}"{}', instructions[-1])[1]

print(message)