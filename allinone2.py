import math
from textblob import TextBlob as tb
import pandas as pd #manipulate csv
import csv #manipulate csv
import string #manipulate string
from collections import defaultdict #dictionary/set of words
import nltk
from nltk.corpus import wordnet


######remove columns########

def remove_columns (path, columns, newpath):
	file=pd.read_csv(path)

	keep_col = columns

	new_file = file[keep_col]

	new_file.to_csv(newpath, index=False)

	return

#####remove asterisks##############

def remove_asterisks (inp_path, out_path):
	input_file = open(inp_path, 'r')
	output_file = open(out_path, 'w')

	data = csv.reader(input_file)
	writer = csv.writer(output_file,quoting=csv.QUOTE_ALL)# dialect='excel')
	specials = '*'

	for line in data:
	    line = [value.replace(specials, ' ').lower() for value in line]
	    writer.writerow(line)

	input_file.close()
	output_file.close()

	return

#########regex find common words################

def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

def common_words (inp_path, out_path):

	input_file = open(inp_path, 'r')
	outfile = open(out_path, 'w')

	data = csv.reader(input_file)

	i = 0;

	bloblist = []
	for line in data:
		if (i == 0):
			i+=1
			continue

		s = line[1]

		bloblist.append(tb(s))


	print (len(bloblist))

	j = 0
	for i, blob in enumerate(bloblist):
		scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
		sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
		j += 1
		for word, score in sorted_words[:4]:
			outfile.write(word + '\n')
		if (j == 600):
			break
	input_file.close()
	outfile.close()

	return

#############merge words#################

def merge_words (f1, f2, f3, out_path):
	file = open(f1,"r")
	file1 = open(f2,"r")
	file2 = open(f3,"r")
	outfile = open(out_path, "w")
	set = {""}

	for line in file: 
		set.add(line)
	for line in file1: 
		set.add(line)
	for line in file2: 
		set.add(line)

	set = sorted(set)
	for x in set:
		outfile.write(x)

	file.close()
	file1.close()
	file2.close()
	outfile.close()

	return

##############add words as columns###############

def create_column_words (in_csv, out_csv, allwords):
	input_file = open(in_csv, 'r')

	input_file2 = open (allwords, 'r')
	ncol = sum(1 for line in input_file2)
	input_file2.close()

	input_file2 = open (allwords, 'r')	
	output_file = open(out_csv, 'w')

	data = csv.reader(input_file)
	writer = csv.writer(output_file,quoting=csv.QUOTE_ALL)

	i = 0

	for line in data:
		if i != 0:
			for i in range(0, ncol):
				line.append('0')
		if i == 0:
			for kk in input_file2:
				line.append(kk[:-1])
			i += 1

		writer.writerow(line)

	input_file.close()
	output_file.close()
	input_file2.close()

	return

######set column to 1 if word present in row##########
def find(L, target):
    start = 0
    end = len(L) - 1
    while start <= end:
        middle = (start + end)// 2
        midpoint = L[middle]
        if midpoint > target:
            end = middle - 1
        elif midpoint < target:
            start = middle + 1
        else:
            return midpoint

def setter (in_csv, out_csv, idx):

	input_file = open(in_csv, 'r')
	output_file = open(out_csv, 'w')

	data = csv.reader(input_file)
	writer = csv.writer(output_file,quoting=csv.QUOTE_ALL)

	i = 0;
	dicto = defaultdict(lambda: 0)
	finded = defaultdict(lambda: 0)
	ALLWORDS = []

	for line in data:
		if (i == 0):
			writer.writerow(line)
			for i in range(idx, len(line)):
				dicto[line[i].lower()] = i
				ALLWORDS.append(line[i].lower())
			i+=1
			continue

		abc = tb(line[1])

		for word in list(set(abc.words)): #pega todas as palavras da descriçao
			if ((find(ALLWORDS, word.lower()) == None) and (finded[word.lower()] == 0)): #se a palavra nao ta na lista das seletas
				now = wordnet.synsets(word) #pega os sinonimos da palavra atual
				achou = 0
				for syn in now: #procura cada sinonimo da palavra atual
					for l in syn.lemmas(): #no array de palavras
						if ((find(ALLWORDS, l.name().lower()) != None) or (finded[word.lower()] != 0 and finded[word.lower()] != -1)):
								line[dicto[l.name().lower()]] = 1
								finded[word] = l.name().lower()
								achou = 1
						if (achou == 1):
							break
					if (achou == 1):
						break
				if (achou == 0):
					finded[word.lower()] = -1
			elif (finded[word.lower()] != 0 and finded[word.lower()] != -1):
				line[dicto[finded[word.lower()]]] = 1
			elif (find(ALLWORDS, word.lower()) != None):
				line[dicto[word.lower()]] = 1
				finded[word.lower()] = word.lower()

		writer.writerow(line)

	input_file.close()
	output_file.close()

	return


# remove_columns ("Train_rev1.csv", ['Title', 'FullDescription', 'LocationRaw', 'LocationNormalized', 'ContractType', 'ContractTime', 'Company', 'SalaryNormalized'], "TrainFixdColumns.csv")
# remove_columns ("Test_rev1.csv", ['Title', 'FullDescription', 'LocationRaw', 'LocationNormalized', 'ContractType', 'ContractTime', 'Company'], "TestFixdColumns.csv")
# remove_columns ("Valid_rev1.csv", ['Title', 'FullDescription', 'LocationRaw', 'LocationNormalized', 'ContractType', 'ContractTime', 'Company'], "ValidFixdColumns.csv")

# remove_asterisks ("TrainFixdColumns.csv", "TrainFixdAsterisks.csv")
# remove_asterisks ("TestFixdColumns.csv", "TestFixdAsterisks.csv")
# remove_asterisks ("ValidFixdColumns.csv", "ValidFixdAsterisks.csv")

# common_words ("TrainFixdAsterisks.csv", "train.txt")
# common_words ("TestFixdAsterisks.csv", "test.txt")
# common_words ("ValidFixdAsterisks.csv", "Valid.txt")

# merge_words ("train.txt", "test.txt", "Valid.txt", "allwords.txt")

# create_column_words ("TrainFixdAsterisks.csv", "TrainWithColumns.csv", "allwords.txt")
# create_column_words ("TrainFixdAsterisks.csv", "TrainWithColumns.csv", "allwords.txt")
# create_column_words ("TestFixdAsterisks.csv", "TestWithColumns.csv", "allwords.txt")

# setter ("TrainWithColumns.csv", "FinalTrain.csv", 8)
# setter ("TestWithColumns.csv", "FinalTest.csv", 7)
setter ("ValidWithColumns.csv", "FinalValid.csv", 7)
