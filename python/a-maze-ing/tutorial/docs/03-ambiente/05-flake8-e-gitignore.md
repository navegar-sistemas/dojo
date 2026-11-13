---
sidebar_position: 7
title: O .flake8 e o .gitignore
---

# O `.flake8` e o `.gitignore`

Três pastas da raiz não são código do projeto: o `.venv`, com as ferramentas instaladas, e as
pastas temporárias `build` e `dist`, que o empacotamento cria. O flake8 não deve conferi-las, e o
git não deve guardá-las. Esta página escreve os dois arquivos que dizem isso.

## `.flake8`: o que o flake8 pula

O flake8 (a ferramenta que confere o estilo do código, explicada na
[página do lint](./03-makefile-limpar-verificar-empacotar.md)) lê a sua configuração de um
arquivo chamado `.flake8`, na raiz. O formato é o **INI**: uma seção entre colchetes e opções
`chave = valor` abaixo dela. O projeto só precisa dizer o que **não** conferir:

```ini
[flake8]
extend-exclude = .venv,build,dist
```

- `.venv`: o código das ferramentas instaladas não é do projeto, e o flake8 acusaria milhares de
  linhas que ninguém aqui escreveu.
- `build`, `dist`: cópias temporárias do código, feitas pelo `make build`.

### `extend-exclude`, não `exclude`

O flake8 já pula, por conta própria, algumas pastas como `.git` e `__pycache__`. A opção
`exclude` **substituiria** essa lista, e o `.git` voltaria a ser conferido. `extend-exclude`
**acrescenta** as três pastas à lista que já existe.

### Nenhuma regra desligada

O arquivo não desliga nenhuma regra e não muda o limite de linha, que fica no padrão de 79
caracteres. O enunciado exige que o código siga o padrão do flake8, e afrouxar a configuração
seria fugir dele.

Pelo mesmo motivo, o código não usa `# noqa`, o comentário que manda o flake8 ignorar uma linha.
Uma linha longa demais se resolve pondo a expressão entre parênteses: dentro deles, o Python
deixa a expressão continuar na linha de baixo. Por exemplo, a conta "o ponto `x,y` está dentro
de um retângulo de `largura` por `altura`?" quebrada em duas linhas:

```python
dentro = (0 <= x < largura
          and 0 <= y < altura)
```

Sem os parênteses, a primeira linha terminaria em `largura`, e o Python acusaria erro na segunda,
que começa com `and`.

### O arquivo completo

```ini title=".flake8"
[flake8]
extend-exclude = .venv,build,dist
```

## `.gitignore`: o que o git não guarda

O **git** é o programa que guarda o histórico do repositório: cada versão de cada arquivo. O
`.gitignore` é a lista de arquivos que ele deve fingir que não existem. O enunciado exige um
`.gitignore` que deixe de fora os **artefatos** do Python: arquivos que as ferramentas geram
sozinhas e que podem ser recriados a qualquer momento.

Cada linha é um padrão de nome:

| Padrão | O que é |
|---|---|
| `.venv/` | o ambiente virtual, recriado por `make install` |
| `__pycache__/` | o bytecode que o Python grava ao importar um módulo, em qualquer pasta |
| `*.pyc` | um arquivo de bytecode solto, fora de um `__pycache__` |
| `.mypy_cache/` | o cache do mypy |
| `build/`, `dist/` | as pastas de trabalho do `make build` |
| `*.egg-info/` | os dados que o setuptools anota sobre o pacote durante o build |
| `maze.txt` | o arquivo de saída do `config.txt`, regravado a cada execução |

O `*` casa com qualquer sequência de caracteres: `*.pyc` é "todo nome que termina em `.pyc`".
Um padrão terminado em `/` só casa com pastas, em qualquer nível da árvore.

### O que **não** está ali

`mazegen-1.0.0-py3-none-any.whl` e `mazegen-1.0.0.tar.gz` são gerados pelo `make build`, mas são
**entregáveis**: o enunciado exige o arquivo do pacote na raiz do repositório. Por isso o
`make build` os copia de `dist/` (ignorada) para a raiz (guardada pelo git).

### O arquivo completo

```text title=".gitignore"
.venv/
__pycache__/
*.pyc
.mypy_cache/
build/
dist/
*.egg-info/
maze.txt
```
