---
sidebar_position: 2
title: O construtor
---

# O construtor

Um **construtor** é o método que o Python chama sozinho no momento em que um objeto é criado.
Em Python, ele tem um nome fixo: `__init__` (de *initialize*, "inicializar"), com dois `_` de
cada lado. Os valores passados entre os parênteses da classe, em `Plant("Rose", 25.0)`, chegam
como parâmetros do `__init__`.

## Um experimento

```python title="experimentos/construtor.py"
class Plant:
    def __init__(self, name: str, height: float) -> None:
        print(f"__init__ recebeu {name} e {height}")
        self.name = name
        self.height = height


rose = Plant("Rose", 25.0)
print(rose.name, rose.height)
```

```bash
python3 experimentos/construtor.py
```

```text
__init__ recebeu Rose e 25.0
Rose 25.0
```

Ninguém escreveu `rose.__init__(...)`: a linha `rose = Plant("Rose", 25.0)` criou o objeto e
chamou o `__init__` com ele no `self`, `"Rose"` em `name` e `25.0` em `height`. Quando a linha
termina, a planta já tem os dois atributos preenchidos.

## Os atributos nascem no construtor

`self.name = name` cria o atributo `name` no objeto novo e guarda nele o valor do parâmetro de
mesmo nome. Os dois `name` são coisas diferentes: `self.name` é o atributo, que fica no objeto
depois que o `__init__` termina; `name` é o parâmetro, que só existe durante a chamada.

As declarações do corpo da classe (`name: str`, do exercício 1) deixam de ser necessárias: o mypy
lê o `__init__` e descobre os atributos e os tipos deles pelos parâmetros, que já têm type hints.
O `__init__` devolve `None`, como todo construtor.

## O construtor da planta

```python
class Plant:
    def __init__(self, name: str, height: float, age_days: int) -> None:
        self.name = name
        self.height = height
        self.age_days = age_days
```

Com ele, `Plant("Rose", 25.0, 30)` cria uma rosa completa: 25 cm, 30 dias, pronta para `show()`,
`grow()` e `age()`.

Instanciar sem os dados agora é um erro: `Plant()` faz o Python reclamar que faltam os argumentos
`name`, `height` e `age_days`, e o mypy aponta o mesmo erro antes mesmo de rodar. Toda planta
nasce completa, ou não nasce.
