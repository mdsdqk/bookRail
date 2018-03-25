from datetime import *
from socket import *

TIMEOUT = 10 # number of seconds your want for timeout

def timeinput():
	try:
			sock.sendall ('You have 10 seconds to type in your stuff...')
			foo = conn.recv(1024)
			return foo
	except:
			# timeout
			return

class user:
	def __init__(self, uid, uname, age, gender, email, phone):
		self.uid = uid
		self.uname = uname
		self.age = age
		self.gender = gender
		self.email = email
		self.phone = phone
		self.bookings = []

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
		self.slPrice = 0
		self.thirdPrice = 0
		self.secondPrice = 0
		self.firstPrice = 0

	def addSeats(self, date, slPrice, slNum, thirdPrice, thirdNum, secondPrice, secondNum, firstPrice, firstNum):
		self.slPrice = slPrice
		self.thirdPrice = thirdPrice
		self.secondPrice = secondPrice
		self.firstPrice = firstPrice
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
			for i in range(0, len(thirdList)):
				if thirdList[i] == 1:
					thirdCount += 1
			for i in range(0, len(secondList)):
				if secondList[i] == 1:
					secondCount += 1
			for i in range(0, len(firstList)):
				if firstList[i] == 1:
					firstCount += 1

			return ("Avaialble Seats in train " + str(self.number) + "\nSleeper Class " + str(slCount) + "\n" + str(slList) + "\n3A Class " + str(thirdCount) + "\n" + str(thirdList) + "\n2A Class " + str(secondCount) + "\n" + str(secondList) + "\nFirst Class " + str(firstCount)+ "\n" + str(firstList) + "\n")

		elif x == 1:
			slList = self.sl.get(date)
			for i in range(0, len(slList)):
				if slList[i] == 1:
					slCount += 1
				
			return ("Avaialble Seats in train " + str(self.number) + "\nSleeper Class " + str(slCount) + "\n")
			
		elif x == 2:
			thirdList = self.third.get(date)
			for i in range(0, len(thirdList)):
				if thirdList[i] == 1:
					thirdCount += 1
			 
			return ("Avaialble Seats in train " + str(self.number) + "\n3A Class " + str(thirdCount) + "\n")

		elif x == 3:
			secondList = self.second.get(date)
			for i in range(0, len(secondList)):
				if secondList[i] == 1:
					secondCount += 1
				
			return ("Avaialble Seats in train " + str(self.number) + "\n2A Class " + str(secondCount) + "\n")

		elif x == 4:
			firstList = self.first.get(date)
			for i in range(0, len(firstList)):
				if firstList[i] == 1:
					firstCount += 1

			return ("Avaialble Seats in train " + str(self.number) + "\nFirst Class " + str(firstCount) + "\n")

	def seatBook(self, date, travelClass, seatNum, conn, tempuser):
		if travelClass == "sl":
			classList = self.sl.get(date)
		elif travelClass == "third":
			classList = self.third.get(date)
		elif travelClass == "second":
			classList = self.second.get(date)
		elif travelClass == "first":
			classList = self.first.get(date)
		
		if classList[seatNum] == 1:
			conn.sendall("The selected seat is available\nSeat blocked for you, Complete booking within 10 seconds to confirm seat\nEnter '1' to Book\n")
			classList[seatNum] = 0
			b = int(conn.recv(1024))

			if b != '' and b == 1:
				classList[seatNum] = -1
				conn.sendall("Booking Successful for seat number " + str(seatNum) + "\n")
				return 1

		elif classList[seatNum] == -1:
			return -1
			
		elif classList[seatNum] == 0:
			return 0
			
