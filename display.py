from mlx import Mlx
from parser_config import configs

mlx = Mlx()

ptr = mlx.mlx_init()

win = mlx.mlx_new_window(ptr, 800, 600, "Maze")

img = mlx.mlx_new_image(ptr, 200, 200)

data, bpp, sl, fmt = mlx.mlx_get_data_addr(img)

def draw_horizontal(x: float, y: float, length: float) -> None:
	for i in range(length):
		offset = y * sl + (x + i) * (bpp // 8)
		data[offset:offset+4] = (0xFFFFFFFF).to_bytes(4, 'little')
def draw_vertical(x: float, y: float, length: float) -> None:
	for i in range(length):
		offset = (y + i) * sl + x * (bpp // 8)
		data[offset:offset+4] = (0xFFFFFFFF).to_bytes(4, 'little')

def draw_square(wall: str, loc: tuple[float, float], length:  float) -> None:
	x = loc[0]
	y = loc[1]
	
	draw_horizontal(x, y, length)
	draw_vertical(x, y, length)
	draw_horizontal(x + length, y, length)
	draw_vertical(x, y + length, length)

draw_square("wall", (400, 300), 40)
draw_vertical(10, 20, 40)
draw_horizontal(10, 20, 40)
draw_vertical(20, 20, 40)
draw_horizontal(10, 40, 40)

mlx.mlx_put_image_to_window(ptr, win, img, 0, 0)

mlx.mlx_destroy_image(ptr, img)

mlx.mlx_loop(ptr)

mlx.mlx_put_image_to_window(ptr, win, img, 0, 0)

mlx.mlx_destroy_image(ptr, img)

mlx.mlx_loop(ptr)
