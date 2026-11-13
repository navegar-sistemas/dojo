---
sidebar_position: 3
title: Cinco plantas
---

# Cinco plantas

Com o construtor, cada planta cabe numa expressão, e as cinco cabem numa **lista**:

```python
    plants = [
        Plant("Rose", 25.0, 30),
        Plant("Oak", 200.0, 365),
        Plant("Cactus", 5.0, 90),
        Plant("Sunflower", 80.0, 45),
        Plant("Fern", 15.0, 120),
    ]
```

- os colchetes formam uma lista com os cinco objetos, na ordem da saída;
- cada `Plant(...)` cria uma planta completa; nenhuma precisa de variável própria, porque a lista
  as guarda;
- a vírgula depois do último item é permitida e é o costume quando cada item fica numa linha: uma
  planta acrescentada depois não mexe na linha anterior;
- as alturas são escritas com `.0`, pelo motivo da página
  [O float e o round](../04-ex2/03-o-float-e-o-round.md).

São cinco plantas de tamanhos bem diferentes, de um cacto de 5 cm a um carvalho de 2 m:

![As cinco plantas da fábrica como barras na mesma escala: Rose 25 cm, Oak 200 cm, Cactus 5 cm, Sunflower 80 cm e Fern 15 cm, cada uma com a idade em dias embaixo](/img/ex3/fabrica.svg)

Um laço `for` percorre a lista, uma planta por volta:

```python
    for plant in plants:
        plant.show()
```

O mypy sabe que `plants` é uma lista de `Plant` (todos os itens são `Plant`), e por isso aceita
`plant.show()`.
