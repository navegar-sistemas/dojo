---
sidebar_position: 1
title: O problema
---

# O problema

Uma missão espacial só é aprovada para o lançamento se a tripulação cumprir as regras de
segurança: alguém no comando, gente experiente nas viagens longas, ninguém afastado. Para
conferir isso, a missão precisa conhecer cada tripulante, e cada tripulante tem os seus próprios
campos e limites. O exercício 2 descreve o tripulante como um modelo e a missão como outro
modelo, que guarda uma lista de tripulantes: modelos **aninhados**
([Modelos aninhados](../02-conceitos/07-modelos-aninhados.md)).

## O que o enunciado pede

Um arquivo `ex2/space_crew.py` com quatro peças.

**O Enum `Rank`**, com as patentes `cadet` (cadete), `officer` (oficial), `lieutenant`
(tenente), `captain` (capitão) e `commander` (comandante).

**O modelo `CrewMember`**, de um tripulante:

| Campo | Tipo | Regra |
|---|---|---|
| `member_id` | texto | de 3 a 10 caracteres |
| `name` | texto | de 2 a 50 caracteres |
| `rank` | `Rank` | uma das cinco patentes |
| `age` | inteiro | de 18 a 80 anos |
| `specialization` | texto | de 3 a 30 caracteres (a especialidade) |
| `years_experience` | inteiro | de 0 a 50 anos de experiência |
| `is_active` | booleano | padrão `True` (se o tripulante está na ativa) |

**O modelo `SpaceMission`**, de uma missão:

| Campo | Tipo | Regra |
|---|---|---|
| `mission_id` | texto | de 5 a 15 caracteres |
| `mission_name` | texto | de 3 a 100 caracteres |
| `destination` | texto | de 3 a 50 caracteres |
| `launch_date` | data e hora | a data do lançamento |
| `duration_days` | inteiro | de 1 a 3650 dias (no máximo 10 anos) |
| `crew` | lista de `CrewMember` | de 1 a 12 tripulantes |
| `mission_status` | texto | padrão `"planned"` (planejada) |
| `budget_millions` | float | de 1.0 a 10000.0 (o orçamento, em milhões de dólares) |

**Quatro regras de segurança**, num `@model_validator(mode='after')` de `SpaceMission`:

1. o `mission_id` começa com `"M"`;
2. a tripulação tem pelo menos um `commander` ou um `captain`;
3. uma missão longa, de mais de 365 dias, precisa de 50% de tripulação experiente: com 5 anos ou
   mais de experiência;
4. todos os tripulantes estão na ativa.

**Uma demonstração** com uma missão válida, mostrando a tripulação, e uma inválida. Os `import`
são os mesmos do exercício 1.

## A saída esperada

```text
Space Mission Crew Validation
=========================================
Valid mission created:
Mission: Mars Colony Establishment
ID: M2024_MARS
Destination: Mars
Duration: 900 days
Budget: $2500.0M
Crew size: 3
Crew members:
- Sarah Connor (commander) - Mission Command
- John Smith (lieutenant) - Navigation
- Alice Johnson (officer) - Engineering

=========================================
Expected validation error:
Mission must have at least one Commander or Captain
```

- as linhas de `=` têm 41 caracteres;
- a missão válida dura 900 dias, mais de 365: a regra 3 vale para ela, e a tripulação precisa ser
  pelo menos metade experiente. A saída não mostra os anos de experiência, que ficam por conta da
  demonstração ([A demonstração](./05-a-demonstracao.md));
- o orçamento aparece como `$2500.0M`: o `float` 2500.0 entre `$` e `M` (de milhões);
- a regra 2 está escrita no enunciado como *Must have at least one Commander or Captain*, e a
  saída mostra *Mission must have at least one Commander or Captain*, com `Mission` na frente. O
  tutorial usa o texto da saída, que é o que dá para conferir com o `diff`.
