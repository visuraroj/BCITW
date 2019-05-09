import socket
import threading

tLock = threading.Lock()
shutdown = False

def receving(name, sock):
    while not shutdown:
        try:
            tLock.acquire()
            while True:
                data, addr = sock.recvfrom(1024)
                print(str(data.decode("utf-8")))
        except:
            pass
        finally:
            tLock.release()

host = ''
port = 0

server = ('localhost', 9090)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

rT = threading.Thread(target=receving, args=("RecvThread",s))
rT.start()

alias = input("Name: ")
s.sendto(("s|" + alias + "|join").encode("utf-8"), server)

while not shutdown:
    try:
        msg = input()

        tLock.acquire()
        if (msg == 'quit'):
            s.sendto(("s|" + alias + "|quit").encode("utf-8"), server)
            shutdown = True
        else:
            s.sendto(("c|" + alias + "|" + msg).encode("utf-8"), server)
        tLock.release()

    except:
        shutdown = True

rT.join()
s.close()