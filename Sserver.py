import socket
import threading

lst_con = []

def constr():
	s = ''
	for e in lst_con:
		s+=e+'\n'

	return s		

cmd = 'get_cons : get all client\nconnect $<addr> : conenct to a client'

s = socket.socket()
try:
	s.bind((socket.gethostname(),1234))
	s.listen(0)

	def getAddr(smg):
		if(isAddr(smg)):
			lt = smg.split('$')
			return lt[1]

	def isAddr(smg):
		if(smg.count('$')!=0):
			lt = smg.split('$')
			if(len(lst_con)!=0 & lst_con.count(lt[1])==1):
				return True

		return False


	def WebHandler(acc,addr):
		bts = []
		with open('test.htm','r') as fl:
			for e in fl:
				bts = btyes(e,'utf-8')
	
		acc.send(bts)
		return			

	def scmd(cmd,acc,addr):
		if(cmd==1):
			acc.send(bytes('send file... ready to recieve..','ascii'))

				# Three thing to receive

			fname = (acc.recv(1024)).decode()
			length = int((acc.recv(1024)).decode())
			data = ''
			for x in range(length):
				tmp = (acc.recv(1024)).decode()
				data = '\n'+tmp
			with file(fname,'w') as fs:
				fs.write(data)
		acc.send(bytes('successfully transfered data','ascii'))

	def Process(acc,addr):
		smg = (acc.recv(1024)).decode()
		if(smg=='get_cons'):
			print('from {0},{1} : {2}'.format(lst_con.count(addr),addr,smg))
			acc.send(bytes(constr(),'ascii'))

		if(isAddr(smg)):



		if(smg=='GET / HTTP/1.1'):
			WebHanlder(acc,addr)
			return
		print('from {0} : {1}'.format(addr,smg))
		if(smg=='cmds'):
			acc.send(bytes('1.fltrans/n2:path'))
			cmd = int((acc.recv(1024)).decode())
			scmd(cmd,acc,addr)
			Process(acc,addr)
		print('from {0},{1} : {2}'.format(lst_con.count(addr),addr,smg))			
		acc.send(bytes(smg.upper(),'ascii'))
		Process(acc,addr)

	while(True):
		acc,addr = s.accept()
		print('Connection from : {0}'.format(addr))
		acc.send(cmd.encode())
		lst_con.append(addr)
		thread = threading.Thread(target=Process,args=(acc,addr,))
		thread.daemon = True
		thread.start()

except OSError as e:
	s.close()
	print('{0} : {1}'.format(type(e),e))
	s = 0



