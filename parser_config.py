from mazegen.generator import locate_pattern
configs: dict[str, int | str | bool] = {
    'WIDTH': 20,
    'HEIGHT': 20,
    'ENTRY': '0,0',
    'EXIT': '',
    'OUTPUT_FILE': 'maze.txt',
    'PERFECT': True,
    'REPRODUCTIBLE': True,
    'SEED': 42
}
configs['EXIT'] = f"{int(configs['WIDTH']) - 1},{int(configs['HEIGHT']) - 1}"


def censure_configs() -> None:
    """
    Validate and sanitize maze configuration values.

    This function checks maze dimensions, entry and exit coordinates,
    and output file names. Invalid values are replaced with safe default
    values to prevent generation errors or overwriting important files.

    The global configuration dictionary is modified directly.
    """
    coord_entry = str(configs['ENTRY']).split(",")
    coord_exit = str(configs['EXIT']).split(",")
    if (len(coord_entry) != 2
            or not coord_entry[0].isdigit()
            or not coord_entry[1].isdigit()):
        print("[INVALID]The given ENTRY config is invalid:")
        print("\t\t->it should follow the syntax 'int,int', ", end="")
        print("example: ENTRY=2,1")
        configs['ENTRY'] = "0,0"
        coord_entry = str(configs['ENTRY']).split(",")
    if (len(coord_exit) != 2
            or not coord_exit[0].isdigit()
            or not coord_exit[1].isdigit()):
        print("[INVALID]The given EXIT config is invalid:")
        print("\t\t->it should follow the syntax 'int,int', ", end="")
        print("prexample: EXIT=10,10")
        val_x = int(float(configs['WIDTH'])) - 1
        configs['EXIT'] = (
            f"{val_x},{int(float(configs['HEIGHT'])) - 1}"
        )
        coord_exit = str(configs['EXIT']).split(",")
    try:
        int(coord_entry[0])
        int(coord_entry[1])
        int(coord_exit[0])
        int(coord_exit[1])
    except Exception:
        valu_x = int((float(coord_entry[0])))
        configs['ENTRY'] = f"{valu_x},{int((float(coord_entry[1])))}"
        configs['EXIT'] = (
            f"{int((float(coord_exit[0])))},{int((float(coord_exit[1])))}"
        )
        coord_entry = str(configs['ENTRY']).split(",")
        coord_exit = str(configs['EXIT']).split(",")
    loc_entry = (int(coord_entry[0])) + (
        (int(configs["WIDTH"]) + 1) * (int(coord_entry[1])))
    loc_exit = (int(coord_exit[0])) + (
        (int(configs["WIDTH"]) + 1) * (int(coord_exit[1])))
    if int(configs["WIDTH"]) > 40:
        configs['WIDTH'] = 40
        print("[GOOD_TO_KNOW]The max width is fixed to 40 in", end="")
        print(" order to avoid a bigger window than our screen:")
        print("\t\t->so if a width bigger than 40 is given ", end="")
        print("it will be set to 40")
    if int(configs['HEIGHT']) > 22:
        configs['HEIGHT'] = 22
        print("[GOOD_TO_KNOW]The max height is fixed to 22 in", end="")
        print(" order to avoid a bigger window than our screen:")
        print("\t\t->so if a height bigger than 22 is given", end="")
        print("it will be set to 22")
    if int(configs['WIDTH']) < 7:
        print("[GOOD_TO_KNOW]The min width is fixed to 7 in", end="")
        print(" order to be sure that a beautiful maze will be generated")
        print("\t\t->so yeah, you won't get a lower width than 7")
        configs['WIDTH'] = 7
    if int(configs['HEIGHT']) < 7:
        print("[GOOD_TO_KNOW]The min height is fixed to 7 in", end="")
        print(" order to be sure that a beautiful maze will be generated")
        print("\t\t->so yeah, you won't get a lower height than 7")
        configs['HEIGHT'] = 7
    if ((loc_entry in locate_pattern(
        int(configs['WIDTH']), int(configs['HEIGHT'])))
        or (int(coord_entry[0]) >= int(configs['WIDTH']))
            or (int(coord_entry[1]) >= int(configs['HEIGHT']))):
        print("[INVALID]The ENTRY cell can't be ", end="")
        print("located outside the maze,", end="")
        print("nor where the 42 pattern is.")
        configs['ENTRY'] = "0,0"
    if ((loc_exit in locate_pattern(
        int(configs['WIDTH']), int(configs['HEIGHT'])))
        or (int(coord_exit[0]) >= int(configs['WIDTH']))
            or (int(coord_exit[1]) >= int(configs['HEIGHT']))):
        print("[INVALID]The EXIT cell can't be ", end="")
        print("located outside the maze,", end="")
        print("nor where the 42 pattern is.")
        configs['EXIT'] = (
            f"{int(configs['WIDTH']) - 1},"
            f"{int(configs['HEIGHT']) - 1}"
        )
    if configs['EXIT'] == configs['ENTRY']:
        print("[INVALID]", end="")
        print("The ENTRY and the EXIT cell can't be located at the same place")
        if configs['ENTRY'] != "0,0":
            configs['EXIT'] = "0,0"
        else:
            configs['EXIT'] = (
                f"{int(configs['WIDTH']) - 1},"
                f"{int(configs['HEIGHT']) - 1}"
            )
    if ((configs['OUTPUT_FILE'] == "") or (configs['OUTPUT_FILE'] in [
        "config.txt", "Makefile", "README.md", "themes.py",
        "mazegen-0.1.0-py3-none-any.whl", "mazegen",
        "a_maze_ing.py", "display.py",
        "draw_maze.py", "/mazegen/generator.py",
        "parser_config.py", "mlx-2.2-py3-none-any.whl",
        "pyproject.toml"
    ])):
        print(f"[HEY!]The filename {configs['OUTPUT_FILE']}", end="")
        print(" was already taken by one of the main file in the project:")
        print("\t\t->so we gave the ouput file the default name 'maze.txt'")
        configs['OUTPUT_FILE'] = "maze.txt"


def update_configs(filename: str, redefine: bool = False) -> None:
    """
    Load and update maze configuration values from the file <filename>.

    The function reads the configuration file, ignores comments and
    invalid lines, converts values to their expected types, and updates
    the global configuration dictionary. After loading, the values are
    validated and corrected using censure_configs().
    """
    try:
        with open(filename, "r") as f:
            l_configs = [
                line.strip()
                for line in f if line != line.capitalize()
                and not line.startswith("#")
            ]
    except Exception:
        l_configs = []

    int_configs = ["WIDTH", "HEIGHT", "SEED"]
    bool_configs = ["PERFECT", "REPRODUCTIBLE"]
    if not redefine:
        try:
            for l_config in l_configs:
                config = [
                    element.strip() for element in str(l_config).split("=")
                    ]
                if config[0] in int_configs:
                    try:
                        if not config[1].isdigit():
                            config[1] = "20"
                        value = int(float(config[1]))
                    except Exception:
                        if config[1].split(",")[0].isalpha():
                            value = int(float(config[1].split(",")[0]))
                    if value > 0:
                        configs[config[0]] = value
                elif config[0] in bool_configs:
                    if config[1] == 'False':
                        configs[config[0]] = False
                    else:
                        configs[config[0]] = True
                else:
                    configs[config[0]] = config[1]
        except Exception:
            pass
    censure_configs()
