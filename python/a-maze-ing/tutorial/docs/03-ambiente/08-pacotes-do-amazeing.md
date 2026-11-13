---
sidebar_position: 10
title: Os pacotes do amazeing
---

# Os pacotes do `amazeing`

A aplicação (tudo o que é deste programa e não vai para o pacote reutilizável: ler o config,
gravar a saída, desenhar, o menu) também precisa das suas pastas. Esta página cria o esqueleto
do `amazeing` e confere que o projeto vazio já passa no lint.

## Uma pasta por camada

A aplicação tem uma subpasta para cada **camada** (um grupo de classes com o mesmo tipo de
trabalho, [parte 2](../02-arquitetura/01-por-que-camadas.md)). Quase todas têm o nome do
**papel** das suas classes ([parte 2](../02-arquitetura/04-papeis-das-classes.md)): `use_cases`,
`repositories`, `services`, `ui` e `utils`. A exceção é `domain`, os dados do programa, que
guarda classes de dois papéis e por isso se divide em `entities/` e `value_objects/`. Cada
subpasta é um pacote com o seu `__init__.py`:

```bash
mkdir -p amazeing/domain/entities amazeing/domain/value_objects amazeing/use_cases \
    amazeing/repositories amazeing/services amazeing/ui amazeing/utils
```

A `\` no fim da primeira linha continua o comando na linha de baixo. Como no `mazegen`, cada
`__init__.py` tem só uma docstring de uma frase.

```python title="amazeing/__init__.py"
"""A-Maze-ing application built on top of the mazegen package."""
```

A raiz da aplicação. Além das subpastas, ela guarda o `errors.py`, com os tipos de erro da
aplicação ([parte 10](../10-utilitarios/05-a-hierarquia-app-error.md)).

```python title="amazeing/domain/__init__.py"
"""Domain layer of the application."""
```

O **domínio** da aplicação: os dados com que o programa trabalha (a configuração lida, o
labirinto pronto, o estado da tela), sem nenhum arquivo e sem terminal.

```python title="amazeing/domain/entities/__init__.py"
"""Mutable entities of the application domain."""
```

A entidade `ViewState`: se o caminho mais curto aparece na tela e qual é a cor das paredes,
dois dados que mudam conforme o usuário usa o menu ([parte 13](../13-tela/01-o-estado-da-tela.md)).

```python title="amazeing/domain/value_objects/__init__.py"
"""Immutable value objects of the application domain."""
```

Os value objects `MazeConfig`, as opções já lidas e validadas
([parte 11](../11-configuracao/01-o-value-object-maze-config.md)), e `GeneratedMaze`, um retrato
do labirinto pronto ([parte 12](../12-geracao-e-saida/01-o-retrato-generated-maze.md)).

```python title="amazeing/use_cases/__init__.py"
"""Application use cases and the ports they depend on."""
```

O use case `GenerateMaze`, a operação "gerar um labirinto e gravá-lo", e a porta
`MazeRepository`, a descrição do método `save` de que ele precisa
([parte 12](../12-geracao-e-saida/03-a-porta-maze-repository.md)).

```python title="amazeing/repositories/__init__.py"
"""Repositories that read and write files."""
```

`FileConfigRepository`, que lê o config ([parte 11](../11-configuracao/05-abrindo-o-arquivo.md)),
e `FileMazeRepository`, que grava o arquivo de saída
([parte 12](../12-geracao-e-saida/05-gravando-o-arquivo.md)). São as únicas classes que abrem
arquivos.

```python title="amazeing/services/__init__.py"
"""Stateless application services."""
```

`RenderService`, que transforma um labirinto em linhas de texto colorido para o terminal
([parte 13](../13-tela/02-a-grade-de-posicoes.md)).

```python title="amazeing/ui/__init__.py"
"""Terminal user interface."""
```

`Menu` ([parte 14](../14-menu-e-main/01-o-laco-do-menu.md)), a única classe que usa `print` e
`input`.

```python title="amazeing/utils/__init__.py"
"""Stateless helpers shared by the application layers."""
```

`ValueParser`, que converte o texto do config em número, booleano ou coordenada, e `Ansi`, os
códigos que mudam a cor do terminal ([parte 10](../10-utilitarios/02-inteiros-sem-surpresa.md)).

## O esqueleto completo

```text
.flake8
.gitignore
Makefile
config.txt
pyproject.toml
mazegen/
    __init__.py
    py.typed
    entities/__init__.py
    value_objects/__init__.py
    services/__init__.py
amazeing/
    __init__.py
    domain/__init__.py
    domain/entities/__init__.py
    domain/value_objects/__init__.py
    use_cases/__init__.py
    repositories/__init__.py
    services/__init__.py
    ui/__init__.py
    utils/__init__.py
```

## Experimente

O esqueleto ainda não faz nada, mas já dá para instalar as ferramentas e rodar a verificação
mais rigorosa:

```bash
make install
make lint-strict
```

A saída dos dois comandos:

```text
python3 -m venv .venv
.venv/bin/python -m pip install --quiet --no-cache-dir --upgrade pip
.venv/bin/python -m pip install --quiet flake8==7.4.1 mypy==2.4.1 build==1.6.1
.venv/bin/python -m flake8 .
.venv/bin/python -m mypy . --strict
Success: no issues found in 13 source files
```

O `make` imprime cada comando antes de rodá-lo. As três primeiras linhas são do `make install`:
ele cria o `.venv` e instala as ferramentas, e o `--quiet` do `pip` esconde o progresso da
instalação. Se o `.venv` já existir, o `python3 -m venv` não o apaga, e o `pip` só confere que
as versões pedidas já estão lá. As três últimas são do `make lint-strict`. O flake8 não imprime
nada quando não encontra problema, e o mypy confere 13 arquivos: os 13 `__init__.py`. A partir daqui, toda peça nova
entra num projeto que já está limpo, e o `make lint-strict` deve continuar sem nenhuma linha de
erro a cada arquivo acrescentado.
