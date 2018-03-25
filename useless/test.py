from datetime import *
import multiprocessing
import signal
## testing to check if infinite loop works


var = 1
b = 0

TIMEOUT = 10 # number of seconds your want for timeout


def timeinput():
    try:
            print ('You have 10 seconds to type in your stuff...')
            foo = raw_input()
            return foo
    except:
            # timeout
            return


#print ('You typed', s)
def book():
	global var
	def interrupted(signum, frame):
		"called when read times out"
		print ('Booking failed')
	signal.signal(signal.SIGALRM, interrupted)
	
	def finalbook():
		b = 0
	    # set alarm
		signal.alarm(TIMEOUT)
		b = timeinput()
		# disable the alarm after success
		signal.alarm(0)
		global var
		'''try:
			int(b)
		except ValueError:
			pass      # or whatever'''
		if b != '' and int(b) == 1:
			var = -1
			print("Booked")
			
		else:
			print "bye"
    

	if var == 1:
		print("available")
		var = 0
		finalbook()

	else:
		print("fail")

	

if __name__ == '__main__':
	a = int(input("Enter 1 to book"))
	if a == 1:
		book()


