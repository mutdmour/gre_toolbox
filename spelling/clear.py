import csv

print "This script will remove all words with .5 or more to cleared.txt"
ans = raw_input("(y|n)? ")
if (ans == "y"):
	file = 'words.csv'
	words = {}
	with open(file, 'rb') as csv_file:
	    reader = csv.reader(csv_file)
	    for key, value in reader:
		words[key] = float(value)
	
	cleared = []
	keys = words.keys()
	for k in keys:
		v = words[k]
		if (v >= .5):
			cleared.append(k)
			words.pop(k)

	ans = raw_input(str(len(cleared)) + " words will be cleared (y|n)? ")
	#print len(cleared), cleared[0:10]
	if (ans == "y"):
		with open(file, 'wb') as csv_file:
		    writer = csv.writer(csv_file)
		    for key, value in words.items():
		       writer.writerow([key, value])

		output_file = 'cleared.txt'
		with open(output_file, 'wb') as write_file:
		    #writer = csv.writer(csv_file)
		    for word in cleared:
			write_file.write(word+"\n")
