import hashlib

import pwn
import parse
import hmac

login = 'gandalfini'.encode()
shared_secret = bytes.fromhex('23fb0c2087b7a315603464a695941a37ff7a03066d4f9ecebeda237e8a74be9e')




r = pwn.remote('35.195.130.106',
               17004,
               # ssl=True,
               )

instructions = [r.readline().decode() for i in range(2)]

for i in range(2):
    print(instructions[i])

tosend = login

print(f'sending {tosend}')

# r.sendline(login)
r.sendlines([login])

answer = r.readlines(2)[1].decode()
m = parse.parse('{}"{}"{}', answer)[1]

print(answer)
print(m)
print()

hasher = hmac.new(shared_secret, digestmod=hashlib.sha256)
hasher.update(m.encode())
hash = hasher.hexdigest()

auth = m.encode()+hash.encode()
print(f"sending {auth}")

r.sendline(auth)
print(r.recvall())