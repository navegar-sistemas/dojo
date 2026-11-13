---
slug: /
sidebar_position: 1
title: O que vamos construir
---

# O que vamos construir

Um programa Python não depende só do próprio código. Ele depende também do Python que o roda, das
bibliotecas instaladas nesse Python e da configuração da máquina onde roda: endereço do banco de
dados, senhas, chaves de acesso. Quando qualquer uma dessas peças muda sem controle, o mesmo
código funciona numa máquina e quebra na outra. Três ferramentas põem essas peças sob controle:

- o **ambiente virtual** (*virtual environment*, ou **venv**): uma pasta com um Python e as
  bibliotecas de um projeto só, separada do Python do sistema;
- o **gerenciador de pacotes**: o programa que baixa e instala bibliotecas feitas por outras
  pessoas. Aqui são dois, o **pip**, que vem com o Python, e o **Poetry**, que é instalado à
  parte;
- as **variáveis de ambiente** e o arquivo **`.env`**: a configuração fica fora do código, e o
  mesmo programa roda em desenvolvimento ou em produção só trocando os valores.

O projeto se chama **The Matrix**, como o filme: Zion, o Oráculo, a pílula vermelha e o
"construto" só dão nome às coisas. O assunto de verdade são as três ferramentas acima.

## Três programas, um por ferramenta

O projeto tem três **exercícios**, cada um numa pasta própria:

| Exercício | Arquivos | O que o programa faz |
|---|---|---|
| 0 | `ex0/construct.py` | descobre se está rodando dentro de um ambiente virtual, mostra qual Python está em uso e onde os pacotes são instalados, e ensina a criar um venv quando não há nenhum |
| 1 | `ex1/loading.py`, `ex1/requirements.txt`, `ex1/pyproject.toml` | analisa dados gerados com as bibliotecas numpy, pandas e matplotlib e salva um gráfico; as bibliotecas são instaladas pelo pip ou pelo Poetry, e, se faltar alguma, o programa diz qual falta e como instalar |
| 2 | `ex2/oracle.py`, `ex2/requirements.txt`, `ex2/.env.example`, `ex2/.gitignore` | lê cinco variáveis de configuração do ambiente e de um arquivo `.env`, recusa configuração ausente e mostra a diferença entre o modo de desenvolvimento e o de produção |

A saída do programa do exercício 2, com a configuração de desenvolvimento:

```text

ORACLE STATUS: Reading the Matrix...

Configuration loaded:
Mode: development
Database: Connected to local instance
API Access: Authenticated
Log Level: DEBUG
Zion Network: Online

Environment security check:
[OK] No hardcoded secrets detected
[OK] .env file properly configured
[OK] Production overrides available

The Oracle sees all configurations.
```

As mensagens são em inglês porque o enunciado do projeto mostra a saída de cada programa, e essa
saída é em inglês. A primeira linha é vazia: as três saídas do enunciado começam com uma linha em
branco.

## O enunciado

O projeto vem com um documento oficial que diz o que precisa ser entregue: o **enunciado** (em
inglês, *subject*). A [próxima página](./02-o-enunciado-em-linguagem-simples.md) resume tudo o
que ele pede.

## As partes

| Parte | Conteúdo |
|---|---|
| Ambiente | prepara o Python, a pasta do projeto e as ferramentas (flake8, mypy e Poetry) |
| Pacotes, venvs e variáveis | explica, com experimentos pequenos, o pip, o ambiente virtual por dentro, a importação de uma biblioteca que talvez não exista e as variáveis de ambiente |
| Exercícios 0 a 2 | constroem os três programas, um por parte, e os rodam em ambientes diferentes |
| Fechamento | confere tudo, mostra como entregar e responde ao que o enunciado pede que você saiba explicar na avaliação |

Cada exercício termina com o arquivo completo e uma página que roda o programa em cada situação.
Os termos novos estão reunidos no [glossário](./05-glossario.md).
