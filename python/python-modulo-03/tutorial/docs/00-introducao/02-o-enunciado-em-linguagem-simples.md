---
sidebar_position: 2
title: O enunciado em linguagem simples
---

# O enunciado em linguagem simples

## Regras que valem para todos os exercícios

- **Python 3.10 ou mais novo.** Os programas são rodados com `python3`
  ([O Python](../01-ambiente/01-o-python.md)).
- **Estilo conferido pelo flake8.** O flake8 é um programa que lê o seu código e aponta o que
  foge do estilo padrão do Python: linha comprida demais, falta de linha em branco entre funções,
  variável criada e nunca usada. O código entregue não pode ter nenhum aviso dele.
- **Type hints em todas as funções e métodos, conferidos pelo mypy.** Um *type hint* é a anotação
  do tipo de cada parâmetro e do retorno, como em `def dobro(n: int) -> int:`. O mypy é o
  programa que confere se esses tipos batem com o uso
  ([Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md)).
- **Um arquivo por exercício**, cada um na sua pasta (`ex0/` a `ex6/`).
- **O programa nunca pode travar.** "Travar" (*crash*) quer dizer parar no meio com uma mensagem
  de erro do Python. Todo erro previsível, como um texto que não é número, precisa ser tratado.
- **Nada de arquivos.** Os programas não abrem, leem nem gravam arquivos. Os dados vêm de três
  lugares: escritos no próprio código, digitados no terminal ou passados na linha de comando, que
  é o texto escrito depois do nome do programa ao rodá-lo
  ([A linha de comando](../03-ex0/02-a-linha-de-comando.md)).
- **Mostrar as operações básicas e as mais avançadas** de cada coleção, com código claro.

## O que pode ser usado

Cada exercício tem uma lista de **funções autorizadas**: as funções prontas do Python que o código
pode chamar. Além delas, duas regras gerais liberam mais coisas:

- a **regra dos tipos**: os tipos `str` (texto), `int` (inteiro) e `float` (número com parte
  decimal, escrita com ponto: `2.5`) podem ser usados com
  todos os seus métodos e construtores, em qualquer exercício. Um **método** é uma função que
  pertence a um tipo e é chamada com ponto, como `"bob".capitalize()`; um **construtor** é a
  chamada pelo nome do tipo que cria um valor dele, como `int("42")`;
- cada coleção nova, a partir do exercício que a apresenta, pode ser usada com todos os seus
  métodos daí em diante. A lista entra no exercício 0, a tupla no 2, o set no 3, o dicionário no 4.

Funções que você mesmo escreve no arquivo podem ser chamadas sempre. As palavras da linguagem,
como `for`, `if`, `try`, `except` e `yield`, não são funções e podem ser usadas à vontade.

| Exercício | Funções autorizadas |
|---|---|
| 0 | `import sys`, `sys.argv`, `len()`, `print()` |
| 1 | `import sys`, `sys.argv`, `len()`, `sum()`, `max()`, `min()`, `print()` |
| 2 | `import math`, `math.sqrt()`, `input()`, `round()`, `print()` |
| 3 | `len()`, `print()`, `import random`, `random.*`, `set()`, `set.union()`, `set.intersection()`, `set.difference()` |
| 4 | `import sys`, `sys.argv`, `len()`, `print()`, `sum()`, `list()`, `round()`, `dict.keys()`, `dict.values()`, `dict.update()` |
| 5 | `next()`, `range()`, `len()`, `print()`, `import typing`, `typing.Generator`, `import random`, `random.*` |
| 6 | `import random`, `random.*`, `print()`, `len()`, `sum()`, `round()` |

`import sys`, `import math`, `import random` e `import typing` trazem **módulos**: arquivos de
código que vêm com o Python e reúnem funções de um assunto. `random.*` quer dizer "qualquer
função do módulo `random`". Cada módulo é explicado no exercício que o usa.

## Os sete exercícios

| Exercício | O que o programa precisa fazer |
|---|---|
| 0 | mostrar o nome do programa e cada argumento recebido na linha de comando ([Exercício 0](../03-ex0/01-o-problema.md)) |
| 1 | ler pontuações da linha de comando, descartar as que não são números inteiros, guardar as válidas numa lista nova e mostrar quantidade, total, média, maior, menor e a diferença entre maior e menor ([Exercício 1](../04-ex1/01-o-problema.md)) |
| 2 | uma função `get_player_pos()` que pede ao usuário uma posição `x,y,z`, insiste até receber uma válida e a devolve como tupla; o programa lê duas posições e mostra a distância da primeira até o centro `(0, 0, 0)` e a distância entre as duas ([Exercício 2](../05-ex2/01-o-problema.md)) |
| 3 | uma função `gen_player_achievements()` que sorteia um set de conquistas a partir de uma lista fixa; o programa sorteia para pelo menos quatro jogadores e mostra todas as conquistas distintas, as que todos têm, as que só um tem e as que faltam a cada um ([Exercício 3](../06-ex3/01-o-problema.md)) |
| 4 | ler itens no formato `nome:quantidade` da linha de comando, descartar os inválidos e os repetidos, guardar o resto num dicionário e mostrar a lista de itens, o total, a porcentagem de cada item, o mais e o menos abundante, e por fim acrescentar um item novo ([Exercício 4](../07-ex4/01-o-problema.md)) |
| 5 | um generator sem fim `gen_event()` que sorteia eventos `(jogador, ação)`; o programa mostra 1000 eventos, monta uma lista com mais 10, e um segundo generator `consume_event` tira eventos dessa lista ao acaso até ela esvaziar ([Exercício 5](../08-ex5/01-o-problema.md)) |
| 6 | comprehensions que transformam uma lista de nomes, filtram os que já começam com maiúscula, montam um dicionário de pontuações sorteadas e outro só com as pontuações acima da média ([Exercício 6](../09-ex6/01-o-problema.md)) |

Para cada exercício, o enunciado mostra a saída do programa; as sete estão em
[O resultado final](./04-o-resultado-final.md).

## Entrega

Só os sete arquivos `.py`, com esses nomes e nessas pastas, num repositório Git
([Entregar](../10-fechamento/02-entregar.md)). O enunciado também pede que se entendam os
princípios de cada estrutura de dados: saber explicar por que cada coleção foi escolhida,
demonstrar operações com elas e acrescentar uma funcionalidade nova a um dos programas
([Perguntas de revisão](../10-fechamento/03-perguntas-de-revisao.md)).

## O que o enunciado cita sem explicar

- **"Sua jornada pelos fundamentos do Python"**: a introdução do enunciado supõe que quem lê já
  conhece o básico de Python, classes e exceções. O que os exercícios usam disso está nos
  [pré-requisitos](./03-pre-requisitos.md).
- **"A estrutura é parecida com a do C: um array de strings"**: na linguagem C, os argumentos da
  linha de comando chegam ao programa como uma sequência de textos. Não é preciso saber C: a versão
  do Python está no [exercício 0](../03-ex0/02-a-linha-de-comando.md).
- **"Estruturas baseadas em hash"**: o prefácio do enunciado conta que trocar listas por elas
  resolveu problemas de velocidade no Twitter. O que elas são está em
  [A estrutura e o algoritmo](../02-colecoes/03-a-estrutura-e-o-algoritmo.md).
- **Instruções sobre IA**: o enunciado tem um capítulo pedindo que só se use conteúdo gerado por
  IA que se entenda por completo e pelo qual se possa responder, e que todo resultado de IA seja
  conferido, questionado e testado. Código que você não consegue explicar não é código que você
  domina.
