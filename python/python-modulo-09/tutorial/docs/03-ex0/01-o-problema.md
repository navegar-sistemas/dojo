---
sidebar_position: 1
title: O problema
---

# O problema

O observatório recebe, de cada estação espacial, um relatório com o tamanho da tripulação, os
níveis de energia e de oxigênio e o estado da estação. Um relatório com 25 tripulantes numa
estação de 20, ou com 150% de oxigênio, é um erro de transmissão, e não pode entrar no sistema.
O exercício 0 descreve esse relatório como um modelo do Pydantic, com o limite de cada campo.

## O que o enunciado pede

Um arquivo `ex0/space_station.py` com o modelo **`SpaceStation`** e estes campos:

| Campo | Tipo | Regra |
|---|---|---|
| `station_id` | texto | de 3 a 10 caracteres |
| `name` | texto | de 1 a 50 caracteres |
| `crew_size` | inteiro | de 1 a 20 pessoas |
| `power_level` | float | de 0.0 a 100.0 (por cento) |
| `oxygen_level` | float | de 0.0 a 100.0 (por cento) |
| `last_maintenance` | data e hora | a data da última manutenção |
| `is_operational` | booleano | padrão `True` |
| `notes` | texto opcional | no máximo 200 caracteres |

E uma função `main()` que:

1. cria uma estação válida;
2. mostra os dados dela de forma clara;
3. tenta criar uma estação inválida, por exemplo com `crew_size` acima de 20;
4. mostra a mensagem do erro de validação.

O quadro do exercício diz `Authorized: None`; os `import` usados são `pydantic` e `datetime`
([Os `import` permitidos](../00-introducao/02-o-enunciado-em-linguagem-simples.md#os-import-permitidos)).

## A saída esperada

```text
Space Station Data Validation
========================================
Valid station created:
ID: ISS001
Name: International Space Station
Crew: 6 people
Power: 85.5%
Oxygen: 92.3%
Status: Operational

========================================
Expected validation error:
Input should be less than or equal to 20
```

- as duas linhas de `=` têm 40 caracteres;
- a saída mostra seis dos oito campos: `last_maintenance` e `notes` não aparecem. O tutorial
  imprime exatamente essas seis linhas, como no enunciado;
- a última linha é a mensagem que o Pydantic escreve para um valor acima do limite `le=20`
  ([Field e restrições](../02-conceitos/03-field-e-restricoes.md)); o programa não a inventa,
  só a repassa.
