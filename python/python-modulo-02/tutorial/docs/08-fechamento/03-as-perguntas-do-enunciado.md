---
sidebar_position: 3
title: As perguntas do enunciado
---

# As perguntas do enunciado

O enunciado deixa perguntas ao longo dos exercícios e avisa que, na avaliação, pode ser pedido
que você explique os conceitos e mostre como os programas lidam com cada problema. Estas são as
perguntas, com as respostas que o projeto construiu.

## Por que o Python tem diferentes tipos de erro?

Porque problemas diferentes pedem reações diferentes. Um texto que não é número pode ser
recusado com uma mensagem; um arquivo ausente pode ser criado; uma divisão por zero pode indicar
um bug. O tipo diz **qual** problema aconteceu, e o `except` escolhe o tipo que sabe tratar,
deixando os outros subirem (páginas [Os tipos embutidos](../02-excecoes/06-os-tipos-embutidos.md)
e [Vários except num try](../05-ex2/04-varios-except.md)).

## Como capturar vários tipos de erro com um único try?

De dois jeitos. Com **vários `except`** depois do mesmo `try`, um por tipo: o Python roda o
primeiro que combina, e cada bloco sabe qual erro capturou. Ou com **uma tupla** de tipos num só
`except`, como `except (ValueError, ZeroDivisionError)`, quando a reação é a mesma para todos. O
exercício 2 usa o primeiro jeito porque precisa escrever o nome de cada tipo e não pode usar
`type()`.

## Capturar Exception ou o tipo exato?

O exercício 0 deixa escolher entre a classe base `Exception` e o tipo que `input_temperature`
lança. `except Exception` captura quase tudo, inclusive erros que ninguém esperava, e os esconde atrás da mesma mensagem. Capturar o tipo exato (`ValueError`)
trata o problema previsto e deixa os imprevistos aparecerem, onde podem ser vistos e corrigidos.

## Quando criar os seus próprios tipos de erro?

Quando o problema é do **assunto do programa** e não da linguagem: uma planta murchando não é um
`ValueError`. Um tipo próprio dá um nome claro ao problema e deixa quem chama capturá-lo sem
confundi-lo com os erros do Python ([Exercício 3](../06-ex3/01-o-problema.md)).

## Como a herança ajuda a organizar os tipos de erro?

Ela forma uma família. `PlantError` e `WaterError` herdam de `GardenError`, então quem quer
tratar qualquer erro do jardim captura só `GardenError`, e quem quer tratar cada caso de um jeito
captura as filhas. Um tipo novo de erro do jardim, criado depois, entra na família e já é
capturado pelo `except GardenError` existente
([Capturar pela base](../06-ex3/06-capturar-pela-base.md)).

## Por que liberar recursos mesmo quando acontecem erros?

Porque o erro não faz o recurso desaparecer: um arquivo continua aberto, uma válvula continua
aberta, e o programa (ou o jardim) paga o preço depois.

## Como o bloco finally ajuda a garantir que a limpeza sempre ocorra?

O `finally` roda em todos os caminhos de saída do `try`: sucesso, erro capturado, erro não
capturado e `return`. Código de limpeza escrito ali não tem como ser pulado
([finally](../07-ex4/02-finally.md)).
