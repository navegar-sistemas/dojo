VENV = .venv
PY = $(VENV)/bin/python

MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports \
	--disallow-untyped-defs --check-untyped-defs

# make run ETAPA=03 roda só os cenários de features/03-*.feature.
ALVO = $(if $(ETAPA),cenarios/test_$(ETAPA)_*.py)

.PHONY: install run test debug clean lint lint-strict faltantes manuais

install:
	@python3 -c 'import sys; sys.exit(sys.version_info < (3, 10))' || \
		{ echo "o python3 do PATH é anterior ao 3.10" >&2; exit 1; }
	python3 -m venv $(VENV)
	$(PY) -m pip install --quiet --no-cache-dir --upgrade pip
	$(PY) -m pip install --quiet --no-cache-dir -r requirements.txt

run:
	$(PY) -m pytest $(ALVO)

test: run

debug:
	$(PY) -m pdb -m pytest $(ALVO)

clean:
	find . -path ./$(VENV) -prune -o -type d -name __pycache__ -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache

lint:
	$(PY) -m flake8 .
	$(PY) -m mypy . $(MYPY_FLAGS)

lint-strict:
	$(PY) -m flake8 .
	$(PY) -m mypy . --strict

faltantes:
	$(PY) -m suporte.faltantes

manuais:
	$(PY) -m pytest -m manual --collect-only -q
