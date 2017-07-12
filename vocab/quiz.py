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
def all_rule(v):
	return True

def run(total=5):
	dictionary = PyDictionary()

	qtypes = ["def","fill-in","example"]
	options = ["quiz", "review", "mastered"]
	prob = [.8, .2, 0]
	count = 0

	print ("q to quit")

	testing = True #more testing of different words

	vocab = reader()
	decks = []
	for w, obj in vocab.iteritems():
		d = obj['deck']
		if (not d in decks):
			decks.append(d)

	print decks

	deck = ''
	while (not deck in decks and deck != "a"):
		deck = raw_input("deck? (a for all) ")
	if (deck == 'a'):
		deck = None

	actions = ['q','qz','r']
	
	reset = yesOrNo('reset?')
	if (reset):
		mastered_words = getList(vocab, all_rule, deck=deck)
		for w in mastered_words:
			vocab[w]['weight']=0

	test_word = None
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
		arr = getList(vocab, rule, deck=deck, limit=50)
		if (test_word and len(arr)>1 and test_word in arr):
			arr.pop(arr.index(test_word))
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
				defQ = True # definition question
				if (random.random() > .5):
					defQ = False
					print "-->", vocab[test_word]['def']
				else:
					print "-->", vocab[test_word]['ex'].replace(test_word, "*"*len(test_word))
			message = "? " #str.format("[{:.3}] word? ",state)  
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
				#if (trials == 1):
					#if (not defQ):
						#print "-->", vocab[test_word]['ex']
					#else:
						#print "-->", vocab[test_word]['def']
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
	new_words = getList(vocab, new_rule, deck=deck)
	review_words = getList(vocab, review_rule, deck=deck)
	mastered_words = getList(vocab, mastered_rule, deck=deck)

	print("total", len(vocab))
	print("not seen", len(new_words))
	print("learning", len(review_words))
	print("mastered", len(mastered_words))

run(1000)
