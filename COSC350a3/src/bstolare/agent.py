import time
"""
Class
Agent

Class object used to represent the AI algorithm agent who will solve the sudoku puzzle

parameters: verbose - parameter to indicate whether debugging print to console will occur
returns:
"""
class Agent:
    def __init__(self, verbose, wait_time):
        self.cell_order = [[], [], [], [], [], [], [], [], [], []]
        self.verbose = verbose
        self.wait_time = wait_time

    """
    Class Function
    solve_sudoku_with_dls
    
    Class function, which will initiate the first depth and step to solving
    the sudoku, but using a depth limit search. 
    
    parameters: grid - the grid that needs to be solved
    returns: 
    """
    def solve_sudoku_with_dls(self, grid):
        self.grid = grid
        queue = self.update_cell_solving_order()
        depth = 0
        self.queue_length = len(queue)
        step = 0


        if queue:
            step += 1
            print("#########################################################")
            print("############### STEP {}  ################################".format(step))
            print("#########################################################\n")
            cell = queue.pop(0)
            self.grid.print_flat_grid_with_focus_cell(cell)

            remaining_cells = self.grid.get_remaining_empty_cell_count()
            print("Agent: Attempting to solve Cell{}, possible values: {}\n".format(cell.coord, cell.possible_values))

            print("Agent: There are currently {} remaining cells to solve\n".format(remaining_cells))

            if not remaining_cells or depth == self.queue_length or not queue:
                if self.verbose > 0:
                    print("\tAgent: Limit reached, returning at depth {}, with queue: {}\n".format(depth, queue))
                return
            else:
                if cell.possible_values:
                    for value in cell.possible_values:
                        if self.grid.check_valid(cell, value):
                            print("Agent: Applying Cell{} with value: {}\n".format(cell.coord, value))
                            self.grid.update_cell(cell, value)
                            depth += 1
                            self.dls(queue, depth, step)
                    if self.verbose > 0:
                        print(
                            "\tAgent: Went through all possible values on Cell{} and didn't find a valid value, at depth {} returning to depth {}\n".format(
                                cell.coord, depth, depth - 1))
                else:
                    print("Agent: Cell{} has no possible values, at depth {} returning to depth {}\n".format(cell.coord, depth, depth - 1))

    """
    Class Function
    dls
    
    Class function, which is the recursion function, allowing for a depth first search. It will have
    a depth limit to remove infinite loops. Once solution is found by remaining empty cells being
    0, it will return completely, otherwise it will return if it finds the depth limit, and/or no
    more cells to solve, or the remaining cells don't have possible values to choose. 
    
    parameters: 
        queue - the current queue of cells left that need to be solved
        depth - the maximum depth of searching for the correct solution
        step - the step count for console user friendly UI purposes
    returns: 
    """
    def dls(self, queue, depth, step):
        time.sleep(self.wait_time)
        step += 1
        remaining_cells = self.grid.get_remaining_empty_cell_count()

        if not remaining_cells or depth == self.queue_length or not queue:
            if self.verbose > 0:
                print("\tAgent: Limit reached, returning at depth {}, with queue: {}\n".format(depth, queue))
            return
        else:
            cell = queue.pop(0)

            print("#########################################################")
            print("############### STEP {}  ################################".format(step))
            print("#########################################################\n")

            self.grid.print_flat_grid_with_focus_cell(cell)


            print("Agent: Attempting to solve Cell{}, possible values: {}\n".format(cell.coord, cell.possible_values))

            print("Agent: There are currently {} remaining cells to solve\n".format(remaining_cells))
            if cell.possible_values:
                for value in cell.possible_values:
                    if self.grid.check_valid(cell, value):
                        print("Agent: Applying Cell{} with value: {}\n".format(cell.coord, value))
                        self.grid.update_cell(cell, value)
                        depth += 1
                        self.dls(queue, depth, step)
                if self.verbose > 0:
                    print(
                        "\tAgent: Went through all possible values on Cell{} and didn't find a valid value, at depth {} returning to depth {}\n".format(
                            cell.coord, depth, depth - 1))
            else:
                print("Agent: Cell{} has no possible values, at depth {} returning to depth {}\n".format(cell.coord, depth, depth - 1))

    """
    Class Function
    update_cell_solving_order
    
    Class function, which takes the multidimensional array cell_order, and flattens it in to a 
    1D array of cells that need to be solved
    
    parameters: 
    returns: queue - 1D array of cells that need to be solved
    """
    def update_cell_solving_order(self):

        self.order_cells_by_least_possible_values(self.grid)
        queue = [j for sub in self.cell_order for j in sub]  # flatten cell order
        return queue

    """
    Class Function
    order_cells_by_least_possible_values
    
    Class function, which goes through the grid's flat grid, and checks each cell's possible value count, 
    and puts that cell in to the corresponding ith element in cell order array. 
    
    parameters: grid - the grid of cells that is to be ordered
    returns: 
    """
    def order_cells_by_least_possible_values(self, grid):
        for row in range(0, grid.cell_dimension):
            for column in range(0, grid.cell_dimension):
                cell = grid.flat_grid[row][column]
                minimum_count = len(cell.possible_values)
                if minimum_count:
                    self.cell_order[minimum_count].append(cell)


