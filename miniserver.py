import socket, sys
def sco(co):
    while True:
        cmd=input('[ $ ] Server | ')
        if cmd=='quit': co.close(),s.close(),sys.exit()
        if len(str.encode(cmd))>0:
            co.send(str.encode(cmd))
            cr=str(co.recv(1024),"utf-8")
            print(f'[ $ ] Client | {cr}',end="\n")
def sc():
      try:
          global h, p, s; h,p,s='',9999,socket.socket()
          print(f'[ + ] Server created | {str(p)}')
      except socket.error as m: print(f'[ - ] Creation failed | {str(m)}')
def sb():
    try:
        global h,p,s; print(f'[ + ] Binding connection | {str(p)}'),s.bind((h,p)),s.listen(5)
    except socket.error as m:
        global bc
        if bc < 3:
            print(f'[ - ] Connection binding error | {str(m)}')
            print(f'[ - ] Reattempting to bind connection...')
            bc += 1; sb()
        else: print(f'[ - ] Failed to bind connection'),s.close()
def sa(): c, a = s.accept(); print(f'[ + ] Connection establisted | {str(a[0])}, {str(a[1])}'),sco(c),c.close()
def main(): sc(),sb(),sa()
main()
