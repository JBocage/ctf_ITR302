import pwn
import parse
import hashlib

r = pwn.remote('35.195.130.106',
               17002,
               # ssl=True,
               )

instructions = [r.readline().decode() for i in range(2)]

for i in range(2):
    print(instructions[i])

for i in range(100):
    parsed = parse.parse('{}"{}" with {}', instructions[-1])

    if parsed:
        to_hash = parsed[1].strip().encode()
        hash_alg = parsed[2].strip().split()

        print(hash_alg)

        if hash_alg[0] == 'SHAKE-128':
            hasher = hashlib.shake_128()
            hasher.update(to_hash)
            hash = hasher.hexdigest(int(hash_alg[2]))
        elif hash_alg[0] == 'SHAKE-256':
            hasher = hashlib.shake_256()
            hasher.update(to_hash)
            hash = hasher.hexdigest(int(hash_alg[2]))
        else:
            hasher = hashlib.new(hash_alg[0])
            hasher.update(to_hash)
            hash = hasher.hexdigest()
        print(to_hash)
        print(hash)


        r.sendline(hash)
        instructions.append(r.readline().decode())

print(r.recvall())