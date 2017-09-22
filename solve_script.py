import pycosat
import numpy as np

cnf = np.load("temp_clauses.npy")
pycosat.solve(cnf,verbose=1)
