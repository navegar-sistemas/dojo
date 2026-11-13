---
sidebar_position: 11
title: Rodar com o Poetry
---

# Rodar com o Poetry

O caminho do Poetry: nenhum ambiente criado à mão, nenhuma ativação. O Poetry lê o
`pyproject.toml`, cria o ambiente do projeto e instala nele. Os comandos continuam na pasta
`ex1`, e nenhum ambiente pode estar ativado (com um ambiente ativado, o Poetry instalaria nele;
[pip e Poetry](./02-pip-e-poetry.md)). O enunciado escreve `poetry install`; aqui o Poetry é
chamado pelo caminho, `../.venv/bin/poetry` ([As ferramentas](../01-ambiente/03-as-ferramentas.md)).

## Conferir o pyproject.toml

```bash
../.venv/bin/poetry check
```

```text
All set!
```

"Tudo pronto": o arquivo está bem escrito.

## Instalar

```bash
../.venv/bin/poetry install
```

```text
Creating virtualenv loading-BeTxmVon-py3.15 in /…/pypoetry/virtualenvs
Updating dependencies
Resolving dependencies...

Package operations: 12 installs, 0 updates, 0 removals

  - Installing numpy (2.5.4)
  - Installing tzdata (2026.6)
  - Installing fonttools (4.68.0)
  - Installing cycler (0.12.1)
  - Installing kiwisolver (1.5.1)
  - Installing contourpy (1.4.0)
  - Installing packaging (26.3)
  - Installing pillow (13.0.0)
  - Installing pyparsing (3.3.3)
  - Installing python-dateutil (4.0.0)
  - Installing matplotlib (3.11.2)
  - Installing pandas (3.1.1)

Writing lock file
```

Linha por linha:

- `Creating virtualenv loading-BeTxmVon-py3.15 in /…/pypoetry/virtualenvs`: o Poetry criou um
  ambiente virtual para o projeto. O nome junta o `name` do `pyproject.toml` (`loading`), um
  código calculado a partir do caminho da pasta do projeto (outro em cada máquina) e a versão do
  Python. A pasta fica no **cache** do Poetry, uma pasta de dados da própria ferramenta, fora do
  projeto: no Linux, `~/.cache/pypoetry/virtualenvs`; no macOS,
  `~/Library/Caches/pypoetry/virtualenvs` (o `~` é a pasta pessoal);
- `Updating dependencies` e `Resolving dependencies...`: ainda não havia `poetry.lock`, e o Poetry
  calculou as versões de tudo;
- `Package operations: 12 installs`: os mesmos 12 pacotes, nas mesmas versões, que o pip
  instalou na [página anterior](./10-rodar-com-pip.md), agora no ambiente do Poetry;
- `Writing lock file`: o Poetry gravou o `poetry.lock`.

As versões e a ordem das linhas `Installing` podem ser outras na sua máquina: o Poetry instala
vários pacotes ao mesmo tempo.

```bash
ls
```

```text
loading.py
matrix_analysis.png
matrix_env
poetry.lock
pyproject.toml
requirements.txt
```

O `poetry.lock` apareceu. O ambiente do Poetry não aparece aqui: ele está no cache. O
`matrix_env` é o ambiente do pip, da página anterior; o Poetry não mexe nele.

## Rodar

`poetry run` roda um comando dentro do ambiente do projeto, sem ativá-lo:

```bash
../.venv/bin/poetry run python loading.py
```

```text

LOADING STATUS: Loading programs...

Checking dependencies:
[OK] pandas (3.1.1) - Data manipulation ready
[OK] numpy (2.5.4) - Numerical computation ready
[OK] matplotlib (3.11.2) - Visualization ready

Analyzing Matrix data...
Processing 1000 data points...
Generating visualization...

Analysis complete!
Results saved to: matrix_analysis.png

Environment: /…/pypoetry/virtualenvs/loading-BeTxmVon-py3.15
```

