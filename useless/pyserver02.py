#!/usr/bin/python
							##replace prints with sendall or appropriate when done
from socket import *
from thread import *
from datetime import *
import time

host = ''

TIMEOUT = 10 # number of seconds your want for timeout

def timeinput():
	try:
			print ('You have 5 seconds to type in your stuff...')
			foo = raw_input()
			return foo
	except:
			# timeout
			return


class train:
	def __init__(self, name, number, source, dest, dep, arr):
		self.name = name
		self.number = number
		self.source = source
		self.dep = dep
		self.dest = dest
		self.arr = arr
		#dictionaries for seat availibility, key is date and value is a list of seats
		#value = -1 means booked, 0 booking and 1 available
		#seat number is index+1
		self.sl = {}	
		self.third = {}
		self.second = {}
		self.first = {}

	def addSeats(self, date, slnum, thirdNum, secondNum, firstNum):
		self.sl[date] = [1] * slNum
		self.third[date] = [1] * thirdNum
		self.second[date] = [1] * secondNum
		self.first[date] = [1] * firstNum

	def availability(self, date, x):
		#x = 0 means show for all classess, 1 sl, 2 3a, 3 2a, 4 first
		slCount = thirdCount = secondCount = firstCount = 0
		if x == 0:
			slList = self.sl.get(date)
			thirdList = self.third.get(date)
			secondList = self.second.get(date)
			firstList = self.first.get(date)
			
			for i in range(0, len(slList)):
				if slList[i] == 1:
					slCount += 1
				if thirdList[i] == 1:
					thirdCount += 1
				if secondList[i] == 1:
					secondCount += 1
				if firstList[i] == 1:
					firstCount += 1

			print("Avaialble Seats in train " + str(self.number))
			print("Sleeper Class " + str(slCount))
			print("3A Class " + str(thirdCount))
			print("2A Class " + str(secondCount))
			print("First Class " + str(firstCount))

		elif x == 1:
			slList = self.sl.get(date)
			for i in range(0, len(slList)):
				if slList[i] == 1:
					slCount += 1
				
			print("Avaialble Seats in train " + str(self.number))
			print("Sleeper Class " + str(slCount))
			
		elif x == 2:
			thirdList = self.third.get(date)
			for i in range(0, len(thirdList)):
				if thirdList[i] == 1:
					thirdCount += 1
			 
			print("Avaialble Seats in train " + str(self.number))
			print("3A Class " + str(thirdCount))

		elif x == 3:
			secondList = self.second.get(date)
			for i in range(0, len(secondList)):
				if secondList[i] == 1:
					secondCount += 1
				
			print("Avaialble Seats in train " + str(self.number))
			print("2A Class " + str(secondCount))

		elif x == 4:
			firstList = self.first.get(date)
			for i in range(0, len(firstList)):
				if firstList[i] == 1:
					firstCount += 1

			print("Avaialble Seats in train " + str(self.number))
			print("First Class " + str(firstCount))

	def seatBook(self, date, travelClass, seatNum):
		classList = self.travelClass.get(date)
		
		def interrupted(signum, frame):
			"called when read times out"
			print ('Booking failed')
			classList[seatNum] = 1
		signal.signal(signal.SIGALRM, interrupted)
		
		if classList[seatNum] == 1:
			print("The selected seat is available")
			print("Seat blocked for you, Complete booking within 10 seconds to confirm seat")
			print("Enter 'Confirm' to Book")
			classList[seatNum] = 0
		
			#start timer
			signal.alarm(TIMEOUT)
			b = timeinput()
			# disable the alarm after success
			signal.alarm(0)
			
			if b == "Confirm":
				classList[seatNum] = -1
				print("Booking Successful for seat number " + str(seatNum))

		elif classList[seatNum] == -1:
			print("Selected seat is not available")

		elif classList[seatNum] == 0:
			print("Seat has been blocked by someone else, please select some other seat or try again later")

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
	hellomsg = 'Hi! I am server\n'
	conn.sendall(hellomsg)
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

