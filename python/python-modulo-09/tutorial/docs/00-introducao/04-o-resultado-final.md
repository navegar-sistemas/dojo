---
sidebar_position: 4
title: O resultado final
---

# O resultado final

Esta é a saída de cada programa pronto, igual à do enunciado. Os programas não recebem
argumentos nem leem o teclado: cada um roda uma demonstração fixa. Os comandos são rodados na
pasta do projeto ([A pasta do projeto](../01-ambiente/02-a-pasta-do-projeto.md)), com o Python do
ambiente virtual, `.venv/bin/python`, que é onde o Pydantic está instalado
([O ambiente virtual](../01-ambiente/03-o-ambiente-virtual.md)). Eles só funcionam depois que os
arquivos existirem: a página "Rodar e conferir" de cada exercício os roda.

## Exercício 0

```bash
.venv/bin/python ex0/space_station.py
```

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

A segunda parte é a tentativa de criar uma estação com 25 tripulantes: o limite é 20, e a
mensagem é a do próprio Pydantic.

## Exercício 1

```bash
.venv/bin/python ex1/alien_contact.py
```

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

## Exercício 2

```bash
.venv/bin/python ex2/space_crew.py
```

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

As linhas de `=` não têm o mesmo tamanho nos três programas: 40 no exercício 0, 38 no 1 e 41 no
2, como no enunciado.
