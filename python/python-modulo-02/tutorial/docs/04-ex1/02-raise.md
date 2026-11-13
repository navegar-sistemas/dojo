---
sidebar_position: 2
title: raise
---

# raise

Até aqui, quem lançava as exceções era o Python (o `int()`). O seu código também pode lançar uma,
com a palavra **`raise`** ("levantar"):

```python
raise ValueError("a mensagem do erro")
```

- `ValueError("a mensagem do erro")` cria o objeto da exceção, com a mensagem escolhida;
- `raise` o lança. Dali em diante, tudo funciona como num erro do próprio Python: a função para
  na hora, a exceção sobe até um `except` que a aceite, e a mensagem é a que você escreveu.

Um experimento, `experimentos/lanca.py`, com uma função que recusa umidades acima de 100%:

```python
def check_humidity(humidity: int) -> int:
    if humidity > 100:
        raise ValueError(f"{humidity}% is not a valid humidity")
    return humidity


print(check_humidity(80))
try:
    check_humidity(120)
except ValueError as error:
    print(f"Caught: {error}")
```

```bash
python3 experimentos/lanca.py
```

```text
80
Caught: 120% is not a valid humidity
```

Com `80`, o `if` é falso e a função devolve o valor. Com `120`, o `raise` interrompe a função
antes do `return`: ela não devolve nada, e quem a chamou recebe a exceção.

## Por que lançar em vez de imprimir?

A função poderia imprimir "temperatura inválida" e devolver algum número. Mas que número? Qualquer
valor devolvido seria tratado como uma temperatura de verdade por quem chamou. Lançar a exceção
obriga quem chamou a perceber o problema, e deixa a decisão do que fazer com quem tem contexto
para isso, a função de teste.

## Por que ValueError?

Uma temperatura de 100 graus é um número inteiro (o tipo certo) com um valor que a função não
aceita. É a definição de `ValueError` da página
[Lendo o traceback](../02-excecoes/02-lendo-o-traceback.md). Há uma segunda vantagem: o
`int("abc")` também lança `ValueError`, então o **mesmo** `except ValueError` da função de teste
captura os dois casos, o texto que não é número e o número fora da faixa.
