import pwn

r = pwn.remote('35.195.130.106',
               17100,
               # ssl=True,
               )

reply=r.recvall()

print(reply)