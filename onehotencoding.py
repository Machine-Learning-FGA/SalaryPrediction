def common_words (inp_path, out_path, column):

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
	ALL = defaultdict(lambda: 0)

	j = 0
	for i, blob in enumerate(bloblist):
		scores = {word: tfidf(word, blob, bloblist) for word in blob.words if (ALL[word] == 0)}
		sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)

		j += 1
		for word, score in sorted_words[:4]:
			ALL[word] = 1
			print(word)

		if (j == 100):
			break

	input_file.close()
	outfile.close()

	return

#############merge words#################

