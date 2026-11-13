---
sidebar_position: 3
title: A mensagem padrão
---

# A mensagem padrão

Cada erro precisa de uma mensagem padrão, usada quando ele é criado sem mensagem: `PlantError()`
deve ter o texto `Unknown plant error`.

## Um parâmetro com valor padrão

Um parâmetro pode ter um **valor padrão**, usado quando quem chama não passa nada:
`def f(message: str = "Unknown")`. O `__init__`, o método que o Python roda ao criar o objeto,
recebe a mensagem assim e a guarda no próprio objeto:

```python
class PlantError(Exception):
    def __init__(self, message: str = "Unknown plant error") -> None:
        self.message = message
```

`self` é o objeto sendo criado. Um **atributo** é uma variável guardada dentro de um objeto e
lida com ponto, como `self.message`: `self.message = message` guarda a mensagem no objeto. O
`__init__` não devolve nada, por isso `-> None`.

## Só isso não basta

Crie `experimentos/semstr.py` com a classe acima e duas linhas que criam o erro, com e sem
mensagem, e o imprimem. Uma exceção é um objeto como outro qualquer: dá para criá-la sem
lançá-la (sem `raise`) e imprimi-la, só para ver o texto dela:

```python
class PlantError(Exception):
    def __init__(self, message: str = "Unknown plant error") -> None:
        self.message = message


print(f"[{PlantError('The tomato plant is wilting!')}]")
print(f"[{PlantError()}]")
```

```bash
python3 experimentos/semstr.py
```

```text
[The tomato plant is wilting!]
[]
```

Os colchetes mostram onde o texto começa e termina. Com mensagem, funciona; **sem** mensagem, o
texto sai vazio, embora `self.message` guarde `"Unknown plant error"`.

O motivo: toda exceção guarda, sozinha, os argumentos passados na criação sem nome (como o texto
em `PlantError("...")`), num atributo chamado `args`, mesmo que o `__init__` não faça nada com
eles. É desse `args` que o texto da exceção
sai; o atributo `message` é só mais um atributo, que ela não usa. Acrescente estas duas linhas
ao fim de `experimentos/semstr.py`, para ver o `args` de cada erro:

```python
print(PlantError("The tomato plant is wilting!").args)
print(PlantError().args)
```

```bash
python3 experimentos/semstr.py
```

```text
[The tomato plant is wilting!]
[]
('The tomato plant is wilting!',)
()
```

O `args` é uma tupla. Uma tupla de um item só se escreve com uma vírgula no fim,
`('The tomato plant is wilting!',)`, para não ser confundida com um valor entre parênteses.
`PlantError()` foi criado sem argumento nenhum: o `args` é a tupla vazia `()`, e por isso o texto
da exceção sai vazio.

Falta fazer a exceção usar o `self.message` como texto: é o assunto da
[próxima página](./04-o-metodo-str.md).
