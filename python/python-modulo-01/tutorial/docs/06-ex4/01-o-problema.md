---
sidebar_position: 1
title: O problema
---

# O problema

Na classe do exercício 3, qualquer linha do programa pode escrever qualquer valor numa planta:
`rose.height = -10` é aceito sem reclamação, e a rosa passa a ter altura negativa. Voluntários do
jardim fizeram exatamente isso, por engano, e corromperam os dados. A classe precisa **proteger**
os dados dela: só aceitar mudanças que façam sentido.

## O que o enunciado pede

Um arquivo `ex4/ft_garden_security.py`, que só pode chamar `print()`, `range()` e `round()`, com
a classe `Plant` melhorada para:

- oferecer **formas controladas de mudar** os dados: os métodos `set_height()` e `set_age()`;
- oferecer **formas seguras de ler** os dados: os métodos `get_height()` e `get_age()`;
- **recusar** altura negativa e idade negativa;
- **imprimir uma mensagem de erro a partir da classe** quando um valor inválido chega, deixando
  o dado como estava, ou, na criação da planta, usando um valor padrão;
- usar **encapsulamento**: os atributos não devem ser usados diretamente de fora da classe, e a
  marca para isso é a **convenção "protected"**, não o *name mangling*.

## A saída esperada

```text
=== Garden Security System ===
Plant created: Rose: 15.0cm, 10 days old

Height updated: 25cm
Age updated: 30 days

Rose: Error, height can't be negative
Height update rejected
Rose: Error, age can't be negative
Age update rejected

Current state: Rose: 25.0cm, 30 days old
```

O programa cria uma rosa de 15 cm e 10 dias, muda a altura para 25 cm e a idade para 30 dias
(as duas mudanças são aceitas), tenta valores negativos (as duas são recusadas, cada uma com o
erro e o aviso de recusa) e mostra que a rosa continua com 25 cm e 30 dias. Linhas vazias separam
as quatro etapas.
