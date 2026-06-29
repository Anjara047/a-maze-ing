#! python3
from mlx import Mlx
from parser_config import configs
from draw_maze import draw_maze

mlx = Mlx()

ptr = mlx.mlx_init()

width = (configs["WIDTH"] * 40) + 40
height = (configs["HEIGHT"] * 40) + 40

win = mlx.mlx_new_window(ptr, width, height, "Maze")

img = mlx.mlx_new_image(ptr, width, height)

data, bpp, sl, fmt = mlx.mlx_get_data_addr(img)


def on_close(data):
    mlx.mlx_loop_exit(ptr)


def on_key(keycode, data):
    print(keycode)
    if keycode == 120:
        mlx.mlx_loop_exit(ptr)


def draw_horizontal(x: float, y: float, length: float,
                    color: int, thickness: int) -> None:
    for i in range(length):
        offset = y * sl + (x + i) * (bpp // 8)
        data[offset:offset + 4] = (color).to_bytes(4, 'little')
# if thickness > 0:
# draw_horizontal(x, y + 1, length, color, thickness - 1)


def draw_vertical(x: float, y: float, length: float,
                  color: int, thickness: int) -> None:
    for i in range(length):
        offset = (y + i) * sl + x * (bpp // 8)
        data[offset:offset + 4] = (color).to_bytes(4, 'little')
    # if thickness > 0:
    # draw_vertical(x + 1, y, length, color, thickness - 1)

# NESW


def draw_square(
        cell: str, loc: tuple[float, float], length: float, color: int) -> None:
    # juste pour tester(a enlever plus tard)
    length = length - 3
    if cell == "F":
        color = 0xFF0000FF
    if cell != "0":
        walls = bin(int(cell, 16))[2:].zfill(4)

        x, y = loc
        thickness = 4
        # N
        if walls[0] == "1":
            draw_horizontal(x, y, length, color, thickness)
        # E
        if walls[1] == "1":
            draw_vertical(x, y, length, color, thickness)
        # S
        if walls[2] == "1":
            draw_horizontal(x, y + length, length, color, thickness)
        # W
        if walls[3] == "1":
            draw_vertical(x + length, y, length, color, thickness)


func_params = {
    "loc": (0, 0),
    "length": 40,
    "color": 0xFFFFFFFF
}
file = open(configs['OUTPUT_FILE'], 'r')
content = file.read()
draw_maze(draw_square, func_params, content)

mlx.mlx_put_image_to_window(ptr, win, img, 10, 10)

mlx.mlx_destroy_image(ptr, img)

mlx.mlx_key_hook(win, on_key, None)
mlx.mlx_hook(win, 33, 0, on_close, None)

mlx.mlx_loop(ptr)
