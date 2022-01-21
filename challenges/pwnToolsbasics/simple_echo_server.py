import pwn
import re

r = pwn.remote('35.195.130.106',
               17101,
               # ssl=True,
               )

replies = [r.readline().decode() for i in range(3)]

for sentance in replies:
    print(sentance)

for i in range(100):
    print(f'Recieved {replies[-1]}, sending it back')
    r.send(replies[-1])
    replies.append(r.readline().decode())
    if re.search(r'Well', replies[-1]):
        break
print()
recieved = r.recvall()
print(recieved)