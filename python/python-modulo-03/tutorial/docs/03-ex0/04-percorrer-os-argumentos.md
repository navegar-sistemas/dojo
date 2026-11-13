---
sidebar_position: 4
title: Percorrer os argumentos
---

# Percorrer os argumentos

Cada argumento sai numa linha com o seu número: `Argument 1: hello`, `Argument 2: world`. O `for`
percorre os elementos, mas não diz em que posição está. O número vem de um **contador**: uma
variável que começa em 1 e cresce a cada volta.

```python
arguments = sys.argv[1:]
number = 1
for argument in arguments:
    print(f"Argument {number}: {argument}")
    number += 1
```

- `arguments` é a fatia só com os argumentos, sem o nome do programa;
- `number += 1` é uma forma curta de `number = number + 1`;
- na primeira volta, `argument` é `"hello"` e `number` é 1; na segunda, `"world"` e 2; na
  terceira, `"42"` e 3.

## Antes do laço: há argumentos?

Sem argumentos, o programa imprime `No arguments provided!` em vez da contagem e da lista:

```python
if len(arguments) == 0:
    print("No arguments provided!")
else:
    print(f"Arguments received: {len(arguments)}")
    # o laço acima
```

`len(arguments)` é a quantidade de argumentos. `len(sys.argv)` é essa quantidade mais um, o nome
do programa, e é o número da linha final, `Total arguments`.

## Outra forma: o índice como número

Os números das linhas coincidem com os índices em `sys.argv`: `hello` está no índice 1 e sai como
`Argument 1`. Um `while` que anda pelos índices dispensa a fatia e o contador:

```python
index = 1
while index < len(sys.argv):
    print(f"Argument {index}: {sys.argv[index]}")
    index += 1
```

O laço começa no índice 1, pulando o nome do programa, e para quando `index` chega a
`len(sys.argv)`, o primeiro índice que não existe. As duas formas imprimem o mesmo, e o arquivo
completo usa a primeira, com a fatia. O enunciado lembra que há várias formas de não imprimir o
nome do programa de novo no meio dos argumentos (ele está em `sys.argv[0]`) e pede que se
conheçam as alternativas: estas duas são exemplos, e outras estão nas
[Perguntas de revisão](../10-fechamento/03-perguntas-de-revisao.md#como-não-repetir-o-nome-do-programa-exercício-0).

As funções `range()` e `enumerate()`, que o Python oferece para contar voltas, não estão na lista
de autorizadas deste exercício.
