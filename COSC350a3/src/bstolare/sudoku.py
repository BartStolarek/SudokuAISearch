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

        self.get_remaining_empty_cell_count()

        grid_global_x = 0
        grid_global_y = 0
        for row in range(0, self.cell_dimension):
            for column in range(0, self.cell_dimension):
                self.flat_grid[row][column].coord = [grid_global_x, grid_global_y]
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


    def update_all_cells_possible_values(self):
        if self.verbose > 0:
            print("Updating all cell's possible values (change verbose to 2+ and re-run to see these updates)")
        for cell_row in range(0, self.cell_dimension):
            for cell_column in range(0, self.cell_dimension):

                cell = self.flat_grid[cell_row][cell_column]

                cell_column_missing_values = self.get_cells_column_missing_values(cell)

                cell_row_missing_values = self.get_cells_column_missing_values(cell)

                cell_box_missing_values = self.get_cells_box_missing_values(cell)

                cells_missing_values = []
                for i in range(1,10):
                    if i in cell_column_missing_values and i in cell_row_missing_values and i in cell_box_missing_values:
                        cells_missing_values.append(i)

                if self.verbose > 1:
                    print("Cell[{}, {}] missing_values: {}".format(cell_row,cell_column,cells_missing_values))

                cell.possible_values = cells_missing_values
        self.get_remaining_empty_cell_count()

    def get_cells_column_missing_values(self,cell):
        present_values = []
        missing_values = []
        if not self.columns[cell.coord[1]]:
            for cell_row in range(0, self.cell_dimension):
                present_values.append(self.flat_grid[cell_row][cell.coord[1]].value)
            for i in range(1, 10):
                if i not in present_values:
                    missing_values.append(i)
            if not missing_values:
                self.columns[cell.coord[1]] = True
        return missing_values

    def get_cells_row_missing_values(self,cell):
        if not self.rows[cell.coord[0]]:
            present_values = []
            missing_values = []
            for cell_column in range(0, self.cell_dimension):
                present_values.append(self.flat_grid[cell.coord[0]][cell_column].value)

            missing_values = []
            for i in range(1, 10):
                if i not in present_values:
                    missing_values.append(i)
            if not missing_values:
                self.rows[cell.coord[0]] = True
        return missing_values

    def get_cells_box_missing_values(self,cell):
        present_values = []
        missing_values = []
        if not self.boxes[cell.box[0]][cell.box[1]].complete:
            for box_row in range(0,self.box_dimension):
                for box_column in range(0, self.box_dimension):
                    present_values.append(self.boxes[cell.box[0]][cell.box[1]].cells[box_row][box_column].value)
            for i in range(1, 10):
                if i not in present_values:
                    missing_values.append(i)
            if not missing_values:
                self.boxes[cell.box[0]][cell.box[1]].complete = True
                self.remaining_boxes -= 1
        return missing_values

    def check_if_box_complete(self,x, y):
        complete_cell_count = 0
        for row in range(0, self.box_dimension):
            for column in range(0, self.box_dimension):
                if self.boxes[x][y].cells[row][column].value > 0:
                    complete_cell_count += 1
        self.boxes[x][y].remaining_cells = 9 - complete_cell_count

        if complete_cell_count == 9:
            self.boxes[x][y].complete = True

    def update_cell(self, cell, value):
        if self.verbose > 0:
            print("Updating Cell{} value to {}".format(cell.coord, value))
        cell.value = value
        self.boxes[cell.box[0]][cell.box[1]] -= 1
        self.update_all_cells_possible_values()
        self.get_remaining_empty_cell_count()
        self.check_if_box_complete(cell.box[0],cell.box[1])
        left_column = self.get_cells_column_missing_values(cell)
        left_row = self.get_cells_row_missing_values(cell)

    def undo_cell_change(self, cell, possible_values):
        if self.verbose > 0:
            print("Undo'ing Cell{} value back to 0".format(cell.coord))
        cell.value = 0
        cell.possible_values = possible_values
        self.boxes[cell.box[0]][cell.box[1]] += 1
        self.update_all_cells_possible_values()
        self.get_remaining_empty_cell_count()
        self.check_if_box_complete(cell.box[0],cell.box[1])
        left_column = self.get_cells_column_missing_values(cell)
        left_row = self.get_cells_row_missing_values(cell)



    def get_cell_with_coords(self, x, y):
        return self.flat_grid[x][y]

    def print_flat_grid_values(self):
        for row in range(0, self.cell_dimension):
            if row % 3 == 0:
                buffer_string = " "
                for sub_column in range(0, self.cell_dimension):
                    if sub_column % 3 == 0:
                        buffer_string = buffer_string + get_unicode_symbol("nesw") + get_unicode_symbol("ew") + get_unicode_symbol("ew") + get_unicode_symbol("ew")
                    else:
                        buffer_string = buffer_string + get_unicode_symbol("ew") + get_unicode_symbol("ew")
                    if sub_column == self.cell_dimension-1:
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
                buffer_string = buffer_string + get_unicode_symbol("nesw") + get_unicode_symbol("ew") + get_unicode_symbol("ew") + get_unicode_symbol("ew")
            else:
                buffer_string = buffer_string + get_unicode_symbol("ew") + get_unicode_symbol("ew")
            if sub_column == self.cell_dimension-1:
                buffer_string = buffer_string + get_unicode_symbol("nesw")
        print(buffer_string)


    def print_flat_grid_coords(self):
        for row in range(0, self.cell_dimension):
            row_string = " "
            for column in range(0, self.cell_dimension):
                row_string = row_string + str(self.flat_grid[row][column].coord) + " "
            print(row_string)
