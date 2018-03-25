#!/usr/bin/python

from socket import *
from thread import *

host = ''

port = 2222

sock = socket(AF_INET, SOCK_STREAM)
print ('Socket created')

try:
    sock.bind((host, port))
except error as msg:
    print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

sock.listen(5)
print("Socket now Listening on port " + str(port))
'''
def strToBytes(strToConvert):
	return str.encode(strToConvert, "UTF-8")

def bytesToStr(dataToConvert):
	return str(dataToConvert, "UTF-8")
'''
def clientthread(conn):
	hellomsg = 'Hi! I am server\n'
	conn.send(hellomsg)
	while True:
		data = conn.recv(1024)
		print (data)
		reply = 'OK...' + data
		if not data: 
			break
     
		conn.sendall(reply)
     
	conn.close()

while 1:
	conn, addr = sock.accept()
	print ('Connected with ' + addr[0] + ':' + str(addr[1]))
	start_new_thread(clientthread ,(conn,))
		

sock.close()

