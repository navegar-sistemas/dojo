---
sidebar_position: 1
title: O problema
---

# O problema

Um programa que conversa com um banco de dados e com serviços externos precisa de endereços e de
senhas. Escritos no código, eles vão parar no repositório, à vista de quem tiver acesso a ele, e
obrigam a mudar o código para trocar de máquina. O exercício 2 lê toda a configuração de
variáveis de ambiente, carregadas de um arquivo `.env` durante o desenvolvimento, e mostra o
mesmo código rodando em desenvolvimento e em produção.

## O que o enunciado pede

Quatro arquivos na pasta `ex2/`:

| Arquivo | O que é |
|---|---|
| `oracle.py` | o programa ("o Oráculo", que conhece toda a configuração) |
| `requirements.txt` | a dependência do programa, o pacote `python-dotenv` |
| `.env.example` | o modelo do arquivo de configuração, sem segredos, que vai para o repositório |
| `.gitignore` | a lista de arquivos que o Git deve ignorar, com o `.env` nela |

O programa:

- carrega a configuração de **variáveis de ambiente**;
- usa um arquivo **`.env`** para as configurações de desenvolvimento, lido com a biblioteca
  **python-dotenv** (o enunciado proíbe escrever um leitor de `.env` próprio);
- mostra configurações diferentes para **desenvolvimento** e **produção**, de um jeito que fique
  visível na saída. Como, fica a critério de quem implementa;
- trata a **configuração ausente** com erros adequados.

As variáveis são cinco:

| Variável | O que guarda |
|---|---|
| `MATRIX_MODE` | o modo: `development` ou `production` |
| `DATABASE_URL` | o endereço do banco de dados, escrito como uma **URL** (o formato dos endereços da web, `esquema://lugar/caminho`); o enunciado o chama de *string de conexão* |
| `API_KEY` | a chave secreta de acesso a serviços externos |
| `LOG_LEVEL` | o nível de detalhe dos *logs* (as mensagens que um programa registra sobre o que faz), como `DEBUG` (tudo) ou `WARNING` (só alertas) |
| `ZION_ENDPOINT` | o endereço (URL) da "rede da resistência", um serviço externo |

O enunciado ainda avisa, em destaque: nunca registrar segredos reais no controle de versão. O
`.env` precisa estar no `.gitignore`, e você precisa saber explicar por quê
([As perguntas do enunciado](../06-fechamento/03-as-perguntas-do-enunciado.md)).

Os módulos autorizados são `os`, `sys`, `python-dotenv` e as operações com arquivos (`open` e
companhia).

## A saída do enunciado

```console
$> python oracle.py

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

Como nos outros exercícios, a saída começa com uma linha vazia.

## Os testes pedidos

Sem configuração nenhuma, o programa deve mostrar avisos de configuração padrão ou ausente:

```console
$> python3 oracle.py
# Should show default/missing configuration warnings
```

Com o `.env`, copiado do modelo e preenchido, deve carregar a configuração dele:

```console
$> cp .env.example .env
$> # Edit .env with your values
$> python3 oracle.py
# Should load configuration from .env file
```

Com variáveis na linha de comando, elas valem mais que as do `.env`:

```console
$> MATRIX_MODE=production API_KEY=secret123 python3 oracle.py
# Should use environment variables over .env file
```

## As decisões do tutorial

O enunciado deixa em aberto o que fazer sem configuração ("avisos de configuração padrão **ou**
ausente") e como mostrar a diferença entre os modos. As escolhas, explicadas nas páginas de cada
peça:

- **sem valores padrão**: uma variável que falta (ou vazia) é um erro, listado pelo nome, e o
  programa termina sem rodar ([Ler a configuração](./04-ler-a-configuracao.md));
- **as linhas de estado vêm da configuração**: `Database` diz se o banco é local ou remoto, pelo
  endereço; as conferências de segurança são verificações de verdade
  ([A conferência de segurança](./06-a-conferencia-de-seguranca.md));
- **produção é mais exigente**: em modo de produção, o programa confere também o nível de log e o
  banco de dados, e avisa o que não serve para produção
  ([Desenvolvimento e produção](./07-desenvolvimento-e-producao.md)).

O programa não se conecta de verdade a nada: não há banco de dados nem rede neste exercício. As
linhas `Connected`, `Authenticated` e `Online` dizem que a configuração para isso está presente,
como na saída de exemplo.
