---
sidebar_position: 2
title: Lendo o traceback
---

# Lendo o traceback

O relatório que o Python imprime quando um programa trava se chama **traceback** ("rastro de
volta"). Ele diz **onde** o erro aconteceu e **qual** foi o erro. O da
[página anterior](./01-o-programa-que-trava.md):

```text
Traceback (most recent call last):
  File "/…/garden-guardian/experimentos/trava.py", line 2, in <module>
    temperature = int("abc")
ValueError: invalid literal for int() with base 10: 'abc'
```

| Linha | O que diz |
|---|---|
| `Traceback (most recent call last):` | começa o relatório; "a chamada mais recente por último" quer dizer que a linha mais perto do erro vem no fim |
| `File "…/trava.py", line 2, in <module>` | o arquivo e a linha onde o erro aconteceu. `<module>` quer dizer "no corpo do arquivo", fora de qualquer função |
| `temperature = int("abc")` | o código daquela linha |
| `ValueError: invalid literal for int() with base 10: 'abc'` | **o erro**: o tipo, antes dos dois-pontos, e a mensagem, depois |

## O erro tem um tipo e uma mensagem

A última linha é a mais importante. Ela tem duas partes:

- **`ValueError`** é o **tipo** do erro. `ValueError` ("erro de valor") é o tipo que o Python usa
  quando uma função recebe um valor do tipo certo (um texto, para o `int()`) mas com um conteúdo
  que ela não aceita;
- **`invalid literal for int() with base 10: 'abc'`** é a **mensagem**, escrita por quem lançou o
  erro, aqui o próprio `int()`: "texto inválido para `int()` na base 10: `'abc'`". A "base 10" é
  a dos números comuns, com os dígitos de 0 a 9.

## O erro é um objeto: a exceção

Quando o `int()` percebe que não consegue converter, ele cria um **objeto** que descreve o
problema e o **lança** (*raise*). Esse objeto se chama **exceção**. Como todo objeto em Python,
ele tem uma classe, que é o tipo do erro (`ValueError`), e guarda a mensagem.

Uma exceção lançada interrompe o código que estava rodando. Se nenhum trecho do programa a
**capturar**, o Python imprime o traceback e encerra o programa. A
[próxima página](./03-try-e-except.md) mostra como capturar.
