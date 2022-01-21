import pwn
import parse
import hashlib

r = pwn.remote('35.195.130.106',
               17000,
               # ssl=True,
               )

instructions = [r.readline().decode() for i in range(2)]

for i in range(2):
    print(instructions[i])

to_hash = parse.parse('{}"{}"{}', instructions[-1])[1].strip().encode()


hasher = hashlib.new('sha256')
hasher.update(to_hash)
hash = hasher.hexdigest()
print(to_hash)
print(hash)

r.sendline(hash)

print(r.recvall())