---
sidebar_position: 4
title: O pyproject.toml
---

# O `pyproject.toml`

## O que é

O arquivo de configuração padrão de um projeto Python, no formato TOML. Ele diz duas coisas:
como empacotar o `mazegen` (lido pelo `python -m build`) e como o mypy deve se comportar (lido
pelo `mypy`).

## `[build-system]`

```toml
[build-system]
requires = ["setuptools>=77"]
build-backend = "setuptools.build_meta"
```

O `build` não empacota sozinho: ele cria um ambiente temporário, instala o que `requires` pede e
chama o `build-backend`. O backend escolhido é o setuptools, o mais comum.

A versão mínima 77 é a que aceita a licença no formato novo, `license = "MIT"` (abaixo). Com o
formato antigo, `license = {text = "MIT"}`, o build imprime um aviso de formato obsoleto, e o
build tem de sair sem nenhum aviso.

## `[project]`

```toml
[project]
name = "mazegen"
version = "1.0.0"
description = "Maze generator: perfect mazes or Pac-Man boards with a \"42\" pattern"
readme = "README.md"
requires-python = ">=3.10"
license = "MIT"
license-files = ["LICENSE.md"]
authors = [{ name = "macoelho" }]
```

| Campo | Para quê |
|---|---|
| `name` | o subject exige um pacote `mazegen-*`; o arquivo gerado se chama `mazegen-1.0.0-py3-none-any.whl` |
| `version` | o `1.0.0` do nome do arquivo; é o único lugar onde a versão aparece |
| `description` | a frase curta que o `pip show mazegen` exibe |
| `readme` | o `README.md` vira a descrição longa do pacote |
| `requires-python` | um `pip` de Python 3.9 recusa instalar o wheel |
| `license`, `license-files` | a licença MIT e o arquivo dela, que vai junto no wheel |
| `authors` | quem escreveu o pacote |

`macoelho` é o login da intra 42 de quem escreveu esta implementação. **Troque pelo seu login.**
Com mais de um autor, um `{ name = "..." }` para cada, separados por vírgula. Os mesmos logins
aparecem na primeira linha do `README.md` e no `LICENSE.md`.

## `[tool.setuptools]`

```toml
[tool.setuptools]
packages = ["mazegen", "mazegen.entities", "mazegen.value_objects", "mazegen.services"]
```

A lista diz **exatamente** quais pacotes vão para o wheel. Ela não é recursiva: cada subpasta
com código precisa aparecer. Com `packages = ["mazegen"]` sozinho, o wheel levaria só os
arquivos de `mazegen/` e deixaria de fora `entities/`, `value_objects/` e `services/`; o
`import mazegen` de quem instalasse o pacote quebraria ao procurar `Maze`.

O que não está na lista fica fora: `amazeing/` e `a_maze_ing.py` são a aplicação, não a
biblioteca reutilizável.

## `[tool.setuptools.package-data]`

```toml
[tool.setuptools.package-data]
mazegen = ["py.typed"]
```

O setuptools só copia arquivos `.py` por padrão. Esta linha inclui o `mazegen/py.typed`, o
marcador vazio que avisa ao mypy que o pacote tem anotações de tipo (ele é criado na página
"Os pacotes do mazegen").

## `[tool.mypy]`

```toml
[tool.mypy]
python_version = "3.10"
exclude = ["^\\.venv/", "^build/", "^dist/"]
```

`python_version = "3.10"` faz o mypy conferir o código **como se** rodasse no Python 3.10, mesmo
que o `.venv` tenha um Python mais novo. O subject exige 3.10 ou posterior, então o código não
pode usar nada que só exista depois. Um recurso do 3.11, por exemplo:

```python
from typing import Self
```

```text
error: Module "typing" has no attribute "Self"  [attr-defined]
```

Sem essa linha, o mypy aceitaria o `Self` num `.venv` com Python 3.11 ou mais novo, e o programa
quebraria no 3.10 do avaliador.

`exclude` usa expressões regulares: o mypy não entra no `.venv` (as ferramentas instaladas), nem
nas pastas temporárias do build.

## O arquivo completo

```toml title="pyproject.toml"
[build-system]
requires = ["setuptools>=77"]
build-backend = "setuptools.build_meta"

[project]
name = "mazegen"
version = "1.0.0"
description = "Maze generator: perfect mazes or Pac-Man boards with a \"42\" pattern"
readme = "README.md"
requires-python = ">=3.10"
license = "MIT"
license-files = ["LICENSE.md"]
authors = [{ name = "macoelho" }]

[tool.setuptools]
packages = ["mazegen", "mazegen.entities", "mazegen.value_objects", "mazegen.services"]

[tool.setuptools.package-data]
mazegen = ["py.typed"]

[tool.mypy]
python_version = "3.10"
exclude = ["^\\.venv/", "^build/", "^dist/"]
```
