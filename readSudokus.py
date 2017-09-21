import csv
import random

def parse(current_path, file, size):
	sudoku = [[0 for x in range(size*size)] for y in range(size*size)]
	print(current_path)
	print(file)
	# join(current_path,file)
	with open(current_path+"/"+file, 'rt') as f:
		reader = csv.reader(f)
		for row in reader:
			sudoku[int(row[0])][int(row[1])] = int(row[2])
	return sudoku

def removePercentage(sudoku, percentage, size):
	numberOfChange = round(percentage * (size**4))
	for x in range(int(numberOfChange)):
		x = random.randint(0,(size**2)-1)
		y = random.randint(0,(size**2)-1)
		sudoku[x][y] = 0;
	return sudoku
