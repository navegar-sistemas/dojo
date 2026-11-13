---
sidebar_position: 2
title: Gerar os dados
---

# Gerar os dados

## O resumo do gerador

```bash
.venv/bin/python tools/data_generator.py
```

```text
🚀 Cosmic Data Observatory - Sample Data Generator
============================================================

📡 Generated 5 space stations:
  LGW125: Titan Mining Outpost - ✅ Operational
  QCH189: Deep Space Observatory - ⚠️  Maintenance
  ISS674: Europa Research Station - ✅ Operational
  ISS877: Mars Orbital Platform - ⚠️  Maintenance
  LGW194: Deep Space Observatory - ⚠️  Maintenance

👽 Generated 6 alien contacts:
  AC_2024_001: visual at Atacama Desert, Chile - ❓ Unverified
  AC_2024_002: radio at Mauna Kea Observatory, Hawaii - ❓ Unverified
  AC_2024_003: telepathic at Very Large Array, New Mexico - ❓ Unverified
  AC_2024_004: telepathic at Roswell, New Mexico - ❓ Unverified
  AC_2024_005: telepathic at SETI Institute, California - ❓ Unverified
  AC_2024_006: radio at Area 51, Nevada - ❓ Unverified

🚀 Generated 3 space missions:
  M2024_TITAN: Solar Observatory Research Mission
    Crew: 5 members, Duration: 451 days
  M2024_MARS: Jupiter Orbit Colony Mission
    Crew: 4 members, Duration: 1065 days
  M2024_EUROPA: Europa Colony Mission
    Crew: 5 members, Duration: 666 days

============================================================
Data generation complete! Use these generators in your exercises.
```

O gerador não precisa do Pydantic; o Python do venv é usado aqui só para manter um único jeito de
rodar os programas do projeto. Com a semente fixa, a saída é a mesma em toda execução
([As ferramentas](./01-as-ferramentas.md#data_generatorpy)). Os símbolos coloridos são
**emojis**, caracteres de texto como os outros; o terminal os desenha.

## Gravar os arquivos

O `data_exporter.py` grava a pasta `generated_data/` na pasta de onde é rodado. Para que ela fique
dentro de `tools`, o programa é rodado de dentro de `tools`:

```bash
(cd tools && ../.venv/bin/python -B data_exporter.py)
```

```text
🔄 Generating complete datasets...
✅ Generated 8 data files:
  📄 generated_data/space_stations.json
  📄 generated_data/space_stations.py
  📄 generated_data/space_stations.csv
  📄 generated_data/alien_contacts.json
  📄 generated_data/alien_contacts.py
  📄 generated_data/alien_contacts.csv
  📄 generated_data/space_missions.json
  📄 generated_data/space_missions.py
🧪 Created validation test scenarios

🎯 All data files ready for testing!
```

- os parênteses rodam os comandos de dentro deles num terminal à parte (um *subshell*): o `cd
  tools` só vale ali dentro, e o terminal continua na pasta `cosmic-data` depois do comando;
- `&&` roda o segundo comando só se o primeiro deu certo;
- de dentro de `tools`, o Python do venv fica em `../.venv/bin/python` (`..` é a pasta de cima);
- o `-B` impede que o Python grave em `tools` a pasta de cache `__pycache__`, que ele criaria ao
  importar o `data_generator`.

A lista impressa tem 8 arquivos; os dois de casos inválidos são gravados depois, na linha
`Created validation test scenarios`. A pasta fica com 10:

```bash
ls -1 tools/generated_data
```

```text
alien_contacts.csv
alien_contacts.json
alien_contacts.py
invalid_contacts.json
invalid_stations.json
space_missions.json
space_missions.py
space_stations.csv
space_stations.json
space_stations.py
```

## Um registro

O começo de `space_stations.json`, com a primeira estação. `head -11` mostra as 11 primeiras
linhas de um arquivo:

```bash
head -11 tools/generated_data/space_stations.json
```

```text
[
  {
    "station_id": "LGW125",
    "name": "Titan Mining Outpost",
    "crew_size": 6,
    "power_level": 76.4,
    "oxygen_level": 95.5,
    "last_maintenance": "2023-07-11T00:00:00",
    "is_operational": true,
    "notes": null
  },
```

As chaves são os nomes dos campos de `SpaceStation`, e os valores estão no formato em que dados
chegam de fora: a data é um texto no formato ISO 8601, e o `null` do JSON vira `None` no Python.
É o caso para o qual o `model_validate` existe
([Conversão de tipos](../02-conceitos/04-conversao-de-tipos.md#e-pelo-construtor)).

## Os casos inválidos

`invalid_contacts.json` tem dois relatos montados para falhar. O segundo serviu de modelo para o
relato inválido da demonstração do exercício 1: um contato telepático com uma testemunha. O
primeiro tem o ID `WRONG_FORMAT`, que não começa com `AC`, e um sinal de 8.5 sem mensagem: duas
regras quebradas no mesmo relato. `invalid_stations.json` tem duas estações com vários campos fora
dos limites. A [próxima página](./03-validar-os-dados.md) mostra o que os modelos dizem de cada
um.
