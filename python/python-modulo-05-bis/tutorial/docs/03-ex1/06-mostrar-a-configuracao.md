---
sidebar_position: 6
title: Mostrar a configuração
---

# Mostrar a configuração

Com a configuração montada, o Oráculo mostra o que faria com cada valor: as cinco linhas do bloco
`Configuration loaded:` da saída do enunciado. É aqui que o modo de desenvolvimento e o de
produção começam a se comportar diferente. As peças entram no `oracle.py` depois de `load_config`.

## O banco de dados

```python
def database_status(url: str) -> str:
    for marker in LOCAL_MARKERS:
        if marker in url:
            return "Connected to local instance"
    return "Connected to remote instance"
```

Um banco é **local** quando fica na própria máquina: um arquivo SQLite (a URL começa com
`sqlite:`) ou um servidor em `localhost` ou `127.0.0.1`, os dois nomes que um computador usa para
se referir a ele mesmo. `marker in url` pergunta se o trecho aparece dentro do texto. Qualquer
outro endereço é **remoto**. O programa não se conecta de verdade: a linha diz a que tipo de banco
ele se conectaria. A regra e o texto `Connected to remote instance` são escolha do tutorial; o
enunciado só mostra o caso local.

## O acesso à API

```python
def api_status(config: dict[str, str]) -> str:
    if config["API_KEY"]:
        return "Authenticated"
    if config["MATRIX_MODE"] == "production":
        return "DENIED - API_KEY is required in production"
    return "Anonymous (development only)"
```

Com uma chave, o acesso é autenticado nos dois modos. Sem chave, o modo decide:

- em **desenvolvimento**, o programa segue sem autenticação (`Anonymous`), o que é aceitável numa
  máquina de testes;
- em **produção**, o acesso é negado (`DENIED`): um programa de verdade sem a sua chave não deve
  fingir que funciona.

Essa é uma das diferenças entre os dois modos, e a escolha de como mostrá-la é livre no enunciado.

## O bloco inteiro

```python
def show_config(config: dict[str, str]) -> None:
    print("Configuration loaded:")
    print(f"Mode: {config['MATRIX_MODE']}")
    print(f"Database: {database_status(config['DATABASE_URL'])}")
    print(f"API Access: {api_status(config)}")
    print(f"Log Level: {config['LOG_LEVEL']}")
    network = "Online" if config["ZION_ENDPOINT"] else "Offline"
    print(f"Remote Network: {network}")
```

- `config['MATRIX_MODE']` lê o valor da chave `MATRIX_MODE`. Dentro de uma f-string com aspas
  duplas, as chaves do dicionário vão entre aspas simples;
- `"Online" if config["ZION_ENDPOINT"] else "Offline"` é uma **expressão condicional**: vale
  `"Online"` se há um endereço (um texto não vazio), e `"Offline"` se não há;
- os rótulos (`Mode:`, `Database:`...) são os do enunciado, na mesma ordem. Nenhuma linha mostra o
  valor da `API_KEY` nem a URL do banco: a saída de um programa também pode parar num lugar
  público (um registro, uma captura de tela), e segredos não aparecem nela.
