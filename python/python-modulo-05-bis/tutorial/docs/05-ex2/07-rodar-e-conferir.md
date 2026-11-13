---
sidebar_position: 7
title: Rodar e conferir
---

# Rodar e conferir

Os programas dos exercícios 2 a 4 não usam bibliotecas externas: rodam com o `python3` global ou
com o do `lab_env`, ativado ou não.

## ft_alembic_0.py contra o enunciado

```bash
diff <(python3 ft_alembic_0.py) - <<'FIM'
=== Alembic 0 ===
Using: 'import ...' structure to access elements.py
Testing create_fire: Fire element created
FIM
```

Sem nenhuma linha impressa, a saída é a esperada. O `<(...)`, o `-` e o `<<'FIM'` são explicados
em [Rodar e conferir do exercício 0](../02-ex0/12-rodar-e-conferir.md).

## ft_alembic_1.py contra o enunciado

O traceback tem o caminho do arquivo e um número de linha, que mudam de uma pasta e de um arquivo
para outro, e a última linha muda com a versão do Python. A comparação pega as seis primeiras
linhas, que não mudam:

```bash
diff <(python3 ft_alembic_1.py 2>&1 | sed -n '1,6p') - <<'FIM'
=== Alembic 1 ===
Accessing the alchemy module using 'import alchemy'
Testing create_air: Air element created
Now show that not all functions can be reached
This will raise an exception!
Testing the hidden create_earth: Traceback (most recent call last):
FIM
```

- `2>&1` manda a saída de erros (o canal `2`, onde sai o traceback) para o mesmo lugar da saída
  padrão (o canal `1`), e o `sed` recebe as duas, na ordem em que aparecem no terminal;
- `sed -n '1,6p'` imprime só as linhas 1 a 6. O `-n` cala as outras.

Sem nenhuma linha impressa. A última linha, à parte (`tail -n 1` guarda só a última linha do que
recebe):

```bash
python3 ft_alembic_1.py 2>&1 | tail -n 1
```

```text
AttributeError: module 'alchemy' has no attribute 'create_earth'. Did you mean '.create_air' instead of '.create_earth'?
```

O mesmo erro do enunciado, `AttributeError: module 'alchemy' has no attribute 'create_earth'`, com
a sugestão escrita do jeito do Python 3.15; do 3.10 ao 3.14, a linha é igual à do enunciado,
terminada em `Did you mean: 'create_air'?`.

O programa termina com erro, de propósito:

```bash
python3 ft_alembic_1.py > /dev/null 2>&1
echo $?
```

```text
1
```

`> /dev/null 2>&1` descarta as duas saídas (`/dev/null` é um arquivo especial que joga fora tudo o
que recebe), e o código de saída `1` mostra que o programa parou numa exceção.

## Estilo e tipos

```bash
.venv/bin/flake8 elements.py alchemy/__init__.py alchemy/elements.py ft_alembic_0.py ft_alembic_1.py
.venv/bin/mypy --disallow-untyped-defs elements.py alchemy/__init__.py alchemy/elements.py ft_alembic_0.py ft_alembic_1.py
```

```text
ft_alembic_1.py:10: error: Module has no attribute "create_earth"; maybe "create_air"?  [attr-defined]
Found 1 error in 1 file (checked 5 source files)
```

O flake8 não imprime nada: a `__all__` resolve o aviso do `__init__.py`. O mypy confere os cinco
arquivos e acusa só a linha proposital
([O erro proposital do mypy](./05-ft-alembic-1.md#o-erro-proposital-do-mypy)).

## O create_earth continua lá

A função não exposta continua alcançável pelo caminho completo, pelos dois jeitos de importar:

```bash
python3 -c 'import alchemy; print(alchemy.elements.create_earth())'
python3 -c 'from alchemy.elements import create_earth; print(create_earth())'
```

```text
Earth element created
Earth element created
```

O `python3 -c`, rodado da raiz, tem a raiz como primeira pasta do `sys.path`, e acha o pacote. O
primeiro comando passa pelo atributo `alchemy.elements`, que o `__init__.py` criou ao carregar o
submódulo; o segundo importa o submódulo direto. O `__init__.py` define o atalho, não uma barreira.
