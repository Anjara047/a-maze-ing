from parser_config import configs
from generator import generate_maps
register = open(configs['OUTPUT_FILE'], 'w')
register.write(generate_maps())
register.close()
import display
