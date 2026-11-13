---
sidebar_position: 5
title: Conferir as dependências
---

# Conferir as dependências

Antes de qualquer análise, o programa confere quais das três bibliotecas estão instaladas e
mostra a versão de cada uma, numa linha por biblioteca:

```text
[OK] pandas (3.1.1) - Data manipulation ready
```

Crie o arquivo `ex1/loading.py` e escreva nele o começo do programa:

```python
import importlib
import sys

OUTPUT = "matrix_analysis.png"
DATA_POINTS = 1000
DEPENDENCIES = [
    ("pandas", "Data manipulation"),
    ("numpy", "Numerical computation"),
    ("matplotlib", "Visualization"),
]
```

- `importlib` importa as bibliotecas pelo nome
  ([Importar pelo nome](../02-conceitos/03-importar-pelo-nome.md)), e `sys` dá o `sys.exit` do
  fim do programa ([O main](./08-o-main.md)). São os dois únicos `import` do arquivo: numpy,
  pandas e matplotlib entram por `importlib`;
- `OUTPUT` e `DATA_POINTS` são **constantes**: valores fixos do programa, escritos uma vez no
  topo, com o nome em maiúsculas, que é o costume do Python para valores que não mudam. O nome do
  arquivo do gráfico aparece em dois lugares do programa, e a constante garante que os dois são
  iguais;
- `DEPENDENCIES` é uma lista de tuplas `(nome, papel)`: o nome da biblioteca e o texto da saída
  que diz para que ela serve. A ordem da lista é a ordem das linhas na saída do enunciado.

## A função de comparação

O enunciado pede "uma função de comparação que mostre as versões dos pacotes instalados". A
função abaixo compara a lista do que o programa precisa com o que o ambiente tem, e mostra a
versão de cada biblioteca encontrada:

```python
def check_dependencies() -> list[str]:
    missing = []
    for name, role in DEPENDENCIES:
        try:
            module = importlib.import_module(name)
        except ImportError:
            print(f"[MISSING] {name} - {role} not available")
            missing.append(name)
        else:
            print(f"[OK] {name} ({module.__version__}) - {role} ready")
    return missing
```

- o `for` separa cada tupla em `name` e `role`;
- `importlib.import_module(name)` tenta importar a biblioteca. Se ela não está instalada, o
  `except ImportError` imprime `[MISSING]` e guarda o nome na lista `missing`;
- se o `import` deu certo, o `else` imprime `[OK]`, com a versão lida de `module.__version__`;
- a função devolve a lista do que falta: vazia quando está tudo instalado.

Rodar a mesma função no ambiente do pip e no do Poetry mostra as versões que cada ferramenta
instalou. No Python 3.10, por exemplo, as versões são outras, porque as mais novas não funcionam
nele.

## Uma importação vale para o programa todo

Importar um módulo uma vez o deixa guardado em `sys.modules`, o dicionário dos módulos já
carregados.
Quando a análise pedir o numpy de novo com `importlib.import_module("numpy")`, o Python devolve o
mesmo módulo, sem carregá-lo outra vez. Conferir antes e usar depois não custa o dobro.
