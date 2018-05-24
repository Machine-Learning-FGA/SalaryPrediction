import csv

def create_column_words (in_csv, out_csv):
	input_file = open(in_csv, 'r')
	output_file = open(out_csv, 'w')

	data = csv.reader(input_file)
	writer = csv.writer(output_file,quoting=csv.QUOTE_ALL)

	j = 0

	for line in data:
		if j == 0:
			for i in range (0, len(line)):
				line[i] = i
			j += 1

		writer.writerow(line)

	input_file.close()
	output_file.close()

	return

create_column_words ("FinalTrainFixdColumns.csv", "FinalTrainNumberized.csv")