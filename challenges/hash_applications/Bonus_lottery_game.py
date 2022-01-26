import hashlib

import pwn
import parse
import hmac
import random as rd
import time
import math

VERBOSE_EVERY = 10      # s

hashes = []

for i in range(100000):
    hasher = hashlib.new('sha256')
    # if i != 0:
    #     hasher.update(i.to_bytes(int(math.log2(i)//8 + 1), "big"))
    # else:
    #     hasher.update(i.to_bytes(1, 'big'))
    hasher.update(str(i).encode())
    hash = hasher.hexdigest()
    hashes.append(hash)

r = pwn.remote('35.195.130.106',
               17008,
               # ssl=True,
               )

instructions = [r.readline().decode() for i in range(3)]

for line in instructions:
    print(line.strip())
hash = parse.parse('{}is {}, let{}', instructions[-1])[1]
random_number_is = hashes.index(hash)
print(f"         This corresponds to {hashes.index(hash)}\n")



player_dists=[]
player_hashes=[]
player_announcement=[]
for i in range(10):
    r.send(bytes())
    player_info = r.readline().decode()
    player_announcement.append(player_info)
    print(player_info.strip())
    player_hash=parse.parse("{}to {}\n", player_info)[1]
    player_number = hashes.index(player_hash)
    print(f'       He got number {player_number} which corresponds to a distance of {abs(player_number-random_number_is)}\n')
    player_dists.append(abs(player_number-random_number_is))
    player_hashes.append(player_hash)

# r.send('Player 3')
print(r.readline())

winner_index = player_dists.index(min(player_dists))
winner_hash = player_hashes[winner_index]

print(f"\n\n  The winner has to be player {winner_index} with hash {winner_hash} !! Congrats !")

r.send(player_announcement[winner_index])

print(r.readlines())