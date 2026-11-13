---
sidebar_position: 2
title: garden_operations
---

# garden_operations

A função escolhe, pelo número recebido, qual trecho defeituoso roda:

```python
def garden_operations(operation_number: int) -> None:
    if operation_number == 0:
        int("abc")
    elif operation_number == 1:
        1 / 0
    elif operation_number == 2:
        open("/non/existent/file")
    elif operation_number == 3:
        # mypy reports this line on purpose: it is the TypeError being shown
        "abc" + 5
```

Ela não devolve nada (`-> None`). O resultado de cada operação nem é guardado, porque nenhuma
delas chega a produzir um resultado: o que interessa é o erro.

## Operação 0: ValueError

`int("abc")` é o mesmo erro dos exercícios anteriores: o texto não é um número.

```text
ValueError: invalid literal for int() with base 10: 'abc'
```

## Operação 1: ZeroDivisionError

`1 / 0` divide por zero, uma conta sem resultado.

```text
ZeroDivisionError: division by zero
```

## Operação 2: FileNotFoundError

`open(caminho)` abre um arquivo para leitura e devolve um objeto com o qual se lê o conteúdo. O
caminho `/non/existent/file` ("arquivo inexistente") não existe em nenhum sistema comum, então o
`open()` lança:

```text
FileNotFoundError: [Errno 2] No such file or directory: '/non/existent/file'
```

`[Errno 2]` é o número que o sistema operacional dá a "arquivo ou pasta não encontrado".

Um arquivo aberto precisa ser fechado depois, com `.close()`. O enunciado lembra que, se o
arquivo não foi aberto, não é preciso chamar `close()`: é o caso aqui, porque o `open()` falhou
e nenhum arquivo chegou a ser aberto.

## Operação 3: TypeError

`"abc" + 5` tenta somar um texto com um número. Entre dois textos, o `+` junta (`"ab" + "c"` dá
`"abc"`); entre dois números, soma. Entre um texto e um número, o Python não adivinha qual dos
dois se quer e lança:

```text
TypeError: can only concatenate str (not "int") to str
```

"Só é possível concatenar (juntar) `str` a `str`, não `int`." O comentário acima da linha explica
para quem lê o código por que o mypy reclama dela, assunto da
[próxima página](./03-o-erro-proposital-do-mypy.md).

## Os outros números

Para `4` ou qualquer outro valor, nenhum `if` é verdadeiro, a função chega ao fim e retorna sem
erro, como o enunciado pede.

## Por que essas operações soltas são aceitas

Uma linha como `1 / 0`, sozinha, calcula um valor e o joga fora. Em código de verdade isso seria
estranho, mas o flake8 não reclama, e aqui é exatamente a intenção: executar a operação só para
ver o erro.
