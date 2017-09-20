from os import listdir
from os.path import isfile, join
import os.path
import pprint
import csv
import random
from sudokusolver import solve

def parse(current_path, file, size):
	sudoku = [[0 for x in range(size*size)] for y in range(size*size)] 
	with open(join(current_path,file), 'rt') as f: 
		reader = csv.reader(f)
		for row in reader:
			sudoku[int(row[0])][int(row[1])] = int(row[2])
	return sudoku

def removePercentage(sudoku, percentage, size): 
	numberOfChange = round(percentage * (size*size)* (size*size))
	for x in range(numberOfChange):
		x = random.randint(0,(size*size)-1)
		y = random.randint(0,(size*size)-1)
		sudoku[x][y] = 0;
	return sudoku

if __name__ == '__main__':
	pp = pprint.PrettyPrinter(indent=4)
	currentDir = os.path.realpath(__file__);

	dir_path = join(os.path.dirname(currentDir),"puzzles")
	dirs = [d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]

	for sudokuType in dirs:
		current_path = join(dir_path,sudokuType)
		onlyfiles = [f for f in listdir(current_path) if isfile(join(current_path, f))];
		for file in onlyfiles:
			sudoku = parse(current_path, file, int(sudokuType))
			pp.pprint(sudoku)
			sudokuWith0 = removePercentage(sudoku, 0.25, int(sudokuType))
			pp.pprint(sudokuWith0)
			solve(sudokuWith0)
			pp.pprint(sudokuWith0)
