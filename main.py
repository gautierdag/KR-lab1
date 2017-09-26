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

    percentages = np.arange(0.2, 1, 0.05) #the percentages of known numbers on the grid
    ALL_STATS = np.zeros((4, len(percentages), 11))
    sdk_type_index = 0
    count = 0
    # print(dirs)
    for sudokuType in [dirs[2]]:
        current_path = join(dir_path, sudokuType)
        onlyfiles = [f for f in listdir(current_path) if isfile(join(current_path, f))];
        TYPE_STATS = np.zeros((len(percentages), 11))
        total = len(onlyfiles)
        if count == 0:
            for file in onlyfiles:
                temp_STATS = np.zeros((len(percentages), 11))
                for p in range(len(percentages)):
                    sudoku = parse(current_path, file, int(sudokuType))
                    # pp.pprint(sudoku)
                    original = deepcopy(sudoku)
                    sudokuWith0 = removePercentage(sudoku, (1-percentages[p]), int(sudokuType))
                    # pp.pprint(sudokuWith0)
                    temp_STATS[p] = solve(sudokuWith0)
                    # pp.pprint(sudokuWith0)
                    #Stats to check if sudoku solution found is different than original
                    # if original != sudokuWith0:
                        # temp_STATS[p][10] = 1.0

                TYPE_STATS = (temp_STATS*(1/total))+TYPE_STATS
                count += 1
                print("Processed: {0} out of {1}".format(count, total))
                if count%5 == 0:
                    print("Saving Current Progress")
                    with open('results.csv','wb') as f:
                        np.savetxt(f, TYPE_STATS, delimiter=",")

            # TYPE_STATS = TYPE_STATS/count
            ALL_STATS[sdk_type_index] = TYPE_STATS
        # sdk_type_index += 1
    with open('results.csv','wb') as f:
        np.savetxt(f, ALL_STATS[0], delimiter=",")

    #Print the Stats for 2by2
    # fig, ax = plt.subplots(5,2, sharex='col')
    #
    # ax[0, 0].plot(percentages, ALL_STATS[sdk_type_index].T[0])
    # ax[0, 0].set_title('Seconds')
    #
    # ax[0, 1].plot(percentages, ALL_STATS[sdk_type_index].T[1])
    # ax[0, 1].set_title('Level')
    #
    # ax[1, 1].plot(percentages, ALL_STATS[sdk_type_index].T[2])
    # ax[1, 1].set_title('Variables')
    #
    # ax[2, 1].plot(percentages, ALL_STATS[sdk_type_index].T[3])
    # ax[2, 1].set_title('Used')
    #
    # ax[3, 1].plot(percentages, ALL_STATS[sdk_type_index].T[4])
    # ax[3, 1].set_title('Original')
    #
    # ax[1, 0].plot(percentages, ALL_STATS[sdk_type_index].T[5])
    # ax[1, 0].set_title('Conflicts')
    #
    # ax[2, 0].plot(percentages, ALL_STATS[sdk_type_index].T[6])
    # ax[2, 0].set_title('Learned')
    #
    # ax[3, 0].plot(percentages, ALL_STATS[sdk_type_index].T[7])
    # ax[3, 0].set_title('Limit')
    #
    # ax[4, 0].plot(percentages, ALL_STATS[sdk_type_index].T[8])
    # ax[4, 0].set_title('Agility')
    #
    # ax[4, 1].plot(percentages, ALL_STATS[sdk_type_index].T[9])
    # ax[4, 1].set_title('MB')
    #
    # fig.subplots_adjust(hspace=0.55)
    #
    # plt.show()

    # ALL_STATS.tofile('results.txt',sep=",",format="%s")




if __name__ == "__main__":
    main()
