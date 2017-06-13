# add vocabs to list
from PyDictionary import PyDictionary
import csv
from './helpers.py' import keys

file = 'vocab.csv'
vocab = {}

with open(file, 'rb') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
	word = row["word"]
	vocab[word] = {}
	for key, value in row.iteritems():
		if (key != "word"):
			if (key == "weight"):
				value = float(value)
			elif (key == "numRight" or key == "numTested"):
				value = int(value)
			elif (key == "lastTested"):
				if (value == ''):
					value = None
				else:
					datetime.strptime(value,"%b %d")
			vocab[word][key] = value

deck = raw_input("Name of deck? ").strip().lower()
source = raw_input("Source (magoosh, barrons...)? ").strip().lower()
if (deck == ""):
	deck = "other"
if (source == ""):
	source = "other"

def yesOrNo(message):
	while (True):
		answer = raw_input("{0} (y|n) ".format(message)).strip().lower()
		if (answer == "y"):
			return True
		elif(answer == "n"):
			return False

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
			print vocab[word]
		else:
			print "Okay, won't add"

print ""
print "Added",addedCount,"words"
print "Now you have a total of", len(vocab), "words"

with open(file, 'wb') as csv_file:
	writer = csv.DictWriter(csv_file, fieldnames=keys)
	writer.writeheader()
	for word, obj in vocab.iteritems():
		res = {k:v for k,v in obj.iteritems()}
		res["word"] = word
		writer.writerow(res)
