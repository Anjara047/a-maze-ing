import random
from collections import deque


class NHError(Exception):
    """
    Exception raised in case dead end is reached

    Args:
        msg: Error message describing the exception
    """
    def __init__(self, msg: str = "Invalid Neighborhood") -> None:
        super().__init__(msg)


def full_cell(width: int, height: int) -> list[list[int]]:
    """
    generate a grid full cells represents the active items and marks the limits

    Args:
        width: number of active cell per row
        height: the total of rows in the grid

    Returns:
        A list representing the initialized maze grid
    """
    output: list[list[int]] = []
    for line in range(height):
        for char in range(width):
            output.append([1, 1, 1, 1])
        output.append([-1, -1, -1, -1])
    return output


def check_neighborhood(
        loc: int, width: int, height: int) -> tuple[int, int, int, int]:
    """
    check the adjacent cardinal neighbor cells

    Args:
        width: number of active cell per row
        height: the total of rows in the grid

    Returns:
        A tupe containing their location
    """
    y = loc // (width + 1)
    x = loc - (y * (width + 1))
    loc_north, loc_east, loc_south, loc_west = (-1, -1, -1, -1)
    if x > 0:
        loc_east = (y * (width + 1)) + x - 1
    if x < (width - 1):
        loc_west = (y * (width + 1)) + x + 1
    if y > 0:
        loc_north = ((y - 1) * (width + 1)) + x
    if y < (height - 1):
        loc_south = ((y + 1) * (width + 1)) + x
    return (loc_north, loc_west, loc_south, loc_east)


def destroy_wall(output: list[list[int]],
                 current_loc: int, next_loc: int,
                 width: int, height: int) -> list[list[int]]:
    """
    carve out the wall between the two adjacents cells

    Args:
        output: Maze grid
        current_loc: index of the current cell
        next_loc: index of the next cell
        width: number of active cell per row
        height: the total of rows in the grid

    Returns:
        The the carved cell
    """
    nh = check_neighborhood(current_loc, width, height)
    if next_loc == nh[0]:
        next_pos = "north"
    elif next_loc == nh[1]:
        next_pos = "east"
    elif next_loc == nh[2]:
        next_pos = "south"
    elif next_loc == nh[3]:
        next_pos = "west"
    if next_pos == "north":
        output[current_loc][0] = 0
        output[next_loc][2] = 0
    elif next_pos == "east":
        output[current_loc][1] = 0
        output[next_loc][3] = 0
    elif next_pos == "south":
        output[current_loc][2] = 0
        output[next_loc][0] = 0
    elif next_pos == "west":
        output[current_loc][3] = 0
        output[next_loc][1] = 0
    return output


