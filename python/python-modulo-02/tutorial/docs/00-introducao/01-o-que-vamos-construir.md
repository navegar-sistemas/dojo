---
slug: /
sidebar_position: 1
title: O que vamos construir
---

# O que vamos construir

Todo programa encontra situações em que algo dá errado: o usuário digita uma letra onde se
esperava um número, um arquivo não existe, uma conta divide por zero. Em Python, cada uma dessas
situações gera uma **exceção**, um aviso de erro que, se ninguém tratar, encerra o programa na
hora. Este tutorial ensina a **tratar** esses avisos, para que o programa perceba o erro, diga o
que aconteceu e continue funcionando.

O projeto se chama **Garden Guardian** ("guardião do jardim"). O tema é um jardim monitorado por
computador: sensores mandam temperaturas, um sistema de irrigação rega as plantas. O tema só dá
nome às coisas; o assunto de verdade é o tratamento de erros em Python.

## Cinco programas pequenos

O projeto tem cinco **exercícios**. Cada um é um programa de um arquivo só, numa pasta própria, e
cada um ensina uma ferramenta nova:

| Exercício | Arquivo | O que ensina |
|---|---|---|
| 0 | `ex0/ft_first_exception.py` | **capturar** um erro com `try` e `except`, para o programa não parar |
| 1 | `ex1/ft_raise_exception.py` | **lançar** um erro de propósito com `raise`, quando um valor não serve |
| 2 | `ex2/ft_different_errors.py` | os **tipos** diferentes de erro e como separar cada um |
| 3 | `ex3/ft_custom_errors.py` | **criar** os seus próprios tipos de erro |
| 4 | `ex4/ft_finally_block.py` | o bloco `finally`, que roda **sempre**, com erro ou sem erro |

Os programas não leem nada do teclado: cada um roda uma pequena demonstração, com casos que dão
certo e casos que dão errado, e imprime o que aconteceu. Um exemplo, o exercício 0 rodando:

```text
=== Garden Temperature ===

Input data is '25'
Temperature is now 25°C

Input data is 'abc'
Caught input_temperature error: invalid literal for int() with base 10: 'abc'

All tests completed - program didn't crash!
```

O texto `"abc"` não é um número, a conversão falha, e o programa avisa o erro e chega ao fim em
vez de parar no meio. As mensagens são em inglês porque o enunciado do projeto mostra a saída
exata de cada programa, e essa saída é em inglês.

## O enunciado

O projeto vem com um documento oficial que diz o que precisa ser entregue: o **enunciado** (em
inglês, *subject*). Este tutorial não pressupõe que você o leu: a
[próxima página](./02-o-enunciado-em-linguagem-simples.md) resume tudo o que ele pede, e cada
regra é explicada de novo na página que a cumpre.

## Como o tutorial avança

| Parte | O que ela faz |
|---|---|
| Ambiente | prepara o Python, a pasta do projeto e as duas ferramentas que conferem o código (flake8 e mypy) |
| O que é uma exceção | explica, com exemplos pequenos, o que acontece quando um erro aparece e como capturá-lo |
| Exercícios 0 a 4 | constroem os cinco programas, um por parte |
| Fechamento | confere tudo, mostra como entregar e responde às perguntas que o enunciado deixa para você pensar |

O código de cada exercício aparece em pedaços e, no fim, o arquivo completo. Os termos novos
estão reunidos no [glossário](./05-glossario.md).
