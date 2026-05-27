import random
from parser_config import configs

def generate_maps() -> str:
	output = ''
	for line in range(configs['HEIGHT']):
		for char in range(configs['WIDTH']):
			rand_int = random.randint(0, 15)
			if rand_int == 0:
				output += '0'
			else:
				output += ((str(hex(rand_int))).strip('0x')).capitalize()
		output += '\n'
	return output

register = open(configs['OUTPUT_FILE'], 'w')
register.write(generate_maps())
