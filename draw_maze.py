from collections.abc import Callable

def draw_maze(function: Callable, function_parameter: , output: str) -> None:
	lines = output.split('\n')
	for line in lines:
		for char in line:
			function(char, *args)
