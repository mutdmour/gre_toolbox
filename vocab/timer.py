import time
from helpers import yesOrNo

start = time.time()
min = 0
resetMin = 0
minCurr = 0
while (True):
	curr = int(time.time() - start)
	if (curr % 30 == 0 and curr > minCurr):
		minCurr = curr
		if (curr % 60 == 0):
			min += 1
			print min, "minutes"
		else:
			print min, "min 30 sec"
	if (min % 2 == 0 and min > resetMin):
		reset = yesOrNo("reset?")
		resetMin = min
		if (reset):
			start = time.time()
			min = 0
			resetMin = 0
			minCurr = 0
