---
sidebar_position: 3
title: Os limites
---

# Os limites

A nova `input_temperature` converte o texto e confere a faixa antes de devolver:

```python
MIN_TEMPERATURE = 0
MAX_TEMPERATURE = 40


def input_temperature(temp_str: str) -> int:
    temperature = int(temp_str)
    if temperature > MAX_TEMPERATURE:
        raise ValueError(
            f"{temperature}°C is too hot for plants (max {MAX_TEMPERATURE}°C)"
        )
    if temperature < MIN_TEMPERATURE:
        raise ValueError(
            f"{temperature}°C is too cold for plants (min {MIN_TEMPERATURE}°C)"
        )
    return temperature
```

## As constantes

`MIN_TEMPERATURE` e `MAX_TEMPERATURE` guardam os limites no topo do arquivo. Os nomes em
maiúsculas são o costume do Python para **constantes**, valores que o programa nunca muda. Com
elas, o limite aparece escrito uma vez só e as mensagens usam o mesmo valor que o `if` confere:
mudar a faixa é mudar uma linha.

## A ordem das conferências

1. `int(temp_str)` vem primeiro. Se o texto não for número, ele lança o `ValueError` dele e as
   linhas seguintes nem rodam. Não há faixa a conferir para algo que não é número.
2. `temperature > MAX_TEMPERATURE`: acima de 40, lança "quente demais".
3. `temperature < MIN_TEMPERATURE`: abaixo de 0, lança "fria demais".
4. Se chegou ao `return`, o valor está na faixa.

## Os limites incluídos

O enunciado manda aceitar 0 e 40. Por isso as comparações são `>` e `<`, não `>=` e `<=`:
`40 > 40` é falso, então 40 passa; `0 < 0` é falso, então 0 passa. Já 41 e -1 são recusados.

| Valor | `> 40`? | `< 0`? | Resultado |
|---|---|---|---|
| `-1` | não | sim | "too cold" |
| `0` | não | não | aceito |
| `25` | não | não | aceito |
| `40` | não | não | aceito |
| `41` | sim | (não chega a conferir) | "too hot" |

## As mensagens

As mensagens repetem o formato do enunciado: o valor lido, `°C`, o motivo e, entre parênteses, o
limite. A string é longa, então fica numa linha própria, dentro dos parênteses do `ValueError(`;
assim nenhuma linha passa de 79 caracteres, o limite que o flake8 confere.
