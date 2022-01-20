import pwn
import parse

r = pwn.remote('35.195.130.106',
               17101,
               # ssl=True,
               )

reply = r.readline().strip().decode()

r.send(reply.split()[2])