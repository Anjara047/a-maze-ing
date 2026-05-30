#! python3
import random
from parser_config import configs


#il n'y a pas de 15/F parcequ'il ne devrai pas y avoir de carre(cellule avec 4 murs dans le maze)
on = {
	'all' : {1,2,3,4,5,6,7,8,9,10,11,12,13,14},
	'north' : {8,9,10,11,12,13,14},
	'south' : {2,3,6,7,10,11,14},
	'east' : {4,5,6,7,12,13,14},
	'west' : {1,3,5,7,9,11,13}
	}

def check_neighborhood_v1(y: int, x: int, output: str) -> tuple[int, int, int, int]:
	north, east, south, west = (0, 0, 0, 0)
	#E
	if  x > 0:
		loc_east = (y * (configs['WIDTH'] + 1)) + x - 1
		east = int(output[loc_east], 16)
	#W
	if x < (configs['WIDTH'] - 1):
		loc_west = (y * (configs['WIDTH'] + 1)) + x + 1
		west = int(output[loc_west], 16)
	#N
	if y > 0:
		loc_north = ((y - 1) * (configs['WIDTH'] + 1)) + x
		north = int(output[loc_north], 16)
	#S
	if y < (configs['HEIGHT'] - 1):
		loc_south = ((y + 1) * (configs['WIDTH'] + 1)) + x
		south = int(output[loc_south], 16)
	return (north, east, south, west)

def check_neighborhood_v2(y: int, x: int, output: str) -> tuple[int, int, int, int]:
	north, east = (0, 0)
	#E
	if  x > 0:
		loc_east = (y * (configs['WIDTH'] + 1)) + x - 1
		east = int(output[loc_east], 16)
	#N
	if y > 0:
		loc_north = ((y - 1) * (configs['WIDTH'] + 1)) + x
		north = int(output[loc_north], 16)
	return (north, east)

def filter_range(neighborhood: tuple[int, int], wall_range: set[int]) -> set[int]:
	result = wall_range
	north, east = neighborhood
	if north in on['south']:
		result = result.intersection(on['north'])
	elif neighborhood[0] != 0:
		result = result - on['north']
	if east in on['west']:
		result = result.intersection(on['east'])
	elif neighborhood[1] != 0:
		result = result - on['east']
	return result

def which_number(y: int, x: int, output: str) -> int:
	wall_range = on['all']
	if y == 0:
		wall_range = wall_range.intersection(on['north'])
	if x == 0:
		wall_range = wall_range.intersection(on['east'])
	if y == configs['HEIGHT'] - 1:
		wall_range = wall_range.intersection(on['south'])
	if x == configs['WIDTH'] - 1:
		wall_range = wall_range.intersection(on['west'])
	wall_range = filter_range(check_neighborhood_v2(y, x, output), wall_range)
	return random.choice(tuple(wall_range))

def generate_maps() -> str:
	output = ''
	for line in range(configs['HEIGHT']):
		for char in range(configs['WIDTH']):
			rand_int = which_number(line, char, output)
			if rand_int == 0:
				output += '0'
			else:
				output += ((str(hex(rand_int))).strip('0x')).capitalize()
		output += '\n'
	return output

register = open(configs['OUTPUT_FILE'], 'w')
register.write(generate_maps())
