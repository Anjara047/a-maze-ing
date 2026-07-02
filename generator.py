#! python3
import random
from parser_config import configs


class NHError(Exception):
    def __init__(self, msg: str = "Invalid Neighborhood") -> None:
        super().__init__(msg)


on = {
    'all': {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14},
    'north': {8, 9, 10, 11, 12, 13, 14},
    'east': {4, 5, 6, 7, 12, 13, 14},
    'south': {2, 3, 6, 7, 10, 11, 14},
    'west': {1, 3, 5, 7, 9, 11, 13}
}

side_on = ("north", "east", "south", "west")

coord_x = configs['WIDTH']
coord_y = configs['HEIGHT']


def full_cell() -> list[list[int]]:
    output: list[list[int]] = []
    for line in range(coord_y):
        for char in range(coord_x):
            output.append([1, 1, 1, 1])
        output.append([-1, -1, -1, -1])
    return output


def check_neighborhood(
        loc: int, output: list[list[int]]) -> tuple[int, int, int, int]:
    # crees qlq chose qui convertit loc en (x,y)
    y = loc // (coord_x + 1)
    x = loc - (y * (coord_x + 1))
    loc_north, loc_east, loc_south, loc_west = (-1, -1, -1, -1)
    # E
    if x > 0:
        loc_east = (y * (coord_x + 1)) + x - 1
    # W
    if x < (coord_x - 1):
        loc_west = (y * (coord_x + 1)) + x + 1
    # N
    if y > 0:
        loc_north = ((y - 1) * (coord_x + 1)) + x
    # S
    if y < (coord_y - 1):
        loc_south = ((y + 1) * (coord_x + 1)) + x
    return (loc_north, loc_east, loc_south, loc_west)


def destroy_wall(output: list[list[int]],
                 current_loc: int, next_loc: int) -> list[list[int]]:
    # current_cell = output[current_loc]
    # next_cell = output[next_loc]
    nh = check_neighborhood(current_loc, output)
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


def draw_pattern():
    pass

def choose_next(output: list[list[int]], current: int,
                processed: list[int]) -> int:
    neighborhood = check_neighborhood(current, output)
    valid_cells = []
    for cell in neighborhood:
        valid = True
        if cell < 0:
            valid = False
        if cell in processed:
            valid = False
        if valid:
            valid_cells += [cell]
    if not valid_cells:
        raise NHError()
    return random.choice(valid_cells)


def hunt_and_kill(output: list[list[int]]) -> list[list[int]]:
    processed_cells = []
    entry: list[str] = configs['ENTRY'].split(",")
    current: int = int(entry[0]) + (int(entry[1]) * (coord_x + 1))
    while len(processed_cells) != (len(output) - coord_y):
        if current not in processed_cells:
            processed_cells += [current]
        try:
            next_cell = choose_next(output, current, processed_cells)
            destroy_wall(output, current, next_cell)
            current = next_cell
        except NHError:
            found = False
            for cell in range(len(output)):
                if output[cell] == [-1, -1, -1, -1]:
                    continue
                if cell in processed_cells:
                    continue
                visited_neighbours = []
                for neighbour in check_neighborhood(cell, output):
                    if neighbour >= 0 and neighbour in processed_cells:
                        visited_neighbours.append(neighbour)
                if visited_neighbours:
                    neighbour = random.choice(visited_neighbours)
                    destroy_wall(output, cell, neighbour)
                    current = cell
                    processed_cells.append(cell)
                    found = True
                    break
            if not found:
                break
    return output


def convert_output(output: list[list[int]]) -> str:
    str_output = ""
    for cell in output:
        if cell != [-1, -1, -1, -1]:
            binary = str(cell[0]) + str(cell[1]) + str(cell[2]) + str(cell[3])
            str_output += (hex(int(binary, 2))[2:]).capitalize()
        else:
            str_output += '\n'
    return str_output


def main():
    output = full_cell()
    output = hunt_and_kill(output)
    with open(configs["OUTPUT_FILE"], 'w') as f:
        f.write(convert_output(output))

if __name__ == "__main__":
    main()
