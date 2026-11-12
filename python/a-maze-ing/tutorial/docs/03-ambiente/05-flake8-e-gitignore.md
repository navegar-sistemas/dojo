---
sidebar_position: 5
title: O .flake8 e o .gitignore
---

# O `.flake8` e o `.gitignore`

## `.flake8`

O flake8 lê a configuração de um arquivo `.flake8` na raiz. O projeto só precisa dizer o que
**não** conferir:

```ini
[flake8]
extend-exclude = .venv,build,dist
```

- `.venv`: o código das ferramentas instaladas não é do projeto, e o flake8 acusaria milhares
  de linhas que não são suas.
- `build`, `dist`: cópias temporárias do código, feitas pelo empacotamento.

### `extend-exclude`, não `exclude`

O flake8 já pula, por padrão, pastas como `.git`, `__pycache__`, `.tox` e `.eggs`. `exclude`
**substituiria** essa lista, e o `.git` voltaria a ser conferido; `extend-exclude` **soma** à
lista padrão.

### As regras

Nenhuma regra é desligada e o limite de linha é o padrão, 79 caracteres. O subject exige o
padrão flake8, e afrouxar a configuração seria fugir dele.

Pelo mesmo motivo, o código não usa `# noqa` (o comentário que cala o flake8 numa linha). Uma
linha longa se resolve quebrando a expressão:

```python
return (isinstance(cell, Cell) and 0 <= cell.x < self.width
        and 0 <= cell.y < self.height)
```

### O arquivo completo

```ini title=".flake8"
[flake8]
extend-exclude = .venv,build,dist
```

## `.gitignore`

O subject pede um `.gitignore` que exclua os artefatos do Python. Cada linha é um padrão de
arquivos que o git não deve versionar:

| Padrão | O que é |
|---|---|
| `.venv/` | o ambiente virtual, recriado por `make install` |
| `__pycache__/` | bytecode, em qualquer pasta |
| `*.pyc` | bytecode solto |
| `.mypy_cache/` | cache do mypy |
| `build/`, `dist/` | saídas temporárias do `make build` |
| `*.egg-info/` | metadados temporários do setuptools |
| `maze.txt` | o arquivo de saída do `config.txt`, regravado a cada execução |

Um padrão terminado em `/` só casa com pastas, em qualquer nível da árvore.

### O que **não** está ali

`mazegen-1.0.0-py3-none-any.whl` e `mazegen-1.0.0.tar.gz` são gerados pelo `make build`, mas são
**entregáveis**: o subject exige o pacote na raiz do repositório. Por isso o `make build` os
copia de `dist/` (ignorada) para a raiz (versionada).

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
