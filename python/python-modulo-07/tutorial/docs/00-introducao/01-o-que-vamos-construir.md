---
slug: /
sidebar_position: 1
title: O que vamos construir
---

# O que vamos construir

Um jogo de cartas de criaturas tem centenas de cartas diferentes. Cada criatura pertence a uma
**família** (a família do fogo, a da água...), começa numa forma **base** e pode **evoluir**
para uma forma mais forte. Algumas sabem curar, outras sabem se transformar, e num torneio cada
uma luta do seu jeito. Se o código que cria as cartas e organiza as lutas precisar conhecer cada
carta pelo nome, toda carta nova obriga a mexer nele.

O projeto **DataDeck** resolve isso com três **padrões de projeto**. Um padrão de projeto
(*design pattern*) é uma solução conhecida, com nome próprio, para um problema que aparece de
novo e de novo quando se organiza um programa:

| Padrão | Problema que resolve |
|---|---|
| **fábrica abstrata** (*abstract factory*) | criar as criaturas de uma família sem que quem as usa precise saber de que classe cada uma é |
| **capacidades** (*capabilities*) | dar habilidades extras (curar, se transformar) a algumas criaturas, em classes separadas que um dia podem servir para outras coisas que não são criaturas |
| **estratégia** (*strategy*) | trocar o jeito de lutar de cada criatura sem que o código do torneio precise conhecer cada habilidade |

As três peças se apoiam em ferramentas que o Python já oferece: **classes abstratas** (classes
que só servem de molde), **herança múltipla** (uma classe com duas classes mães) e **pacotes**
(pastas de código que se importam com `import`). A parte
[Pacotes, classes abstratas e herança múltipla](../02-conceitos/01-modulos-e-pacotes.md) explica
cada uma com experimentos pequenos.

## Três exercícios, um construído sobre o outro

O projeto tem três **exercícios**. Cada um é uma pasta de código (um **pacote**) e um programa de
teste, que fica fora da pasta e usa o pacote:

| Exercício | Pacote | Programa de teste | O que constrói |
|---|---|---|---|
| 0 | `ex0/` | `battle.py` | a classe abstrata `Creature`, quatro criaturas de duas famílias (fogo e água) e uma **fábrica** para cada família |
| 1 | `ex1/` | `capacitor.py` | as capacidades de curar e de se transformar, duas famílias novas que as usam e as fábricas delas |
| 2 | `ex2/` | `tournament.py` | três estratégias de luta e um torneio em que cada criatura luta com a sua |

Cada exercício usa o código do anterior: o `ex1` importa a classe `Creature` do `ex0`, e o `ex2`
usa as criaturas dos dois.

Um trecho da saída do exercício 2. A criatura de fogo foi inscrita com a estratégia agressiva,
que exige uma criatura capaz de se transformar, e o torneio é interrompido com uma mensagem:

```text
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
```

As mensagens são em inglês porque o enunciado do projeto mostra a saída de cada programa, e essa
saída é em inglês.

## O enunciado

O projeto vem com um documento oficial que diz o que precisa ser entregue: o **enunciado** (em
inglês, *subject*). A [próxima página](./02-o-enunciado-em-linguagem-simples.md) resume tudo o
que ele pede.

## As partes

| Parte | Conteúdo |
|---|---|
| Ambiente | prepara o Python, a pasta do projeto e as duas ferramentas que conferem o código (flake8 e mypy) |
| Pacotes, classes abstratas e herança múltipla | explica, com experimentos pequenos, módulos e pacotes, classes abstratas com `super()`, herança múltipla e como o `isinstance` informa o tipo ao mypy |
| Exercícios 0 a 2 | constroem os três pacotes e os três programas de teste, um exercício por parte |
| Fechamento | confere tudo, mostra como entregar e responde ao que o enunciado deixa para a avaliação |

Cada exercício termina com os arquivos completos. Os termos novos estão reunidos no
[glossário](./05-glossario.md).
