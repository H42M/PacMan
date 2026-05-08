install:
	python3 -m venv .venv
	.venv/bin/python -m pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt

debug:
	.venv/bin/python -m pdb a_maze_ing.py config.txt

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +

fclean:
	make clean
	rm -rf .venv
	rm -f maze.txt

lint: install
	.venv/bin/flake8 . --exclude=.venv,.env
	.venv/bin/mypy . --exclude '\.venv|\.env' --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
	make clean

lint-strict: install
	.venv/bin/flake8 . --exclude=.venv,.env
	.venv/bin/mypy . --exclude '\.venv|\.env' --strict
	make clean

lint-doc: install
	.venv/bin/flake8 . --exclude=.venv,.env --extend-ignore=D100,D101,D102,D103,D104
	.venv/bin/mypy . --exclude '\.venv|\.env' --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
	make clean


run: install
	.venv/bin/python temp_main.py
	make clean

package: install
	.venv/bin/python -m pip install --upgrade build
	.venv/bin/python -m build
	cp dist/mazegen-*.whl .