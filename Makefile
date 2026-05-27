PYTHON = python3.10
PIP = pip
MAIN = a_maze_ing.py

.PHONY: install run debug clean lint lint-strict

install:
	$(PIP) install -r requirements.txt

run:
	@$(PYTHON) $(MAIN)

debug:
	@$(PYTHON) -m pdb $(MAIN)

clean:
	@rm -rf __pycache__
	@rm -rf .mypy_cache

lint:
	flake8 .
	mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs`

lint-strict:
	flake8 .
	mypy . --strict
