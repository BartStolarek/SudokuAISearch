from math import sqrt


class Cell:

    def __init__(self):
        self.value = 0
        self.box = [-1, -1]
        self.coord = [-1, -1]


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


class Row:
    def __init__(self, dimension):
        self.dimension = dimension
        self.cells = []
        self.coord = -1
        self.complete = False
        self.remaining_cells = 9


class Column:
    def __init__(self, dimension):
        self.dimension = dimension
        self.cells = []
        self.coord = -1
        self.complete = False
        self.remaining_cells = 9


class Grid:
    def __init__(self, box_count, input_grid):

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
                        cell.box = [x_box, y_box]
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

        grid_global_x = 0
        grid_global_y = 0
        for row in range(0, self.cell_dimension):
            for column in range(0, self.cell_dimension):
                self.flat_grid[row][column].coord = [grid_global_x, grid_global_y]
                grid_global_y += 1
            grid_global_y = 0
            grid_global_x += 1

    def return_missing_value(self, present_values):
        for i in range(1, 10):
            if i not in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                return i
        raise ValueError("return_missing_value: no missing value was found")

    def check_for_final_cell(self):
        found_something = False
        for i in range(0, self.cell_dimension):

            # Check all rows
            missing_row_cells = self.check_row_incomplete(i)
            if missing_row_cells:
                if len(missing_row_cells[0]) == 1:
                    missing_row_cells[0].value = self.return_missing_value(missing_row_cells[1])
                    found_string = "Found {} for row {}".format(missing_row_cells[0].value, i)
                    print(found_string)
                    found_something = True
                else:
                    nothing_found_string = "Nothing found for row {}".format(i)
                    print(nothing_found_string)

            # Check all columns
            missing_column_cells = self.check_column_incomplete(i)
            if missing_column_cells:
                if len(missing_column_cells[0]) == 1:
                    missing_column_cells[0].value = self.return_missing_value(missing_column_cells[1])
                    found_string = "Found {} for column {}".format(missing_column_cells[0].value, i)
                    print(found_string)
                    found_something = True
                else:
                    nothing_found_string = "Nothing found for column {}".format(i)
                    print(nothing_found_string)


        for row in range(0, self.grid_dimension):
            for column in range(0, self.grid_dimension):
                missing_box_cells = self.check_box_incomplete(row, column)
                if missing_box_cells:
                    if len(missing_box_cells[0]) == 1:
                        missing_box_cells[0].value = self.return_missing_value(missing_box_cells[1])
                        found_string = "Found {} for box {}".format(missing_box_cells[0].value, self.boxes[row][column].coord)
                        print(found_string)
                        found_something = True
                    else:
                        nothing_found_string = "Nothing found for box {}".format(self.boxes[row][column].coord)
                        print(nothing_found_string)
        return found_something

    def check_row_incomplete(self, x):
        if not self.rows[x]:
            cells = []
            present_values = []
            incomplete_cells = []
            for column in range(0, self.cell_dimension):
                if self.flat_grid[x][column].value == 0:
                    incomplete_cells.append(self.flat_grid[x][column])
                else:
                    present_values.append(self.flat_grid[x][column].value)
            if not incomplete_cells:
                self.rows[x] = True
                return 0
            else:
                cells.append(incomplete_cells)
                cells.append(present_values)
                return cells
        else:
            return 0

    def check_column_incomplete(self, y):
        if not self.columns[y]:
            cells = []
            present_values = []
            incomplete_cells = []
            for row in range(0, self.cell_dimension):
                if self.flat_grid[row][y].value == 0:
                    incomplete_cells.append(self.flat_grid[row][y])
                else:
                    present_values.append(self.flat_grid[row][y].value)
            if not incomplete_cells:
                self.columns[y] = True
                return 0
            else:
                cells.append(incomplete_cells)
                cells.append(present_values)
                return cells
        else:
            return 0

    def check_box_incomplete(self, x, y):
        if not self.boxes[x][y].complete:
            cells = []
            present_values = []
            incomplete_cells = []
            for row in range(0, self.box_dimension):
                for column in range(0, self.box_dimension):
                    if self.boxes[x][y].cells[row][column].value == 0:
                        incomplete_cells.append(self.boxes[x][y].cells[row][column])
                    else:
                        present_values.append(self.boxes[x][y].cells[row][column].value)
            if not incomplete_cells:
                self.boxes[x][y].complete = True
                return 0
            else:
                cells.append(incomplete_cells)
                cells.append(present_values)
                return cells
        else:
            return 0

    def get_cell_with_coords(self, x, y):
        for row in range(0, self.cell_dimension):
            for column in range(0, self.cell_dimension):
                if self.flat_grid[row][column].coord == [x, y]:
                    return self.flat_grid[row][column]

    def print_flat_grid_values(self):
        for row in range(0, self.cell_dimension):
            row_string = " "
            for column in range(0, self.cell_dimension):
                row_string = row_string + str(self.flat_grid[row][column].value) + " "

            print(row_string)

    def print_flat_grid_coords(self):
        for row in range(0, self.cell_dimension):
            row_string = " "
            for column in range(0, self.cell_dimension):
                row_string = row_string + str(self.flat_grid[row][column].coord) + " "
            print(row_string)
