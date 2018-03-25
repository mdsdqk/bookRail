#!/usr/bin/python
							##replace prints with sendall or appropriate when done
from socket import *
from _thread import *
from datetime import *
import time
import train
import addtrains

host = ''
trainList = addtrains.trainList

userList = []

def dispTrains():
	conn.sendall("Trains running are\n")
	for i in range(0, len(trainList)):
		temp = [ trainList[i].number, trainList[i].name, trainList[i].source, trainList[i].dep, trainList[i].dest, trainList[i].arr ]
		conn.sendall(str(temp))
		conn.sendall('\n')
	
def findTrains(src, dest):
	foundList = []
	for i in range(0, len(trainList)):
		if src in trainList[i].source and dest in trainList[i].dest:
			temp = [ trainList[i].number, trainList[i].name, trainList[i].source, trainList[i].dep, trainList[i].dest, trainList[i].arr ]
			foundList.append(temp)

	if len(foundList) == 0:
		conn.sendall("No Trains found between the given route :(")
		conn.sendall('\n')
	
	else:
		conn.sendall("Trains from " + src + " to " + dest + "\n")
		for i in range(0, len(foundList)):
			conn.sendall(str(foundList[i]))
			conn.sendall("\n")

def trainNumIn():
	while 1:
		msg = 'Enter train number to proceed'
		conn.sendall(msg)
		conn.sendall("\n")
		recvd = conn.recv(1024)
		if len(recvd) == 5:
			return recvd
			break
		else:
			conn.sendall("Invalid Train Number")
			conn.sendall("\n")

def trainInfo(number):
	temp = "null"
	for i in range(0, len(trainList)):
		if number == trainList[i].number:
			temp = [ trainList[i].number, trainList[i].name, trainList[i].source, trainList[i].dep, trainList[i].dest, trainList[i].arr ]
			conn.sendall(str(temp))
			conn.sendall("\n")
			break

	if temp == "null":
		conn.sendall("No train with the given number found")
		conn.sendall("\n")

def checkAvail(number, date, x):
	for i in range(0, len(trainList)):
		if number == trainList[i].number:
			temp = trainList[i]
			break

	res = temp.availability(date, x)
	conn.sendall(str(res))

def book(number, date, travelClass, seatNum, conn, uid):
	for i in range(0, len(trainList)):
		if number == trainList[i].number:
			temp = trainList[i]
			break

	ret = temp.seatBook(date, travelClass, seatNum, conn, uid)

	if ret == -1:
		conn.sendall("Seat Not Available\n")
	
	elif ret == 0:
		conn.sendall("Seat has been blocked by someone else, please select some other seat or try again later\n")

	elif ret == 1:
		tempuser = getUser(uid)
		conn.sendall("Ticket Details are\nName : " + str(tempuser.uname) + "\tAge : " + str(tempuser.age) + "\nEmail : " + str(tempuser.email) + "\nPhone : " + str(tempuser.phone))
		conn.sendall("\n\n")

def welcomeinit():
	conn.sendall("Enter user id\n")
	uid = conn.recv(1024)
	conn.sendall("Enter Name\n")
	uname = conn.recv(1024)
	conn.sendall("Enter age\n")
	age = conn.recv(1024)
	conn.sendall("Enter gender\n")
	gender = conn.recv(1024)
	conn.sendall("Enter email\n")
	email = conn.recv(1024)
	conn.sendall("Enter phone\n")
	phone = conn.recv(1024)

	for i in range(0, len(userList)):
		if uid == userList[i].uid:
			conn.sendall("Welcome back " + userList[i].name + "\n")
			return uid

	obj = train.user(uid, uname, age, gender, email, phone)
	userList.append(obj)
	return uid

def getUser(uid):
	for i in range(0, len(userList)):
		if uid == userList[i].uid:
			temp = userList[i]
			return temp

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

#Required for py3
#def strToBytes(strToConvert):
#	return str.encode(strToConvert, "UTF-8")
#
#def bytesToStr(dataToConvert):
#	return str(dataToConvert, "UTF-8")

def clientthread(conn):
	hellomsg = 'Hi there!, Welcome to Railway Booking System\n'
	conn.sendall(hellomsg)
	uid = welcomeinit()
	while True:
		msg = 'Enter...\n1 to see all the running trains\n2 to search trains\n3 to get train info by train number\n4 to check availibilty\n5 to book a seat\n6 to visit profile\n9 to exit'
		conn.sendall(msg)
		conn.sendall("\n")
		data = conn.recv(1024)
		if int(data) == 9:
			conn.close()
			exit()
			break

		elif int(data) == 1:
			dispTrains()
			continue

		elif int(data) == 2:
			msg = 'Enter Source - Destination (in the given format, e.g.- Bengaluru - Mysuru)\n'
			conn.sendall(msg + "\n")
			recieved = conn.recv(1024)
			src,dest = recieved.strip(' ').split('-')
			findTrains(src, dest)
			conn.sendall("\nEnter..\nTrain number to check availibility for that train\n0 to go back")
			conn.sendall("\n")
			if int(conn.recv(1024)) == 0:
				continue
			else:
				data = 4

		elif int(data) == 3:
			recvd = trainNumIn()
			trainInfo(int(recvd))
			continue

		elif int(data) == 4 or int(data) == 5:
			trNum = trainNumIn()
			conn.sendall("Enter date and class in 'dd-mm-yyyy,c' format where c = 0 for all, 1 for sl, 2 for 3ac, 3 for 2ac, and 4 for first class")
			conn.sendall("\n")
			recvd = conn.recv(1024)
			date, x = recvd.strip(" ").split(",")
			checkAvail(int(trNum), date, int(x))
			conn.sendall('Enter\n1 to book\n0 to return to main menu')
			conn.sendall("\n")
			if(int(conn.recv(1024)) == 0):
				continue

			else:
				temp = getUser(uid)
				if int(x) == 0:
					conn.sendall('Enter Class (sl, third, second, first), seat number to book a seat\n')
					rcvd = conn.recv(1024)
					x, seatNum = rcvd.strip(' ').split(',')
				
				else:
					if int(x) == 1:
						x = "sl"
					if int(x) == 2:
						x = "third"
					if int(x) == 3:
						x = "second"
					if int(x) == 4:
						x = "first"
					conn.sendall('Enter seat Number to book')
					conn.sendall("\n")
					seatNum = conn.recv(1024)

				book(int(trNum), date, x, int(seatNum), conn, uid)
		
		elif int(data) == 6:
			conn.sendall("Profile\n")
			tempuser = getUser(uid)
			
			conn.sendall("Name " + tempuser.uname + "\n")
			conn.sendall("Username " + tempuser.uid + "\n")
			conn.sendall("Age " + tempuser.age + "\n")
			conn.sendall("Email id" + tempuser.email + "\n")
			conn.sendall("Press 1 to check your booking history\n0 to go back")
			resp = conn.recv(1024)
			if resp == 1:
				conn.sendall("\nhere is your booking history\n")
				conn.sendall(str(temp.bookings) + "\n")
				continue

			if resp == 0:
				continue
			



while 1:
	conn, addr = sock.accept()
	print ('Connected with ' + addr[0] + ':' + str(addr[1]))
	start_new_thread(clientthread ,(conn,))
		

sock.close()
