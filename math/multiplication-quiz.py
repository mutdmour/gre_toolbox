import random
import time

def isDigit(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

num = range(2,13)

opts = [0 for _ in range(0,20)]
weights = {i:opts[:] for i in range(2,20)}

def updateW(x,y,res=True, time=True):
	if (res):
		if (weights[x][y] < 1):
			if (time):
				weights[x][y] += .5
			else: 
				weights[x][y] += .25
	else:
		weights[x][y] = -1

def isNotMastered():
	sum = 0 
	for k, v in weights.iteritems():
		for i in v:
			sum += i
			if (i < 0):
				return True 
	if (sum == 0):
		return True
	return False

def getNotMastered():
	total = 10
	count = 0
	opts = []
	res = (0,0)
	for k, v in weights.iteritems():
		for i in range(0,len(v)):
			if (v[i] < 0):
				opts.append((k,i))
				count += 1
	if (len(opts) > 0):
		res = random.choice(opts)
	return res[0],res[1]

total = 100
count = 1
right = 0
print "reminder: q to quit"
while (count <= total or isNotMastered()):
	print str.format("{0}.", count)

	if (count <= total):
		x = random.choice(num)
		y = random.choice(num)
		if (x == 11 and y < 10): #multiples of 11
			y = random.choice(range(11,18))
		elif (y == 11 and x < 10): #multiples of 11
			x = random.randint(11,18)
		elif (x == 10 or y == 10): #squares
			x = random.randint(13,19)
			y = x
		elif (x == 9 or x == 2):
			y = random.randint(2,19)
		elif (y == 9 or y == 2):
			x = random.randint(2,19)
	else:
		x, y = getNotMastered()
		if (x == 0):
			break

	multiply = random.random() > .5


	start = time.time()
	if (multiply):
		res = x * y
		message =  str.format("{0}*{1}= ", x, y)
	else: 
		res = y
		message =  str.format("{0}/{1}= ", x*y, x)
	input = raw_input(message)
	end = time.time()

	if (input == "q"):
		break
	if (isDigit(input)):
		answer = int(input)
		if (answer == res):
			elapsed = end - start
			if (elapsed > 5):
				right += .5
				updateW(x, y, time=False)
				print "Ahh you got it, but took too long :/"
			else: 
				right += 1
				updateW(x, y)
				print "You got it :)"
		else:
			updateW(x, y, res=False)
			print "Nop, it's ", res
	else: 
		updateW(x, y, res=False)
		print "Nop, it's ", res
	print ""
	count += 1

count -= 1
if (count >= 0):
	perc = right/count*100
	print str.format("You got a {:0.2f}%", perc)
