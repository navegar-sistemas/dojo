---
sidebar_position: 1
title: O problema
---

# O problema

Num torneio, criaturas de famílias diferentes lutam entre si, e cada uma age do seu jeito: a que
cura ataca e depois cura; a que se transforma se transforma, ataca e volta ao normal; as outras
só atacam. Se o código do torneio decidir isso com um `if` por capacidade, cada capacidade nova
obriga a mexer nele. O exercício 2 tira essa decisão do torneio: cada criatura entra no torneio
com uma **estratégia**, um objeto que sabe como ela age.

## O que o enunciado pede

Um pacote `ex2/` com:

| Classe | Tipo | O que tem |
|---|---|---|
| `BattleStrategy` | abstrata | os métodos abstratos `is_valid` (devolve um `bool`: a criatura serve para esta estratégia?) e `act` (a criatura age na luta; chamado pelo torneio) |
| `NormalStrategy` | concreta, filha de `BattleStrategy` | serve para qualquer criatura; só ataca |
| `AggressiveStrategy` | concreta, filha de `BattleStrategy` | serve para as criaturas que se transformam; transforma, ataca e volta ao normal |
| `DefensiveStrategy` | concreta, filha de `BattleStrategy` | serve para as criaturas que curam; ataca e depois cura |

E uma regra para as combinações inválidas (uma estratégia com uma criatura que não serve para
ela): `is_valid` devolve `False`, e `act` lança uma **exceção dedicada**, uma classe de exceção
própria do projeto, com uma mensagem clara.

O pacote `ex2` não tem restrição sobre o que expõe.

## O teste pedido

Um programa `tournament.py`, na raiz, que:

1. cria várias fábricas de criaturas, do `ex0` e do `ex1`;
2. cria as três estratégias;
3. define uma **única** função `battle`, que:
   - recebe a lista de oponentes do torneio, cada um uma tupla `(fábrica, estratégia)`;
   - faz cada oponente lutar uma vez contra cada um dos outros;
   - organiza cada luta usando a estratégia de cada criatura;
   - trata as tuplas inválidas, em que a estratégia não serve para a criatura.

## A saída esperada

```text
Tournament 0 (basic)
 [ (Flameling+Normal), (Healing+Defensive) ]
*** Tournament ***
2 opponents involved

* Battle *
Flameling is a Fire type Creature
 vs.
Sproutling is a Grass type Creature
 now fight!
Flameling uses Ember!
Sproutling uses Vine Whip!
Sproutling heals itself for a small amount

Tournament 1 (error)
 [ (Flameling+Aggressive), (Healing+Defensive) ]
*** Tournament ***
2 opponents involved

* Battle *
Flameling is a Fire type Creature
 vs.
Sproutling is a Grass type Creature
 now fight!
Battle error, aborting tournament: Invalid Creature 'Flameling' for this aggressive strategy

Tournament 2 (multiple)
 [ (Aquabub+Normal), (Healing+Defensive), (Transform+Aggressive) ]
*** Tournament ***
3 opponents involved

* Battle *
Aquabub is a Water type Creature
 vs.
Sproutling is a Grass type Creature
 now fight!
Aquabub uses Water Gun!
Sproutling uses Vine Whip!
Sproutling heals itself for a small amount

* Battle *
Aquabub is a Water type Creature
 vs.
Shiftling is a Normal type Creature
 now fight!
Aquabub uses Water Gun!
Shiftling shifts into a sharper form!
Shiftling performs a boosted strike!
Shiftling returns to normal.

* Battle *
Sproutling is a Grass type Creature
 vs.
Shiftling is a Normal type Creature
 now fight!
Sproutling uses Vine Whip!
Sproutling heals itself for a small amount
Shiftling shifts into a sharper form!
Shiftling performs a boosted strike!
Shiftling returns to normal.
```

## O que a saída revela

- cada torneio começa com o título e a lista de oponentes, no formato
  `(criatura+estratégia)`. Os rótulos da esquerda não seguem uma regra: as fábricas do `ex0`
  aparecem pelo nome da criatura base (`Flameling`, `Aquabub`), e as do `ex1` pelo nome da
  família (`Healing`, `Transform`). São textos fixos do cenário;
- as criaturas que lutam são sempre as **base** de cada fábrica;
- com 3 oponentes, há 3 lutas: o 1º contra o 2º, o 1º contra o 3º e o 2º contra o 3º;
- em cada luta, depois da apresentação, o primeiro oponente age inteiro com a sua estratégia, e
  depois o segundo;
- no torneio 1, `Flameling` foi inscrita com a estratégia agressiva, mas não sabe se transformar.
  O erro aparece na primeira luta, depois da apresentação, quando a estratégia tenta agir; o
  torneio é **abortado** (interrompido) e o programa segue para o próximo torneio.
