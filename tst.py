
#double threaded thing only work with the gui 
#if two has to conv. need two differet components

import socket
import threading

lock = threading.Lock()

def Receive(acc,addr):
	print((acc.recv(1024)).decode())
	Receive(acc,addr)

sender = socket.socket()
sender.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sender.connect((socket.gethostname(),8888))
print('connected to the server\nsending stream online...')

receiver = socket.socket()
receiver.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
receiver.bind((socket.gethostname(),8889))
receiver.listen(0)
print('receiver listening for server connection ....')

acc,addr = receiver.accept()

th = threading.Thread(target=Receive,args=(acc,addr))
th.daemon = True
th.start()

while(True):
	lock.acquire()
	sender.send(bytes(input(),'ascii'))
	print('sent')
	lock.release()

