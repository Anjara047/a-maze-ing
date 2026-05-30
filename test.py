from parser_config import configs

def check_neighborhood(y: int, x: int, output: str):
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

file = open("maze.txt", "r")
output = file.read()

on = {
	'all' : {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15},
	'north' : {8,9,10,11,12,13,15},
	'south' : {2,3,6,7,10,11,14,15},
	'east' : {4,5,6,7,12,13,14,15},
	'west' : {1,3,5,7,9,11,13,15}
				}

print(list(on.keys()))
