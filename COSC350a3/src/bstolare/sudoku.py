from math import sqrt

"""
Global Function 
get_unicode_symbol

A function to return the symbol shape when a corresponding code is provided. 
For each compass direction, use the first letter of the direction, start from
North, and go clockwise to west for the required walls. 

parameters: unicode - text/string of up to 4 characters corresponding to north, east, south, west first characters.
returns: unicode symbol corresponding to the unicode
"""
def get_unicode_symbol(unicode):
    unicode_symbols = {'nesw': '┼',
                       'ew': '─',
                       'ns': '│',
                       }
    return unicode_symbols[unicode]

"""
Class
Cell

A class object which is to represent each cell in the grid/sudoku puzzle. The cell
will know its global coordinates, the box it is in coordinates, and possible legal
values based on sudoku rules. If the value is 0, then the cell is considered empty. 

parameters: 
returns:
"""
class Cell:

    def __init__(self):
        self.value = 0
        self.box = [-1, -1]
        self.coord = [-1, -1]
        self.possible_values = []

"""
Class
Box

A class object which is to represent a each box in a grid. A box is to be made up of 3 x 3 cells, which 
are held in a 2D array called cells. 
The dimensions are the square root of the total cell count in the box. The coords are the boxes coordinates in the grid, and not
to be confused with cell global coordinates. The box also has a complete boolean and a remaining cells
to solve count. 

parameters: cell_count is provided to the box, to ensure the box knows how many cells to include.
returns: 
"""
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

