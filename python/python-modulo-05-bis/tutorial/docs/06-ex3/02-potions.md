---
sidebar_position: 2
title: potions.py
---

# potions.py

As duas poções usam os quatro elementos, e eles estão em dois módulos com o mesmo nome:
`elements.py` na raiz (fogo e água) e `alchemy/elements.py` no pacote (terra e ar). O
`potions.py`, dentro do pacote, precisa dizer de qual dos dois quer cada função. Crie
`alchemy/potions.py`:

```python title="alchemy/potions.py"
from elements import create_fire, create_water

from .elements import create_air, create_earth


def healing_potion() -> str:
    return (f"Healing potion brewed with '{create_earth()}'"
            f" and '{create_air()}'")


def strength_potion() -> str:
    return (f"Strength potion brewed with '{create_fire()}'"
            f" and '{create_water()}'")
```

## Os dois elements

- `from elements import create_fire, create_water` é um import **absoluto**: o módulo `elements`
  é procurado nas pastas do `sys.path`, e a primeira é a raiz do projeto, onde o programa rodado
  está ([Onde o Python procura](../04-conceitos/02-onde-o-python-procura.md)). É o `elements.py` da
  raiz. Um import absoluto nunca procura "perto" de quem importa: mesmo escrito dentro do pacote
  `alchemy`, `elements` quer dizer o módulo de nível mais alto com esse nome;
- `from .elements import create_air, create_earth` é um import **relativo**: o ponto é o pacote do
  próprio `potions.py`, o `alchemy`. É o `alchemy/elements.py`.

Os elementos de fora do pacote só podem ser alcançados pelo import absoluto: o relativo não sai do
pacote mais alto ([Absoluto e relativo](../04-conceitos/04-absoluto-e-relativo.md)). Os de dentro
poderiam ser alcançados também pelo absoluto, `from alchemy.elements import ...`; o relativo é
escolha do tutorial, e deixa claro, na leitura, qual dos dois `elements` é qual.

Pedir ao `elements` da raiz uma função que só existe no outro falha, e mostra qual arquivo o
Python usou:

```bash
python3 -c 'from elements import create_earth'
```

```text
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    from elements import create_earth
ImportError: cannot import name 'create_earth' from 'elements' (/path/to/the-codex/elements.py). Did you mean: 'create_fire'?
```

(`/path/to/the-codex` está no lugar do caminho da pasta do projeto; no Python 3.10, sem a linha do
código e sem a sugestão `Did you mean`.)

## As frases

- cada função monta a frase com uma f-string, chamando as funções dos elementos dentro das
  chaves. As aspas simples em volta de cada elemento fazem parte da frase;
- a frase é longa demais para uma linha de 79 caracteres, e foi dividida em duas f-strings
  seguidas dentro de parênteses: o Python junta textos escritos lado a lado num só, e os
  parênteses deixam a expressão continuar na linha de baixo. O espaço antes do `and` está no
  começo do segundo pedaço.

## Uma dependência que o pacote não controla

O `potions.py` só acha o `elements.py` da raiz porque quem roda é um programa da raiz, e a raiz é a
primeira pasta do `sys.path`. É a organização que o enunciado fixa (os `ft_*.py` ao lado do
`elements.py`), e é o que dispensa mexer no `sys.path`.
