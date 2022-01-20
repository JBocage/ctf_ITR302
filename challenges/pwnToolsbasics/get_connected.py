import pwn

r = pwn.remote('35.195.130.106',
               17101,
               # ssl=True,
               )

reply=r.readline()

