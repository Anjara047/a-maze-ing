from mlx import Mlx
from parser_config import configs
from draw_maze import draw_maze

mlx = Mlx()

ptr = mlx.mlx_init()

win = mlx.mlx_new_window(ptr, 800, 600, "Maze")

img = mlx.mlx_new_image(ptr, 800, 600)

data, bpp, sl, fmt = mlx.mlx_get_data_addr(img)

def draw_horizontal(x: float, y: float, length: float, color: int, thickness : int) -> None:
	for i in range(length):
		offset = y * sl + (x + i) * (bpp // 8)
		data[offset:offset+4] = (color).to_bytes(4, 'little')
	if thickness > 0:
		draw_horizontal(x, y + 1, length, color, thickness - 1)

def draw_vertical(x: float, y: float, length: float, color: int, thickness : int) -> None:
	for i in range(length):
		offset = (y + i) * sl + x * (bpp // 8)
		data[offset:offset+4] = (color).to_bytes(4, 'little')
	if thickness > 0:
		draw_vertical(x + 1, y, length, color, thickness - 1)

def draw_square(wall: int, loc: tuple[float, float], length:  float, color: int) -> None:
	x, y = loc
	thickness = 4
	draw_horizontal(x, y, length, color, thickness)
	draw_vertical(x, y, length, color, thickness)
	draw_vertical(x - (thickness + 1) + length, y, length, color, thickness)
	draw_horizontal(x, y + length, length, color, thickness)

draw_maze()

mlx.mlx_put_image_to_window(ptr, win, img, 0, 0)

mlx.mlx_destroy_image(ptr, img)

mlx.mlx_loop(ptr)

mlx.mlx_put_image_to_window(ptr, win, img, 0, 0)

mlx.mlx_destroy_image(ptr, img)

mlx.mlx_loop(ptr)
