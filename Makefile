PYTHON = python3
PIP = pip
MAIN = a_maze_ing.py
FILENAME =config.txt
RUN = poetry run

.PHONY: install run debug clean lint lint-strict

install:
	@$(PIP) install poetry
	@poetry install
	@$(RUN) pip install ./mlx-2.2-py3-none-any.whl

run:
	@$(RUN) $(PYTHON) $(MAIN) $(FILENAME)

debug:
	@$(RUN) $(PYTHON) -m pdb $(MAIN)

clean:
	@rm -rf __pycache__
	@rm -rf mazegen/__pycache__
	@rm -rf .mypy_cache
	@find . -mindepth 1 \
		\( -name mazegen -o -name .git \) -prune -o \
		\( -name "a_maze_ing.py" -o \
			-name "display.py" -o \
			-name "draw_maze.py" -o \
			-name "parser_config.py" -o \
			-name "mazegen-0.1.0-py3-none-any.whl" -o \
			-name "README.md" -o \
			-name "config.txt" -o \
			-name "Makefile" -o \
			-name "pyproject.toml" -o \
			-name "mlx-2.2-py3-none-any.whl" -o \
			-name "themes.py" -o \
			-name ".gitignore" \) -o \
		-exec rm -rf {} +

lint:
	-@$(RUN) flake8 .
	-@$(RUN) mypy . --warn-return-any \
					--warn-unused-ignores \
					--ignore-missing-imports \
					--disallow-untyped-defs \
					--check-untyped-defs
