---
sidebar_position: 3
title: As perguntas do enunciado
---

# As perguntas do enunciado

O enunciado deixa quatro perguntas para pensar, em dois quadros *Think About* ("pense nisto"),
com duas perguntas cada: um no exercício 0 e outro no exercício 2. Deixa também duas dicas: uma
na introdução e outra no exercício 1. O enunciado não diz como a avaliação usa essas perguntas.

## Como funciona a conversão automática de tipos do Pydantic?

Cada campo tem um tipo declarado. Quando o valor recebido não é desse tipo, o Pydantic tenta
**convertê-lo** sem perder informação: o texto `"85.5"` vira o `float` `85.5`, o texto `"6"` vira
o `int` `6`, o `int` `85` vira o `float` `85.0`, o texto `"yes"` vira `True`. Uma conversão que
perderia algo, ou que não tem sentido, é recusada com um erro no campo: `6.5` não vira `int` (o
`.5` se perderia), `"high"` não vira número. Esse é o modo leniente, o padrão do Pydantic
([Conversão de tipos](../02-conceitos/04-conversao-de-tipos.md)).

## O que acontece quando se passa um texto de data e hora para um campo datetime?

Se o texto está num formato de data conhecido, como o ISO 8601 (`"2024-01-15T10:30:00"`, ou só
a data, `"2024-01-15"`), o Pydantic o converte num objeto `datetime`, e o campo guarda o
`datetime`, não o texto. Os testes do exercício 0 mostram isso com o próprio `SpaceStation`: o
relatório com `"last_maintenance": "2024-01-15T10:30:00"` vira
`last_maintenance=datetime.datetime(2024, 1, 15, 10, 30)`, e o texto `"soon"` é recusado com
`Input should be a valid datetime or date, input is too short`
([Testar cada limite](../03-ex0/05-rodar-e-conferir.md#testar-cada-limite)).

O mypy enxerga outra coisa: no construtor, ele exige um `datetime` e recusa o texto, mesmo que o
Pydantic fosse convertê-lo. Por isso o texto de data entra pelo `model_validate`, o caminho dos
dados de fora, e o código escrito à mão usa `datetime(...)`
([E pelo construtor?](../02-conceitos/04-conversao-de-tipos.md#e-pelo-construtor)).

## Como o Pydantic trata a validação de modelos aninhados?

Um campo cujo tipo é outro modelo, como `crew: list[CrewMember]`, faz o Pydantic validar cada
item com aquele modelo, com todos os tipos, limites e regras dele. Um item que chega como
dicionário vira um objeto `CrewMember`. Os campos da missão são conferidos um a um; ao chegar em
`crew`, cada tripulante é validado por inteiro. Só quando todos os campos passam, tripulantes
incluídos, rodam as regras do `@model_validator` da missão, que recebem tripulantes prontos
([Modelos aninhados](../02-conceitos/07-modelos-aninhados.md)).

## O que acontece quando um CrewMember falha dentro de uma SpaceMission?

Depende de como o tripulante chega:

- **como dicionário, dentro dos dados da missão** (o caso de dados de fora): a missão inteira é
  recusada com uma `ValidationError` de `SpaceMission`, e o `loc` do erro dá o caminho até o
  campo errado. No teste do exercício 2, um tripulante de 17 anos na posição 1 dá
  `Input should be greater than or equal to 18` com `loc: ('crew', 1, 'age')`
  ([Testar cada regra](../05-ex2/07-rodar-e-conferir.md#testar-cada-regra));
- **como objeto criado com `CrewMember(...)`**: o erro acontece ao criar o tripulante, antes de a
  missão ser chamada, e a `ValidationError` é de `CrewMember`
  ([Modelos aninhados](../02-conceitos/07-modelos-aninhados.md#o-que-aconteceu)).

Nos dois casos, nenhuma missão com um tripulante inválido chega a existir, e as regras da missão
não rodam.

## A dica da introdução

A introdução do enunciado diz que o Pydantic converte tipos compatíveis e dá mensagens de erro
detalhadas. As duas coisas aparecem no projeto: a conversão nas respostas acima, e as mensagens no
relatório da `ValidationError`, que diz o campo, a mensagem, o tipo do erro e o valor recebido
([ValidationError](../02-conceitos/02-validationerror.md#o-que-a-validationerror-traz)).

## A dica do exercício 1

A dica lembra de terminar o método do `@model_validator` com `return self`. Sem ele, o método
devolve `None`: o Pydantic emite um aviso, o `model_validate` devolve `None` no lugar do objeto,
e o mypy acusa `Missing return statement`
([Esquecer o return self](../02-conceitos/06-model-validator.md#esquecer-o-return-self)).

## Comentários e nomes

O enunciado pede que o código mostre o aprendizado com comentários claros e nomes de variáveis
que digam o que guardam. Os comentários dos três arquivos, em inglês como o resto do código,
registram o que não se vê na linha: a conversão do campo de data, por que a estação inválida não
vira objeto, por que as regras podem confiar nos campos, de onde vem a mensagem sem
`Value error, ` e a conta da metade da tripulação. Os nomes seguem o enunciado nos modelos e nos
campos, e dizem o que guardam no resto (`leaders`, `experienced`, `inactive`,
`validation_message`).
