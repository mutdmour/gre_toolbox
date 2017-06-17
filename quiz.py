import random
import numpy as np
from PyDictionary import PyDictionary
from helpers import reader, writer, speak, repeat, getList, yesOrNo

def new_rule(v):
	return v['weight'] == 0
def review_rule(v):
	return v['weight'] != 0 and v['weight'] < 1
def mastered_rule(v):
	return v['weight'] == 1

def run(total=5):
	dictionary = PyDictionary()

	qtypes = ["def","fill-in","example"]
	options = ["quiz", "review", "mastered"]
	prob = [0, 1, 0] #xxx allow for input from command line
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
		rule = new_rule
		if (state == "review"):
			rule = review_rule
		elif (state == "mastered"):
			rule = mastered_rule

		#get list of words that match our rule to randomly select one from
		arr = getList(vocab, rule, limit=10)
		if (len(arr) > 0):
			test_word = random.choice(arr)
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
			if (trials == 1):
				print vocab[test_word]['def']
			message = str.format("[{:.3}] word? ",state)  
			answer = raw_input(message)
			answer = answer.strip().lower()
			if (answer == "q"):
				if (yesOrNo("quit?")):
					more = False
					testing = False
				else:
					trials -= 1
			else:
				#speak(test_word)
				if (answer == test_word):
					reward = ""
					if (trials == 1): #if you got it right the first time
						if (vocab[test_word]['weight'] < 1):
							vocab[test_word]['weight'] += .5
							reward = "+.5"
							if (vocab[test_word]['weight'] == 1):
								reward = "Mastered!"
					more = False
					print "You got it.", reward
				else:
					vocab[test_word]['weight'] = -1
					print "Nop [=-1], it's", test_word

	writer(vocab)

	#use get list or make a getcount version of it
	new_words = [k for k, v in vocab.iteritems() if v['weight'] == 0]
	review_words = [k for k, v in vocab.iteritems() if v['weight'] != 0 and v['weight'] < 1]
	mastered_words = [k for k, v in vocab.iteritems() if v['weight'] == 1]

	print("total", len(vocab))
	print("not seen", len(new_words))
	print("learning", len(review_words))
	print("mastered", len(mastered_words))

run(50)
