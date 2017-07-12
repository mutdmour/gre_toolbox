# transform original list of words from wikipedia into a csv
import csv

input_file = open("original_list.txt","r")

words = {}
count = 0
for line in input_file:
	count += 1
	line = line.strip()
	index = line.index("->")
	line = line[index+2:]
	line = line.split(",")
	def add(word):
		word = word.strip().lower()
		words[word] = 0
		return word
	map(add, line)

output_file = 'words.csv'
with open(output_file, 'wb') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in words.items():
       writer.writerow([key, float(value)])

print("# of original lines", count)
print("# of words in dic:", len(words))
print("outputed result to ",output_file)