As linhas do enunciado são as mesmas da execução pelo pip; a diferença está na última. Pelo pip, o
ambiente era o `matrix_env`, dentro da pasta `ex1`; pelo Poetry, é o ambiente que ele criou na
pasta de cache dele, o mesmo que o `Creating virtualenv` anunciou. O `matrix_analysis.png` foi gravado de novo, igual ao anterior: a
semente fixa gera os mesmos dados ([A análise](./07-a-analise.md#o-numpy-gera-os-dados)).

## Instalar de novo

Com o `poetry.lock` pronto, um novo `poetry install` não calcula nada: lê as versões do arquivo.

```bash
../.venv/bin/poetry install
```

```text
Installing dependencies from lock file

No dependencies to install or update
```

"Instalando as dependências do arquivo de trava; nenhuma dependência a instalar ou atualizar."
Numa máquina nova, com o mesmo `poetry.lock`, este comando instalaria exatamente as versões
travadas, mesmo que existam outras mais novas.

## Onde está o ambiente e o que tem nele

```bash
../.venv/bin/poetry env info --path
```

```text
/…/pypoetry/virtualenvs/loading-BeTxmVon-py3.15
```

```bash
../.venv/bin/poetry show --top-level
```

```text
matplotlib      3.11.2 Python plotting package
numpy           2.5.4  Fundamental package for array computing in Python
pandas          3.1.1  Powerful data structures for data analysis, time ser...
```

`poetry show` lista os pacotes do projeto; com `--top-level` ("primeiro nível"), só as
dependências declaradas no `pyproject.toml`, sem as dependências delas. A descrição longa é
cortada com `...`.

## Dentro do poetry.lock

O `poetry.lock` é um arquivo TOML com uma tabela por pacote. O `grep` procura um texto num arquivo
e mostra as linhas encontradas; com `-A4`, mostra também as quatro linhas seguintes:

```bash
grep -A4 '^name = "numpy"' poetry.lock
```

```text
name = "numpy"
version = "2.2.6"
description = "Fundamental package for array computing in Python"
optional = false
python-versions = ">=3.10"
--
name = "numpy"
version = "2.4.6"
description = "Fundamental package for array computing in Python"
optional = false
python-versions = ">=3.11"
--
name = "numpy"
version = "2.5.4"
description = "Fundamental package for array computing in Python"
optional = false
python-versions = ">=3.12"
```

O `^` no começo do texto procurado quer dizer "no começo da linha". O arquivo tem **três**
versões do numpy: como o `pyproject.toml` aceita do Python 3.10 em diante
(`requires-python = ">=3.10"`), o Poetry resolveu as dependências para cada faixa de versões do
Python e travou uma versão do numpy para cada uma: a 2.2.6 para o 3.10, a 2.4.6 para o 3.11 e a
2.5.4 do 3.12 em diante. Mais abaixo, em cada tabela, uma linha `markers` diz para qual Python
ela vale. O `requirements.txt` não guarda nada disso.

## Em outras versões do Python

No Python 3.14, tudo sai igual, com `py3.14` no nome do ambiente. Com o Poetry instalado num
`.venv` criado pelo Python 3.10, o ambiente do projeto se chama `loading-…-py3.10`, o Poetry
instala 14 pacotes (os mesmos do pip no 3.10) e as linhas `[OK]` mostram pandas 2.3.3, numpy
2.2.6 e matplotlib 3.10.9. No meio da saída do `poetry install` aparece um aviso longo, que
começa com o caminho do Poetry e continua com `RuntimeWarning: Skip installing
numpy/distutils/__pycache__/conv_template.cpython-310.pyc from numpy. Installing files in a
__pycache__ directory poses a security risk.`: o pacote do numpy 2.2.6 traz um arquivo de cache
que não deveria trazer, e o Poetry pula esse arquivo. O aviso não impede nada, e o numpy funciona. O `poetry.lock` sai igual: ele é
calculado para todas as versões de Python aceitas, qualquer que seja a que está rodando.
