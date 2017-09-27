"""
Hypothesis:

Increasing the % of known numbers in similary spatially distributed sudoku board,
We expect performance (eg: the rate at which backtrack) to increase at
the same rate for different board sizes."""

from os import listdir
from os.path import isfile, join
import os.path
import pprint
import numpy as np
from copy import copy, deepcopy

from sudokusolver import solve
from readSudokus import parse, removePercentage
import matplotlib.pyplot as plt

def main():
    pp = pprint.PrettyPrinter(indent=4)
    currentDir = os.path.realpath(__file__);
    dir_path = join(os.path.dirname(currentDir), "puzzles")
    dirs = [d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]

    percentages = np.arange(0.2, 1, 0.1) #the percentages of known numbers on the grid
    ALL_STATS = np.zeros((4, len(percentages), 10))
    sdk_type_index = 0
    count = 0
    # print(dirs)
    for sudokuType in [dirs[3]]:
        current_path = join(dir_path, sudokuType)
        onlyfiles = [f for f in listdir(current_path) if isfile(join(current_path, f))];
        TYPE_STATS = np.zeros((len(percentages), 10))
        total = len(onlyfiles[-1000:])
        if count == 0:
            for file in onlyfiles[-1000:]:
                temp_STATS = np.zeros((len(percentages), 10))
                for p in range(len(percentages)):
                    sudoku = parse(current_path, file, int(sudokuType))
                    # pp.pprint(sudoku)
                    sudokuWith0 = removePercentage(sudoku, (1-percentages[p]), int(sudokuType))
                    # pp.pprint(sudokuWith0)
                    temp_STATS[p] = solve(sudokuWith0)
                    # pp.pprint(sudokuWith0)

                TYPE_STATS = (temp_STATS*(1/total))+TYPE_STATS
                count += 1
                print("Processed: {0} out of {1}".format(count, total))
                if count%5 == 0:
                    print("Saving Current Progress")
                    with open('results.csv','wb') as f:
                        np.savetxt(f, TYPE_STATS, delimiter=",")

            ALL_STATS[sdk_type_index] = TYPE_STATS
        # sdk_type_index += 1
    with open('results.csv','wb') as f:
        np.savetxt(f, ALL_STATS[0], delimiter=",")

if __name__ == "__main__":
    main()
