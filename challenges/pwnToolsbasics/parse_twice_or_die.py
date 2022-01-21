import pwn
import parse

r = pwn.remote('35.195.130.106',
               17103,
               # ssl=True,
               )

replies = [r.readline().decode() for i in range(3)]

for i in range(3):
    print(replies[i])

for i in range(100):
    reply = replies[-1]
    sentances = parse.parse('{}"{}"{}', reply)
    if sentances:

        # idx determination
        instruction = sentances[0].split()[7]
        try:
            idx = ['first', 'second', 'third', 'fourth', 'fifth'].index(instruction)
        except:
            raise(ValueError(f'instruction was {instruction}'))

        sentance=sentances[1].split()[idx]
        print(f'recieved {sentance} Sending it back !')
        r.sendline(sentance.encode())
        replies.append(r.readline().decode())

print(r.recvall())