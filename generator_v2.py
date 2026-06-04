#! python3
import random
from parser_config import configs

on = {
	'all' : {1,2,3,4,5,6,7,8,9,10,11,12,13,14},
	'north' : {8,9,10,11,12,13,14},
	'east' : {4,5,6,7,12,13,14},
	'south' : {2,3,6,7,10,11,14},
	'west' : {1,3,5,7,9,11,13}
	}

side_on = ("north", "east", "south", "west")

coord_x = configs['WIDTH']
coord_y = configs['HEIGHT']

def full_cell()-> str:
	output = ''
	for line in range(coord_y):
		for char in range(coord_x):
				output += 'F'
		output += '\n'
	return output


def check_neighborhood(loc: int, output: str) -> tuple[int, int, int, int]:
    #crees qlq chose qui convertit loc en (x,y)
	y = loc // (coord_x + 1)
	x = loc - (y * (coord_x + 1))
	north, east, south, west = (0, 0, 0, 0)
	#E
	if  x > 0:
		loc_east = (y * (coord_x + 1)) + x - 1
		east = int(output[loc_east], 16)
	#W
	if x < (coord_x - 1):
		loc_west = (y * (coord_x + 1)) + x + 1
		west = int(output[loc_west], 16)
	#N
	if y > 0:
		loc_north = ((y - 1) * (coord_x + 1)) + x
		north = int(output[loc_north], 16)
	#S
	if y < (coord_y - 1):
		loc_south = ((y + 1) * (coord_x + 1)) + x
		south = int(output[loc_south], 16)
	print(f"cell is {output[loc]},x:{x},y:{y}")
	return (north, east, south, west)
		

def sculpt_output(output: str, perfect : bool):
    for 'F' in output:
        