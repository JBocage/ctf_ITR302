import hashlib
import os.path

import pwn
import parse
import hmac
import random as rd
import time
import re

SALT_POSITION = 'end'                               # 'beginning' or 'end'
SYMBOLS_POSITION = 'end'                            # 'beginning' or 'end'
SYMBOLS = '~`!@#$%^&*()_-+={[}]|\:;"\'<,>.?/'
VERBOSE_EVERY = 2                                  # s
HASH_ALG = 'sha1'
salt = 'lrnsodmcbnriwjccbskgfsgrsjclenov'




# Build the words dictionnaire
words = []
with open(os.path.abspath(os.path.join(__file__, "..", "..", "..", "data", "words_alpha.txt"))) as file:
    words.append(file.readline().strip())
    while words[-1] != '':
        words.append(file.readline().strip())
    file.close()
words.pop()

start_time = time.time()
n_verbose = 1
# found = False
# password = ''
passwords = []
hashes = []
for widx, word in enumerate(words):
    for symbol in SYMBOLS:
            pos = len(word)
        # for pos in range(len(word) + 1):
            hasher = hashlib.new(HASH_ALG)
            hasher.update((word[:pos]+symbol+ word[pos:]+salt).encode())
            hash = hasher.hexdigest()
            # if hash == msg:
            #     found = True
            #     password = (word[:pos]+symbol+ word[pos:])
            #     salt_pos = 'end'
            hashes.append(hash)
            passwords.append(word[:pos]+symbol+ word[pos:])
            hasher = hashlib.new(HASH_ALG)
            hasher.update((salt + word[:pos] + symbol + word[pos:]).encode())
            hash = hasher.hexdigest()
            hashes.append(hash)
            # if hash == msg:
            #     found = True
            #     password = (word[:pos] + symbol + word[pos:])
            #     salt_pos = 'beginning'
            if time.time()-start_time>n_verbose*VERBOSE_EVERY:
                print(f"    Still looking for the password.\n"
                      f"         Current password : {word[:pos]+symbol+ word[pos:]}\n"
                      f"         Ratio        : {round(100*widx/len(words), 4)} %")
                n_verbose += 1
            # if found:
            #     break
        # if found:
        #     break
    # if found:
    #     break

r = pwn.remote('35.195.130.106',
               17007,
               # ssl=True,
               )

# r.send("")

print(r.readline().decode())

for i in range(100):
    instructions = [r.readline().decode() for i in range(1)]

    for line in instructions:
        print(line.strip())

    if re.search(r"Well", instructions[0]):
        break
    else:
        parsed = parse.parse("{} to {} with salt {}?\n", instructions[-1])
        msg = parsed[1]
        salt = parsed[2]

        print(msg)
        print(salt)

        index = hashes.index(msg)
        r.sendline(passwords[index//2])

print(r.recvall())

# if not password:
#     print("Nothing was found !!")
# else:
#     print(f"password was : {password}")
#
# r.sendline(password)

# print(r.recvall())