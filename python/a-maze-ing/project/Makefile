VENV = .venv
PY = $(VENV)/bin/python

MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports \
	--disallow-untyped-defs --check-untyped-defs

.PHONY: install run debug clean lint lint-strict build

install:
	python3 -m venv $(VENV)
	$(PY) -m pip install --quiet --no-cache-dir --upgrade pip
	$(PY) -m pip install --quiet --no-cache-dir flake8==7.4.1 mypy==2.4.1 build==1.6.1

run:
	$(PY) a_maze_ing.py config.txt

debug:
	$(PY) -m pdb a_maze_ing.py config.txt

clean:
	find . -path ./$(VENV) -prune -o -type d -name __pycache__ -exec rm -rf {} +
	rm -rf .mypy_cache build dist *.egg-info

lint:
	$(PY) -m flake8 .
	$(PY) -m mypy . $(MYPY_FLAGS)

lint-strict:
	$(PY) -m flake8 .
	$(PY) -m mypy . --strict

build:
	rm -rf dist
	$(PY) -m build
	cp dist/mazegen-*.whl dist/mazegen-*.tar.gz .