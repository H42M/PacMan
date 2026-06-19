VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(PYTHON) -m pip
MAIN = pac-man.py
CONFIG = config/config.json
DEPENDENCIES = requirements.txt

.PHONY: install run debug clean fclean re lint lint-strict package package-clean package-zip

$(PYTHON):
	python3 -m venv $(VENV)

install: $(PYTHON)
	$(PIP) install --upgrade pip
	$(PIP) install -r $(DEPENDENCIES)

run: $(PYTHON)
	$(PYTHON) $(MAIN) $(CONFIG)

debug: $(PYTHON)
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

package: install
	$(PYTHON) -m PyInstaller --clean --noconfirm pacman.spec

package-clean:
	rm -rf build dist

package-zip: package
	cd dist && zip -r PacMan-linux.zip PacMan

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache build dist *.egg-info

fclean: clean
	rm -rf $(VENV)

re: fclean install

lint: $(PYTHON)
	@$(PYTHON) -m flake8 . --exclude=.git,.venv,venv,__pycache__,.mypy_cache,.pytest_cache,build,dist,mazegenerator-00001-py3-none-any
	@$(PYTHON) -m mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs \
		--exclude '(\.venv|venv|build|dist|mazegenerator-00001-py3-none-any)'

lint-strict: $(PYTHON)
	@$(PYTHON) -m flake8 . --exclude=.git,.venv,venv,__pycache__,.mypy_cache,.pytest_cache,build,dist,mazegenerator-00001-py3-none-any
	@$(PYTHON) -m mypy . --strict \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs \
		--exclude '(\.venv|venv|build|dist|mazegenerator-00001-py3-none-any)'