"""
Class
Grid

A class object which is to represent the grid. The grid will contain a box count of 9, in a 2D array, formed as 
3 x 3. The grid will also indicate how to represent the empty value in console, as well as control and manage
the flat grid, global coordinates, box coordinates and values. 

parameters: 
    input grid - a array of boxes, which the user as input
    verbose - indicate whether debugging and printing more to console is necessary
    empty_value - user defined representation of the empty value 
returns: 
"""
class Grid:
    def __init__(self, input_grid, verbose, empty_value):
        # Assigning variables
        self.empty_value = str(empty_value)
        self.verbose = verbose
        self.box_count = 9
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
        self.remaining_boxes = len(input_grid)

        input_grid_multidimension = False

        if len(input_grid[0]) != 1:
            input_grid_multidimension = True


        # Create Grid and populate
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
                        if input_grid_multidimension:
                            cell.value = input_grid[x_grid][y_grid][x_box][y_box]  # get value from input grid
                        else:
                            cell.value = 0
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

        # Create flat grid without boxes
        for x_grid in range(0, self.grid_dimension):
            for x_box in range(0, self.box_dimension):
                grid_row = []
                for y_grid in range(0, self.grid_dimension):
                    for y_box in range(0, self.box_dimension):
                        cell = self.boxes[x_grid][y_grid].cells[x_box][y_box]
                        grid_row.append(cell)
                self.flat_grid.append(grid_row)

        # Create row and column checkers
        for row in range(0, self.cell_rowscolumns):
            self.rows.append(False)
            self.columns.append(False)
            self.cell_dimension += 1



        # Update cell's global coordinates
        grid_global_x = 0
        grid_global_y = 0
        counter_iteration = 0
        for row in range(0, self.cell_dimension):
            for column in range(0, self.cell_dimension):
                cell = self.flat_grid[row][column]
                cell.coord = [grid_global_x, grid_global_y]
                if not input_grid_multidimension:
                    cell.value = int(input_grid[counter_iteration])  # get value from input gri
                    if cell.value != 0:  # Adjust box's remaining cells to find if cell already has a value
                        box.remaining_cells -= 1

                    counter_iteration += 1

                grid_global_y += 1
            grid_global_y = 0
            grid_global_x += 1
        self.update_all_cells_possible_values()
        self.remaining_empty_cells = self.get_remaining_empty_cell_count()


    """
    Class Function
    get_remaining_empty_cell_count
    
    A class function which will  go through the flat grid, and check each cell for whether its empty or has
    a value. Then update the grids remaining empty cell count as well as returning it. 
    
    parameters: 
    returns: count - the number of empty cells remaining in the grid
    """
    def get_remaining_empty_cell_count(self):
        count = 0
        for row in range(0, self.cell_dimension):
            for column in range(0, self.cell_dimension):
                cell = self.flat_grid[row][column]
                if cell.value == 0:
                    count += 1
        self.remaining_empty_cells = count
        return count

    """
    Class Function
    update_cell_possible_values
    
    A class function which will update the cells possible values, as well as update
    the rows and column finished checks, and box finish checks if necessary, and update the possible
    values for the effected cells. 
    
    parameters: cell - the cell object that is to be updated
    returns: 
    """
    def update_cell_possible_values(self, cell):
        if self.verbose > 0:
            print("Grid: Cell{} is having its possible values updated".format(cell.coord))
        if cell.value:
            cell.possible_values = []
        else:
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

    """
    Class Function
    update_all_cells_possible_values
    
    A class function which will  go through the flat grid,and call update cell value function on each cell.
    
    parameters:
    returns: 
    """
    def update_all_cells_possible_values(self):
        for row in range(0, self.cell_dimension):
            for column in range(0, self.cell_dimension):
                self.update_cell_possible_values(self.flat_grid[row][column])
        self.get_remaining_empty_cell_count()

    """
    Class Function
    check_if_box_complete
    
    A class function which will  go through each cell in a box and check whether there is a value, if so
    it will update the boxes complete attribute
    
    parameters:
        x - the x coordinate of the box in the grid
        y - the y coordinate of the box in the grid
    returns: 
    """
    def check_if_box_complete(self, x, y):
        complete_cell_count = 0
        for row in range(0, self.box_dimension):
            for column in range(0, self.box_dimension):
                if self.boxes[x][y].cells[row][column].value > 0:
                    complete_cell_count += 1
        self.boxes[x][y].remaining_cells = 9 - complete_cell_count

        if complete_cell_count == 9:
            self.boxes[x][y].complete = True

    """
    Class Function
    check_valid
    
    Class function which checks whether provided cell, and its value is a valid sudoku move
    
    parameters:
        cell - the cell object to be checked
        value - the value that is being checked
    returns: validity - as 1 or 0, 1 if it is a valid move, 0 if it is not a valid move
    """
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

    """
    Class Function
    update_cell
    
    Class function, which takes the cell and updates the value, as well as updating some grid attributes to help
    track the current solved status of the puzzle
    
    parameters:
        cell - the cell object to be checked
        value - the value that is being input
    returns: 
    """
    def update_cell(self, cell, value):
        if self.verbose > 0:
            print("Grid: Updating Cell{} value to {}".format(cell.coord, value))

        cell.value = value
        self.boxes[cell.box[0]][cell.box[1]].remaining_cells -= 1
        self.update_all_cells_possible_values()
        self.get_remaining_empty_cell_count()
        self.check_if_box_complete(cell.box[0], cell.box[1])

    """
    Class Function
    print_flat_grid_values
    
    Class function, which goes through each cell in flat grid, and builds a visual walled sudoku puzzle,
    and prints it out to console
    
    parameters:
    returns: 
    """
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
                if self.flat_grid[row][column].value == 0:
                    row_string = row_string + self.empty_value + " "
                else:
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

    """
    Class Function
    print_flat_grid_coords
    
    Class function, which goes through each cell in flat grid, and prints that cell's coords out in a 2D array
    
    parameters:
    returns: 
    """
    def print_flat_grid_coords(self):
        for row in range(0, self.cell_dimension):
            row_string = " "
            for column in range(0, self.cell_dimension):
                row_string = row_string + str(self.flat_grid[row][column].coord) + " "
            print(row_string)

    """
    Class Function
    print_flat_grid_box
    
    Class function, which goes through each cell in flat grid, and prints that cell's box's coordinates in a
    2D array
    
    parameters:
    returns: 
    """
    def print_flat_grid_box(self):
        for row in range(0, self.cell_dimension):
            row_string = " "
            for column in range(0, self.cell_dimension):
                row_string = row_string + str(self.flat_grid[row][column].box) + " "
            print(row_string)

    """
    Class Function
    print_flat_grid_possible_values
    
    Class function, which goes through each cell in flat grid, and prints that cell's possible values in a
    2D array
    
    parameters:
    returns: 
    """
    def print_flat_grid_possible_values(self):
        for row in range(0, self.cell_dimension):
            row_string = " "
            for column in range(0, self.cell_dimension):
                row_string = row_string + str(self.flat_grid[row][column].possible_values) + " "
            print(row_string)

    """
    Class Function
    print_flat_grid_with_focus_cell
    
    Class function, which goes through each cell in flat grid, and builds a visual walled sudoku puzzle,
    and prints it out to console. With the cell in focus marked with a 'X'
    
    parameters:
    returns: 
    """
    def print_flat_grid_with_focus_cell(self, cell):
        cell.value = "X"

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
                if self.flat_grid[row][column].value == 0:
                    row_string = row_string + self.empty_value + " "
                else:
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
        cell.value = 0
        print("")
        print("X marks the current cell in focus\n".format(self.empty_value))
