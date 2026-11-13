---
sidebar_position: 4
title: Ler a configuração
---

# Ler a configuração

O programa começa garantindo duas coisas: que o python-dotenv está instalado e que as cinco
variáveis existem. Sem qualquer uma delas, ele não tem como continuar.

## O import do python-dotenv

Crie o arquivo `ex2/oracle.py` e escreva nele:

```python
import os
import sys

try:
    from dotenv import dotenv_values, load_dotenv
except ImportError:
    print("ORACLE ERROR: python-dotenv is not installed.")
    print("Install it with: pip install -r requirements.txt")
    sys.exit(1)
```

- `os` dá o acesso ao ambiente (`os.getenv`, `os.environ`) e a função que confere se um arquivo
  existe; `sys` dá o `sys.exit`;
- o `from dotenv import ...` fica dentro de um `try`: rodado num Python sem o python-dotenv (por
  exemplo, o global, fora do venv), o programa diz o que falta e como instalar, e termina com o
  código `1`, em vez de mostrar um traceback. É a regra de testar "com e sem dependências" do
  enunciado.

Aqui o `import` é o comum, e não `importlib` como no exercício 1: o programa usa as duas funções
de verdade, e o mypy confere o uso delas, porque o python-dotenv traz os próprios type hints. O
preço é que o mypy precisa encontrar a biblioteca. O enunciado aceita avisos de `import` do flake8
e do mypy só no exercício 1; aqui, um `import-not-found` do mypy é um aviso como outro qualquer, e
precisa sumir. O mypy procura as bibliotecas no Python em que ele mesmo está instalado (o `.venv`
das ferramentas), e ativar o `matrix_env` não muda isso: ele não enxerga o python-dotenv. A opção
`--python-executable matrix_env/bin/python` manda o mypy procurar as bibliotecas no Python do
`matrix_env`, onde o python-dotenv está instalado
([Rodar e conferir](./10-rodar-e-conferir.md#conferir-estilo-e-tipos)).

## As constantes

```python
ENV_FILE = ".env"
IGNORE_FILE = ".gitignore"
VARIABLES = [
    "MATRIX_MODE",
    "DATABASE_URL",
    "API_KEY",
    "LOG_LEVEL",
    "ZION_ENDPOINT",
]
SECRETS = ["API_KEY", "DATABASE_URL"]
MODES = ["development", "production"]
LOCAL_MARKERS = ["sqlite", "localhost", "127.0.0.1"]
```

- `ENV_FILE` e `IGNORE_FILE`: os nomes dos dois arquivos que o programa lê, na pasta atual;
- `VARIABLES`: as cinco variáveis do enunciado, na ordem dele;
- `SECRETS`: as variáveis que guardam segredos: a chave e o endereço do banco, que costuma levar
  usuário e senha dentro dele ([A conferência de segurança](./06-a-conferencia-de-seguranca.md));
- `MODES`: os dois modos aceitos;
- `LOCAL_MARKERS`: trechos de endereço que indicam um banco de dados na própria máquina
  ([Mostrar a configuração](./05-mostrar-a-configuracao.md)).

Nenhuma dessas constantes é configuração: são fatos do programa, iguais em toda máquina.

## Carregar o .env

```python
def load_env_file() -> None:
    try:
        load_dotenv(ENV_FILE)
    except (OSError, UnicodeDecodeError) as error:
        print(f"ORACLE ERROR: cannot read {ENV_FILE}: {error}")
        sys.exit(1)
```

O `load_dotenv` abre e lê o `.env`, e a leitura de um arquivo pode falhar mesmo com ele presente:

- `OSError` é a família dos erros do sistema de arquivos, como `PermissionError` (sem permissão
  de leitura);
- `UnicodeDecodeError` acontece quando o arquivo não é um texto UTF-8 válido, como um `.env`
  salvo com outra codificação ou com um byte corrompido.

Sem o `try`, qualquer um deles derrubaria o programa com um traceback. Com ele, o programa diz qual
arquivo não pôde ler e por quê, e termina com o código `1`: com um `.env` ilegível, não há como
saber se a configuração está completa. Um `.env` que não existe não é erro: o `load_dotenv` não
carrega nada, e a falta das variáveis é acusada logo depois. A função entra depois das constantes;
a página [Rodar e conferir](./10-rodar-e-conferir.md#arquivos-ilegíveis) provoca os dois erros.

## Encontrar os problemas

```python
def find_problems() -> list[str]:
    problems = []
    for name in VARIABLES:
        if not os.getenv(name):
            problems.append(f"[MISSING] {name} is not set")
    mode = os.getenv("MATRIX_MODE")
    if mode and mode not in MODES:
        problems.append("[INVALID] MATRIX_MODE must be development "
                        f"or production, not '{mode}'")
    return problems
```

- `os.getenv(name)` devolve o valor, ou `None` se a variável não existe. `not os.getenv(name)` é
  verdadeiro nos dois casos de falta: variável inexistente (`None`) e variável vazia (`""`), como a
  `API_KEY=` do `.env.example`;
- `MATRIX_MODE` só aceita os dois valores do enunciado. `if mode and ...` pula a conferência
  quando o modo falta, que já foi acusado no laço;
- a mensagem do modo inválido é longa demais para uma linha de 79 caracteres e foi dividida em
  dois textos seguidos dentro dos parênteses. O Python junta textos escritos lado a lado num só:
  `"ab" "cd"` é `"abcd"`. Só o segundo tem `{mode}`, e por isso só ele tem o `f`;
- a função devolve a lista de problemas, vazia quando a configuração está completa. Juntar todos
  antes de reclamar deixa o programa listar de uma vez tudo o que falta, em vez de um erro por
  execução.

## Sem valores padrão

O enunciado pede "avisos de configuração padrão ou ausente" quando falta configuração. A
**escolha do tutorial** é tratar toda falta como erro, e nunca inventar um valor: com um padrão
escrito no código, um `DATABASE_URL` esquecido no servidor faria o programa de produção usar, sem
aviso nenhum, o banco de dados de desenvolvimento
([Quando a variável falta](../02-conceitos/04-variaveis-de-ambiente.md#quando-a-variável-falta)).
Os valores de desenvolvimento existem, mas no `.env.example`, onde quem configura os vê e os
copia de propósito.

## Ler os valores

Depois que `find_problems` não achou nada, todas as variáveis existem, e a leitura é direta:

```python
def read_config() -> dict[str, str]:
    config = {}
    for name in VARIABLES:
        config[name] = os.environ[name]
    return config
```

`os.environ[name]` lançaria `KeyError` com uma variável inexistente, mas aqui isso não acontece:
o `main` só chama `read_config` quando não há problema ([O main](./08-o-main.md)). O resultado é
um dicionário `{"MATRIX_MODE": "development", ...}`, do tipo `dict[str, str]`: só textos, sem
`None`, e o resto do programa não precisa mais conferir nada.
