import random
from parser_config import configs

def which_number(y: int, x: int, output: str) -> int:
	all_number = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15}
	north_on = {8,9,10,11,12,13,15}
	south_on = {2,3,6,7,10,11,14,15}
	east_on = {4,5,6,7,12,13,14,15}
	west_on = {1,3,5,7,9,11,13,15}
	wall_range = all_number
	if y == 0:
		wall_range = wall_range.intersection(north_on)
	if x == 0:
		wall_range = wall_range.intersection(east_on)
	if y == configs['HEIGHT'] - 1:
		wall_range = wall_range.intersection(south_on)
	if x == configs['WIDTH'] - 1:
		wall_range = wall_range.intersection(west_on)
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
