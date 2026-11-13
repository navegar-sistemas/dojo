---
sidebar_position: 6
title: As instruções de instalação
---

# As instruções de instalação

Quando falta alguma biblioteca, a análise não pode rodar. Em vez de um traceback, o programa
diz o que falta e como instalar, pelos dois caminhos. A função entra depois de
`check_dependencies`:

```python
def show_install_help(missing: list[str]) -> None:
    print(f"Missing dependencies: {', '.join(missing)}")
    print()
    print("With pip: installs the packages listed in requirements.txt")
    print("into the active environment (activate a venv first)")
    print("  pip install -r requirements.txt")
    print("  python3 loading.py")
    print()
    print("With Poetry: reads pyproject.toml, creates its own virtual")
    print("environment and records the exact versions in poetry.lock")
    print("  poetry install")
    print("  poetry run python loading.py")
```

- `', '.join(missing)` junta os nomes da lista num texto só, com vírgula e espaço entre eles:
  `["pandas", "matplotlib"]` vira `pandas, matplotlib`. Dentro de uma f-string com aspas duplas, o
  separador vai entre aspas simples;
- cada caminho tem uma frase sobre o que a ferramenta faz e os comandos, com dois espaços na
  frente para destacá-los do texto.

As mensagens não são do enunciado: o enunciado só diz que esta saída deve mostrar o que falta e as
instruções de instalação para o pip e o Poetry. O texto é **escolha do tutorial**, e resume a
diferença entre as duas ferramentas ([pip e Poetry](./02-pip-e-poetry.md)):

- o pip instala no ambiente **ativo**, a partir do `requirements.txt`; por isso a instrução manda
  ativar um venv antes;
- o Poetry lê o `pyproject.toml`, cria o próprio ambiente e grava as versões exatas no
  `poetry.lock`.

## Como fica a saída

Com o numpy instalado e as outras duas faltando, a saída completa do programa é:

```text

LOADING STATUS: Loading programs...

Checking dependencies:
[MISSING] pandas - Data manipulation not available
[OK] numpy (2.5.4) - Numerical computation ready
[MISSING] matplotlib - Visualization not available

Missing dependencies: pandas, matplotlib

With pip: installs the packages listed in requirements.txt
into the active environment (activate a venv first)
  pip install -r requirements.txt
  python3 loading.py

With Poetry: reads pyproject.toml, creates its own virtual
environment and records the exact versions in poetry.lock
  poetry install
  poetry run python loading.py
```

O programa termina aí, com o código de saída `1` ([O main](./08-o-main.md)). A página
[Rodar com o pip](./10-rodar-com-pip.md) produz essa saída de verdade.
