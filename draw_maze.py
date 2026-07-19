from collections.abc import Callable
from parser_config import update_configs
from typing import Any


def draw_maze(function: Callable[..., None], func_params: dict[str, Any],
              output: str, img: str, echelle: int, filename: str) -> None:
    """
    Draw a maze by applying a drawing function to each cell.

    The maze content is parsed row by row, and every non-empty cell is
    passed to the provided drawing function with the configured position,
    size, colors, and image buffer.

    Args:
        function: Function used to draw an individual maze cell.
        func_params: Dictionary containing drawing configuration such as
            position, length, colors and height.
        output: String representation of the maze grid.
        img: Image buffer where the maze is rendered.
        scale: factor used to position and resize the drawing.
    """
    update_configs(filename)
    x, y = func_params["loc"]
    scale = (echelle - 1) * (func_params["length"] // 2)
    lines = output.split('\n')
    for line in lines[0:func_params["height"]]:
        x = func_params["loc"][0]
        for char in line:
            if char != "O":
                function(
                    char,
                    (x + scale,
                     y + scale),
                    func_params["length"],
                    func_params["colors"],
                    img)
            x += func_params["length"] * echelle
        y += func_params["length"] * echelle
