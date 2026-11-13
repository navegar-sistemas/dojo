---
sidebar_position: 3
title: Os arquivos de apoio
---

# Os arquivos de apoio

Antes do programa, os três arquivos que o acompanham na entrega.

## requirements.txt

O programa depende de uma biblioteca só:

```text title="ex2/requirements.txt"
python-dotenv
```

Sem restrição de versão, o pip instala a mais nova que serve para o seu Python
([Versões](../02-conceitos/01-pacotes-e-o-pip.md#versões)). O programa só usa duas funções da
biblioteca, `load_dotenv` e `dotenv_values`, que existem em todas as versões atuais; no exercício
1, os mínimos vinham das versões da saída do enunciado, e aqui o enunciado não cita versão
nenhuma.

## .env.example

O modelo da configuração, que vai para o repositório:

```ini title="ex2/.env.example"
# Copy to .env and fill in the values. Never commit .env.
MATRIX_MODE=development
DATABASE_URL=sqlite:///matrix.db
API_KEY=
LOG_LEVEL=DEBUG
ZION_ENDPOINT=http://localhost:8080/zion
```

- o comentário da primeira linha lembra o que fazer com o arquivo ("copie para `.env` e preencha
  os valores; nunca registre o `.env` no Git");
- as variáveis que não são segredo já vêm com valores de desenvolvimento, que funcionam em
  qualquer máquina: o modo `development`, o nível de log `DEBUG` (o mais detalhado) e dois
  endereços locais. `sqlite:///matrix.db` é a URL de um banco de dados SQLite, um banco guardado
  num arquivo, aqui o `matrix.db` na pasta atual; `localhost` é o nome da própria máquina;
- `API_KEY=` fica **vazia**: a chave é o segredo, e cada pessoa preenche a sua no `.env`. Com ela
  vazia, o programa recusa rodar e diz que falta a `API_KEY`
  ([Ler a configuração](./04-ler-a-configuracao.md)), o que obriga a editar o `.env`, como manda o
  exemplo do enunciado (`# Edit .env with your values`).

Os valores de desenvolvimento são **escolha do tutorial**; o enunciado só fixa os nomes das
variáveis e os dois valores possíveis de `MATRIX_MODE`.

## .gitignore

O `.gitignore` lista, um por linha, os nomes que o Git deve ignorar: arquivos e pastas que não
entram no repositório mesmo que alguém peça para adicionar a pasta inteira. Ele vale para a pasta
onde está e as de dentro dela.

```text title="ex2/.gitignore"
.env
matrix_env/
.mypy_cache/
```

- `.env`: a configuração de verdade, com o segredo. É a linha que o enunciado exige;
- `matrix_env/`: o ambiente virtual do exercício, que também não é entregue (a `/` no fim diz que
  é uma pasta);
- `.mypy_cache/`: a pasta que o mypy cria ao conferir o código desta pasta.

A página [Entregar](../06-fechamento/02-entregar.md) confere, com o próprio Git, que o `.env` é
ignorado.
