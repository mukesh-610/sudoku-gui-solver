# sudoku-gui-solver
A GUI based sudoku solver, written in Python, with Tkinter as the GUI frontend.

# How to run:
Clone this repo.
- run `solver_gui.pyw`.
- Input the sudoku (You can either input the unsolved puzzle directly, or choose to input it from a file. If you want to input it from a file, make sure that the file's format is similar to the format of `puzzfile.txt` in this repo.)
- Click on solve.

# Input format:
- Please input digits 0 through 9 for each cell.
- 0 stands for a blank box, while 1-9 indicates a pre-filled box.

The solver can only solve puzzles which are "valid" sudokus i.e., which are solvable and contain only one unique solution.

# Reporting bugs or improvements:
Bugs or improvements can be sent by opening a new issue or PR here.
