---
sidebar_position: 2
title: List comprehension
---

# List comprehension

Uma lista nova feita a partir de outra, com um laço, segue sempre o mesmo molde: começar vazia,
percorrer, acrescentar.

```python
squares = []
for n in [1, 2, 3, 4, 5]:
    squares.append(n * n)
```

A **list comprehension** escreve o mesmo molde numa linha, entre colchetes:

```python
squares = [n * n for n in [1, 2, 3, 4, 5]]
```

Lê-se "`n * n` para cada `n` da lista". A expressão da esquerda é o que entra na lista nova; o
`for` da direita diz de onde vêm os valores. Um `if` no fim filtra: só entram os valores que
passam no teste.

```python title="experimentos/comprehension.py"
numbers = [1, 2, 3, 4, 5]
print([n * n for n in numbers])
print([n for n in numbers if n % 2 == 0])
print([n * 10 for n in numbers if n > 2])
print(numbers)
```

```bash
python3 experimentos/comprehension.py
```

```text
[1, 4, 9, 16, 25]
[2, 4]
[30, 40, 50]
[1, 2, 3, 4, 5]
```

- `[n * n for n in numbers]` **transforma**: cada elemento vira o seu quadrado;
- `[n for n in numbers if n % 2 == 0]` **filtra**: entram só os pares (`%` é o resto da divisão,
  e um número par tem resto 0 na divisão por 2);
- `[n * 10 for n in numbers if n > 2]` faz os dois: filtra os maiores que 2 e transforma;
- `numbers` não muda: a comprehension cria uma lista **nova**.

## capitalize

O método `capitalize()` de um texto devolve o texto com a primeira letra maiúscula e **todas as
outras minúsculas**:

```python title="experimentos/capitalize.py"
for name in ["bob", "Alice", "ALICE", "mcDonald"]:
    print(name, name.capitalize(), name == name.capitalize())
```

```bash
python3 experimentos/capitalize.py
```

```text
bob Bob False
Alice Alice True
ALICE Alice False
mcDonald Mcdonald False
```

A última coluna compara o nome com a versão corrigida. É `True` só quando `capitalize()` não muda
nada, ou seja, quando o nome **já estava** com a inicial maiúscula e o resto minúsculo. Esse é o
teste que o exercício usa para "o nome já começava com maiúscula", e ele combina com a primeira
comprehension: um nome entra na segunda lista exatamente quando a primeira o deixaria como
estava. Os nomes do exercício são todos só com a inicial, então nomes como `ALICE` não aparecem.

## As duas comprehensions do exercício

```python
capitalized = [name.capitalize() for name in PLAYERS]
already = [name for name in PLAYERS if name == name.capitalize()]
```

| Nome | `capitalized` recebe | entra em `already`? |
|---|---|---|
| `Alice` | `Alice` | sim |
| `bob` | `Bob` | não |
| `Charlie` | `Charlie` | sim |
| `dylan` | `Dylan` | não |

e assim por diante para os nove nomes:

![A lista inicial de nove nomes passa por duas comprehensions. A primeira aplica capitalize a cada nome e devolve os nove com inicial maiúscula: bob vira Bob, dylan vira Dylan, john vira John, kevin vira Kevin. A segunda deixa passar só os nomes que capitalize não muda, Alice, Charlie, Emma, Gregory e Liam, e descarta os outros quatro](/img/ex6/comprehensions.svg)
