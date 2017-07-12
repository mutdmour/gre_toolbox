import random, time

def run(total=100, minScore=0):
	qTypes = {"~":(estimationQ, exactly, "estimation quiz", 10),
			"/5":(dividingBy5, exactly, "dividing by 5", 10),
			"doublehalf":(doubleAndHalf, exactly, "double and half", 15),
			"numbersense":(numberSense, evaluate, "number sense game", 30),
			"prime":(primeNumbers, compareArray, "prime number ranges", 30),
			"cubes":(cubes, exactly, "find cubes of any number between 1 and 10", 20),
			"square":(square, exactly, "find square of any number", 20)}
	qIndex = getQType(qTypes)
	#qIndex = 'r'
	if (qIndex != "r"):
		question, validation = qTypes[qIndex][0], qTypes[qIndex][1]
		pIndex = qIndex
	count = 0
	right = 0
	score = 0
	while (count < total or (score/count*100) < minScore):
		if (qIndex == "r"):
			pIndex = random.choice(qTypes.keys())
			question, validation = qTypes[pIndex][0], qTypes[pIndex][1]
		count += 1
		print("")
		start = time.time()
		correct, answer = question()
		end = time.time()
		if (answer == "q"):
			count -= 1
			break
		res = validation(correct, answer)
		diff = end-start
		if (res):
			right += 1
			score = updateScore(count, score, True, diff, qTypes[pIndex][3])
			print("You got it")
		else:
			score = updateScore(count, score, False, diff, qTypes[pIndex][3])
			print "Nop, it was", correct
		print "That took", "{:.2f}".format(diff),"s"
	if (count > 0):
		print ""
		print "You got","{:.2f}%".format(float(right)/count*100), "right"
		print "And a score of","{:.2f}%".format(float(score)/count*100)


def compareArray(actualArray, stringAnswer):
	ans = stringAnswer.split(" ")
	#print ans
	if (len(ans) != len(actualArray)):
		return False
	for i in ans:
		try:
			i = int(i)
			if (not i in actualArray):
				return False
		except:
			return False
	return True

def updateScore(count, score, result, time, maxTime):
	if (result and time > maxTime):
		score += 1.
	elif (result and time < maxTime):
		score += .5
	else: 
		score -= 1.
		if (score < 0):
			score = 0
	return score

def exactly(x,y):
	return x == y

def evaluate(correct, answer):
	try:
		res = eval(answer)
		print "Evaluated to",res
		return correct == res
	except:
		print "Could not evaluate this"
		return False

def powerQ(x, y):
	question = str(x)+"^"+str(y)+"= "
	ans = raw_input(question)
	res = str(x**y)
	return res, ans

def cubes():
	return powerQ(random.randint(2,10), 3)

def primeNumbers():
	primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
	# 1. list all numbers in a certain range
	# 2. is this number prime or not?
	# 3. product/sum of all primes in a certain range
	# 
	min = random.randint(0,len(primes)-2)
	max = min + 4
	if (max > len(primes)):
		max = len(primes)
	print "List the next 4 primes that are more than or equal to", primes[min], "but less than 115 [use spaces to seperate number]"
	#print primes[min:max]
	return primes[min:max], raw_input("? ")

def numberSense():
	num = [] 
	while (len(num) != 4):
		x = random.randint(1,9)
		if (not x in num):
			num.append(x)
	res = random.randint(1,20)
	print "You got",num[0],num[1],num[2],num[3],". Try to get",res
	print "You can multiply, divide, add, subtract them in anyway"
	#answer = ""
	#while(len(answer) < 7):
	check = False
	while(not check):
		answer = raw_input("? ")
		if (answer.strip().lower() == "q"):
			break
		check = True
		barren = ""
		if (len(answer) < 7):
			check = False
		else: 
			for n in num:
				if (answer.count(str(n)) != 1):
					check = False
					break
		
	return res, answer

def getQType(qTypes, rand=False):
	choices = qTypes.keys() + ["r"]
	if (rand):
		return random.choice(choices)
	for k, v in qTypes.iteritems():
		print k,"-",v[2]
	print "r - randomly mixed quiz"
	print "q - to quit"

	choice = None
	while (not choice in choices):
		choice = raw_input("quiz type? ").strip().lower()
	return choice

def square():
	a = 8
	while ((a-8)%10 == 0 or (a-7)%10 == 0 or (a-3)%10 == 0):
		a = random.randint(1,100)
	return powerQ(a,2)

def doubleAndHalf():
	a = random.randint(1,150) * 2
	b = 5 * random.randint(1,20)
	if (b % 10 == 0):
		b += 5
	res = a * b
	answer = raw_input(str(a) + "*" + str(b) + "= ")
	res = str(res)
	return res, answer

def dividingBy5():
	a = random.randint(100, 1000) * 5
	b = 5
	res = a / b
	answer = raw_input(str(a) + "/" + str(b) + "= ")
	res = str(res)
	return res, answer

def estimationQ():
	s = "{:.2f}"
	a = random.randint(1000,10000)
	b = random.random()*100
	res = a * b / 100
	print "What is",s.format(b),"% of",a,"? "
	opts = []
	numOpts = 3
	rng = .1 * a
	while (len(opts) < 3):
		x = a * random.random()
		if (abs(res - x) > rng):
			opts.append(s.format(x))
	res = s.format(res)
	opts.append(res)
	answer = printOpts(opts, line=True)
	return res, answer

def printOpts(opts, line=False, shuffle=True, first='a'):
	n = ord(first)
	line = ""
	if (shuffle):
		random.shuffle(opts)
	for opt in opts:
		opt = chr(n) + ") " + str(opt) + " "
		if (line):
			line = line + opt
		else:
			print opt
		n += 1
	if (line):
		print line
	index = -1
	while(index == -1):
		answer = raw_input("? ").strip().lower()
		if (len(answer) != 1):
			pass
		elif (answer == 'q'):
			return answer
		else:
			index = ord(answer) - ord(first)
			if (index < 0 or index >= len(opts)):
				index = -1
	return opts[index]
			

total = 100
try:
        total = int(raw_input("how many questions? "))
except:
        print("Will do 100")
run(total)
