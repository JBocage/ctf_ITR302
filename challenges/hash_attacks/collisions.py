import re

import pwn
import parse
import hashlib

import time
import random as rd

import bisect

collision_index = 48

r = pwn.remote('35.195.130.106',
               17006,
               # ssl=True,
               )

instructions = [r.readline().decode() for i in range(2)]

for i in range(2):
    print(instructions[i])

### Collision finding script

search_set = []

print("###   Starting search set generation")
hasher = hashlib.sha256()
strt = time.time()
for i in range(2**(collision_index//2)):
    m = str(rd.random()).encode()
    hasher.update(m)
    hm = hasher.hexdigest()[:collision_index//4]
    hasher = hashlib.sha256()
    search_set.append((hm, m))
print(f'      Generation time : {time.time()-strt} s\n')

print('###   Sorting the search set')
strt = time.time()
search_set.sort(key=lambda x: x[0])
print(f'      Sorting time : {time.time()-strt} s \n')
hms = [i[0] for i in search_set]
lenhms=len(hms)
#
# print('###   Looking for a collision')
# strt=time.time()
# verbose_threshold = 10  # s
# researched = 0
# while True:
#     if time.time()-strt > verbose_threshold:
#         print(f'      Still looking for a collision ! Ellapsed time : {time.time()-strt} s\n'
#               f'                                      Tries         : {researched}')
#         verbose_threshold += 10
#     m = str(rd.random()).encode()
#     hasher.update(m)
#     hm = hasher.hexdigest()[:collision_index//4]
#     hasher = hashlib.sha256()
#     # print(hm)
#     idx = bisect.bisect_left(hms, hm)
#     if idx<lenhms:
#         if hm==hms[idx]:
#             print(f'      Collision found between\n'
#                   f'         -> {m}\n'
#                   f'         -> {search_set[idx][1]}\n'
#                   f'      because both following are equal \n'
#                   f'         -> {hm}\n'
#                   f'         -> {hms[idx]}'
#                   )
#             break
#     researched += 1

# r.sendlines([m, search_set[idx][1]])

first = b'0.03780379538749323'
second = b'0.7836929071998952'

r.sendlines([first, second])

rec = r.recvall().decode().split('\n')
for line in rec:
    print(line)



