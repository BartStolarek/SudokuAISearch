import random


class Change:
    def __init__(self):
        self.nothing


class Node:
    def __init__(self, cell, value):
        self.cell = cell
        self.value = value


class Agent:
    def __init__(self):
        self.cell_order = [[], [], [], [], [], [], [], [], [], []]
        self.queue = []
        self.change_log = []  # 2D array containing historical: [cell, value, possible_values, tried_values]
        self.change_log_values = []
        self.step_count = 0
        self.visited = set()
        self.change_log = []

    def eds_advice(self, grid):
        self.grid = grid
        #queue = self.update_cell_solving_order()
        depth = 0
        self.queue_length = len(self.queue)
        queue = self.queue



        cell = queue.pop(0)
        print("Cell{} with pv: {}".format(cell.coord, cell.possible_values))

        remaining_cells = self.grid.get_remaining_empty_cell_count()
        print("Queue len: {}, depth: {}, remaining_cells: {}".format(self.queue_length, depth, remaining_cells))
        if not remaining_cells or depth == self.queue_length or not queue:
            print("Returning at depth {}, with queue: {}".format(depth, queue))
            return
        else:

            if cell.possible_values:
                for value in cell.possible_values:
                    if self.grid.check_valid(cell, value):
                        print("Applying Cell{} with value: {}".format(cell.coord, value))
                        self.grid.update_cell(cell, value)
                        depth += 1
                        self.dls(queue, depth)
                print("Went through all possible values on Cell{} and didn't find a valid, returning on depth {}".format(cell.coord, depth))
            else:
                print("No Cell{} possible values, returning at depth {}".format(cell.coord, depth))

    def dls(self,queue,  depth):
        remaining_cells = self.grid.get_remaining_empty_cell_count()
        print("Queue len: {}, depth: {}, remaining_cells: {}".format(self.queue_length, depth, remaining_cells))
        if not remaining_cells or depth == self.queue_length or not queue:
            print("Returning at depth {}, with queue: {}".format(depth, queue))
            return
        else:
            cell = queue.pop(0)
            if cell.possible_values:
                for value in cell.possible_values:
                    if self.grid.check_valid(cell, value):
                        print("Applying Cell{} with value: {}".format(cell.coord, value))
                        self.grid.update_cell(cell, value)
                        depth += 1
                        self.dls(queue, depth)
                print("Went through all possible values on Cell{} and didn't find a valid, returning on depth {}".format(cell.coord, depth))
            else:
                print("No Cell{} possible values, returning at depth {}".format(cell.coord, depth))




    def update_cell_solving_order(self, grid):

        self.order_cells_by_least_possible_values(grid)
        self.queue = [j for sub in self.cell_order for j in sub]  # flatten cell order


    def order_cells_by_least_possible_values(self, grid):
        for row in range(0, grid.cell_dimension):
            for column in range(0, grid.cell_dimension):
                cell = grid.flat_grid[row][column]
                minimum_count = len(cell.possible_values)
                if minimum_count:
                    self.cell_order[minimum_count].append(cell)

    def order_cells_by_closest_to_finish(self, grid):
        for row in range(0, grid.cell_dimension):
            for column in range(0, grid.cell_dimension):
                cell = grid.flat_grid[row][column]
                minimum_count = grid.get_minimum_remaining(cell)
                self.cell_order[minimum_count].append(cell)
