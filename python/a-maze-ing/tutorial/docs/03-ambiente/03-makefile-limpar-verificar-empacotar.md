---
sidebar_position: 3
title: "Makefile: limpar, verificar e empacotar"
---

# Makefile: limpar, verificar e empacotar

## `clean`

```makefile
clean:
	find . -path ./$(VENV) -prune -o -type d -name __pycache__ -exec rm -rf {} +
	rm -rf .mypy_cache build dist *.egg-info
```

O Python grava o bytecode de cada módulo numa pasta `__pycache__` **ao lado do módulo**. O
projeto tem pacotes dentro de pacotes, então há um `__pycache__` em `mazegen/`, outro em
`mazegen/entities/`, outro em `amazeing/domain/entities/`, e assim por diante. Um
`rm -rf __pycache__` apagaria só o da raiz.

O `find` percorre a árvore inteira:

| Pedaço | Significado |
|---|---|
| `find .` | a partir da raiz do projeto |
| `-path ./.venv -prune` | não entra no `.venv`: o ambiente virtual fica intacto |
| `-o` | "senão", para tudo o que não é o `.venv` |
| `-type d -name __pycache__` | pastas chamadas `__pycache__` |
| `-exec rm -rf {} +` | apaga as pastas encontradas, várias por chamada do `rm` |

A segunda linha apaga o cache do mypy e o que o empacotamento deixa: `build/`, `dist/` e
`mazegen.egg-info/`. Ficam o `.venv` e os arquivos de entrega da raiz, inclusive o `.whl` e o
`.tar.gz`.

## `lint`

```makefile
MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports \
	--disallow-untyped-defs --check-untyped-defs
```

```makefile
lint:
	$(PY) -m flake8 .
	$(PY) -m mypy . $(MYPY_FLAGS)
```

São os dois comandos do subject, com as flags exatas. As flags ficam numa variável porque a
linha não caberia no editor; a `\` no fim da primeira linha continua a variável na linha de
baixo. Na hora de rodar, o `make` monta tudo numa linha só.

| Flag | Efeito |
|---|---|
| `--warn-return-any` | acusa função com tipo de retorno declarado que devolve um valor `Any` |
| `--warn-unused-ignores` | acusa um `# type: ignore` que não ignora nada |
| `--ignore-missing-imports` | não acusa biblioteca de terceiros sem anotações de tipo |
| `--disallow-untyped-defs` | acusa função ou método sem anotação de tipo |
| `--check-untyped-defs` | confere também o corpo de funções sem anotação |

`flake8 .` confere o estilo (PEP 8) de todo o projeto; o que fica de fora está no `.flake8`.

## `lint-strict`

```makefile
lint-strict:
	$(PY) -m flake8 .
	$(PY) -m mypy . --strict
```

`--strict` liga quase todas as verificações do mypy, entre elas as do `lint`. O subject a deixa
opcional e "fortemente recomendada". O projeto passa nas duas regras, sem nenhum
`# type: ignore` nem `# noqa`.

## `build`

```makefile
build:
	rm -rf dist
	$(PY) -m build
	cp dist/mazegen-*.whl dist/mazegen-*.tar.gz .
```

1. Apaga o `dist/` antigo, para o `cp` copiar só a versão atual.
2. `python -m build` lê o `pyproject.toml` e gera, em `dist/`, o código-fonte empacotado
   (`mazegen-1.0.0.tar.gz`) e o wheel (`mazegen-1.0.0-py3-none-any.whl`).
3. Copia os dois para a raiz, porque o subject exige o arquivo do pacote na raiz do
   repositório.

O build exige o `README.md` e o `LICENSE.md`, que o `pyproject.toml` cita, e o gerador
completo. Por isso o `make build` só roda a partir da parte 9, quando o pacote fica pronto.

## Experimente

```bash
make -n lint lint-strict
```

```text
.venv/bin/python -m flake8 .
.venv/bin/python -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
.venv/bin/python -m flake8 .
.venv/bin/python -m mypy . --strict
```

## O arquivo completo

As linhas de comando começam com TAB. Ao copiar, confira se o editor não as trocou por
espaços.

```makefile title="Makefile"
VENV = .venv
PY = $(VENV)/bin/python

MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports \
	--disallow-untyped-defs --check-untyped-defs

.PHONY: install run debug clean lint lint-strict build

install:
	python3 -m venv $(VENV)
	$(PY) -m pip install --quiet --no-cache-dir --upgrade pip
	$(PY) -m pip install --quiet flake8==7.4.1 mypy==2.4.1 build==1.6.1

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
```
