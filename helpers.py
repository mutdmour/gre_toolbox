import csv, random
from gtts import gTTS

keys = ["word","deck","source","def","ex", "weight", "lastTested","numTested","numRight"]
words_file = "vocab.csv"

input_file = words_file
def reader():
	vocab = {}
	with open(input_file, 'rb') as csv_file:
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
	return vocab;

output_file = words_file
header_keys = keys
def writer(vocab):
	with open(output_file, 'wb') as csv_file:
		writer = csv.DictWriter(csv_file, fieldnames=header_keys)
		writer.writeheader()
		for word, obj in vocab.iteritems():
			res = {k:v for k,v in obj.iteritems()}
			res["word"] = word
			writer.writerow(res)


def yesOrNo(message):
        while (True):
                answer = raw_input("{0} (y|n) ".format(message)).strip().lower()
                if (answer == "y"):
                        return True
                elif(answer == "n"):
                        return False


sound_file = "word.mp3"

def play():
        os.system("mpg321 --quiet -o alsa {0}".format(sound_file))

def speak(word):
        tts = gTTS(text=word, lang='en')
        tts.save(sound_file)
        play()

def repeat():
        play()


# takes a rule func that returns either True or false based on the value of a key
# in a dictionary. the limit sets how many keys it needs to consider. there's no 
# default limit
def getList(words, rule, limit=None, shuffle=False):
        c = 0
        l = []
        for k, v in words.iteritems():
                if (limit != None and c >= limit):
                        break
                if (rule(v)):
                        c += 1
                        l.append(k)
	if (shuffle):
		random.shuffle(l)
        return l

