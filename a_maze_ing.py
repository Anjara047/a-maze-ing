import sys
import mazegen
from parser_config import configs, update_configs
from display import mlx, initialize_mlx, update_filename, show_maze, launch
try:
    filename = sys.argv[1]
    with open(filename) as file:
        pass
except Exception:
    print()
    print("###"*10)
    print("missing or invalid configuration file, for example: 'config.txt'")
    print("-usage: python3 a_maze_ing.py <file_name(or path)>")
    print("-other option: just update the filename in the Makefile")
    print("example: FILENAME=config.txt")
    print("###"*10)
    print()
    sys.exit()
update_configs(filename)
coord_entry: list[int] = [int(str(configs["ENTRY"]).split(",")[0]),
                          int(str(configs["ENTRY"]).split(",")[1])]
coord_exit: list[int] = [int(str(configs["EXIT"]).split(",")[0]),
                         int(str(configs["EXIT"]).split(",")[1])]
maze = mazegen.MazeGenerator(
    int(configs['SEED']),
    bool(configs["PERFECT"]),
    bool(configs["REPRODUCTIBLE"]),
    coord_entry,
    coord_exit,
    int(configs["WIDTH"]),
    int(configs["HEIGHT"]))
maze.generate()
with open(configs["OUTPUT_FILE"], 'w') as f:
    f.write(
        f"{maze.get_maze()}\n"
        f"{configs['ENTRY']}\n"
        f"{configs['EXIT']}\n"
        f"{maze.get_solution()}\n")
update_filename(filename)
initialize_mlx(mlx)
show_maze(maze)
launch()
