# KR-lab1
Knowledge Representation - UvA - lab1
Authors: Juan Buhagiar Gautier Dagan

## Details:

This is our repo for the 2017 KR class - Sudoku Lab.
To run experiment, please edit the MAIN variables in main.py ()
and run file.

Please keep in mind that choosing a high number of sudokus and low % interval will affect the time
considerably.

Other files include:
  - scraper.py (scrapes menneske.no for 2b2, 3b3, 4b4, and 5b5 sudokus).
  - solve-script.py (python script called in subprocess with temporary cnf file)
  - sudokusolver.py (python file containing logic for the encoding the sudokus and calling the subprocess)
  - readSudokus.py (python file containing logic to read in sudoku.txt files obtained from scraper)
  - .CSV files are results from the experiments that we obtained
  - results.xlxs is an excel file with the combined statistics for all sizes.
