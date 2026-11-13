---
sidebar_position: 1
title: O problema
---

# O problema

Programas precisam de informações que não são código: o endereço do banco de dados, a chave
secreta de um serviço externo (uma **chave de API**, a senha que um programa usa para falar com
outro), o quanto de detalhe registrar. Escritas no código, essas informações vão para o
repositório junto com ele, e um `git push` descuidado entrega a senha a quem puder ler o
repositório. Além disso, elas mudam: o banco do computador de quem desenvolve não é o banco do
servidor de verdade.

O exercício 1 tira a configuração do código. O programa lê cada valor de uma **variável de
ambiente** e, durante o desenvolvimento, de um arquivo `.env` que fica ao lado do programa e
nunca vai para o repositório.

## O que o enunciado pede

Quatro arquivos na pasta `ex1/`. Os `import` permitidos são `os`, `sys` e a biblioteca externa
`python-dotenv`, além de operações com arquivos (`open`).

- **`oracle.py`**, um programa que:
  - lê a configuração de variáveis de ambiente;
  - usa um arquivo `.env` para a configuração de desenvolvimento, lido com a biblioteca
    `python-dotenv` (escrever o próprio leitor de `.env` não vale);
  - se comporta de um jeito em **desenvolvimento** e de outro em **produção**, com a diferença
    visível na saída (o jeito de mostrar é livre);
  - trata a configuração que falta sem travar;
- **`requirements.txt`**, com a dependência `python-dotenv`;
- **`.env.example`**, um modelo do `.env`, que vai para o repositório no lugar dele;
- **`.gitignore`**, que lista o `.env`, para o git nunca registrá-lo. Na avaliação, é preciso saber
  explicar por quê.

As cinco variáveis de configuração:

| Variável | O que guarda |
|---|---|
| `MATRIX_MODE` | o modo: `development` (desenvolvimento) ou `production` (produção) |
| `DATABASE_URL` | o endereço de conexão com o banco de dados |
| `API_KEY` | a chave secreta para serviços externos |
| `LOG_LEVEL` | o nível de detalhe dos registros (*logs*) do programa, como `DEBUG` (tudo) ou `INFO` |
| `ZION_ENDPOINT` | o endereço (URL) da rede remota |

**Desenvolvimento** é o computador de quem escreve o programa, com dados de teste; **produção** é
onde o programa roda de verdade, para os usuários.

## O roteiro de testes do enunciado

| Situação | Comandos | O que deve acontecer |
|---|---|---|
| sem nenhuma configuração | `python3 ex1/oracle.py` | mostrar valores padrão e avisar que falta configuração |
| com um `.env` | `cp ex1/.env.example ex1/.env`, editar o `ex1/.env` com os seus valores, `python3 ex1/oracle.py` | ler a configuração do `.env` |
| sobrescrevendo pelo ambiente | `MATRIX_MODE=production API_KEY=secret123 python3 ex1/oracle.py` | preferir as variáveis de ambiente ao `.env` |

## A saída esperada

O exemplo do enunciado, com um `.env` completo de desenvolvimento:

```text

ORACLE STATUS: Consulting the configuration...

Configuration loaded:
Mode: development
Database: Connected to local instance
API Access: Authenticated
Log Level: DEBUG
Remote Network: Online

Configuration security check:
[OK] No hardcoded secrets detected
[OK] .env file properly ignored by git
[OK] Production overrides available

The Oracle sees all configurations.
```

A saída começa com uma linha vazia. O enunciado só mostra esse caso; as saídas sem configuração e
em produção ficam por conta de quem faz o exercício, e as do tutorial aparecem na página
[Rodar e conferir](./09-rodar-e-conferir.md).

## Onde o programa roda

O `oracle.py` importa o `python-dotenv`, uma biblioteca externa, e roda no `lab_env` do exercício
0, com o ambiente ativado: os comandos desta parte escrevem `python3`, como o enunciado. O
`python-dotenv` é instalado na [página 3](./03-o-arquivo-env-e-o-python-dotenv.md).
