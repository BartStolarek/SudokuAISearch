from sudoku import Cell, Box, Grid
from math import sqrt


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

    grid = Grid(boxes_in_grid, input_grid)



    grid.print_flat_grid_values()

    print("")

    grid.print_flat_grid_coords()

    found = True
    while found:
        print("")
        found = grid.check_for_final_cell()





if __name__ == '__main__':
    main()
