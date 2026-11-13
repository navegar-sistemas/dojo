---
sidebar_position: 8
title: Rodar e conferir
---

# Rodar e conferir

## As cinco saídas sem erro

```bash
diff <(for f in ft_alembic_0.py ft_alembic_1.py ft_alembic_2.py ft_alembic_3.py ft_alembic_5.py; do python3 "$f"; done) - <<'FIM'
=== Alembic 0 ===
Using: 'import ...' structure to access elements.py
Testing create_fire: Fire element created
=== Alembic 1 ===
Using: 'from ... import ...' structure to access elements.py
Testing create_water: Water element created
=== Alembic 2 ===
Accessing alchemy/elements.py using 'import ...' structure
Testing create_earth: Earth element created
=== Alembic 3 ===
Accessing alchemy/elements.py using 'from ... import ...' structure
Testing create_air: Air element created
=== Alembic 5 ===
Accessing the alchemy module using 'from alchemy import ...'
Testing create_air: Air element created
FIM
```

- `for f in ...; do python3 "$f"; done` roda os cinco scripts em sequência: o comando entre `do`
  e `done` repete uma vez para cada nome da lista, com o nome na variável `f`, e `"$f"` é o valor
  dela;
- `<( ... )` entrega ao `diff` a saída desses comandos como se fosse um arquivo;
- o `-` diz ao `diff` para ler o segundo texto da entrada do comando, em vez de um arquivo;
- `<<'FIM'` escreve nessa entrada as linhas seguintes, até a linha `FIM`: as saídas copiadas do
  enunciado, uma depois da outra. Cole o bloco inteiro, até a linha `FIM`; sem ela, o terminal
  fica esperando mais linhas;
- o `diff` compara os dois textos linha a linha e só imprime as diferenças.

Sem nenhuma linha impressa, as cinco saídas são as esperadas.

## A saída com o traceback

O traceback do `ft_alembic_4.py` traz o caminho da pasta, que muda de máquina para máquina, e é
escrito na saída de erro, que o `diff` não recebe sozinho. O comando abaixo resolve as duas
coisas antes de comparar:

```bash
diff <(python3 ft_alembic_4.py 2>&1 | sed "s|$(pwd -P)|/tmp/Python/module-06|") - <<'FIM'
=== Alembic 4 ===
Accessing the alchemy module using 'import alchemy'
Testing create_air: Air element created
Now show that not all functions can be reached
This will raise an exception!
Testing the hidden create_earth: Traceback (most recent call last):
  File "/tmp/Python/module-06/ft_alembic_4.py", line 12, in <module>
    print(f"{alchemy.create_earth()}")
            ^^^^^^^^^^^^^^^^^^^^
AttributeError: module 'alchemy' has no attribute 'create_earth'. Did you mean: 'create_air'?
FIM
```

- `2>&1` junta a saída de erro (o canal número 2) à saída padrão (o canal 1): o traceback passa
  a ir para o mesmo lugar que os `print`;
- o `|` (*pipe*) liga a saída do script à entrada do `sed`, um programa que edita texto linha a
  linha. `s|A|B|` troca o texto `A` pelo texto `B`;
- `$(pwd -P)` é substituído pelo resultado do comando `pwd -P`: o caminho completo da pasta
  atual. O `-P` dá o caminho real no disco, o mesmo que o Python escreve no traceback, mesmo que
  a pasta tenha sido aberta por um atalho. Com a troca, o caminho fica igual ao do enunciado.

```text
9c9
<              ^^^^^^^^^^^^^^^^^^^^
---
>             ^^^^^^^^^^^^^^^^^^^^
```

O `diff` acusa uma única diferença: `9c9` quer dizer "a linha 9 da primeira entrada mudou em
relação à linha 9 da segunda". A linha com `<` é a do script; a com `>`, a do enunciado. É a
linha dos `^`, que no Python 3.14 começa uma coluna depois
([Lendo o traceback](./06-o-erro-proposital.md#lendo-o-traceback)). Todo o resto, inclusive a
linha 12 e a sugestão `Did you mean: 'create_air'?`, é igual.

No Python 3.10, que não imprime a linha dos `^`, a diferença aparece assim:

```text
8a9
>             ^^^^^^^^^^^^^^^^^^^^
```

"Depois da linha 8 da primeira entrada, falta a linha 9 da segunda."

## Conferir estilo e tipos

```bash
.venv/bin/flake8 *.py alchemy
.venv/bin/mypy --disallow-untyped-defs *.py alchemy
```

```text
ft_alembic_4.py:12: error: Module has no attribute "create_earth"; maybe "create_air"?  [attr-defined]
Found 1 error in 1 file (checked 9 source files)
```

`*.py alchemy` passa às duas ferramentas os arquivos `.py` da raiz e a pasta `alchemy` inteira, e
deixa de fora a `.venv` e a pasta `experimentos`. O flake8 não imprime nada. O mypy confere os
nove arquivos da Parte I e acusa só a linha proposital do `ft_alembic_4.py`
([O erro do mypy](./06-o-erro-proposital.md#o-erro-do-mypy)); qualquer outra linha na saída dele
é um problema a corrigir.

## Rodar de outra pasta

O primeiro item do `sys.path` é a pasta do script, e não a pasta onde você está
([Onde o Python procura](../02-conceitos/02-onde-o-python-procura.md)). Por isso os scripts
funcionam chamados de fora da `the-codex`:

```bash
cd ..
python3 the-codex/ft_alembic_0.py
cd the-codex
```

```text
=== Alembic 0 ===
Using: 'import ...' structure to access elements.py
Testing create_fire: Fire element created
```

## O cache

```bash
ls -1 alchemy
```

```text
__init__.py
__pycache__
elements.py
```

`ls -1` lista um nome por linha. A pasta `__pycache__` apareceu em `alchemy` (e também na raiz)
na primeira vez que os módulos foram importados
([A pasta `__pycache__`](../02-conceitos/01-o-modulo-e-o-import.md#a-pasta-__pycache__)). Ela não
é entregue.
