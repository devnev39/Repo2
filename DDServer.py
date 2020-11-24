import socket
import threading

#multithreaded server with two ends not possible with one console

lock = threading.Lock()

listener = socket.socket()
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

def handler(acc,addr):
	lock.acquire()
	print('from {0} : {1}'.format(addr,(acc.recv(1024)).decode()))
	lock.release()
	handler(acc,addr)

def Shandler():
	sender = socket.socket()
	sender.connect((socket.gethostname(),8889))
	print('Sender thread connected.....')
	while(True):
		
		sender.send(bytes(input('your : '),'ascii'))
		

try:
	listener.bind((socket.gethostname(),8888))

	listener.listen(0)
	print('listener binded and listening..')

	while(True):
		Accepted , Addr = listener.accept()
		print('Connection from {0}'.format(Addr))

		print('setting thread to sender....')

		th = threading.Thread(target=handler,args=(Accepted,Addr))
		ths = threading.Thread(target=Shandler,args=())
		th.daemon = True
		ths.daemon = True


		ths.start()
		th.start()



except OSError as E:
	print('{0} : {1}'.format(type(E),E))