---
sidebar_position: 5
title: "Makefile: limpar, empacotar e o arquivo completo"
---

# Makefile: limpar, empacotar e o arquivo completo

O Python e as ferramentas criam arquivos sozinhos, que não fazem parte da entrega. E o enunciado
exige o gerador num arquivo que outro projeto instala com `pip`, e na avaliação pede para
reconstruir esse arquivo a partir do código. Esta página escreve as duas regras que faltam no
`Makefile`: `clean`, que apaga esses arquivos, e `build`, que monta o pacote com um comando só.
No fim está o `Makefile` completo, com as regras desta página e das duas anteriores
([instalar e rodar](./02-makefile-instalar-e-rodar.md) e
[verificar](./03-makefile-limpar-verificar-empacotar.md)).

## `clean`

```makefile
clean:
	find . -path ./$(VENV) -prune -o -type d -name __pycache__ -exec rm -rf {} +
	rm -rf .mypy_cache build dist *.egg-info
```

Na primeira vez que um módulo é importado, o Python o traduz para um formato mais rápido de
carregar, o **bytecode**, e o guarda numa pasta `__pycache__` **ao lado do módulo**. O projeto
tem pastas dentro de pastas, então surge um `__pycache__` em `mazegen/`, outro em
`mazegen/entities/`, outro em `amazeing/domain/entities/`, e assim por diante. Um
`rm -rf __pycache__` apagaria só o da raiz.

O `find` procura em todas as pastas:

| Pedaço | Significado |
|---|---|
| `find .` | procura a partir da pasta atual, a raiz do projeto |
| `-path ./.venv -prune` | não entra no `.venv`: o ambiente virtual fica intacto |
| `-o` | "senão": o resto vale para tudo o que não é o `.venv` |
| `-type d -name __pycache__` | só pastas chamadas `__pycache__` |
| `-exec rm -rf {} +` | apaga as pastas encontradas: o `{}` é trocado pelos caminhos achados, e o `+` no fim junta todos eles num único `rm`, em vez de rodar um `rm` por pasta |

A segunda linha apaga o que as outras ferramentas deixam:

- `.mypy_cache`: o cache do mypy, que guarda o resultado da última verificação para a próxima
  ser mais rápida;
- `build`, `dist` e `*.egg-info`: as pastas de trabalho do empacotamento (a regra `build`,
  logo abaixo). O `*` quer dizer "qualquer texto": `*.egg-info` pega toda pasta cujo nome
  termina em `.egg-info`. Neste projeto só existe uma, a `mazegen.egg-info`, mas o nome dela
  muda se o pacote mudar de nome, e o `*` continua pegando.

Ficam o `.venv` e os arquivos de entrega da raiz, inclusive os dois arquivos do pacote.

## Os dois formatos do pacote

O arquivo do pacote precisa se chamar `mazegen-` seguido da versão e ficar na raiz do
repositório. O enunciado aceita dois formatos, os que o empacotamento padrão do Python gera:

- **wheel** (`.whl`): o pacote pronto para instalar; o `pip` só copia os arquivos para o lugar
  certo. Ex.: `mazegen-1.0.0-py3-none-any.whl`.
- **sdist** (*source distribution*, `.tar.gz`): um arquivo compactado com o código-fonte e a
  configuração do pacote; o `pip` monta o pacote antes de instalar.

O projeto entrega os dois, por escolha: um basta para o enunciado, e o outro sai do mesmo
comando sem custo.

## A regra `build`

```makefile
build:
	rm -rf dist
	$(PY) -m build
	cp dist/mazegen-*.whl dist/mazegen-*.tar.gz .
```

1. Apaga a pasta `dist/` antiga, para o `cp` copiar só os arquivos da versão atual.
2. `python -m build` lê o `pyproject.toml` ([próxima página](./04-pyproject.md)) e gera, em
   `dist/`, o `mazegen-1.0.0.tar.gz` e o `mazegen-1.0.0-py3-none-any.whl`.
3. Copia os dois para a raiz, onde o enunciado exige que o pacote fique. O `*` do nome casa com
   qualquer versão.

O build precisa do `README.md` e do `LICENSE.md`, que o `pyproject.toml` cita, e do gerador
completo. Por isso o `make build` só funciona a partir da [parte 9](../09-gerador/08-o-pacote.md),
quando o pacote fica pronto.

## Experimente

```bash
make -n clean build
```

```text
find . -path ./.venv -prune -o -type d -name __pycache__ -exec rm -rf {} +
rm -rf .mypy_cache build dist *.egg-info
rm -rf dist
.venv/bin/python -m build
cp dist/mazegen-*.whl dist/mazegen-*.tar.gz .
```

O `-n` só imprime os comandos, já com o `$(VENV)` e o `$(PY)` trocados pelos valores. O
`make clean` pode rodar de verdade a qualquer momento. Já o `make build` de verdade ainda falha,
porque o `pyproject.toml`, o `README.md`, o `LICENSE.md` e o gerador ainda não existem.

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
