from mazegen import MazeGenerator
import sys
try:
    from mlx import Mlx
except Exception:
    print("####"*20)
    print("\n\t\t\t ********HEEEEEEEYYYYYYYYY********\n")
    print("\t\t\tPlease run the command make install")
    print("\t\t\t  The dependency is yet to install\n")
    print("####"*20)
    sys.exit()
from parser_config import configs
from draw_maze import draw_maze
import random
from typing import Any
from themes import r_extra_diff_colors, extra_diff_colors, diff_colors

filename = ""


def update_filename(name: str) -> None:
    """
    update the variable filename's value
    """
    global filename
    filename = name


display = False
theme = "cyberpunk"
mlx = Mlx()
ptr = mlx.mlx_init()
win = None
images: list[Any] = []
bases: list[Any] = []
imgs: list[Any] = []
width = None
height = None


def generate_params(theme: str = "cyberpunk") -> list[dict["str", Any]]:
    """
    Create parameters to be set as arguments for the draw_square
    function

    Args:
        theme:the maze's theme color id
    Return:
        list of dicts who contain the parameters
    """
    global bases
    bases = bases
    if len(bases) == 0:
        return []
    if theme not in ["cyberpunk", "ocean", "forest", "ice",
                     "royal", "sunset",
                     "vintage", "toxic", "cosmic",
                     "desert", "inferno", "matrix",
                     "sakura", "glitch", "steampunk",
                     "nordic", "neon_pulse",
                     "atlantis", "autumn", "nebula",
                     "eclipse", "safari", "vaporwave",
                     "magma", "deep_sea", "nuclear",
                     "candy", "gothic"]:
        theme = "cyberpunk"
    img1_params = {
        "loc": (0, 0),
        "length": 40,
        "colors": diff_colors[theme],
        "height": bases[1]
    }

    img2_params = {
        "loc": (0, 0),
        "length": 20,
        "colors": extra_diff_colors[theme],
        "height": bases[1]
    }

    img3_params = {
        "loc": (0, 0),
        "length": 20,
        "colors": r_extra_diff_colors[theme],
        "height": bases[1]
    }
    return [img1_params, img2_params, img3_params]


def initialize_mlx(mlx: Mlx) -> None:
    """
    Initialize global variables

    Args:
        mlx: Object of the class Mlx
    """
    global win
    global images
    global bases
    global imgs
    bases += [configs["WIDTH"]]
    bases += [configs["HEIGHT"]]
    width = int((configs["WIDTH"] * 40)) + 80
    height = int((configs["HEIGHT"] * 40)) + 80

    win = mlx.mlx_new_window(ptr, width, height, "Maze")
    images += [mlx.mlx_new_image(ptr, width, height)]
    images += [mlx.mlx_new_image(ptr, width, height)]
    images += [mlx.mlx_new_image(ptr, width, height)]

    imgs += [mlx.mlx_get_data_addr(images[0])]
    imgs += [mlx.mlx_get_data_addr(images[1])]
    imgs += [mlx.mlx_get_data_addr(images[2])]


def clear_mlx_image(img_struct: tuple[Any, int, int, int]) -> None:
    """
    Clear an MLX image by resetting all pixel data to zero.

    The image buffer is filled with null bytes, making the entire image black.

    Args:
        img_struct: A tuple containing the image buffer and its metadata
        in the form ``(data, bits_per_pixel, size_line, format)``
    """
    data, bpp, sl, fmt = img_struct
    total_bytes = len(data)
    data[0:total_bytes] = b'\x00' * total_bytes


def on_close(data: Any) -> None:
    """
    Handle the closing of the window(by stopping the loop)
    and destroying images

    Args:
        data: data provided by the MLX callback
    """
    global images
    images = images
    if len(images) == 0:
        return
    mlx.mlx_loop_exit(ptr)
    mlx.mlx_destroy_image(ptr, images[0])
    mlx.mlx_destroy_image(ptr, images[1])
    mlx.mlx_destroy_image(ptr, images[2])


