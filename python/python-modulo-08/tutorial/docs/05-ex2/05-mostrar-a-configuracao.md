---
sidebar_position: 5
title: Mostrar a configuração
---

# Mostrar a configuração

O bloco `Configuration loaded:` da saída do enunciado tem uma linha por variável:

```text
Configuration loaded:
Mode: development
Database: Connected to local instance
API Access: Authenticated
Log Level: DEBUG
Zion Network: Online
```

Nenhuma linha mostra a URL do banco nem a chave: uma URL de banco costuma ter usuário e senha
dentro dela, e um programa não deve imprimir segredos, porque a saída de um programa vai parar em
telas e em arquivos de log. As linhas mostram o **estado** de cada item.

## Local ou remoto

```python
def is_local(url: str) -> bool:
    for marker in LOCAL_MARKERS:
        if marker in url:
            return True
    return False
```

Um banco de dados é **local** quando roda na própria máquina: um arquivo SQLite (`sqlite:///...`)
ou um servidor no endereço `localhost` ou `127.0.0.1`, os dois nomes da própria máquina. A função
responde se algum desses trechos aparece na URL. Qualquer outro endereço, como
`postgresql://db.zion.net:5432/matrix`, é **remoto**: outra máquina, na rede.

## As linhas da configuração

A função entra depois de `is_local`:

```python
def show_config(config: dict[str, str]) -> None:
    place = "local" if is_local(config["DATABASE_URL"]) else "remote"
    print("Configuration loaded:")
    print(f"Mode: {config['MATRIX_MODE']}")
    print(f"Database: Connected to {place} instance")
    print("API Access: Authenticated")
    print(f"Log Level: {config['LOG_LEVEL']}")
    print("Zion Network: Online")
```

- `"local" if ... else "remote"` é uma **expressão condicional**: vale `"local"` se a condição é
  verdadeira, e `"remote"` se não é;
- `Mode` e `Log Level` mostram os valores das variáveis, que não são segredo;
- `Database` diz se o banco é local ou remoto: `Connected to local instance` no `.env` de
  desenvolvimento, como no enunciado;
- dentro de uma f-string com aspas duplas, as chaves do dicionário vão entre aspas simples:
  `config['MATRIX_MODE']`.

`API Access: Authenticated` e `Zion Network: Online` saem sempre, porque quando `show_config` roda
a `API_KEY` e o `ZION_ENDPOINT` já foram conferidos: o programa não roda sem eles. Como diz a
página [O problema](./01-o-problema.md#as-decisões-do-tutorial), nada se conecta de verdade: um
*pipeline* de verdade abriria aqui a conexão com o banco e com o serviço, usando esses valores.
