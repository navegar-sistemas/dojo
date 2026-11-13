---
sidebar_position: 10
title: Conferir e instalar o pacote
---

# Conferir e instalar o pacote

O pacote gerado por `make build` ([página anterior](./08-o-pacote.md)) só cumpre o enunciado se
levar o código e a documentação e se funcionar **sozinho**: instalado com `pip` num lugar onde a
pasta `mazegen/` do repositório não existe, como vai acontecer no projeto futuro que o reutilizar.
Esta página confere o conteúdo do pacote, faz essa instalação e mostra por que os dois arquivos do
pacote ficam guardados no repositório.

## O que vai dentro

O wheel leva os quatro pacotes listados na chave `packages` da seção `[tool.setuptools]` do
`pyproject.toml` (`mazegen`, `mazegen.entities`, `mazegen.value_objects` e `mazegen.services`) e
os dados do pacote, na pasta `mazegen-1.0.0.dist-info/`. O wheel é um arquivo zip, e o módulo
`zipfile` do Python lista o que há dentro dele. Na raiz do projeto:

```bash
.venv/bin/python -c 'import zipfile; print("\n".join(zipfile.ZipFile("mazegen-1.0.0-py3-none-any.whl").namelist()))'
```

`zipfile.ZipFile(...)` abre o arquivo zip, `namelist()` devolve a lista dos nomes dos arquivos de
dentro, e `"\n".join(...)` os junta, um por linha. (O comando
`.venv/bin/python -m zipfile -l mazegen-1.0.0-py3-none-any.whl` mostra a mesma lista com a data e
o tamanho de cada arquivo.)

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

- A documentação do módulo vai dentro do código, na docstring de `mazegen/__init__.py`
  ([página 6](./05-documentacao-do-modulo.md)). É assim que o pacote cumpre "código e
  documentação num único arquivo".
- `py.typed` é um arquivo vazio que avisa ao `mypy` de quem instala o pacote que ele tem anotações
  de tipo, para o `mypy` conferi-las.
- `METADATA` começa com nome, versão e licença, seguidos do README como descrição longa. As
  primeiras linhas:

```text
Metadata-Version: 2.4
Name: mazegen
Version: 1.0.0
Summary: Maze generator: perfect mazes or Pac-Man boards with a "42" pattern
Author: macoelho
License-Expression: MIT
Requires-Python: >=3.10
```

O sdist leva os mesmos módulos, mais o `pyproject.toml`, o `README.md`, o `LICENSE.md` e os
arquivos que o `setuptools` gera (`PKG-INFO`, `setup.cfg`, `mazegen.egg-info/`).

Nenhum dos dois leva `amazeing/` nem `a_maze_ing.py`: a aplicação (o arquivo de configuração, o
desenho, o menu) não é reutilizável e fica fora do pacote.

## Um ambiente novo

Crie um ambiente virtual novo e rode o Python numa pasta que não tenha a pasta `mazegen/`; assim
o `import` só pode vir do pacote instalado. Comece na raiz do projeto, onde está o arquivo
`mazegen-1.0.0-py3-none-any.whl`:

```bash
python3 -m venv /tmp/mazegen-test
/tmp/mazegen-test/bin/python -m pip install mazegen-1.0.0-py3-none-any.whl
cd /tmp
/tmp/mazegen-test/bin/python -c 'import mazegen; print(mazegen.__file__)'
```

- a primeira linha cria o ambiente virtual em `/tmp/mazegen-test`, com o `python3` do sistema
  (precisa ser 3.10 ou mais novo, veja abaixo);
- a segunda instala o wheel nele, com o `pip` desse ambiente. O nome do arquivo é relativo à pasta
  atual, por isso o comando roda na raiz do projeto;
- a terceira sai do projeto e entra em `/tmp`, uma pasta sem `mazegen/` dentro;
- a quarta imprime de que arquivo o `mazegen` foi importado (`__file__`).

O caminho impresso termina em `site-packages/mazegen/__init__.py`. `site-packages` é a pasta onde
o `pip` instala os pacotes: o import veio do pacote instalado.

Ainda em `/tmp`, rode o exemplo da docstring ([página 6](./05-documentacao-do-modulo.md)) com o
Python desse ambiente. Depois, `cd -` volta para a pasta anterior (a raiz do projeto), e o
`rm -rf` apaga o ambiente de teste:

```bash
/tmp/mazegen-test/bin/python - <<'EOF'
from mazegen import MazeGenerator

gen = MazeGenerator(width=20, height=15, seed=42)
gen.generate()
walls = gen.grid[0][0]
print("north wall of (0, 0) closed:", bool(walls & 1))
print(len(gen.pattern), "cells draw the 42")
print(gen.solution)
EOF
cd -
rm -rf /tmp/mazegen-test
```

```text
north wall of (0, 0) closed: True
18 cells draw the 42
SSEEESSSSSENNNESSSSEESSSSEESSEEEENNESSEEEEE
```

O `cd -` também imprime o caminho da pasta para onde voltou, que muda de computador para
computador e por isso não aparece acima.

Um `python3` anterior ao 3.10 recusa a instalação, por causa do `requires-python = ">=3.10"` do
`pyproject.toml` (o enunciado exige Python 3.10 ou mais novo):

```text
ERROR: Package 'mazegen' requires a different Python: 3.9.6 not in '>=3.10'
```

## Guardar os dois arquivos no repositório

O `.gitignore` é a lista de arquivos que o git não guarda no repositório
([parte 3](../03-ambiente/05-flake8-e-gitignore.md)). Ele ignora as pastas `build/` e `dist/`,
geradas a cada empacotamento, mas **não** os dois arquivos copiados para a raiz: eles fazem parte
da entrega. Depois de qualquer mudança em `mazegen/`, rode `make build` de novo para o pacote da
raiz continuar igual ao código.