def on_key(keycode: int, maze: MazeGenerator) -> None:
    """
    Doing specifics actions depending on the keycode:to regenerate the maze,
    to quit the open window, to show the path and changing the color of the
    maze

    Args:
        keycode: assign to the number of the keycode on keyboard
        maze: Instance of MazeGenerator
    """
    global theme
    global filename
    global display
    global win
    global bases
    global images
    filename = filename
    win = win
    bases = bases
    images = images
    if len(images) == 0 or len(bases) == 0:
        return
    if keycode == 114:
        mlx.mlx_clear_window(ptr, win)
        configs["WIDTH"] = bases[0]
        configs["HEIGHT"] = bases[1]
        coord_entry: list[int] = [int(str(configs["ENTRY"]).split(",")[0]),
                                  int(str(configs["ENTRY"]).split(",")[1])]
        coord_exit: list[int] = [int(str(configs["EXIT"]).split(",")[0]),
                                 int(str(configs["EXIT"]).split(",")[1])]
        maze = MazeGenerator(
            int(configs['SEED']),
            bool((configs["PERFECT"])),
            coord_entry,
            coord_exit,
            int(configs["WIDTH"]),
            int(configs["HEIGHT"]))
        maze.generate()
        maze.solve()
        with open(configs["OUTPUT_FILE"], 'w') as f:
            f.write(
                f"{maze.get_maze()}\n"
                f"{configs['ENTRY']}\n"
                f"{configs['EXIT']}\n"
                f"{maze.get_solution()}\n")
        show_maze(maze)
    elif keycode == 120:
        on_close(None)
    elif keycode == 99:
        mlx.mlx_clear_window(ptr, win)
        theme = random.choice(
            ["cyberpunk", "ocean", "forest", "ice",
             "royal", "sunset", "vintage", "toxic",
             "cosmic", "desert", "inferno", "matrix",
             "sakura", "glitch", "steampunk", "nordic",
             "neon_pulse", "atlantis", "autumn", "nebula",
             "eclipse", "safari", "vaporwave", "magma",
             "deep_sea", "nuclear", "candy", "gothic"])
        show_maze(maze)
    elif keycode == 115:
        display = not display
        if display:
            mlx.mlx_put_image_to_window(ptr, win, images[2], 10, 10)
        else:
            mlx.mlx_clear_window(ptr, win)
            show_maze(maze)


