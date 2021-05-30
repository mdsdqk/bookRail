#!usr/bin/python
from socket import *
import sys

host = 'localhost' # '127.0.0.1' can also be used
port = 2222

sock = socket()
#Connecting to socket
sock.connect((host, port)) #Connect takes tuple of host and port

loop = True
while(loop):
    data = sock.recv(1024)
    print(data.decode())
    choice = input()
    sock.send(str(choice).encode())
    if(len(str(choice)) == 1):
        if(int(choice) == 9):
            sock.close()
            print("Press enter to Exit")
            foo=input()
            break
        
sys.exit()