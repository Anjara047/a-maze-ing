import sys
from typing import Any
from mazegen.generator import locate_pattern

configs: dict[str, Any] = {
    'WIDTH': None,
    'HEIGHT': None,
    'ENTRY': None,
    'EXIT': None,
    'OUTPUT_FILE': None,
    'PERFECT': None,
    'SEED': -69
}


def assign_param(key: str, value: str, mess: list[str]) -> bool:
    """
    Validate and assign a configuration parameter.

    Checks whether the value associated with the given configuration key
    is valid. If the value is valid, it is assigned with it's key.
    Otherwise, an error message is appended to ``mess``.

    Args:
        key: The name of the configuration parameter.
        value: The value associated with the parameter.
        mess: A list used to collect validation error messages.

    Returns:
        True if the parameter was successfully validated and assigned,
        False otherwise.

    Raises:
        ValueError: If the entry and exit coordinates are identical.
    """
    state = False
    if key == 'WIDTH':
        try:
            int(value)
        except ValueError as error:
            mess += [f"[WIDTH]: {error}"]
        else:
            if int(value) > 40:
                value = "40"
                print("[:)]max WIDTH is 40 by default because ", end="")
                print("more than that would be too large for the screen")
                print()
            elif int(value) < 7:
                value = "7"
                print("[:)]min WIDTH is 7 by default because", end="")
                print(" it'd be too small to get a beautiful maze")
                print()
            configs[key] = int(value)
            state = True
    elif key == 'HEIGHT':
        try:
            int(value)
        except ValueError as error:
            mess += [f"[HEIGHT]: {error}"]
        else:
            if int(value) > 23:
                value = "23"
                print("[:)]max HEIGHT is 23 by default because", end="")
                print("more than that would be too large for the screen")
                print()
            elif int(value) < 7:
                value = "7"
                print("[:)]min HEIGHT is set 7 by default because", end="")
                print(" it'd be too small to get a beautiful maze")
                print()
            configs[key] = int(value)
            state = True
    elif key == 'ENTRY':
        values = value.split(",")
        if value == configs['EXIT']:
            raise ValueError(
                "The coordinate of EXIT cannot be the same as ENTRY")
        try:
            if len(values) != 2:
                raise ValueError("The coordinate must be similar to 'x,y'")
            for coord in values:
                int(coord)
        except ValueError as error:
            mess += [f"[ENTRY]: {error}"]
        else:
            configs[key] = value
            state = True

    elif key == 'EXIT':
        values = value.split(",")
        try:
            if value == configs['ENTRY']:
                raise ValueError(
                    "The coordinate of EXIT cannot be the same as ENTRY")
            if len(values) != 2:
                raise ValueError("The coordinate must be similar to 'x,y'")
            for coord in values:
                int(coord)
        except ValueError as error:
            mess += [f"[EXIT]: {error}"]
        else:
            configs[key] = value
            state = True

    elif key == 'OUTPUT_FILE':
        if value in [
            "config.txt", "Makefile", "README.md", "themes.py",
            "mazegen-0.1.0-py3-none-any.whl", "mazegen",
            "a_maze_ing.py", "display.py",
            "draw_maze.py", "mazegen/generator.py", "mazegen/__init__.py",
            "parser_config.py", "mlx-2.2-py3-none-any.whl",
            "pyproject.toml", ""
        ]:
            mess += ["[OUTPUT_FILE]: name has already been exist"]
        else:
            configs[key] = value

    elif key == 'PERFECT':
        if value == 'True':
            configs[key] = True
            state = True
        elif value == 'False':
            configs[key] = False
            state = True
        else:
            mess += ["[PERFECT]: It must be either True or False"]

    elif key == 'SEED':
        try:
            int(value)
        except ValueError as error:
            mess += [f"[SEED]: {error}"]
        else:
            configs[key] = int(value)
            state = True
    return state


def update_configs(filename: str, first_call: bool = False) -> None:
    """
    Read the configs file and update the configuration file,
    it opens the configuration file and extract each parameter that does
    not start with "#"
    It also checks the postion of the entry and exit if they are valid,
    and raise a message in case they are not.

    Args:
        filename: name of the config file
        first_call: checking on whether it's the first call of the function
    """
    mess: list[str] = []
    try:
        with open(filename) as config_file:
            config_lines = [
                line.strip()
                for line in config_file.readlines()
                if (not line.startswith("#")
                    and line != line.capitalize())
            ]
    except OSError as error:
        print(f"Invalid config file: {error}")
        sys.exit(1)
    for config_line in config_lines:
        param = config_line.split("=")
        if len(param) == 2:
            if param[0] in configs.keys():
                assign_param(param[0], param[1], mess)
    try:
        coo_ent = configs['ENTRY'].split(",")
        if (not (int(coo_ent[0]) >= 0 and int(coo_ent[0]) < configs['WIDTH'])):
            mess += ["[ENTRY]The coordinate x is outside the area of the maze"]
        if not (int(coo_ent[1]) >= 0 and int(coo_ent[1]) < configs['HEIGHT']):
            mess += ["[ENTRY]The coordinate y is outside the area of the maze"]
        co_ex = configs['EXIT'].split(",")
        if (not (int(co_ex[0]) >= 0 and int(co_ex[0]) < configs['WIDTH'])):
            mess += ["[EXIT]The coordinate x is outside the area of the maze"]
        if (not (int(co_ex[1]) >= 0 and int(co_ex[1]) < configs['HEIGHT'])):
            mess += ["[EXIT]The coordinate y is outside the area of the maze"]
        loc_ent = int(coo_ent[0]) + (int(coo_ent[1]) * (configs['WIDTH'] + 1))
        loc_exit = int(co_ex[0]) + (int(co_ex[1]) * (configs['WIDTH'] + 1))
        if loc_ent in locate_pattern(configs['WIDTH'], configs['HEIGHT']):
            mess += ["[ENTRY] The coordinate cannot be at the 42 pattern"]
        if loc_exit in locate_pattern(configs['WIDTH'], configs['HEIGHT']):
            mess += ["[EXIT] The coordinate cannot be at the 42 pattern"]
        if first_call:
            if configs['WIDTH'] < 10 or configs['HEIGHT'] < 10:
                print("[HEY!]The Area is too small for the pattern")
                print("\t\t->so the pattern is omitted.\n")
    except Exception:
        pass
    if len(mess) > 0:
        for message in mess:
            print("#", message, "\n")
        sys.exit()
    if None in configs.values():
        print("\n"*2)
        print("\t\t\t***********HEEEEEYYYYYY*********")
        print("\t\t      WHAT ARE YOU DOING,THAT'S IMPOSSIBLE")
        print("\t\t   Missing mandatory element in the config file")
        print("\n"*2)
        sys.exit()
