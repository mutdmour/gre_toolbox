# add vocabs to list
from PyDictionary import PyDictionary
import csv
from helpers import  reader, writer, yesOrNo

vocab = reader()

deck = raw_input("Name of deck? ").strip().lower()
source = raw_input("Source (magoosh, barrons...)? ").strip().lower()
if (deck == ""):
	deck = "other"
if (source == ""):
	source = "other"

more = True
addedCount = 0
while(more):
	print ""
	dictionary = PyDictionary()
	word = raw_input("new word? ").strip().lower()
	add = True
	if (word == "q"):
		break
	elif (word in vocab):
		print word, "already exists in list"
		print vocab[word]
		print ""

		check = yesOrNo("overwrite?")
		if (not check):
			add = False
			print "Okay, will pass"
	if (add):
		definition = None
		while(definition == None):
			definition = raw_input("definition? ").strip()
			if (definition == "q"):
				break
			if (definition == "def"):
				definition = None
				meaning = dictionary.meaning(word)
				print meaning
			elif (word in definition):
				check = yesOrNo("nop, cannot use word in definition, redo?")
				if (check):
					definition = None
		if (definition == "q"):
			break

		example = None
		while(example == None):
			example = raw_input("example? ").strip()
			if (example == "q"):
				break
			if (not word in example):
				check = yesOrNo("nop, you have to use the word in your example, redo?")
				if (check):
					example = None
		if (example == "q"):
			break

		check = yesOrNo("add?")
		if (check):
			addedCount += 1
			vocab[word] = {"deck":deck, 
					"source":source,
					"def":definition, 
					"ex":example, 
					"lastTested":None, 
					"numTested":0,
					"numRight":0,
					"weight":0.}
			print "Added", word
			#print vocab[word]
		else:
			print "Okay, won't add"

writer(vocab)

print ""
print "Added",addedCount,"words"
print "Now you have a total of", len(vocab), "words"
