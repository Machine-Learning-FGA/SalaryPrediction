import random
import csv
import os
from textblob import TextBlob as tb
from collections import defaultdict #dictionary/set of words
import math
import pandas as pd
from numpy.random import permutation

def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

# o=open("FinalTrem.txt", 'w')

csvfile = pd.read_csv('TestFixdAsterisks.csv')

bloblist = []

j = 0
for i in permutation(110000):
	bloblist.append(tb(csvfile.values[i+1][3]))
	j += math.log(csvfile.size, 1.15)
	if (j >= 110000):
		break
j = 0
ALL = defaultdict(lambda: 0)

for i, blob in enumerate(bloblist):
	scores = {word: tfidf(word, blob, bloblist) for word in blob.words if (ALL[word] == 0)}
	sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)

	j += 1
	for word, score in sorted_words[:4]:
		ALL[word] = 1
		print (word)

	if (j == 1000):
		break