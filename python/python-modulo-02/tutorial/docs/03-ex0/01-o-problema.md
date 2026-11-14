---
sidebar_position: 1
title: O problema
---

# O problema

Sensores de um jardim mandam temperaturas para um programa. A leitura chega como **texto**: às
vezes um número, como `"25"`, às vezes lixo, como `"abc"`, quando o sensor falha ou alguém digita
errado. O programa precisa converter o texto em número e, quando não der, avisar e continuar.

![Uma linha de temperaturas: o texto "25" vira o inteiro 25 e cai na linha; o texto "abc" fica de fora, porque int() lança ValueError antes de existir uma temperatura](/img/ex0/temperaturas.svg)

## O que o enunciado pede

Um arquivo `ex0/ft_first_exception.py`, que só pode chamar as funções prontas `int()` e
`print()`, com:

- uma função **`input_temperature(temp_str)`** que recebe um texto, o converte em número e
  devolve a temperatura como **inteiro**;
- uma função **`test_temperature()`** que testa a primeira com uma entrada válida (`"25"`) e uma
  inválida (`"abc"`), imprime uma mensagem quando `input_temperature` falha e mostra que o
  programa continua depois do erro.

O enunciado deixa escolher o tipo capturado: a classe base `Exception` ou o tipo exato que
`input_temperature` pode lançar. O programa captura o tipo exato, `ValueError`, pelo motivo da
página [Os tipos embutidos](../02-excecoes/06-os-tipos-embutidos.md): capturar só o erro
esperado.

O enunciado também diz que escolher os type hints certos das duas funções fica por sua conta, e
que isso vale para todos os exercícios. Os type hints são obrigatórios; a escolha é de qual tipo
anotar em cada parâmetro e retorno.

## A saída esperada

```text
=== Garden Temperature ===

Input data is '25'
Temperature is now 25°C

Input data is 'abc'
Caught input_temperature error: invalid literal for int() with base 10: 'abc'

All tests completed - program didn't crash!
```

A saída mostra a estrutura do programa: um título; para cada entrada, uma linha vazia, a entrada
entre aspas simples e o resultado (a temperatura ou o erro capturado); por fim, uma linha vazia e
a mensagem de que nada travou.
