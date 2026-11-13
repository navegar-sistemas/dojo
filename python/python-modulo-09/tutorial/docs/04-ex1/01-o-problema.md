---
sidebar_position: 1
title: O problema
---

# O problema

O observatório recebe relatos de contato com alienígenas. Conferir cada campo sozinho não basta:
um relato de contato físico que ninguém verificou, ou um contato telepático com uma única
testemunha, tem todos os campos dentro dos limites e mesmo assim é suspeito. O exercício 1 junta
os limites de campo do exercício 0 com **regras de negócio**: regras do assunto tratado (aqui, os
relatos de contato) que comparam campos entre si.

## O que o enunciado pede

Um arquivo `ex1/alien_contact.py` com três peças.

**O Enum `ContactType`**, com os tipos de contato `radio`, `visual`, `physical` e `telepathic`
([Enum](../02-conceitos/05-enum.md)).

**O modelo `AlienContact`**, com estes campos:

| Campo | Tipo | Regra |
|---|---|---|
| `contact_id` | texto | de 5 a 15 caracteres |
| `timestamp` | data e hora | o momento do contato |
| `location` | texto | de 3 a 100 caracteres |
| `contact_type` | `ContactType` | um dos quatro tipos |
| `signal_strength` | float | de 0.0 a 10.0 (a força do sinal) |
| `duration_minutes` | inteiro | de 1 a 1440 (no máximo 24 horas) |
| `witness_count` | inteiro | de 1 a 100 (o número de testemunhas) |
| `message_received` | texto opcional | no máximo 500 caracteres (a mensagem recebida) |
| `is_verified` | booleano | padrão `False` (se o relato foi verificado) |

**Quatro regras**, num `@model_validator(mode='after')`
([model_validator](../02-conceitos/06-model-validator.md)):

1. o `contact_id` começa com `"AC"` (de *Alien Contact*);
2. um contato `physical` precisa estar verificado (`is_verified` verdadeiro);
3. um contato `telepathic` precisa de pelo menos 3 testemunhas;
4. um sinal forte, acima de 7.0, precisa trazer uma mensagem recebida.

A quarta regra diz *should include* ("deveria incluir"), e não *must* ("precisa"). Escolha do
tutorial: tratar as quatro como obrigatórias, porque o enunciado as lista juntas como regras de
validação.

**Uma demonstração** que mostra um relato válido e um inválido, com mensagens de erro claras. Os
`import` são `pydantic`, `datetime` e `enum`
([Os `import` permitidos](../00-introducao/02-o-enunciado-em-linguagem-simples.md#os-import-permitidos)).

## A saída esperada

```text
Alien Contact Log Validation
======================================
Valid contact report:
ID: AC_2024_001
Type: radio
Location: Area 51, Nevada
Signal: 8.5/10
Duration: 45 minutes
Witnesses: 5
Message: 'Greetings from Zeta Reticuli'

======================================
Expected validation error:
Telepathic contact requires at least 3 witnesses
```

- as linhas de `=` têm 38 caracteres;
- o relato válido tem sinal 8.5, acima de 7.0, e por isso traz uma mensagem: a quarta regra passa;
- a mensagem aparece entre aspas simples;
- a última linha é a mensagem da terceira regra, escrita pelo próprio código, e aparece sem
  nenhum acréscimo do Pydantic ([A mensagem do erro](./04-a-mensagem-do-erro.md)).

O enunciado fala em relatos válidos e inválidos, no plural, mas a saída esperada mostra um de
cada. O tutorial segue a saída; os outros casos inválidos ficam nos testes de
[Rodar e conferir](./07-rodar-e-conferir.md).