def draw_horizontal(x: float, y: float, length: float,
                    color: int, img: tuple[Any, int, int, int]) -> None:
    """
    Draw a horizontal line on an MLX image.

    The line starts at the given coordinates and extends to the right by
    the specified length. Pixels are written directly into the image
    buffer.

    Args:
        x: X-coordinate of the starting point.
        y: Y-coordinate of the starting point.
        length: Length of the line in pixels.
        color: Color encoded as a 32-bit integer.
        img: Tuple containing the image buffer and its metadata in the
        form ``(data, bits_per_pixel, size_line, format)``.
    """
    data, bpp, sl, fmt = img
    ix, iy = int(x), int(y)
    for i in range(int(length)):
        offset = iy * sl + (ix + i) * (bpp // 8)
        data[offset:offset + 4] = (color).to_bytes(4, 'little')


def draw_vertical(x: float, y: float, length: float,
                  color: int, img: tuple[Any, int, int, int]) -> None:
    """
    Draw a vertical line on an MLX image.

    The line starts at the given coordinates and extends downward by the
    specified length. Pixels are written directly into the image buffer.

    Args:
        x: X-coordinate of the starting point.
        y: Y-coordinate of the starting point.
        length: Length of the line in pixels.
        color: Color encoded as a 32-bit integer.
        img: Tuple containing the image buffer and its metadata in the
            form ``(data, bits_per_pixel, size_line, format)``.
    """
    data, bpp, sl, fmt = img
    ix, iy = int(x), int(y)
    for i in range(int(length)):
        offset = (iy + i) * sl + ix * (bpp // 8)
        data[offset:offset + 4] = (color).to_bytes(4, 'little')


def draw_square(
        cell: str, loc: tuple[float, float],
        length: float, colors: tuple[int, int],
        img: tuple[Any, int, int, int]) -> None:
    """
    Draw the walls of a maze cell on an MLX image.
    The cell value is interpreted as a binary representation of
    four wall states: north, east, south, and west. Each active wall is
    drawn using the corresponding drawing function.

    Args:
    cell: Hexadecimal representation of the cell walls.
    loc: Coordinates of the top-left corner of the cell.
    length: define the size of the cell.
    colors: Tuple containing the default and special cell colors.
    img: Tuple containing the MLX image buffer and metadata.
    """
    length = length - 3
    color = colors[0]
    if cell == "F":
        color = colors[1]
    if cell != "0":
        walls = bin(int(cell, 16))[2:].zfill(4)
        x, y = loc
        if walls[3] == "1":
            draw_horizontal(x, y, length, color, img)
        if walls[0] == "1":
            draw_vertical(x, y, length, color, img)
        if walls[1] == "1":
            draw_horizontal(x, y + length, length, color, img)
        if walls[2] == "1":
            draw_vertical(x + length, y, length, color, img)


def fill_content(to_avoid: list[int] = []) -> str:
    """
    Create a string similar to the output file but only contain
    "F","0" and "\n"

    Args:
        to_avoid:List of indexes for the string to assign the
                character "F", the rest will be "0" and "\n"
    return:
        Either a string representing the image for the endpoints
        or another one representing the image for path, it depends
        on the "to_avoid" list
    """
    global filename
    global bases
    filename = filename
    bases = bases
    if len(bases) == 0:
        return ""
    configs["WIDTH"] = bases[0]
    configs["HEIGHT"] = bases[1]
    e: list[str] = str(configs["ENTRY"]).split(",")
    entry_cell: tuple[int, int] = (int(e[0]), int(e[1]))
    ex: list[str] = str(configs["EXIT"]).split(",")
    exit_cell: tuple[int, int] = (int(ex[0]), int(ex[1]))
    output: str = ""
    for line in range(int(configs["HEIGHT"])):
        for char in range(int(configs["WIDTH"])):
            if (len(to_avoid) == 0
                and ((char == entry_cell[0] and line == entry_cell[1])
                     or (char == exit_cell[0] and line == exit_cell[1]))):
                output += "F"
            elif (
                to_avoid
                and (char + ((int(configs["WIDTH"]) + 1) * line))
                in to_avoid[1:(len(to_avoid) - 1)]
            ):
                output += "F"
            else:
                output += "O"
        output += "\n"
    return output


def show_maze(maze: MazeGenerator) -> None:
    """
    Render the maze and display it in the MLX window.

    This function clears previous image buffers, generates visual
    layers for the maze, entry/exit points, and solution path,
    then displays them in the window. It also registers keyboard
    and window-close callbacks.

    Args:
        maze: MazeGenerator instance
    """
    global theme
    global filename
    global imgs
    global bases
    filename = filename
    imgs = imgs
    bases = bases
    if len(imgs) == 0 or len(bases) == 0:
        return
    theme = theme
    clear_mlx_image(imgs[0])
    clear_mlx_image(imgs[1])
    clear_mlx_image(imgs[2])
    configs["WIDTH"] = bases[0]
    configs["HEIGHT"] = bases[1]
    file = open(configs['OUTPUT_FILE'], 'r')
    content = file.read()
    content2 = fill_content()
    content3 = fill_content(maze.path)
    params = generate_params(theme)
    file.close()
    draw_maze(draw_square, params[0], content, imgs[0], 1)
    draw_maze(draw_square, params[1], content2, imgs[1], 2)
    draw_maze(draw_square, params[2], content3, imgs[2], 2)
    instructions1 = "R: regen  S: path"
    instructions2 = "C: color  X: quit"
    mlx.mlx_string_put(
        ptr,
        win,
        40,
        ((bases[1] * 40) + 20),
        params[1]["colors"][0],
        instructions1)
    mlx.mlx_string_put(
        ptr,
        win,
        40,
        ((bases[1] * 40) + 40),
        params[1]["colors"][0],
        instructions2)
    mlx.mlx_put_image_to_window(ptr, win, images[0], 10, 10)
    mlx.mlx_put_image_to_window(ptr, win, images[1], 10, 10)

    mlx.mlx_key_hook(win, on_key, maze)
    mlx.mlx_hook(win, 33, 0, on_close, None)


def launch() -> None:
    """
    Start the MLX event loop.
    The event loop keeps the graphical window active and listens for
    user interactions such as keyboard input and window events.
    """
    mlx.mlx_loop(ptr)
