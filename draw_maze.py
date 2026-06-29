from collections.abc import Callable


def draw_maze(function: Callable, func_params: dict, output: str) -> None:
    x, y = func_params["loc"]

    lines = output.split('\n')
    for line in lines:
        x = func_params["loc"][0]
        for char in line:
            function(char, (x, y), func_params["length"], func_params["color"])
            x += func_params["length"]
        y += func_params["length"]
