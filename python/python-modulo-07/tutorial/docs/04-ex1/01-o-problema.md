---
sidebar_position: 1
title: O problema
---

# O problema

As criaturas do exercício 0 só atacam. Agora algumas ganham **capacidades** (*capabilities*):
curar e se transformar. Uma capacidade não é exclusividade de criaturas: um dia, um item do jogo
também poderia curar. Por isso, cada capacidade fica numa classe abstrata **separada**, que não
herda de `Creature`, e a criatura que tem a capacidade herda das duas.

## O que o enunciado pede

Um pacote `ex1/`, construído sobre o `ex0` (ele usa a classe `Creature` e a `CreatureFactory`
de lá), com:

| Classe | Tipo | O que tem |
|---|---|---|
| `HealCapability` | abstrata, **não** filha de `Creature` | o método abstrato `heal` ("curar") |
| `TransformCapability` | abstrata, **não** filha de `Creature` | os métodos abstratos `transform` ("transformar") e `revert` ("voltar ao normal"), e um atributo que guarda se a criatura está transformada; esse estado muda o `attack` da criatura |
| `Sproutling`, `Bloomelle` | concretas, filhas de `Creature` **e** de `HealCapability` | uma família: `Sproutling` é a base, `Bloomelle` a evoluída |
| `Shiftling`, `Morphagon` | concretas, filhas de `Creature` **e** de `TransformCapability` | uma família: `Shiftling` é a base, `Morphagon` a evoluída |
| `HealingCreatureFactory` | concreta, filha de `CreatureFactory` | cria `Sproutling` e `Bloomelle` |
| `TransformCreatureFactory` | concreta, filha de `CreatureFactory` | cria `Shiftling` e `Morphagon` |

Os métodos das capacidades devolvem textos que descrevem a ação, como o `attack`. E, de novo, o
pacote **só expõe as fábricas**.

O enunciado deixa o `heal` receber, se quem programa quiser, um parâmetro "alvo" (*target*): a
criatura curada. O tutorial escolhe não usar alvo: as mensagens da saída ("cura a si mesma",
"cura a si mesma e aos outros") não citam ninguém, e um parâmetro sem uso só complicaria a
**assinatura** do método (o nome, os parâmetros com os tipos e o tipo de retorno).

## O teste pedido

Um programa `capacitor.py`, na raiz, que:

1. cria a fábrica das criaturas que curam;
2. cria a criatura base e depois a evoluída, e faz cada uma: se descrever, atacar e curar;
3. cria a fábrica das criaturas que se transformam;
4. cria a criatura base e depois a evoluída, e faz cada uma: se descrever, atacar, se
   transformar, atacar de novo e voltar ao normal.

## A saída esperada

```text
Testing Creature with healing capability
 base:
Sproutling is a Grass type Creature
Sproutling uses Vine Whip!
Sproutling heals itself for a small amount
 evolved:
Bloomelle is a Grass/Fairy type Creature
Bloomelle uses Petal Dance!
Bloomelle heals itself and others for a large amount

Testing Creature with transform capability
 base:
Shiftling is a Normal type Creature
Shiftling attacks normally.
Shiftling shifts into a sharper form!
Shiftling performs a boosted strike!
Shiftling returns to normal.
 evolved:
Morphagon is a Normal/Dragon type Creature
Morphagon attacks normally.
Morphagon morphs into a dragonic battle form!
Morphagon unleashes a devastating morph strike!
Morphagon stabilizes its form.
```

As linhas ` base:` e ` evolved:` começam com um espaço. Nas criaturas que se transformam, o
mesmo `attack` dá duas frases diferentes: `attacks normally.` antes do `transform`, e um golpe
reforçado depois dele.
