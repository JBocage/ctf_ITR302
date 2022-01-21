import pwn
import parse

r = pwn.remote('35.195.130.106',
               17102,
               # ssl=True,
               )

replies = [r.readline().decode() for i in range(3)]

for i in range(3):
    print(replies[i])

for i in range(100):
    reply = replies[-1]
    sentances = parse.parse('{}"{}"{}', reply)
    if sentances:
        sentance=sentances[1]
        print(f'recieved {sentance} Sending it back !')
        r.sendline(sentance.encode())
        replies.append(r.readline().decode())

print(r.recvall())