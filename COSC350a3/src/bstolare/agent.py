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

    def keep_going(self, grid):
        iteration = 1
        visited = []
        print(len(self.queue))
        for cell in self.queue:
            print("{}: Cell{} in Box{} with pv: {}".format(iteration, cell.coord,cell.box,cell.possible_values))
            iteration += 1
        if self.queue:
            cell = self.queue.pop(0)
            for value in cell.possible_values:
                node = Node(cell, value)



    def startDFS(self, grid):
        self.grid = grid
        visited = []
        row = 0
        column = 0
        cell = self.grid.flat_grid[row][column]
        print("here Cell{}".format(cell.coord))
        for value in range(1, 10):
            node = Node(cell, value)
            print("check valid: {}".format(grid.check_valid(node.cell, value)))
            if node not in visited and grid.check_valid(node.cell, value):
                visited.append(node)
                print("Agent: updating Cell{} to value {}".format(node.cell.coord, node.cell.value))
                self.grid.update_cell(node.cell, node.value)
                self.mydfsNew(row, column + 1, visited)

    def newest(self, grid):
        visited = []
        self.grid = grid
        row = 0
        column = 0
        cell = self.grid.flat_grid[row][column]
        if cell.value == 0:
            print("Cell{} has value 0".format(cell.coord))
            for value in range(1, 10):
                node = Node(cell, value)
                if node not in visited and self.grid.check_valid(node.cell, value):
                    visited.append(node)
                    print("Cell{} updating to {}".format(node.cell.coord, value))
                    self.grid.update_cell(node.cell, value)
                    self.newestDFS(row, column + 1, visited)
        else:
            print("Cell{} has value {}".format(cell.coord, cell.value))
            self.newestDFS(row, column + 1, visited)

    def newestDFS(self, row, column, visited):
        column = column % 8
        if column == 0:
            row += 1
        if not self.grid.remaining_empty_cells or row >= self.grid.cell_dimension or column >= self.grid.cell_dimension:
            return

        cell = self.grid.flat_grid[row][column]
        if cell.value == 0:
            print("Cell{} has value 0".format(cell.coord))
            for value in range(1, 10):
                node = Node(cell, value)
                if node not in visited and self.grid.check_valid(node.cell, value):
                    visited.append(node)
                    print("Cell{} updating to {}".format(node.cell.coord, value))
                    self.grid.update_cell(node.cell, value)
                    self.newestDFS(row, column + 1, visited)
        else:
            print("Cell{} has value {}".format(cell.coord, cell.value))
            self.newestDFS(row, column + 1, visited)

    def another_one(self, grid):
        self.grid = grid
        iteration = 0
        value_list = []
        valid_cells = 0
        total_cells = grid.remaining_empty_cells
        row = 0
        column = 0
        cell = self.queue[0]
        print("Start with Cell{}".format(cell.coord))
        for value in cell.possible_values:
            if valid_cells == total_cells:
                return
            if self.grid.check_valid(cell, value):
                valid_cells += 1
                value_list.append(value)
                if valid_cells == total_cells:
                    return
                print("Added Cell{} value {} to value_list: {}".format(cell.coord, value, value_list))
                self.stuff(iteration + 1, valid_cells, total_cells, value_list)
            valid_cells -= 1
            value_list.pop()
        print(value_list)

    def stuff(self, iteration, valid_cells, total_cells, value_list):
        if valid_cells == total_cells or iteration == len(self.queue):
            return
        cell = self.queue[iteration]
        print("Cell{}".format(cell.coord))
        for value in cell.possible_values:
            if valid_cells == total_cells:
                return
            if self.grid.check_valid(cell, value):
                valid_cells += 1
                value_list.append(value)
                if valid_cells == total_cells:
                    return
                print("Added Cell{} value {} to value_list: {}".format(cell.coord, value, value_list))
                self.stuff(iteration + 1, valid_cells, total_cells, value_list)
            valid_cells -= 1
            value_list.pop()

    def mydfsNew(self, row, column, visited):

        column = column % 8
        if column == 0:
            row += 1
        if not self.grid.remaining_empty_cells or row >= self.grid.cell_dimension or column >= self.grid.cell_dimension:
            return

        cell = self.grid.flat_grid[row][column]
        if cell.value == 0:
            for value in range(1, 10):
                node = Node(cell, value)
                if node not in visited and self.grid.check_valid(node.cell, value):
                    visited.append(node)
                    print("Agent: updating Cell{} to value {}".format(node.cell.coord, value))
                    self.grid.update_cell(node.cell, value)
                    if not self.grid.remaining_empty_cells:
                        return
                    self.mydfsNew(row, column + 1, visited)
        else:
            self.mydfsNew(row, column + 1, visited)

    def solve_next_cell_new(self, grid):

        # Add move to cells position in change log

        cell = self.queue.pop(0)
        if cell not in self.change_log_cells:
            self.change_log_cells.append(cell)

        index = self.change_log_cells.index(cell)
        print(index)

    def solve_next_cell(self, grid):

        self.step_count += 1
        if self.queue:
            cell = self.queue.pop(0)
            current_cell_value = cell.value
            cell.value = "X"
            print("")
            print("#########################################################")
            print("################ STEP {} ################################".format(self.step_count))
            print("#########################################################")
            print("")
            grid.print_flat_grid_values()
            cell.value = current_cell_value
            print("")
            print("Agent: Focusing on Cell{} in Box{}, marked with an X\n".format(cell.coord, cell.box))
            print("Agent: Cell has {} as possible values\n".format(cell.possible_values))

            for i in cell.possible_values:
                change = [cell, i]
                if change not in self.change_log or len(cell.possible_values) <= 1:
                    if grid.check_valid(cell, i):
                        grid.update_cell(cell, i)
                        self.change_log.append(change)
                        self.update_cell_solving_order
                    else:
                        print("Cell{} failed validity check with value {}".format(cell.coord, i))
                else:
                    print("Agent: Cell{} with value {} in change log".format(cell.coord, i))

        elif not self.queue and grid.remaining_empty_cells > 2:

            for i in range(len(self.change_log) - 1, 0, -1):
                cell = self.change_log[i][0]
                for j in cell.possible_values:
                    change = [cell, j]
                    if change not in self.change_log:
                        print("")
                        print("#########################################################")
                        print("################ STEP {} ################################".format(self.step_count))
                        print("#########################################################")
                        print("")
                        print("Agent: No more cells with possible values, puzzle still unsolved")
                        print("Agent: Changing Cell{} value back to 0, and re-adding back to queue".format(cell.coord))
                        grid.undo_cell_change(cell)
                        self.update_cell_solving_order
                        self.queue.append(cell)
                        return
                    else:
                        print("Agent: Cell{} with value {} in change log".format(cell.coord, j))

        print("Queue: {}".format(self.queue))

        print("Grid remaining: {}".format(grid.remaining_empty_cells))

    def solve_the_sudoku(self, grid):
        iteration = 0
        length = len(self.queue)
        while iteration < length:
            for i in range(0,len(self.queue)):
                cell = self.queue[i]
                if len(cell.possible_values) == 1:
                    print("Set Cell{} to {}, pv: {}".format(cell.coord, cell.value, cell.possible_values))
                    cell.value = cell.possible_values[0]
                    grid.update_all_cells_possible_values()
                    iteration += 1


    def update_cell_solving_order(self, grid):

        self.order_cells_by_least_possible_values(grid)

        stuff = self.cell_order.pop(0)

        self.queue = [j for sub in self.cell_order for j in sub]  # flatten cell order

    def order_cells_by_least_possible_values(self, grid):
        for row in range(0, grid.cell_dimension):
            for column in range(0, grid.cell_dimension):
                cell = grid.flat_grid[row][column]
                minimum_count = len(cell.possible_values)
                self.cell_order[minimum_count].append(cell)
    def order_cells_by_closest_to_finish(self, grid):
        for row in range(0, grid.cell_dimension):
            for column in range(0, grid.cell_dimension):
                cell = grid.flat_grid[row][column]
                minimum_count = grid.get_minimum_remaining(cell)
                print("Cell{} has minimum count: {}".format(cell.coord, minimum_count))
                self.cell_order[minimum_count].append(cell)
