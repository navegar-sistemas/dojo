---
sidebar_position: 1
title: As ferramentas
---

# As ferramentas

As demonstrações dos exercícios testam um objeto válido e um inválido. Um modelo de verdade
recebe centenas de registros. O enunciado traz duas ferramentas que geram dados de teste para os
três modelos, e esta parte as usa para passar muitos registros pelos modelos prontos.

As ferramentas vêm num arquivo anexo ao enunciado, o `data_generator.tar`. Um arquivo `.tar`
junta vários arquivos num só, como um pacote. Elas não fazem parte da entrega.

## Extrair

Copie o `data_generator.tar` para a pasta `cosmic-data` e liste o que há dentro dele:

```bash
tar -tf data_generator.tar
```

```text
data_generator.py
data_exporter.py
```

`tar` é o programa que lida com esses pacotes: `-t` lista o conteúdo, e `-f` diz qual é o
arquivo. São dois programas em Python. O enunciado fala em importar dados "do diretório de
ferramentas" (*tools directory*); o tutorial põe os dois numa pasta `tools`:

```bash
mkdir tools
tar -xf data_generator.tar -C tools
ls -1 tools
```

```text
data_exporter.py
data_generator.py
```

- `-x` extrai os arquivos, e `-C tools` os põe dentro da pasta `tools`;
- `ls -1` lista um nome por linha.

## data_generator.py

Gera registros parecidos com os dos três exercícios, sorteando os valores dentro de faixas
realistas. Ele usa só a biblioteca padrão: o módulo `random`, que sorteia números, e o
`datetime`. O arquivo tem três classes, uma por tipo de dado:

| Classe | Gera | Faixas principais |
|---|---|---|
| `SpaceStationGenerator` | estações | tripulação de 3 a 12, energia de 70.0 a 98.5, oxigênio de 85.0 a 99.2; a estação está em operação quando a energia passa de 75 e o oxigênio passa de 90 |
| `AlienContactGenerator` | relatos de contato | IDs `AC_2024_001`, `AC_2024_002`...; sinal de 1.0 a 10.0, de 5 a 240 minutos, de 1 a 15 testemunhas; contato físico sempre verificado; contato telepático com pelo menos 3 testemunhas; mensagem só em parte dos sinais acima de 6.0 |
| `CrewMissionGenerator` | missões com tripulação | IDs como `M2024_MARS`; de 90 a 1200 dias, de 3 a 8 tripulantes, o primeiro sempre `captain` ou `commander`; tripulantes de 25 a 55 anos |

As faixas ficam dentro dos limites do enunciado, e as correções (contato físico verificado,
telepatia com 3 testemunhas, um líder em cada missão) seguem as regras de negócio dos
exercícios.

O sorteio começa sempre do mesmo ponto: a **semente** (*seed*) do `random` é fixa, `42`. Com a
mesma semente, o `random` sorteia sempre a mesma sequência, e o gerador produz os mesmos dados em
toda execução e em toda máquina.

Rodado direto, o `data_generator.py` só imprime um resumo do que gera. Quem grava os dados em
arquivos é o outro programa.

## data_exporter.py

Importa as três classes do `data_generator.py`, gera um conjunto maior (10 estações, 15 relatos e
5 missões) e grava cada conjunto numa pasta `generated_data/`, em três formatos:

- **JSON**, um formato de texto para dados: listas entre `[]`, dicionários entre `{}`, textos
  entre aspas duplas, e `true`, `false` e `null` no lugar de `True`, `False` e `None`;
- **CSV**, uma tabela em texto: uma linha por registro, campos separados por vírgula. As missões
  não vão para CSV, porque a lista de tripulantes não cabe numa linha de tabela;
- **Python**, um arquivo `.py` com a lista escrita como código.

Ele também grava dois arquivos de **casos inválidos**, `invalid_stations.json` e
`invalid_contacts.json`, com registros que quebram os limites e as regras de propósito.

A pasta `generated_data/` é criada **na pasta de onde o programa é rodado**, e o `import` do
`data_generator` só funciona se os dois arquivos estiverem na mesma pasta. A
[próxima página](./02-gerar-os-dados.md) roda os dois programas.

## O código das ferramentas não é do projeto

O código das ferramentas é do enunciado, não do projeto: não é entregue e não segue as regras de
estilo do projeto. O flake8, se rodado na pasta `tools`, acusa mais de cem avisos, quase todos de
linhas em branco com espaços e de linhas longas. Por isso o flake8 e o mypy são sempre rodados nas
pastas `ex0`, `ex1`, `ex2` e `experimentos`, e nunca em `tools`.
