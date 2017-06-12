# add vocabs to list
import csv
 

file = 'vocab.csv'
vocab = {}

keys = ["word","deck","def","ex", "weight", "lastTested","numTested","numRight"]

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

def yesOrNo(message):
	while (True):
		answer = raw_input("{0} (y|n) ".format(message)).strip().lower()
		if (answer == "y"):
			return True
		elif(answer == "n"):
			return False

more = True
while(more):
	print ""
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
			print "Okay, will pass"
	if (add):
		definition = None
		while(definition == None):
			definition = raw_input("definition? ").strip()
			if (definition.lower().index(word) >= 0):
				definition = None
				print "nop, cannot use word in definition"
		if (definition == "q"):
			break

		example = None
		while(example == None):
			example = raw_input("example? ").strip()
			if (example.lower().index(word) < 0 and example != "q"):
				example = None
				print "nop, you have to use the word in the example"
		if (example == "q"):
			break

		check = yesOrNo("add?")
		if (check):
			vocab[word] = {"deck":deck, 
					"def":definition, 
					"ex":example, 
					"lastTested":None, 
					"numTested":0,
					"numRight":0,
					"weight":0.}
			print "Added", word
		else:
			print "Okay, won't add"

with open(file, 'wb') as csv_file:
	writer = csv.DictWriter(csv_file, fieldnames=keys)
	writer.writeheader()
	for word, obj in vocab.iteritems():
		res = {k:v for k,v in obj.iteritems()}
		res["word"] = word
		writer.writerow(res)
