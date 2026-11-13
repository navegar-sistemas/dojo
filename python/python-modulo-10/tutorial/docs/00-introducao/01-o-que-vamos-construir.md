---
slug: /
sidebar_position: 1
title: O que vamos construir
---

# O que vamos construir

No Python, uma função é um valor como um número ou um texto: pode ser guardada numa variável,
passada para outra função e devolvida por outra função. Isso permite escrever funções que
**criam, combinam e modificam outras funções**. Esse é o centro da **programação funcional**, um
jeito de programar em que o trabalho é feito por funções que recebem dados e devolvem resultados,
sem depender de variáveis compartilhadas pelo programa inteiro.

O projeto se chama **FuncMage**. O tema é o ano de 2142, em que "magos das funções" lançam
feitiços: um feitiço (*spell*) é uma função, um mago (*mage*) é um dicionário com nome e poder, e
um artefato (*artifact*) é outro dicionário. O tema só dá nome às coisas; o assunto de verdade é:

- **lambda**: uma função curta, sem nome, escrita numa expressão só;
- **função de ordem superior**: uma função que recebe ou devolve outra função;
- **closure**: uma função que lembra as variáveis do lugar onde foi criada;
- o módulo **`functools`**: ferramentas prontas do Python para trabalhar com funções;
- **decorador**: uma função que embrulha outra função e muda o comportamento dela sem mexer no
  código dela.

## Cinco programas

O projeto tem cinco **exercícios**. Cada um é um programa de um arquivo só, numa pasta própria,
independente dos outros:

| Exercício | Arquivo | O que constrói |
|---|---|---|
| 0 | `ex0/lambda_spells.py` | quatro funções que ordenam, filtram, transformam e resumem listas de artefatos e de magos, cada uma com lambdas |
| 1 | `ex1/higher_magic.py` | quatro funções que recebem feitiços e devolvem feitiços novos: combinado, amplificado, condicional e em sequência |
| 2 | `ex2/scope_mysteries.py` | quatro funções que devolvem closures: um contador, um acumulador, uma fábrica de encantamentos e um cofre de memórias |
| 3 | `ex3/functools_artifacts.py` | quatro funções que usam ferramentas do `functools`: `reduce`, `partial`, `lru_cache` e `singledispatch` |
| 4 | `ex4/decorator_mastery.py` | três decoradores (cronômetro, validador de poder e nova tentativa) e uma classe com um método estático |

Um trecho da saída do exercício 2:

```text
Testing mage counter...
counter_a call 1: 1
counter_a call 2: 2
counter_b call 1: 1
```

`counter_a` e `counter_b` são duas funções criadas pela mesma função, `mage_counter`. Cada uma
conta as próprias chamadas: a segunda chamada de `counter_a` devolve 2, e a primeira de
`counter_b` devolve 1. A contagem fica guardada dentro de cada função, numa closure, sem nenhuma
variável do programa inteiro. As mensagens são em inglês porque o enunciado do projeto mostra a
saída de cada programa, e essa saída é em inglês.

## O enunciado

O projeto vem com um documento oficial que diz o que precisa ser entregue: o **enunciado** (em
inglês, *subject*). A [próxima página](./02-o-enunciado-em-linguagem-simples.md) resume tudo o
que ele pede.

## As partes

| Parte | Conteúdo |
|---|---|
| Ambiente | prepara o Python, a pasta do projeto, as duas ferramentas que conferem o código (flake8 e mypy) e o gerador de dados de teste que vem com o enunciado |
| Funções como valores | explica, com experimentos pequenos, funções guardadas em variáveis, lambdas, funções que devolvem funções, escopo e closures, `*args` e `**kwargs`, e decoradores |
| Exercícios 0 a 4 | constroem os cinco programas, um por parte |
| Fechamento | confere tudo, mostra como entregar e responde às perguntas de revisão sobre os conceitos |

Cada exercício termina com o arquivo completo e uma página que roda e confere o programa. Os
termos novos estão reunidos no [glossário](./05-glossario.md).
