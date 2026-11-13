---
sidebar_position: 9
title: Rodar e conferir
---

# Rodar e conferir

## Comparar com o enunciado

```bash
diff <(python3 battle.py) - <<'FIM'
Testing factory
Flameling is a Fire type Creature
Flameling uses Ember!
Pyrodon is a Fire/Flying type Creature
Pyrodon uses Flamethrower!

Testing factory
Aquabub is a Water type Creature
Aquabub uses Water Gun!
Torragon is a Water type Creature
Torragon uses Hydro Pump!

Testing battle
Flameling is a Fire type Creature
 vs.
Aquabub is a Water type Creature
 fight!
Flameling uses Ember!
Aquabub uses Water Gun!
FIM
```

- `<(python3 battle.py)` entrega ao `diff` a saída do programa como se fosse um arquivo;
- o `-` diz ao `diff` para ler o segundo texto da entrada do comando, em vez de um arquivo;
- `<<'FIM'` escreve nessa entrada as linhas seguintes, até a linha `FIM`: a saída copiada do
  enunciado. Cole o bloco inteiro, até a linha `FIM`; sem ela, o terminal fica esperando mais
  linhas;
- o `diff` compara os dois textos linha a linha e só imprime as diferenças.

Sem nenhuma linha impressa, a saída é a esperada, inclusive o espaço no começo de ` vs.` e
` fight!`.

## Conferir estilo e tipos

```bash
.venv/bin/flake8 battle.py ex0
.venv/bin/mypy --disallow-untyped-defs battle.py ex0
```

```text
Success: no issues found in 4 source files
```

O flake8 não imprime nada, e o mypy confere os quatro arquivos: `battle.py` e os três da pasta
`ex0`.

## O pacote só expõe fábricas

```bash
python3 -B -c 'import ex0; print(ex0.__all__); print(hasattr(ex0, "Flameling"))'
```

```text
['CreatureFactory', 'FlameFactory', 'AquaFactory']
False
```

O `-B` impede o Python de gravar a pasta `__pycache__`, que este teste não precisa, e o `;`
separa os comandos Python escritos na mesma linha. Rodado da
raiz, o `python3 -c` acha o pacote `ex0` na pasta atual
([Onde o Python procura](../02-conceitos/01-modulos-e-pacotes.md#onde-o-python-procura)). O pacote
oferece as três fábricas e não tem o nome `Flameling`. O mypy recusa o import antes de rodar:

```bash
.venv/bin/mypy -c 'from ex0 import Flameling'
```

```text
<string>:1: error: Module "ex0" has no attribute "Flameling"  [attr-defined]
Found 1 error in 1 file (checked 1 source file)
```

Rodando, o mesmo import termina com `ImportError: cannot import name 'Flameling' from 'ex0'`,
seguido do caminho do `__init__.py` na sua máquina.

O módulo de dentro continua alcançável pelo nome completo
([O que fica de fora](./06-o-init-do-pacote.md#o-que-fica-de-fora)):

```bash
python3 -B -c 'import ex0; print(hasattr(ex0, "creature"), ex0.creature.Flameling().describe())'
```

```text
True Flameling is a Fire type Creature
```

## As classes abstratas não são instanciadas

```bash
python3 -B -c 'from ex0 import CreatureFactory; CreatureFactory()'
```

A última linha da saída é:

```text
TypeError: Can't instantiate abstract class CreatureFactory without an implementation for abstract methods 'create_base', 'create_evolved'
```

No Python 3.10 e no 3.11, a mensagem é
`Can't instantiate abstract class CreatureFactory with abstract methods create_base, create_evolved`.
O mesmo vale para `Creature`, com o método `attack`.

## A pasta `__pycache__`

```bash
ls -1 ex0
```

```text
__init__.py
__pycache__
creature.py
factory.py
```

O `python3 battle.py` do `diff` importou o pacote e criou a `__pycache__` dentro de `ex0`
([O `__pycache__`](../02-conceitos/01-modulos-e-pacotes.md#o-__pycache__)). Ela não é
entregue ([Entregar](../06-fechamento/02-entregar.md)).
