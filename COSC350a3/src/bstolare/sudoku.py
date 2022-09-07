from math import sqrt


def get_unicode_symbol(unicode):
    unicode_symbols = {'nesw': '┼',
                       'ew': '─',
                       'ns': '│',
                       }

    return unicode_symbols[unicode]


class Cell:

    def __init__(self):
        self.value = 0
        self.box = [-1, -1]
        self.coord = [-1, -1]
        self.possible_values = []


class Box:

    def __init__(self, cell_count):

        self.cell_count = cell_count
        self.dimension = sqrt(cell_count)
        if self.cell_count % self.dimension != 0:
            raise ValueError("Cell count is not a square of a positive integer")
        else:
            self.dimension = int(self.dimension)
        self.cells = []
        self.coord = [-1, -1]
        self.complete = False
        self.remaining_cells = 9


class Grid:
    def __init__(self, box_count, input_grid, verbose):
        self.verbose = verbose
        self.box_count = box_count
        self.grid_dimension = sqrt(self.box_count)
        if self.box_count % self.grid_dimension != 0:
            raise ValueError("Box count is not a square of a positive integer")
        else:
            self.grid_dimension = int(self.grid_dimension)
        self.boxes = []
        self.flat_grid = []
        self.rows = []
        self.columns = []
        self.cell_dimension = 0
        self.remaining_empty_cells = 0
        self.remaining_boxes = box_count

        # Create Grid
        for x_grid in range(0, self.grid_dimension):
            grid_row = []
            for y_grid in range(0, self.grid_dimension):
                box = Box(9)
                # Create a box
                for x_box in range(0, 3):
                    # Create a row in the box
                    cell_row = []
                    for y_box in range(0, 3):

                        # Create cell in box's row
                        cell = Cell()
                        cell.value = input_grid[x_grid][y_grid][x_box][y_box]  # get value from input grid
                        if cell.value != 0:  # Adjust box's remaining cells to find if cell already has a value
                            box.remaining_cells -= 1
                        cell.box = [x_grid, y_grid]

                        cell_row.append(cell)  # add cell to box's row

                    # Add row of cells to box
                    box.cells.append(cell_row)

                # Update box coord
                box.coord = [x_grid, y_grid]

                # Add box to row of boxes
                grid_row.append(box)

            # Add box row to grid
            self.boxes.append(grid_row)
        # Grid creation done.

        # Store common box dimension for grid, and number of global rows/columns (square)
        self.box_dimension = self.boxes[0][0].dimension
        self.cell_rowscolumns = self.grid_dimension * self.box_dimension

        # Create
        for x_grid in range(0, self.grid_dimension):
            for x_box in range(0, self.box_dimension):
                grid_row = []
                for y_grid in range(0, self.grid_dimension):
                    for y_box in range(0, self.box_dimension):
                        cell = self.boxes[x_grid][y_grid].cells[x_box][y_box]
                        grid_row.append(cell)
                self.flat_grid.append(grid_row)

        for row in range(0, self.cell_rowscolumns):
            self.rows.append(False)
            self.columns.append(False)
            self.cell_dimension += 1

        self.get_remaining_empty_cell_count()

        grid_global_x = 0
        grid_global_y = 0
        for row in range(0, self.cell_dimension):
            for column in range(0, self.cell_dimension):
                cell = self.flat_grid[row][column]
                cell.coord = [grid_global_x, grid_global_y]

                grid_global_y += 1
            grid_global_y = 0
            grid_global_x += 1

    def get_remaining_empty_cell_count(self):
        count = 0
        for row in range(0, self.cell_dimension):
            for column in range(0, self.cell_dimension):
                cell = self.flat_grid[row][column]
                if cell.value == 0:
                    count += 1
        self.remaining_empty_cells = count
        return count

    def update_cell_possible_values(self, cell):
        if self.verbose > 1:
            print("Cell{} is having its possible values updated".format(cell.coord))

        cells_row = cell.coord[0]
        cells_column = cell.coord[1]
        box = self.boxes[cell.box[0]][cell.box[1]]

        present_values = []
        if not self.rows[cells_row]:
            value_check = 45
            for column in range(0, self.cell_dimension):
                value_check -= self.flat_grid[cells_row][column].value
                present_values.append(self.flat_grid[cells_row][column].value)
            if not value_check:
                self.rows[cells_row] = True


        if not self.columns[cells_column]:
            value_check = 45
            for row in range(0, self.cell_dimension):
                value_check -= self.flat_grid[row][cells_column].value
                present_values.append(self.flat_grid[row][cells_column].value)
            if not value_check:
                self.columns[cells_column] = True

        if not box.complete:
            value_check = 45
            for row in range(0, self.box_dimension):
                for column in range(0, self.box_dimension):

                    value_check -= box.cells[row][column].value
                    present_values.append(box.cells[row][column].value)


            if not value_check:
                box.complete = True

        present_values = list(set(present_values))

        missing_values = []
        for i in range(1, 10):
            if i not in present_values:
                missing_values.append(i)
        cell.possible_values = missing_values


    def get_minimum_remaining(self, cell):
        if self.verbose > 1:
            print("Cell{} is having its possible values updated".format(cell.coord))

        cells_row = cell.coord[0]
        cells_column = cell.coord[1]
        box = self.boxes[cell.box[0]][cell.box[1]]
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        row_present = []
        if not self.rows[cells_row]:
            for column in range(0, self.cell_dimension):
                cell = self.flat_grid[cells_row][cells_column]
                if cell.value not in numbers:
                    row_present.append(cell.value)

        column_present = []
        if not self.columns[cells_column]:
            for row in range(0, self.cell_dimension):
                cell = self.flat_grid[row][cells_column]
                if cell.value not in numbers:
                    column_present.append(cell.value)

        box_present = []
        if not box.complete:
            for row in range(0, self.box_dimension):
                for column in range(0, self.box_dimension):
                    cell = box.cells[row][column]
                    if cell.value not in numbers:
                        box_present.append(cell.value)

        return min(len(row_present), len(column_present), len(box_present))

    def update_all_cells_possible_values(self):
        for row in range(0, self.cell_dimension):
            for column in range(0, self.cell_dimension):


                self.update_cell_possible_values(self.flat_grid[row][column])
        self.get_remaining_empty_cell_count()

    def check_if_box_complete(self, x, y):
        complete_cell_count = 0
        for row in range(0, self.box_dimension):
            for column in range(0, self.box_dimension):
                if self.boxes[x][y].cells[row][column].value > 0:
                    complete_cell_count += 1
        self.boxes[x][y].remaining_cells = 9 - complete_cell_count

        if complete_cell_count == 9:
            self.boxes[x][y].complete = True

    def check_valid(self, cell, value):
        cells_row = cell.coord[0]
        cells_column = cell.coord[1]
        box = self.boxes[cell.box[0]][cell.box[1]]
        present_values = []
        if not self.rows[cells_row]:
            value_check = 45
            for column in range(0, self.cell_dimension):
                value_check -= self.flat_grid[cells_row][column].value
                present_values.append(self.flat_grid[cells_row][column].value)
            if not value_check:
                self.rows[cells_row] = True
        if not self.columns[cells_column]:
            value_check = 45
            for row in range(0, self.cell_dimension):
                value_check -= self.flat_grid[row][cells_column].value
                present_values.append(self.flat_grid[row][cells_column].value)
            if not value_check:
                self.columns[cells_column] = True
        if not box.complete:
            value_check = 45
            for row in range(0, self.box_dimension):
                for column in range(0, self.box_dimension):
                    value_check -= box.cells[row][column].value
                    present_values.append(box.cells[row][column].value)
            if not value_check:
                box.complete = True

        present_values = list(set(present_values))

        if value in present_values:
            return 0
        return 1

    def update_cell(self, cell, value):
        if self.verbose > 1:
            print("Updating Cell{} value to {}".format(cell.coord, value))


        cell.value = value
        self.boxes[cell.box[0]][cell.box[1]].remaining_cells -= 1
        self.update_all_cells_possible_values()
        self.get_remaining_empty_cell_count()
        self.check_if_box_complete(cell.box[0], cell.box[1])


    def undo_cell_change(self, cell):
        if self.verbose > 1:
            print("Undo'ing Cell{} value back to 0".format(cell.coord))
        cell.value = 0
        self.boxes[cell.box[0]][cell.box[1]].remaining_cells += 1
        self.boxes[cell.box[0]][cell.box[1]].complete = False
        self.rows[cell.coord[0]] = False
        self.columns[cell.coord[0]] = False
        self.update_all_cells_possible_values()
        self.get_remaining_empty_cell_count()
        self.check_if_box_complete(cell.box[0], cell.box[1])


    def get_cell_with_coords(self, x, y):
        return self.flat_grid[x][y]

    def print_flat_grid_values(self):
        for row in range(0, self.cell_dimension):
            if row % 3 == 0:
                buffer_string = " "
                for sub_column in range(0, self.cell_dimension):
                    if sub_column % 3 == 0:
                        buffer_string = buffer_string + get_unicode_symbol("nesw") + get_unicode_symbol(
                            "ew") + get_unicode_symbol("ew") + get_unicode_symbol("ew")
                    else:
                        buffer_string = buffer_string + get_unicode_symbol("ew") + get_unicode_symbol("ew")
                    if sub_column == self.cell_dimension - 1:
                        buffer_string = buffer_string + get_unicode_symbol("nesw")
                print(buffer_string)
            row_string = " "
            for column in range(0, self.cell_dimension):
                if column % 3 == 0:
                    row_string = row_string + get_unicode_symbol("ns") + " "
                row_string = row_string + str(self.flat_grid[row][column].value) + " "
            row_string = row_string + get_unicode_symbol("ns")
            print(row_string)
        buffer_string = " "
        for sub_column in range(0, self.cell_dimension):
            if sub_column % 3 == 0:
                buffer_string = buffer_string + get_unicode_symbol("nesw") + get_unicode_symbol(
                    "ew") + get_unicode_symbol("ew") + get_unicode_symbol("ew")
            else:
                buffer_string = buffer_string + get_unicode_symbol("ew") + get_unicode_symbol("ew")
            if sub_column == self.cell_dimension - 1:
                buffer_string = buffer_string + get_unicode_symbol("nesw")
        print(buffer_string)

    def print_flat_grid_coords(self):
        for row in range(0, self.cell_dimension):
            row_string = " "
            for column in range(0, self.cell_dimension):
                row_string = row_string + str(self.flat_grid[row][column].coord) + " "
            print(row_string)

    def print_flat_grid_box(self):
        for row in range(0, self.cell_dimension):
            row_string = " "
            for column in range(0, self.cell_dimension):
                row_string = row_string + str(self.flat_grid[row][column].box) + " "
            print(row_string)
