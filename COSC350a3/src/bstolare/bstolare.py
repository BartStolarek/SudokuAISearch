from sudoku import Cell, Box, Grid
from math import sqrt
from agent import Agent
import sys

def main():

    args = sys.argv[1:]
    args = ["f","./grid.txt",0, 0, 0]

    print("PROJECT DETAILS:")
    print("Formal Name: Depth Limit Search Sudoku Solver")
    print("App Name: sudokuAIsearch")
    print("Author: Bartholomew Stolarek")
    print("Author's Email: bstolare@myune.edu.au")
    print("URL: https://github.com/BartStolarek/SudokuAISearch")
    print("License: BSD")
    print("GUI Framework: NA - Console only\n\n")

    print("PLEASE READ THE README FIRST\n\n")

    # Assigning Variables
    empty_value = 0
    verbose = 0
    wait_time = 0
    input_grid = []


    """ PARSING ARGUMENTS """
    # If no arguments
    if len(args) == 0:
        # Create pre-defined 2D * 2D array to represent maze
        print("No user arguments, building default grid")
        # Create 2D array of cells to present each box
        box00 = [[9, 0, 0],
                 [1, 6, 0],
                 [0, 0, 8]]
        box01 = [[1, 7, 0],
                 [0, 4, 0],
                 [0, 0, 3]]
        box02 = [[4, 0, 2],
                 [0, 9, 5],
                 [0, 0, 0]]
        box10 = [[0, 1, 0],
                 [0, 4, 0],
                 [5, 8, 9]]
        box11 = [[9, 0, 0],
                 [0, 0, 0],
                 [0, 0, 7]]
        box12 = [[5, 7, 3],
                 [0, 2, 0],
                 [0, 1, 0]]
        box20 = [[0, 0, 0],
                 [6, 7, 0],
                 [3, 0, 1]]
        box21 = [[4, 0, 0],
                 [0, 2, 0],
                 [0, 5, 8]]
        box22 = [[7, 0, 0],
                 [0, 5, 8],
                 [0, 0, 6]]

        # Combine boxes in to a 2D array
        input_grid = [
            [box00, box01, box02],
            [box10, box11, box12],
            [box20, box21, box22]
        ]
        # Set the empty value to zero and verbose to 0
        empty_value = 0
        verbose = 0
    else:
        # Command line arguments present

        # Check whether enough arguments were provided
        if len(args) != 5:
            raise ValueError("Main: Number of arguments provided is incorrect")

        # if first argument is not f, then use pre-defined grid
        elif args[0] != "f":
            print("Building default grid from main function")
            empty_value = args[2]
            verbose = args[3]
            wait_time = args[4]
            box00 = [[9, 0, 0],
                     [1, 6, 0],
                     [0, 0, 8]]
            box01 = [[1, 7, 0],
                     [0, 4, 0],
                     [0, 0, 3]]
            box02 = [[4, 0, 2],
                     [0, 9, 5],
                     [0, 0, 0]]
            box10 = [[0, 1, 0],
                     [0, 4, 0],
                     [5, 8, 9]]
            box11 = [[9, 0, 0],
                     [0, 0, 0],
                     [0, 0, 7]]
            box12 = [[5, 7, 3],
                     [0, 2, 0],
                     [0, 1, 0]]
            box20 = [[0, 0, 0],
                     [6, 7, 0],
                     [3, 0, 1]]
            box21 = [[4, 0, 0],
                     [0, 2, 0],
                     [0, 5, 8]]
            box22 = [[7, 0, 0],
                     [0, 5, 8],
                     [0, 0, 6]]

            input_grid = [
                [box00, box01, box02],
                [box10, box11, box12],
                [box20, box21, box22]
            ]

        # If there are arguments and first user input argument is 'f' then take grid from provided
        # file name
        elif args:
            print("Obtaining grid from file provided\n")
            file = args[1]
            empty_value = args[2]
            verbose = args[3]
            wait_time = args[4]
            f = open(file, 'r')
            input_grid = f.read()

            f.close()
        else:
            raise ValueError("Main: Passed Arguments are incorrect, please read the readme and try again")

    verbose = int(verbose)
    empty_value = str(empty_value)
    wait_time = int(wait_time)
    """ CREATE GRID """
    grid = Grid(input_grid, verbose, empty_value)

    print("#########################################################")
    print("##### STARTING PUZZLE  ##################################")
    print("#########################################################")
    grid.print_flat_grid_values()
    print("")
    if verbose > 0:
        print("Printing the coords for each cell:")
        grid.print_flat_grid_coords()
        print("")
        print("Printing the box coords for each cell:")
        grid.print_flat_grid_box()
        print("")
        print("Printing the possible values for each cell:")
        grid.print_flat_grid_possible_values()
    print("#########################################################")
    print("#########################################################\n")
    print("Grid: There are {} remaining cells to solve\n".format(grid.remaining_empty_cells))

    grid.update_all_cells_possible_values()
    print("")

    """ CREATE AGENT AND START SOLVING """

    print("Creating Agent to solve sudoku puzzle\n")
    agent = Agent(verbose, wait_time)

    agent.solve_sudoku_with_dls(grid=grid)
    print("\n#########################################################")
    print("##### RESULTS  ##########################################")
    print("#########################################################\n")

    if not grid.remaining_empty_cells:
        print("SOLVED!\n")
    else:
        print("NOT SOLVED!\n")

    grid.print_flat_grid_values()

    print("\n\n")


if __name__ == '__main__':
    print("here")
    main()
