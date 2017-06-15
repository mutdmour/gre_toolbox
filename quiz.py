import random
import numpy as np
from PyDictionary import PyDictionary
from helpers import reader, writer, speak, repeat, getList, yesOrNo


def run(total=5):
	dictionary = PyDictionary()

	options = ["quiz", "review", "mastered"]
	prob = [1, 0, 0] #xxx allow for input from command line
	count = 0

	print ("q to quit")

	testing = True #more testing of different words

	vocab = reader()

	while(testing):
		more = True #more testing of the same word
		if (count == total):
			more = False
			testing = False
		count += 1

		state = np.random.choice(options, p=prob)
		if (state == "new"):
			def rule(v):
				return v[weight] == 0
		elif (state == "review"):
			def rule(v):
				return v[weight] != 0 and v[weight] < 1
		elif (state == "mastered"):
			def rule(v):
				return v[weight] == 1
		
		#get list of words that match our rule to randomly select one from
		arr = getList(vocab, rule, limit=10)
		obj = None
		if (len(arr) > 0):
			test_word = random.choice(arr)
			test_word = test_word.strip().lower()
			obj = vocab[test_word]
			print ""
		else:
			more = False

		trials = 0
		answer = None
		while (more): # testing same word
			trials += 1
			#if (trials == 1 and answer != "r"):
				#speak(test_word)
			#else:
				#repeat()
			print obj['def']
			message = str.format("[{:.3}] word? ",state,)  
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

	writer(words)

	new_words = [k for k, v in words.iteritems() if v == 0]
	review_words = [k for k, v in words.iteritems() if v != 0 and v < 1]
	mastered_words = [k for k, v in words.iteritems() if v == 1]

	print("total", len(words))
	print("not seen", len(new_words))
	print("learning", len(review_words))
	print("mastered", len(mastered_words))
