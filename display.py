from mlx import Mlx
from parser_config import configs

mlx = Mlx()

ptr = mlx.mlx_init()

win = mlx.mlx_new_window(ptr, 800, 600, "Maze")

img = mlx.mlx_new_image(ptr, 200, 200)

data, bpp, sl, fmt = mlx.mlx_get_data_addr(img)

def draw_horizontal(x: float, y: float) -> None:
	x, y = 20, 0
	for x in range(40):
		offset = y * sl + x * (bpp // 8)
		data[offset:offset+4] = (0xFFFFFFFF).to_bytes(4, 'little')
def draw_vertical(x: float, y: float) -> None:
	x, y = 0, 20
	for y in range(40):
		offset = y * sl + x * (bpp // 8)
		data[offset:offset+4] = (0xFFFFFFFF).to_bytes(4, 'little')

def draw_square(wall: str, loc: tuple[int, int]) -> None:
	

mlx.mlx_put_image_to_window(ptr, win, img, 0, 0)

mlx.mlx_destroy_image(ptr, img)

mlx.mlx_loop(ptr)

mlx.mlx_put_image_to_window(ptr, win, img, 0, 0)

mlx.mlx_destroy_image(ptr, img)

mlx.mlx_loop(ptr)
