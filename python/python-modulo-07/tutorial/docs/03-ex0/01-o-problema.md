---
sidebar_position: 1
title: O problema
---

# O problema

O jogo precisa de cartas de criatura. As criaturas vêm em **famílias**: cada família tem uma
forma **base** e uma forma **evoluída**. Quem monta uma partida quer "a criatura base da família
do fogo", e não precisa saber que ela se chama `Flameling` nem de que classe ela é. O exercício 0
cria as criaturas e, para cada família, uma **fábrica** que as cria.

## O que o enunciado pede

Um pacote `ex0/` (pasta com `__init__.py`) com:

| Classe | Tipo | O que tem |
|---|---|---|
| `Creature` | abstrata | atributos com o nome e o tipo da criatura; o método abstrato `attack`; o método concreto `describe`, que devolve uma mensagem padrão com o nome e o tipo |
| `Flameling`, `Pyrodon`, `Aquabub`, `Torragon` | concretas, filhas de `Creature` | um `attack` que devolve a mensagem de ataque de cada uma |
| `CreatureFactory` | abstrata | os métodos abstratos `create_base` (cria a criatura base da família) e `create_evolved` (cria a evoluída) |
| `FlameFactory` | concreta, filha de `CreatureFactory` | cria `Flameling` (base) e `Pyrodon` (evoluída) |
| `AquaFactory` | concreta, filha de `CreatureFactory` | cria `Aquabub` (base) e `Torragon` (evoluída) |

E uma regra sobre o pacote: ele **não pode expor as criaturas concretas**, só as fábricas. Quem
importa `ex0` consegue `FlameFactory`, mas não `Flameling`
([O `__init__.py` do pacote](./06-o-init-do-pacote.md)).

## O teste pedido

Um programa `battle.py`, na raiz do projeto, fora do pacote, que:

1. cria a fábrica do fogo e a da água (o enunciado as chama de "fábricas de Flameling e de
   Aquabub", pelo nome da criatura base; são a `FlameFactory` e a `AquaFactory`);
2. usa **uma única função**, que recebe uma fábrica qualquer, para testar as duas: a função cria a
   criatura base e a evoluída, e faz cada uma se descrever e atacar;
3. usa outra função, que recebe as duas fábricas, para fazer as duas criaturas base lutarem.

Uma única função para as duas fábricas quer dizer que a função não sabe qual fábrica recebeu: é o
mesmo código para o fogo e para a água.

## A saída esperada

```text
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
```

Da saída saem os dados de cada criatura:

| Criatura | Família | Forma | Tipo | Ataque |
|---|---|---|---|---|
| `Flameling` | fogo | base | `Fire` | `Ember` |
| `Pyrodon` | fogo | evoluída | `Fire/Flying` | `Flamethrower` |
| `Aquabub` | água | base | `Water` | `Water Gun` |
| `Torragon` | água | evoluída | `Water` | `Hydro Pump` |

As linhas ` vs.` e ` fight!` começam com um espaço.

O enunciado permite usar outras criaturas, desde que os conceitos fiquem: famílias de criaturas
e fábricas abstratas. O tutorial usa as do exemplo, para que a saída possa ser comparada linha a
linha com a do enunciado.
