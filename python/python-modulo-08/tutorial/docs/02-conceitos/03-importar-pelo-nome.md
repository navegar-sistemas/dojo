---
sidebar_position: 3
title: Importar pelo nome
---

# Importar pelo nome

O programa do exercício 1 precisa funcionar também quando as bibliotecas **não** estão
instaladas: em vez de quebrar, ele diz o que falta e como instalar. Para isso, ele precisa tentar
o `import` e reagir à falha.

## O import que falha

Sem o numpy instalado no Python global:

```bash
python3 -c 'import numpy'
```

A última linha do traceback é:

```text
ModuleNotFoundError: No module named 'numpy'
```

`ModuleNotFoundError` ("módulo não encontrado") é um tipo de `ImportError`, o erro de qualquer
`import` que falha. Um `except ImportError` captura os dois.

## A primeira tentativa

Crie `experimentos/importar.py` com um `try` em volta dos `import`:

```python title="experimentos/importar.py"
try:
    import numpy
    import pandas
except ImportError as error:
    print(f"Missing: {error.name}")
else:
    print("numpy and pandas are installed")
```

`error.name` é o nome do módulo que não foi encontrado.

```bash
python3 experimentos/importar.py
```

```text
Missing: numpy
```

O programa funciona, mas para no primeiro módulo que falta: o `import pandas` nem chega a ser
tentado. E as duas ferramentas de conferência reclamam:

```bash
.venv/bin/flake8 experimentos
```

```text
experimentos/importar.py:2:5: F401 'numpy' imported but unused
experimentos/importar.py:3:5: F401 'pandas' imported but unused
```

```bash
.venv/bin/mypy --disallow-untyped-defs experimentos
```

```text
experimentos/importar.py:2: error: Cannot find implementation or library stub for module named "numpy"  [import-not-found]
experimentos/importar.py:2: note: See https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports
experimentos/importar.py:3: error: Library stubs not installed for "pandas"  [import-untyped]
experimentos/importar.py:3: note: Hint: "python3 -m pip install pandas-stubs"
experimentos/importar.py:3: note: (or run "mypy --install-types" to install all missing stub packages)
Found 2 errors in 1 file (checked 3 source files)
```

- o flake8 acusa `F401`, "importado mas não usado": os módulos só foram importados para testar se
  existem;
- o mypy, para conferir os tipos, procura cada biblioteca importada no Python onde ele está
  instalado, o `.venv`, e lá não há numpy nem pandas. Para o numpy, ele diz que não encontrou o
  módulo. Para o pandas, ele sabe que os type hints do pandas vêm num pacote separado, o
  `pandas-stubs` (um *stub* é um arquivo só com os type hints de uma biblioteca), e reclama da
  falta dele.

O enunciado permite, só no exercício 1, esses avisos de `import`, e lembra que existem jeitos de
evitá-los. O jeito mais simples está na biblioteca padrão.

## importlib.import_module

O módulo `importlib`, autorizado no exercício 1, tem a função `import_module`, que importa um
módulo **pelo nome**, escrito num texto, e devolve o módulo:

```python
module = importlib.import_module("numpy")
```

faz o mesmo que `import numpy`, mas o módulo fica na variável `module`. Se ele não existe, a
função lança o mesmo `ImportError`. Reescreva `experimentos/importar.py`:

```python title="experimentos/importar.py"
import importlib

for name in ["numpy", "pandas"]:
    try:
        module = importlib.import_module(name)
    except ImportError:
        print(f"Missing: {name}")
    else:
        print(f"{name} {module.__version__}")
```

- o laço tenta cada nome da lista, e um módulo que falta não impede a tentativa do seguinte;
- `module.__version__` é o atributo onde a maioria das bibliotecas guarda o número da própria
  versão.

```bash
python3 experimentos/importar.py
```

```text
Missing: numpy
Missing: pandas
```

```bash
.venv/bin/flake8 experimentos
.venv/bin/mypy --disallow-untyped-defs experimentos
```

```text
Success: no issues found in 3 source files
```

Os dois ficam quietos:

- para o flake8, não há mais `import numpy` nem `import pandas`: há uma chamada de função com um
  texto;
- para o mypy, `import_module` devolve um valor do tipo `ModuleType` ("um módulo qualquer"). O
  mypy não procura biblioteca nenhuma, e aceita qualquer atributo lido de um `ModuleType`, como
  `module.__version__`, com o tipo `Any` ("qualquer tipo").

## O preço

O mypy deixa de conferir o uso da biblioteca: um nome de função escrito errado, como
`module.__versoin__`, passa pelo mypy e só falha quando o programa roda. Para um programa que
precisa rodar sem as bibliotecas instaladas e só chama meia dúzia de funções delas, é uma troca
razoável, e é a escolha do tutorial no exercício 1. Num projeto grande, que sempre tem as
bibliotecas instaladas, o normal é o `import` comum, com os pacotes de stubs instalados no
ambiente do mypy.
