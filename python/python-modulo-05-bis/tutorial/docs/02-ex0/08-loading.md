---
sidebar_position: 8
title: loading.py
---

# loading.py

`loading.py` confere os reagentes: tenta importar cada biblioteca declarada, mostra a versão das
que estão instaladas e, se faltar alguma, ensina a instalar, sem travar. Crie `ex0/loading.py` com
as peças desta página, na ordem em que aparecem; a [próxima página](./09-loading-completo.md)
mostra o arquivo inteiro.

## Importar pelo nome

Um `import pandas` no topo do arquivo não serve: sem a biblioteca instalada, o programa pararia na
primeira linha com `ModuleNotFoundError`, antes de imprimir qualquer coisa. O import precisa
acontecer dentro de um `try`, e para cada biblioteca da lista. O módulo `importlib`, permitido no
exercício, faz isso:

```python
import importlib

REAGENTS = [
    ("pandas", "Data manipulation"),
    ("numpy", "Numerical computation"),
]
```

`importlib.import_module("pandas")` faz o mesmo que `import pandas`, mas recebe o nome como um
texto, e devolve o módulo importado. Com o nome num texto, o programa percorre uma lista.

`REAGENTS` é a lista dos reagentes declarados em `requirements.txt` e `pyproject.toml`, cada um
com a sua função, como aparece na saída (`Data manipulation ready`). O nome em maiúsculas é o
costume para uma **constante**: um valor fixo do programa, que nenhuma função altera. Repetir os
dois nomes aqui, em vez de ler o `requirements.txt`, é escolha do tutorial: é o mais simples, e o
arquivo de dependências não é parte do que o programa precisa interpretar.

Há um segundo motivo para não escrever `import pandas`: o mypy confere cada `import` e precisa
das informações de tipo da biblioteca. A `pandas` não traz essas informações, e o mypy acusaria
`Library stubs not installed for "pandas"`. Com `import_module`, o nome é só um texto para o
mypy, e não há o que conferir.

## A versão de um reagente

```python
def installed_version(name: str) -> str | None:
    try:
        module = importlib.import_module(name)
    except ImportError:
        return None
    return str(module.__version__)
```

- `except ImportError` captura a falha do import. Quando o módulo não existe, o Python lança
  `ModuleNotFoundError`, que é um tipo particular de `ImportError`; capturar o tipo mais geral
  também cobre uma biblioteca instalada pela metade;
- o retorno `str | None` diz que a função devolve um texto ou `None`
  ([Type hints](../01-ambiente/04-type-hints-flake8-e-mypy.md#type-hints)). `None` quer dizer
  "não instalado";
- `module.__version__` é a versão da biblioteca, um texto como `"2.5.4"`. Quase toda biblioteca
  guarda a sua versão num atributo com esse nome, e as duas do projeto guardam. Para o mypy, um
  atributo de um módulo importado por `import_module` pode ser qualquer coisa; o `str(...)` garante
  que a função devolve um texto.

## Conferir a lista

```python
def check_reagents() -> list[str]:
    missing: list[str] = []
    for name, purpose in REAGENTS:
        version = installed_version(name)
        if version is None:
            print(f"[MISSING] {name} - {purpose} unavailable")
            missing.append(name)
        else:
            print(f"[OK] {name} ({version}) - {purpose} ready")
    return missing
```

Uma linha por reagente: `[OK]` com a versão, no formato do enunciado, ou `[MISSING]`
("faltando"), no mesmo formato, para o caso que o enunciado não mostra. A função devolve a lista
dos que faltam, para o fim do programa decidir o que dizer. `missing` é anotada porque começa
vazia ([Type hints](../01-ambiente/04-type-hints-flake8-e-mypy.md#type-hints)).

`version is None` pergunta se o valor é exatamente `None`. `if not version` seria parecido, mas
trataria também um texto vazio como "não instalado".

## pip vs Poetry

```python
def explain_managers() -> None:
    print("pip vs Poetry:")
    print("  requirements.txt declares what to install;"
          " pip resolves it at install time.")
    print("  pyproject.toml declares the same constraints,"
          " and Poetry pins the resolved")
    print("  versions in poetry.lock so every install is identical.")
```

As três linhas do enunciado, com os dois espaços do começo. As duas primeiras passam de 79
caracteres, o limite do flake8, e foram divididas em dois textos seguidos dentro dos parênteses:
o Python junta textos escritos lado a lado num só (`"ab" "cd"` é `"abcd"`).

## Quando falta algo

```python
def explain_install(missing: list[str]) -> None:
    print(f"Missing reagents: {', '.join(missing)}")
    print("Install them with pip:")
    print("  pip install -r ex0/requirements.txt")
    print("Or with Poetry:")
    print("  poetry -P ex0 install")
    print("  poetry -P ex0 run python ex0/loading.py")
```

O enunciado pede uma mensagem com o comando de instalação para os dois gerenciadores, sem fixar
o texto. A mensagem é escolha do tutorial: os nomes que faltam, separados por vírgula com
`", ".join(...)`, e os comandos para rodar na pasta do projeto. O `-P ex0` dos comandos do Poetry
diz a ele que o `pyproject.toml` está na pasta `ex0`
([Instalar com o Poetry](./11-instalar-com-poetry.md)).

## O main

```python
def main() -> None:
    print()
    print("REAGENT STATUS: Loading reagents...")
    print()
    print("Checking dependencies:")
    missing = check_reagents()
    print()
    explain_managers()
    print()
    if missing:
        explain_install(missing)
    else:
        print("All reagents present and accounted for.")


if __name__ == "__main__":
    main()
```

A saída começa com uma linha vazia, como a do enunciado. A comparação entre o pip e o Poetry
aparece sempre, com ou sem reagentes; a última parte muda: `All reagents present and accounted
for.` ("todos os reagentes presentes e contabilizados") quando nada falta, e as instruções de
instalação quando falta algo. `if missing:` é verdadeiro quando a lista tem algum item.
