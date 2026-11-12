---
sidebar_position: 8
title: "make build: o wheel e o sdist"
---

# make build: o wheel e o sdist

## O que o subject pede

- todo o módulo reutilizável, código e documentação, num **único arquivo** instalável com
  `pip`;
- o nome começa com `mazegen-`, e o arquivo fica na **raiz** do repositório;
- `.whl` e `.tar.gz` são aceitos, "conforme gerados pelo build padrão de um pacote Python";
- o repositório tem tudo o que é preciso para **reconstruir** o pacote: na avaliação, ele é
  refeito a partir dos fontes, num virtualenv.

## A regra `build`

A regra do `Makefile` (parte 3):

```makefile
build:
	rm -rf dist
	$(PY) -m build
	cp dist/mazegen-*.whl dist/mazegen-*.tar.gz .
```

1. apaga `dist/`, para que o `cp` copie só a versão recém-gerada;
2. roda `python -m build`, a ferramenta padrão de empacotamento, instalada no `.venv` pelo
   `make install`;
3. copia os dois arquivos gerados para a raiz.

Com o `README.md` e o `LICENSE.md` no lugar:

```bash
make build
```

O começo e o fim da saída:

```text
rm -rf dist
.venv/bin/python -m build
* Creating isolated environment: venv+pip...
* Installing packages in isolated environment:
  - setuptools>=77
...
Successfully built mazegen-1.0.0.tar.gz and mazegen-1.0.0-py3-none-any.whl
cp dist/mazegen-*.whl dist/mazegen-*.tar.gz .
```

O `build` cria um ambiente isolado, instala nele o `setuptools` pedido em `[build-system]` do
`pyproject.toml` (por isso precisa de rede) e gera primeiro o sdist, depois o wheel a partir
dele. Nenhuma linha da saída contém `warning`.

## Dois formatos

| Arquivo | O que é |
|---|---|
| `mazegen-1.0.0.tar.gz` | o **sdist** (*source distribution*): os fontes e os arquivos de build. O `pip` constrói o pacote na hora de instalar |
| `mazegen-1.0.0-py3-none-any.whl` | o **wheel**: um zip pronto para instalar, sem passo de build |

O nome do wheel diz onde ele roda: `py3` (qualquer Python 3), `none` (nenhuma extensão em C),
`any` (qualquer sistema operacional). O `mazegen` é Python puro e só usa a biblioteca padrão.

## O que vai dentro

O wheel leva os quatro pacotes listados em `[tool.setuptools]` e os metadados:

```text
mazegen/__init__.py
mazegen/errors.py
mazegen/generator.py
mazegen/py.typed
mazegen/entities/__init__.py
mazegen/entities/maze.py
mazegen/services/__init__.py
mazegen/services/braider.py
mazegen/services/carver.py
mazegen/services/solver.py
mazegen/value_objects/__init__.py
mazegen/value_objects/cell.py
mazegen/value_objects/direction.py
mazegen/value_objects/pattern42.py
mazegen-1.0.0.dist-info/licenses/LICENSE.md
mazegen-1.0.0.dist-info/METADATA
mazegen-1.0.0.dist-info/WHEEL
mazegen-1.0.0.dist-info/top_level.txt
mazegen-1.0.0.dist-info/RECORD
```

- A documentação do módulo vai dentro do código, na docstring de `mazegen/__init__.py`.
- `py.typed` avisa ao `mypy` de quem instala que o pacote tem anotações de tipo.
- `METADATA` começa com nome, versão e licença, seguidos do README como descrição longa:

```text
Metadata-Version: 2.4
Name: mazegen
Version: 1.0.0
Summary: Maze generator: perfect mazes or Pac-Man boards with a "42" pattern
Author: macoelho
License-Expression: MIT
Requires-Python: >=3.10
```

O sdist leva os mesmos módulos, mais `pyproject.toml`, `README.md`, `LICENSE.md` e os arquivos
que o `setuptools` gera (`PKG-INFO`, `setup.cfg`, `mazegen.egg-info/`).

Nenhum dos dois leva `amazeing/` nem `a_maze_ing.py`: a aplicação não é reutilizável e fica fora
do pacote.

## Instalar num ambiente novo

Para ver o pacote funcionando longe dos fontes, num virtualenv novo e numa pasta sem `mazegen/`:

```bash
python3 -m venv /tmp/mazegen-test
/tmp/mazegen-test/bin/python -m pip install mazegen-1.0.0-py3-none-any.whl
cd /tmp && /tmp/mazegen-test/bin/python -c 'import mazegen; print(mazegen.__file__)'
```

O caminho impresso termina em `site-packages/mazegen/__init__.py`: o import veio do pacote
instalado. O exemplo da docstring, rodado nesse ambiente:

```text
north wall of (0, 0) closed: True
18 cells draw the 42
SSEEESSSSSENNNESSSSEESSSSEESSEEEENNESSEEEEE
```

Um `python3` anterior ao 3.10 recusa a instalação, por causa do `requires-python` do
`pyproject.toml`:

```text
ERROR: Package 'mazegen' requires a different Python: 3.9.6 not in '>=3.10'
```

## Versionar os dois arquivos

O `.gitignore` ignora `build/` e `dist/`, mas **não** os dois arquivos copiados para a raiz:
eles são parte da entrega. Depois de qualquer mudança em `mazegen/`, rode `make build` de novo
para que o pacote da raiz corresponda ao código.
