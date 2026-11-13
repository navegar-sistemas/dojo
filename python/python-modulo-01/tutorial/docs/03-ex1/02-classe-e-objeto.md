---
sidebar_position: 2
title: Classe e objeto
---

# Classe e objeto

Uma **classe** é um molde: ela descreve que dados e que ações todas as coisas de um tipo têm. A
classe `Plant` diz que toda planta tem nome, altura e idade, e que toda planta sabe se mostrar.
Ela mesma não é nenhuma planta.

Um **objeto** é uma coisa feita a partir do molde, com os seus próprios valores: a rosa, com 25
cm e 30 dias, é um objeto; o girassol, com 80 cm e 45 dias, é outro. Um objeto feito a partir de
uma classe também se chama **instância** dessa classe, e criar um objeto se chama **instanciar**
a classe.

![A classe Plant como um molde com os campos name, height e age_days e o método show(); três linhas saem dela para três objetos, Rose com 25 e 30, Sunflower com 80 e 45, Cactus com 15 e 120](/img/ex1/molde-e-instancias.svg)

## Escrever uma classe

A classe mais simples possível:

```python
class Plant:
    pass
```

- `class` começa a definição; `Plant` é o nome, em `PascalCase` como o enunciado pede (cada
  palavra com inicial maiúscula);
- os dois-pontos e o recuo de quatro espaços marcam o corpo da classe, como num `def`;
- `pass` quer dizer "nada": uma classe precisa ter pelo menos uma linha no corpo, e esta ainda
  não tem nada a dizer.

## Instanciar

Uma classe é chamada como se fosse uma função, com parênteses; cada chamada cria um objeto novo:

```python
rose = Plant()
sunflower = Plant()
```

`rose` e `sunflower` são dois objetos diferentes, cada um com o seu espaço para guardar os seus
próprios dados, guardados nos [atributos](./03-os-atributos.md).
