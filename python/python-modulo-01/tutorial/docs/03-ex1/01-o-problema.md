---
sidebar_position: 1
title: O problema
---

# O problema

O jardim comunitário agora acompanha várias plantas. Com o jeito do exercício 0, cada planta
precisaria de três variáveis próprias:

```python
rose_name = "Rose"
rose_height = 25
rose_age = 30
sunflower_name = "Sunflower"
sunflower_height = 80
sunflower_age = 45
```

Três plantas são nove variáveis; trinta plantas, noventa. Nada no código diz que `rose_height` e
`rose_age` são da mesma planta, só o nome. E o código que imprime uma planta precisa ser repetido,
ou receber três valores soltos de cada vez. O que falta é um jeito de dizer "toda planta tem
nome, altura e idade, e sabe se mostrar", uma vez só, e depois criar quantas plantas forem
precisas. Esse jeito é a **classe**.

## O que o enunciado pede

Um arquivo `ex1/ft_garden_data.py`, que só pode chamar `print()`, com:

- uma **classe `Plant`** que serve de molde para qualquer planta: toda planta tem um nome, uma
  altura em centímetros e uma idade em dias;
- para cada planta, a classe é **instanciada** (uma planta nova é criada a partir dela) e, **em
  seguida**, os dados daquela planta são preenchidos um por um;
- um **método `show()`** na classe, que imprime os dados da planta;
- pelo menos **três** plantas.

Os nomes dos dados (dos *atributos*) ficam por sua conta.

## A saída esperada

```text
=== Garden Plant Registry ===
Rose: 25cm, 30 days old
Sunflower: 80cm, 45 days old
Cactus: 15cm, 120 days old
```

Um título e uma linha por planta: o nome, dois-pontos, a altura em centímetros e a idade em dias.
As alturas são inteiras (`25cm`, sem casa decimal).

## As perguntas do enunciado

O enunciado pergunta como você está guardando os dados das plantas e que problemas apareceriam
com mais plantas, e avisa que talvez a abordagem precise evoluir nos próximos exercícios. A
resposta deste exercício é a classe; os próximos a melhoram: dados preenchidos na criação
(exercício 3), dados protegidos (exercício 4), tipos especiais de planta (exercício 5).
