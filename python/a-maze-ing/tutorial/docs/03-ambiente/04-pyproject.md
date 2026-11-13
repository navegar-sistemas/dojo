---
sidebar_position: 6
title: O pyproject.toml
---

# O `pyproject.toml`

O `make build` (a regra do `Makefile` que monta o pacote do gerador,
[escrita na página anterior](./09-makefile-empacotar.md)) precisa saber o nome do pacote, a
versão, quais pastas entram nele e quem o escreveu. O mypy precisa saber para qual versão do
Python conferir o código. As duas ferramentas leem essas respostas de um mesmo arquivo na raiz,
o `pyproject.toml`.

## O formato TOML

O `pyproject.toml` é o arquivo de configuração padrão de um projeto Python. Ele é escrito em
**TOML**, um formato de texto simples:

- `chave = valor` define uma opção; textos vão entre aspas, listas entre colchetes;
- uma linha `[nome]` abre uma **seção**, e as opções abaixo dela pertencem a ela;
- seções com ponto no nome, como `[tool.mypy]`, são a configuração de uma ferramenta: o mypy lê
  só a `[tool.mypy]`;
- `{ chave = valor }` é uma **tabela em linha** (*inline table*): um grupo pequeno de opções
  escrito numa linha só, entre chaves, como um dicionário do Python. `[{ name = "macoelho" }]`
  é uma lista com uma tabela dentro, que equivale ao Python `[{"name": "macoelho"}]`.

## `[build-system]`: quem monta o pacote

```toml
[build-system]
requires = ["setuptools>=77"]
build-backend = "setuptools.build_meta"
```

O `build`, instalado no `.venv`, não monta o pacote sozinho. Ele cria um ambiente temporário,
instala ali o que `requires` pede, e passa o trabalho ao **backend**: o programa que de fato
junta os arquivos no `.whl` e no `.tar.gz`. O backend escolhido é o setuptools, o mais comum.

`>=77` pede a versão 77 ou mais nova, a primeira que aceita a licença no formato novo,
`license = "MIT"` (abaixo). Com o formato antigo, `license = {text = "MIT"}`, o build imprime um
aviso de formato obsoleto. Exigir um build sem nenhum aviso é uma escolha do projeto: um aviso
ignorado hoje vira um erro numa versão futura.

## `[project]`: a identidade do pacote

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
| `name` | o enunciado exige um pacote chamado `mazegen-...`; o arquivo gerado se chama `mazegen-1.0.0-py3-none-any.whl` |
| `version` | o `1.0.0` do nome do arquivo; é o único lugar do projeto onde a versão aparece |
| `description` | a frase curta que o `pip show mazegen` exibe; o `\"` é uma aspa dentro do texto |
| `readme` | o `README.md` vira a descrição longa do pacote |
| `requires-python` | o enunciado exige Python 3.10 ou mais novo; um `pip` de Python 3.9 recusa instalar o pacote |
| `license`, `license-files` | a licença MIT e o arquivo com o texto dela, que vai junto no pacote |
| `authors` | quem escreveu o pacote |

A licença existe porque o enunciado exige um `LICENSE.md` que permita a outros projetos
reutilizar o gerador. A MIT, que permite usar, copiar e modificar desde que o aviso de licença
vá junto, é a escolha do projeto ([parte 9](../09-gerador/06-a-licenca.md)).

`macoelho` é o login (o nome de usuário) de quem escreveu esta implementação. **Troque pelo
seu login.**
Com mais de um autor, um `{ name = "..." }` para cada, separados por vírgula. Os mesmos logins
aparecem na primeira linha do `README.md` e no `LICENSE.md`.

## `[tool.setuptools]`: o que entra no pacote

```toml
[tool.setuptools]
packages = ["mazegen", "mazegen.entities", "mazegen.value_objects", "mazegen.services"]
```

A lista diz **exatamente** quais pastas vão para o pacote. O nome com ponto aponta uma subpasta:
`mazegen.entities` é a pasta `mazegen/entities/`.

A lista não inclui subpastas sozinha. Com `packages = ["mazegen"]` apenas, o pacote levaria só
os arquivos soltos de `mazegen/` e deixaria de fora `entities/`, `value_objects/` e `services/`.
Quem instalasse o pacote veria o `import mazegen` quebrar, porque o gerador não acharia a classe
`Maze`.

O que não está na lista fica fora: `amazeing/` e `a_maze_ing.py` são a aplicação, não a
biblioteca reutilizável (a [parte 2](../02-arquitetura/02-dois-pacotes.md) explica essa
divisão).

## `[tool.setuptools.package-data]`: um arquivo que não é `.py`

```toml
[tool.setuptools.package-data]
mazegen = ["py.typed"]
```

O setuptools só copia arquivos `.py` para o pacote. Esta linha acrescenta o `mazegen/py.typed`,
um arquivo vazio que avisa ao mypy de outros projetos que o `mazegen` tem anotações de tipo. Ele
é criado na página [Os pacotes do mazegen](./07-pacotes-do-mazegen.md).

## `[tool.mypy]`: para qual Python conferir

```toml
[tool.mypy]
python_version = "3.10"
exclude = ["^\\.venv/", "^build/", "^dist/"]
```

`python_version = "3.10"` faz o mypy conferir o código **como se** ele fosse rodar no Python
3.10, mesmo que o `.venv` tenha um Python mais novo. O enunciado exige 3.10 ou mais novo, então
o código não pode usar nada que só exista depois. Um exemplo de recurso que só existe a partir
do 3.11:

```python
from typing import Self
```

Com `python_version = "3.10"`, o mypy acusa:

```text
error: Module "typing" has no attribute "Self"  [attr-defined]
```

Sem essa linha, o mypy aceitaria o `Self` num `.venv` com Python 3.11 ou mais novo, e o programa
quebraria no Python 3.10 do avaliador.

`exclude` lista as pastas que o mypy não deve conferir: o `.venv` (o código das ferramentas
instaladas, que não é do projeto) e as pastas temporárias do build. Cada item é uma **expressão
regular**, um padrão de texto: `^` quer dizer "no começo do caminho", e `\.` quer dizer "um
ponto de verdade" (um `.` sozinho casaria com qualquer caractere).

No arquivo, o padrão aparece com **duas** barras, `"^\\.venv/"`. É que, dentro de aspas no
TOML, a barra invertida já é um caractere especial: é ela que escreve uma aspa dentro do texto,
como o `\"` da `description` acima. Para o texto lido conter uma barra, o arquivo precisa de
duas. O TOML entrega ao mypy `^\.venv/`, com uma barra só, e é esse o padrão que o mypy usa.

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
