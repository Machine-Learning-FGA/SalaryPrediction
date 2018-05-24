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

merge_words ("titulos_relevantes.txt", "titulos_relevantes1.txt", "titulos_relevantes2.txt", "alltitulos.txt")
merge_words ("locaisraw_relevantes.txt", "locaisraw_relevantes1.txt", "locaisraw_relevantes2.txt", "alllocaisraw.txt")
merge_words ("locais_relevantes.txt", "locais_relevantes1.txt", "locais_relevantes2.txt", "alllocais.txt")
