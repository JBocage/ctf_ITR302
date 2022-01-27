import hashlib
import os

import pwn
import parse
import hmac
import random as rd
import time

import crypt
import pwd
import getpass
from hmac import compare_digest as compare_hash

hashes = []
salts = []
user_data = []
with open(os.path.abspath(os.path.join(__file__, "..", "..", "..", "data", "leaked_shadow"))) as file:
    while True:
        line = file.readline()
        if line:
            user_data.append(line.strip())
        else:
            break

common_passwords = []
with open(os.path.abspath(os.path.join(__file__, "..", "..", "..", "data", "best110.txt"))) as file:
    while True:
        line = file.readline()
        if line:
            common_passwords.append(line.strip())
        else:
            break

info = {}
for data in user_data:
    parsed = parse.parse('{}:{}:{}:{}:{}:{}:{}', data)
    hash_parsed = parse.parse("${}${}${}",parsed[1])
    info[parsed[0]] = {'type': hash_parsed[0],
                       'salt': hash_parsed[1],
                       'hash': hash_parsed[2],
                       'change_date': parsed[2],
                       'minimum_age': parsed[3],
                       'maximum_age': parsed[4],
                       'warning_period': parsed[5]}
    hashes.append(hash_parsed[2])
    salts.append(hash_parsed[1])

def display_info():
    for key in info.keys():
        print(f'Displaying info from user {key}')
        for ukey in info[key].keys():
            print(f'    {ukey} : {info[key][ukey]}')

passwords = ['' for i in range(len(hashes))]

for pwd in common_passwords:
    for idx, elmt in enumerate(zip(hashes, salts)):
        hash, salt = elmt
        hashed = crypt.crypt(pwd, "$6$"+salt)
        if compare_hash(hashed[-86:], hash):
            passwords[idx] = pwd

print(passwords)