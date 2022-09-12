CONTENTS OF THIS FILE
---------------------

* Author & Project
* Introduction
* Requirements
* Recommended modules
* Installation
* Configuration
* Troubleshooting
* Maintainers

AUTHOR & PROJECT
------------

* Formal Name: Depth Limit Search Sudoku Solver
* App Name: sudokuAIsearch
* Bundle: com.sudokuAIsearch
* Project Name: Depth Limit Search Sudoku Solver
* Author: Bartholomew Stolarek
* Author's Email: bstolare@myune.edu.au
* URL: https://github.com/BartStolarek/SudokuAISearch
* License: BSD
* GUI Framework: NA - console only


INTRODUCTION
------------

The SudokuAISearch python module aka file 'bstolre.py' will take none or 4 command line arguments.
The program will then build a grid and create an agent, who will solve the puzzle in steps using a Depth
Limit Search algorithm. Each step will update the cell's possible values to help quickly identify the
correct solution.

REQUIREMENTS
------------

This module requires the following modules:

* [sudoku](../sudoku.py)
* [agent](../agent.py)


RECOMMENDED MODULES
-------------------

* [grid](../grid.txt)

INSTALLATION
------------

* No installation required, python version needs to be 3.10.6 or greater
* Make sure to chmod +x bstolare.py if using linux terminal



CONFIGURATION - Command Line Arguments
-------------
 * No command line arguments can be provided

 *  Command line arguments can be provided in this order (example: bstolare.py f ./grid.txt " " 0):

   - first argument

     This is the name of the program to be run, in this case "bstolare.py"

   - second argument

        This indicates that a file is to be used to create the grid. Use 'f' to indicate that a file
        is to be used, use 'n' to indicate that no file is to be used and grid is to be generated from
        internal python code.

   - third argument

        if second argument is a 'f', put in the address of the file that the grid is to be taken from.
        The file should have all digits in one line, and zero's are to be considered as empty cells.
        The program will then create the grid row by row.
        If 'n' is used in second argument then put a 'n' in this argument too

   - fourth argument

        This argument is used for the user to define how they would they like the sudoku puzzle to represent
        empty cells. Recommended inputs for this is either " " or 0

   - fifth argument

        This is used more for debugging purposes. If the user would like to see more output on to the console,
        the user should input a 1, other input a 0

   - sixth argument

        This argument is to indicate to the agent, how many seconds to wait between printing steps to console.
        This has no effect on calculation, purely a user friendliness configuration


TROUBLESHOOTING
---------------

 * If there is an issue, then use the verbose (fifth commandline argument) to debug the system.



MAINTAINERS
-----------

Current maintainers:
* Bart Stolarek https://github.com/BartStolarek

