---
sidebar_position: 2
title: O método estático
---

# O método estático

A pergunta "30 dias é mais que um ano?" não depende de planta nenhuma: a resposta só usa o
número de dias. Um método comum recebe o objeto no `self`, e para chamá-lo seria preciso ter uma
planta. Um **método estático** não recebe nem o objeto nem a classe: é uma função comum, guardada
dentro da classe porque o assunto dela é da classe.

## O decorador @staticmethod

```python
    @staticmethod
    def is_older_than_a_year(age_days: int) -> bool:
        return age_days > 365
```

- a linha `@staticmethod`, logo antes do `def`, é um **decorador**: ela passa o método pela função
  `staticmethod()`, uma das autorizadas, que o transforma em método estático. O enunciado aceita
  essa sintaxe;
- não há `self`: o único parâmetro é a idade em dias;
- `age_days > 365` devolve `True` ou `False`. Um ano tem 365 dias, então 365 dias é exatamente um
  ano, e não **mais** que um ano; só a partir de 366 a resposta é `True`.

Ele é chamado pela classe, sem objeto nenhum: `Plant.is_older_than_a_year(30)`.

## Um experimento

```python title="experimentos/estatico.py"
class Plant:
    @staticmethod
    def is_older_than_a_year(age_days: int) -> bool:
        return age_days > 365


print(Plant.is_older_than_a_year(30))
print(Plant.is_older_than_a_year(400))
```

```bash
python3 experimentos/estatico.py
```

```text
False
True
```

A classe nem tem construtor, e nenhuma planta foi criada: a pergunta foi feita à classe.

## No programa

A saída pergunta por 30 e por 400 dias, e cada linha repete o número perguntado:

```python
    print("=== Check year-old")
    for days in (30, 400):
        older = Plant.is_older_than_a_year(days)
        print(f"Is {days} days more than a year? -> {older}")
```

`(30, 400)` é uma tupla com as duas idades. Um `bool` dentro de uma f-string vira o texto `True`
ou `False`.
