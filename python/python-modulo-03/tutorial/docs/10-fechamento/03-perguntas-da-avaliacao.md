---
sidebar_position: 3
title: Perguntas da avaliação
---

# Perguntas da avaliação

O enunciado avisa que a avaliação pode pedir explicações sobre as coleções, demonstrações e
extensões dos programas, e cita as alternativas do exercício 0 e o set vazio do exercício 3.

## Que outras formas há de não imprimir o nome do programa junto com os argumentos? (exercício 0)

O nome do programa está em `sys.argv[0]`, e os argumentos, nas posições seguintes. Cada forma
abaixo percorre só os argumentos:

| Forma | Código | Ideia |
|---|---|---|
| fatia | `for argument in sys.argv[1:]:` com um contador | a fatia é uma lista nova, sem o índice 0 |
| índice | `while index < len(sys.argv):` começando em `index = 1` | o laço pula o índice 0, e o índice é o número do argumento |
| `range` e `enumerate` | `for index in range(1, len(sys.argv)):` ou `enumerate(sys.argv[1:], 1)` | funções prontas que contam as voltas; não autorizadas neste exercício |

As duas primeiras estão em [Percorrer os argumentos](../03-ex0/04-percorrer-os-argumentos.md).

## Como o Python imprime um set vazio, e por quê? (exercício 3)

Como `set()`. As chaves vazias `{}` já são o dicionário vazio, então o Python escreve o set vazio
como a chamada que o cria ([Sets](../06-ex3/02-sets.md#como-um-set-vazio-é-impresso)).

## Comprehensions de set (exercício 6)

O enunciado lembra que comprehensions também funcionam com sets: entre chaves e sem os
dois-pontos, como `{n % 3 for n in numbers}`. O resultado é um set, sem repetições
([Dict comprehension](../09-ex6/03-dict-comprehension.md)).

## Por que cada coleção?

| Exercício | Coleção | Por quê |
|---|---|---|
| 0 | lista | `sys.argv` é uma lista: ordenada e com acesso pela posição, que dá o nome do programa (índice 0) e os argumentos em ordem |
| 1 | lista | as pontuações têm ordem de chegada, podem se repetir e a lista cresce com `append` a cada válida |
| 2 | tupla | uma posição tem sempre três partes de significado fixo e não muda; uma posição nova é uma tupla nova |
| 3 | set | conquistas não se repetem e não têm ordem, e as perguntas do exercício são união, interseção e diferença |
| 4 | dicionário | cada item tem uma quantidade, a busca é pelo nome e cada nome aparece uma vez; a ordem de chegada resolve o empate |
| 5 | generator | os eventos não acabam; produzir um de cada vez evita guardar todos na memória |
| 6 | comprehensions | transformar e filtrar coleções inteiras numa linha, dizendo o que entra na coleção nova |

## Por que trocar listas por sets acelerou o Twitter?

Perguntar se um valor está numa lista compara com um elemento de cada vez, e o tempo cresce com o
tamanho da lista. Num set, o hash do valor aponta direto para a gaveta onde ele estaria, e o
tempo não depende do tamanho ([A estrutura e o algoritmo](../02-colecoes/03-a-estrutura-e-o-algoritmo.md)).

## Acrescentar uma funcionalidade

Pedidos de extensão costumam mexer numa parte só do programa. Alguns exemplos e onde mexer:

| Pedido | Onde |
|---|---|
| mostrar quantas pontuações ficaram acima da média (exercício 1) | um laço com contador em `show_stats` |
| um quinto jogador (exercício 3) | um nome a mais em `PLAYERS`; os laços percorrem a lista toda |
| mostrar os itens com quantidade acima de 2 (exercício 4) | um laço sobre o dicionário em `main` |
| uma nova ação de jogador (exercício 5) | um texto a mais em `ACTIONS` |
| as pontuações abaixo da média (exercício 6) | outra dict comprehension, com `<` no lugar de `>` |
