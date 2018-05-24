def merge_words (in_path, out_path):
	fileIN = open(in_path,"r")
	fileOUT = open(out_path,"w")

	for x in fileIN:
		h = '\''
		s = h + x[:-1] + h + ","

		fileOUT.write(s)

	fileIN.close()
	fileOUT.close()
	return

merge_words("allwords.txt", "gambiarreited.txt")