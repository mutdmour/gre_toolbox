import csv
import random
import numpy as np
from gtts import gTTS
import os
from PyDictionary import PyDictionary

dictionary = PyDictionary()


options = ["new", "review", "mastered"]
prob = [1, 0, 0] #xxx allow for input from command line

sound_file = "word.mp3"

def play(f):
	try:
		os.system("mpg321 --quiet -o alsa {0}".format(f))
	except:
		os.system("mpg321 --quiet {0}".format(f))

def speak(word):
	tts = gTTS(text=word, lang='en')
	tts.save(sound_file)
	play(sound_file)

def repeat():
	play(sound_file)

file = 'words.csv'
words = {}
with open(file, 'rb') as csv_file:
    reader = csv.reader(csv_file)
    for key, value in reader:
    	words[key] = float(value)

#keys = words.keys()


count = 0
total = 100
# xxx allow input for total from command line

print ("d to delete word")
print ("c if you got it correct the first time")
print ("q to quit")

testing = True #more testing of different words

def getList(rule):
	limit = 50
	c = 0
	l = []
	for k, v in words.iteritems():
		if (c >= limit):
			break
		if (rule(v)):
			c += 1
			l.append(k)
	return l

while(testing):
	more = True #more testing of the same word
	if (count == total):
		more = False
		testing = False
	count += 1

	state = np.random.choice(options, p=prob)
	if (state == "new"):
		def rule(v):
			return v == 0
	elif (state == "review"):
		def rule(v):
			return v != 0 and v < 1
	elif (state == "mastered"):
		def rule(v):
			return v == 1

	arr = getList(rule)
	if (len(arr) > 0):
		test_word = random.choice(arr)
		test_word = test_word.strip().lower()
		print ""
	else:
		more = False
	trials = 0
	answer = None
	while (more): # testing same word
		trials += 1
		if (trials == 1 and answer != "r"):
			speak(test_word)
		else:
			repeat()
		message = str.format("[{:.3}] word? ",state) #"word? " 
		answer = raw_input(message)
		answer = answer.strip().lower()
		if (answer == "q"):
			quit = raw_input("quit? (y|n) ")
			if (quit == "y"):
				more = False
				testing = False
			else:
				trials -= 1
		elif (answer == "d"):
			delete = raw_input("delete [{0}]? (y|n) ".format(test_word))
			if (delete == "y"):
				words.pop(test_word)
				more = False
				count -= 1
			else:
				trials -= 1
		elif (answer == "c"):
			if (trials > 1):
				correct = raw_input("correct? (y|n) ")
				if (correct == "y"):
					if (trials == 2 and words[test_word] < 1): #if you got it right the first time
						words[test_word] = 0
					more = False
			else:
				print "gotta try it first"
			trials -= 1
		elif (answer == "r" or answer == ""):
			trials -= 1
		elif (answer == "def"):
			if (trials > 1):
				print (dictionary.meaning(test_word))
			else:
				print "gotta try it first"
			trials -= 1
		else:
			if (answer == test_word):
				reward = ""
				if (trials == 1): #if you got it right the first time
					if (words[test_word] < 1):
						words[test_word] += .5
						reward = "+.5"
						if (words[test_word] == 1):
							reward = "Mastered!"
				more = False
				print "You got it.", reward
			else:
				words[test_word] = -1
				print "Nop [=-1], it's", test_word

with open(file, 'wb') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in words.items():
       writer.writerow([key, value])

new_words = [k for k, v in words.iteritems() if v == 0]
review_words = [k for k, v in words.iteritems() if v != 0 and v < 1]
mastered_words = [k for k, v in words.iteritems() if v == 1]

print("total", len(words))
print("not seen", len(new_words))
print("learning", len(review_words))
print("mastered", len(mastered_words))
