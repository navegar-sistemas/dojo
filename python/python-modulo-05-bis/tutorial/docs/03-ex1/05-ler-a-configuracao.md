---
sidebar_position: 5
title: Ler a configuração
---

# Ler a configuração

O primeiro trabalho do Oráculo é montar a configuração: carregar o `.env`, se houver, e ler as
cinco variáveis, avisando sobre cada uma que falta. Crie `ex1/oracle.py` com as peças desta página
e das duas seguintes, na ordem em que aparecem; a página
[Os arquivos completos](./08-os-arquivos-completos.md) mostra o arquivo inteiro.

## Os imports e as constantes

```python
import os

from dotenv import load_dotenv

HERE = os.path.dirname(os.path.abspath(__file__))
VARIABLES = ["MATRIX_MODE", "DATABASE_URL", "API_KEY", "LOG_LEVEL",
             "ZION_ENDPOINT"]
DEFAULTS = {
    "MATRIX_MODE": "development",
    "DATABASE_URL": "sqlite:///oracle.db",
    "LOG_LEVEL": "INFO",
}
MODES = ["development", "production"]
LOCAL_MARKERS = ["sqlite:", "localhost", "127.0.0.1"]
```

- `HERE` é a pasta onde está o próprio `oracle.py`. `__file__` é uma variável que o Python
  preenche com o caminho do arquivo que está rodando; `os.path.abspath` o transforma em caminho
  absoluto, e `os.path.dirname` tira o nome do arquivo e deixa a pasta. Com `HERE`, o programa acha
  o `.env` e o `.gitignore` da pasta `ex1` mesmo quando é rodado de outra pasta, como no roteiro do
  enunciado (`python3 ex1/oracle.py`, rodado da pasta do projeto);
- `VARIABLES` são as cinco variáveis do enunciado, na ordem em que aparecem lá;
- `DEFAULTS` são os **valores padrão**, usados quando a variável falta, como o enunciado pede
  ("mostrar valores padrão"). Só três variáveis têm padrão. A `API_KEY` não tem, de propósito: um
  segredo padrão escrito no código seria exatamente o segredo no código que o exercício quer
  evitar. O `ZION_ENDPOINT` também não tem: sem endereço, a rede remota fica desligada. Quais
  variáveis têm padrão, e quais são esses padrões, é escolha do tutorial;
- `MODES` são os dois modos válidos;
- `LOCAL_MARKERS` são os trechos que indicam um banco de dados local, usados na
  [próxima página](./06-mostrar-a-configuracao.md).

Um valor padrão silencioso é perigoso: o programa "funciona" com ele e ninguém percebe que a
configuração está faltando. Por isso cada padrão usado vira um aviso na saída.

## load_config

```python
def load_config() -> tuple[dict[str, str], list[str]]:
    warnings: list[str] = []
    env_file = os.path.join(HERE, ".env")
    if os.path.isfile(env_file):
        load_dotenv(env_file)
    else:
        warnings.append("No .env file found, reading the environment only")
    config: dict[str, str] = {}
    for name in VARIABLES:
        value = os.environ.get(name)
        if value:
            config[name] = value
        elif name in DEFAULTS:
            config[name] = DEFAULTS[name]
            warnings.append(f"{name} not set, using default: "
                            f"{DEFAULTS[name]}")
        else:
            config[name] = ""
            warnings.append(f"{name} not set and has no default")
    if config["MATRIX_MODE"] not in MODES:
        warnings.append(f"MATRIX_MODE '{config['MATRIX_MODE']}' is unknown, "
                        "using development")
        config["MATRIX_MODE"] = "development"
    return config, warnings
```

A função devolve duas coisas numa tupla: a configuração montada, um dicionário do nome da
variável para o valor, e a lista de avisos. O tipo de retorno `tuple[dict[str, str], list[str]]`
diz exatamente isso. Os passos:

1. **O `.env`.** `os.path.join(HERE, ".env")` monta o caminho `ex1/.env` (o `join` põe a barra
   entre as partes). `os.path.isfile` responde se o arquivo existe; se existe, `load_dotenv` o
   carrega, sem trocar as variáveis que já existem no ambiente
   ([Quem ganha](./03-o-arquivo-env-e-o-python-dotenv.md#quem-ganha-o-ambiente-ou-o-env)). Se não
   existe, um aviso. Conferir antes com `isfile` é escolha do tutorial, para avisar; o
   `load_dotenv` sozinho não reclama de um arquivo que falta.
2. **As cinco variáveis.** Para cada nome, `os.environ.get(name)` traz o valor, venha ele do
   terminal ou do `.env`. `if value:` é falso para `None` (a variável não existe) e para `""` (a
   variável existe, mas vazia, como o `API_KEY=` do `.env.example`): nos dois casos, a variável
   conta como faltando. Faltando, entra o padrão, com um aviso; sem padrão, entra um texto vazio,
   também com aviso.
3. **O modo.** Um `MATRIX_MODE` que não é nenhum dos dois válidos (um erro de digitação como
   `prodution`) também vira aviso, e o programa segue em desenvolvimento, o modo que não finge
   estar em produção.

`warnings` e `config` são anotadas porque começam vazias
([Type hints](../01-ambiente/04-type-hints-flake8-e-mypy.md#type-hints)).

Nada aqui lança exceção: falte o que faltar, a função devolve uma configuração completa e a lista
do que foi improvisado. É o "tratar a configuração que falta sem travar" do enunciado.
