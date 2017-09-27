"""
The implementation of this Sudoku solver is based on the paper:
    "A SAT-based Sudoku solver" by Tjark Weber
    https://www.lri.fr/~conchon/mpri/weber.pdf
"""
import pycosat
import subprocess
import numpy as np
from pprint import pprint

def v(i, j, d, size):
    """
    Return the number of the variable of cell i, j and digit d,
    which is an integer in the range of 1 to 729 (including).
    """
    return (size**2) * (i - 1) + size * (j - 1) + d


def sudoku_clauses(size):
    """
    Create the Sudoku clauses - depending on the size of the sudoku,
    (4, 9, 16, 25) and return them as a list.
    Note that these clauses are *independent* of the particular
    Sudoku puzzle at hand.
    """
    res = []
    # for all cells, ensure that the each cell:
    for i in range(1, (size+1)):
        for j in range(1, (size+1)):
            # denotes (at least) one of the 9 digits (1 clause)
            res.append([v(i, j, d, size) for d in range(1, (size+1))])
            # does not denote two different digits at once (36 clauses)
            for d in range(1, (size+1)):
                for dp in range(d + 1, (size+1)):
                    res.append([-v(i, j, d, size), -v(i, j, dp, size)])

    def valid(cells):
        # Append 324 clauses, corresponding to 9 cells, to the result.
        # The 9 cells are represented by a list tuples.  The new clauses
        # ensure that the cells contain distinct values.
        for i, xi in enumerate(cells):
            for j, xj in enumerate(cells):
                if i < j:
                    for d in range(1, (size+1)):
                        res.append([-v(xi[0], xi[1], d, size), -v(xj[0], xj[1], d, size)])

    # ensure rows and columns have distinct values
    for i in range(1, (size+1)):
        valid([(i, j) for j in range(1, (size+1))])
        valid([(j, i) for j in range(1, (size+1))])


    if size == 4:
        # print(size)
        for i in 1, 3:
            for j in 1, 3:
                valid([(i + k % 2, j + k // 2) for k in range(size)])
        assert len(res) == 400
        # print(len(res))
    elif size == 9:
        # ensure 3x3 sub-grids "regions" have distinct values
        for i in 1, 4, 7:
            for j in 1, 4 ,7:
                valid([(i + k % 3, j + k // 3) for k in range(size)])
        # print(len(res))
        assert len(res) == (size**2) * (1 + 36) + 27 * 324
    elif size == 16:
        for i in 1, 5, 9, 13:
            for j in 1, 5, 9, 13:
                valid([(i + k % 4, j + k // 4) for k in range(size)])
        assert len(res) == 123136
    elif size == 25:
        for i in 1, 6, 11, 16, 21:
            for j in 1, 6, 11, 16, 21:
                valid([(i + k % 5, j + k // 5) for k in range(size)])
        # print(len(res))
        assert len(res) == 750625
    else:
        print(size)
        raise ValueError("Size of Sudoku Unknown")

    return res


def solve(grid):
    """
    solve a Sudoku grid inplace
    """
    size = len(grid[0])
    clauses = sudoku_clauses(size)
    for i in range(1, (size+1)):
        for j in range(1, (size+1)):
            d = grid[i - 1][j - 1]
            # For each digit already known, a clause (with one literal).
            # Note:
            #     We could also remove all variables for the known cells
            #     altogether (which would be more efficient).  However, for
            #     the sake of simplicity, we decided not to do that.
            if d:
                clauses.append([v(i, j, d, size)])

    # solve the SAT problem using subprocess to capture output as string
    # print(clauses)
    # with open('temp_clauses.txt','wb') as f:
    np.save("temp_clauses", clauses)
    temp_str = "cnf = " + repr(clauses) + ";"
    proc = subprocess.Popen(["python", "solve_script.py"],
       stdout=subprocess.PIPE)
    out = proc.communicate()[0]
    stats = parse_stats_output(out)
    return stats

def parse_stats_output(output_str):
    return np.array(list(filter(lambda x: x != "" and is_number(x), output_str.decode().split(" ")))[-10:]).astype(np.float)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