def locate_pattern(width: int, height: int) -> list[int]:
    """
    localize the position of the 42 pattern

    Args:
        width: number of active cell per row
        height: the total of rows in the grid
    Returns:
        return the coordinate of its localization
        it returns an empty list when height or width is less than 10
    """
    if width < 10 or height < 10:
        return []
    center = (width // 2, (height // 2))
    pattern: list[int] = []
    pattern.append((center[0] - 3) + ((width + 1) * (center[1] - 2)))
    for loc in range(1, 4):
        pattern.append((center[0] + loc) + ((width + 1) * (center[1] - 2)))
    pattern.append((center[0] - 3) + ((width + 1) * (center[1] - 1)))
    pattern.append((center[0] + 3) + ((width + 1) * (center[1] - 1)))
    for loc1 in range(1, 4):
        pattern.append((center[0] - loc1) + ((width + 1) * (center[1] - 0)))
        pattern.append((center[0] + loc1) + ((width + 1) * (center[1] - 0)))
    pattern.append((center[0] - 1) + ((width + 1) * (center[1] + 1)))
    pattern.append((center[0] + 1) + ((width + 1) * (center[1] + 1)))
    pattern.append((center[0] - 1) + ((width + 1) * (center[1] + 2)))
    for loc2 in range(1, 4):
        pattern.append((center[0] + loc2) + ((width + 1) * (center[1] + 2)))
    return pattern


def choose_next(current: int,
                processed: list[int],
                pattern: list[int], width: int, height: int) -> int:
    """
    choose randomly the next unvisited neighbor in the valid cells
    when an error occurs, an error is raised

    Returns:
        returns the choosen valid cells randomly

    Raises:
        NHError: If no valid neighboring cell is available.
    """
    neighborhood = check_neighborhood(current, width, height)
    valid_cells = []
    for cell in neighborhood:
        valid = True
        if cell < 0:
            valid = False
        if cell in processed:
            valid = False
        if cell in pattern:
            valid = False
        if valid:
            valid_cells += [cell]
    if not valid_cells:
        raise NHError()
    return random.choice(valid_cells)


def hunt_and_kill(output: list[list[int]], width: int, height: int,
                  entry: int, perfect: bool) -> list[list[int]]:
    """
    Visit all the cells not processed one by one
    by using a loop(The loop begin by processing the entry cell
    , and only ends when all cells have been processed):
    The process consist to:
    declare the actual cell = 'current'
    then chose a next cell randomly,
    walls between those two cells will be carved;
    If a dead-end is reached:
    Choose a new current by scannig
        from the very first cell of the maze (0,0)
        all the unprocessed cells : if at least
        one of the cell's neighbour is a processed cell,
        the actual scanned cell become the current and
        walls between a random processed neighbour and
        the current are destroyed.
    If an unperfect maze is asked, before the scan
        (the step explained above),choose a random cell
        among the current's neighbor and destroy walls between
        them...then choose a new current like in the scanning
        step.

    Args:
        output: Maze grid to modify.
        width: Width of the maze.
        height: Height of the maze.
        entry: Starting cell index.
        perfect: Whether to generate a perfect maze.
    return:
        the maze as a list of list(cell) of int(walls)
    """
    pattern: list[int] = locate_pattern(width, height)
    processed_cells: list[int] = []
    current: int = entry
    while len(processed_cells) != (len(output) - height):
        if current not in processed_cells:
            processed_cells += [current]
        try:
            while current in pattern:
                if current not in processed_cells:
                    processed_cells += [current]
                current = choose_next(current, processed_cells,
                                      pattern, width, height)
            next_cell = choose_next(current, processed_cells,
                                    pattern, width, height)
            destroy_wall(output, current, next_cell, width, height)
            previous = current
            current = next_cell
        except NHError:
            if not perfect:
                neighbours = []
                for neighbour in check_neighborhood(current, width, height):
                    if neighbour >= 0 and (neighbour != previous):
                        neighbours += [neighbour]
                next_cell = random.choice(neighbours)
                if next_cell not in pattern:
                    destroy_wall(output, current, next_cell, width, height)
            found = False
            for cell in range(len(output)):
                if output[cell] == [-1, -1, -1, -1]:
                    continue
                if cell in processed_cells or cell in pattern:
                    continue
                visited_neighbours = []
                for neighbour in check_neighborhood(cell, width, height):
                    if neighbour >= 0 and neighbour in processed_cells:
                        visited_neighbours.append(neighbour)
                if visited_neighbours:
                    neighbour = random.choice(visited_neighbours)
                    destroy_wall(output, cell, neighbour, width, height)
                    previous = current
                    current = cell
                    processed_cells.append(cell)
                    found = True
                    break
            if not found:
                break
    return output


def convert_output(output: list[list[int]]) -> str:
    """
    Convert the maze grid into its hexadecimal string representation.

    Each cell is encoded as a hexadecimal digit corresponding to the
    binary representation of its four walls (north, east, south, west).
    Separator rows are converted into newline characters.

    Args:
        output:The ouput from the result of the hunt&kill algorithm

    Returns:
         A string containing the uppercase
         hexadecimal representation of the maze.
    """
    str_output = ""
    for cell in output:
        if cell != [-1, -1, -1, -1]:
            dec = (cell[0]*1) + (cell[1]*2) + (cell[2] * 4) + (cell[3] * 8)
            str_hex = (hex(dec)[2:]).capitalize()
            str_output += str_hex
        else:
            str_output += '\n'
    return str_output


def breadth_first_search(entry_cell: int,
                         exit_cell: int, maze: list[list[int]],
                         width: int, height: int) -> list[int]:
    """
    Find the shortest path by traversing the opening maze grid
    to track back the links and reconstruct the optimal path
    from the entry to the exit position
    Args:
        entry_cell: Index of the maze entry cell.
        exit_cell: Index of the maze exit cell.
        maze: Maze grid containing wall information.
        width: Width of the maze.
        height: Height of the maze.
    Returns:
        returns the shortest path found
    """
    queue = deque([entry_cell])
    precedent: int = entry_cell
    visited: dict[int, int] = {entry_cell: precedent}
    while queue:
        precedent = queue.popleft()
        if precedent == exit_cell:
            break
        index = 0
        neighbours_indexes = []
        for wall in maze[precedent]:
            if wall == 0:
                neighbours_indexes += [index]
            index += 1
        neighbours_locs = check_neighborhood(precedent, width, height)
        valid_neighbours: list[int] = []
        for index in neighbours_indexes:
            if ((neighbours_locs[index] not in visited)
                    and (neighbours_locs[index] != precedent)):
                valid_neighbours += [neighbours_locs[index]]
                visited[neighbours_locs[index]] = precedent
                queue.append(neighbours_locs[index])
    reversed_path: list[int] = []
    while precedent != entry_cell:
        precedent = visited[precedent]
        reversed_path.append(precedent)
    return list(reversed(reversed_path))


def convert_path(path: list[int], entry_cell: int,
                 exit_cell: int, width: int) -> str:
    """
    Convert the path into directional instructions.
    Args:
        path: List of cell indices representing the solution path.
        entry_cell: Index of the maze entry cell.
        exit_cell: Index of the maze exit cell.
        width: Width of the maze.
    Returns:
        The list of all the directional instructions to follow to
        reach the exit cell
    """
    solution = ""
    path += [exit_cell]
    actual_cell = entry_cell
    for next_cell in path:
        if next_cell == (actual_cell - 1):
            solution += "W"
        elif next_cell == (actual_cell + 1):
            solution += "E"
        elif next_cell == (actual_cell - (width + 1)):
            solution += "N"
        elif next_cell == (actual_cell + (width + 1)):
            solution += "S"
        actual_cell = next_cell
    return solution


class MazeGenerator:
    """
    A class which generate and solve mazes.
    Toinstantiate it:
    Create a variable to put the object of the class,
    then all the class' methods can be applied on the object
    (variable)

    Example:
    >>>>>>> maze = MazeGenerator(42,True,[0,0],[1,1],7,9)
            maze.generate()

    The generator can create either perfect or imperfect mazes and
    compute the shortest path between the entry and exit cells.
    """

    def __init__(self, seed: int, perfect: bool,
                 coord_entry: list[int], coord_exit: list[int],
                 width: int, height: int) -> None:
        self.seed = seed
        self.perfect = perfect
        self.maze: list[list[int]] = []
        self.path: list[int] = []
        self.entry = (coord_entry[0]) + ((coord_entry[1]) * (width + 1))
        self.exit = (coord_exit[0]) + ((coord_exit[1]) * (width + 1))
        self.width = width
        self.height = height

    def generate(self) -> None:
        """
        Generate the maze by calling the strategies
        which has been created above:
        Initializing all walls before using
        the hunt & kill algorithm
        """
        if self.seed != -69:
            random.seed(self.seed)
        output = full_cell(self.width, self.height)
        output = hunt_and_kill(
            output,
            self.width,
            self.height,
            self.entry,
            self.perfect)
        self.maze = output

    def get_maze(self) -> str:
        """
        Get the generated maze

        Returns:
            The hexadecimal string representation of the maze.
        """
        if self.maze == []:
            self.generate()
        return convert_output(self.maze)

    def solve(self) -> None:
        """
            Compute the shortest solution
        """
        if self.maze == []:
            self.generate()
        maze = self.maze
        self.path = breadth_first_search(
            self.entry, self.exit, maze, self.width, self.height)

    def get_solution(self) -> str:
        """
            get the maze's solution(the path)

            Returns:
                A string containing the sequence of movements from the entry
            to the exit.
        """
        if not self.path:
            self.solve()
        return convert_path(self.path, self.entry, self.exit, self.width)
