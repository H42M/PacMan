PYTHON = python3
MAIN = pac-man.py
MAIN_RENDER = render_main
MAIN_STATES = states_main
TEST_MODULE = tests
CONFIG = config/config.json
DEPENDENCIES = requirements.txt

.PHONY: install run debug clean lint lint-strict

install:
	$(PYTHON) -m pip install -r $(DEPENDENCIES)

run:
	$(PYTHON) $(MAIN) $(CONFIG)

run-render:
	$(PYTHON) -m $(TEST_MODULE).$(MAIN_RENDER)
	make clean

run-states:
	$(PYTHON) -m $(TEST_MODULE).$(MAIN_STATES)
	make clean

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache build dist *.egg-info

lint:
	@$(PYTHON) -m flake8 . --exclude=.git,.venv,venv,__pycache__,.mypy_cache,.pytest_cache,build,dist,mazegenerator-00001-py3-none-any
	@$(PYTHON) -m mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs \
		--exclude '(\.venv|venv|build|dist|mazegenerator-00001-py3-none-any)'

lint-strict:
	@$(PYTHON) -m flake8 . --exclude=.git,.venv,venv,__pycache__,.mypy_cache,.pytest_cache,build,dist,mazegenerator-00001-py3-none-any
	@$(PYTHON) -m mypy . --strict \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs \
		--exclude '(\.venv|venv|build|dist|mazegenerator-00001-py3-none-any)'