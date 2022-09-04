from sudoku import Cell, Box, Grid
from math import sqrt
from agent import Agent


def main():
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
    boxes_in_grid = 9
    verbose = 1

    grid = Grid(boxes_in_grid, input_grid, verbose)

    print("#########################################################")
    print("##### STARTING PUZZLE  ##################################")
    print("#########################################################")
    grid.print_flat_grid_values()
    print("#########################################################")
    print("#########################################################\n")
    print("Grid: There are {} remaining cells to solve\n".format(grid.remaining_empty_cells))

    grid.update_all_cells_possible_values()
    print("")
    print("Creating Agent to solve sudoku puzzle\n")
    agent = Agent()

    style1 = "min_ascending_values_row"

    style2 = "min_ascending_values_column"

    style3 = "min_ascending_cell_values_box"

    style4 = "min_ascending_remaining_box"

    #while (grid.remaining_empty_cells != 0):
    agent.update_cell_solving_order(grid, style4)
    agent.solve_next_cell(grid)


if __name__ == '__main__':
    main()
