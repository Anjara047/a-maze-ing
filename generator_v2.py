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


def full_cell() -> str:
    output = ''
    for line in range(coord_y):
        for char in range(coord_x):
            output += 'F'
        output += '\n'
    return output


def check_neighborhood(loc: int, output: str) -> tuple[int, int, int, int]:
    # crees qlq chose qui convertit loc en (x,y)
    y = loc // (coord_x + 1)
    x = loc - (y * (coord_x + 1))
    loc_north, loc_east, loc_south, loc_west = (-1,-1,-1,-1)
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
    print(f"cell is {output[loc]},x:{x},y:{y}")
    return (loc_north, loc_east, loc_south, loc_west)


def destroy_wall(output: str, current_loc: int, next_loc: int) -> str:
	current_cell = output[current_loc]
	next_cell = output[next_loc]
	nh = check_neighborhood(current_loc, output)
	next_pos = "north" if next_loc == nh[0]
	next_pos = "east" if next_loc == nh[1]
	next_pos = "south" if next_loc == nh[2]
	next_pos = "west" if next_loc == nh[3]
	


def choose_next(output: str, current: int, processed: list[int]) -> int:
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


def hunt_and_kill(output: str) -> str:
    processed_cells = []
    entry: list[str] = configs['ENTRY'].split(",")
    current: int = int(entry[0]) + (int(entry[1]) * (coord_x + 1))
    while 'F' in output:
        processed_cells += [current]
		try:
			next_cell = choose_next(output, current, processed_cells)

		except NHError:
			for x in range(len(output)):
				if x not in processed_cells
						and output[x] != '\n':
					current = x
					break


def main():
    output = full_cell()
    hunt_and_kill(output)


if __name__ == "__main__":
    main()
