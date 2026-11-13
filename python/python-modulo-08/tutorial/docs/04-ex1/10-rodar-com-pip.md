---
sidebar_position: 10
title: Rodar com o pip
---

# Rodar com o pip

O caminho do pip: um ambiente virtual criado e ativado à mão, as bibliotecas instaladas pelo
`requirements.txt`. No caminho, o programa roda em três situações: sem nenhuma biblioteca, com
uma só e com todas.

Os comandos desta página e das duas seguintes são rodados dentro da pasta `ex1`, sem nenhum
ambiente ativado:

```bash
cd ex1
```

## Um ambiente vazio

Crie o ambiente do exercício e ative-o:

```bash
python3 -m venv matrix_env
source matrix_env/bin/activate
```

Um venv novo não tem biblioteca nenhuma, só o pip:

```bash
python3 loading.py
```

```text

LOADING STATUS: Loading programs...

Checking dependencies:
[MISSING] pandas - Data manipulation not available
[MISSING] numpy - Numerical computation not available
[MISSING] matplotlib - Visualization not available

Missing dependencies: pandas, numpy, matplotlib

With pip: installs the packages listed in requirements.txt
into the active environment (activate a venv first)
  pip install -r requirements.txt
  python3 loading.py

With Poetry: reads pyproject.toml, creates its own virtual
environment and records the exact versions in poetry.lock
  poetry install
  poetry run python loading.py
```

```bash
echo $?
```

```text
1
```

O código de saída `1` confirma que o programa parou sem fazer a análise.

## Uma biblioteca só

Com o ambiente ativado, `pip` é o pip do `matrix_env`, e instala nele:

```bash
pip install numpy
```

A saída termina com:

```text
Installing collected packages: numpy
Successfully installed numpy-2.5.4

[notice] A new release of pip is available: 26.1.1 -> 26.3
[notice] To update, run: pip install --upgrade pip
```

As duas linhas `[notice]` avisam que existe um pip mais novo que o que veio no venv. Elas só
aparecem quando há versão nova, não impedem nada e podem ser ignoradas; seguir a sugestão
(`pip install --upgrade pip`) atualiza o pip deste ambiente.

```bash
python3 loading.py
```

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

O programa reconhece o numpy, mostra a versão dele e lista só as duas que faltam.

## Todas as bibliotecas

```bash
pip install -r requirements.txt
```

O pip lê as três linhas do arquivo. O numpy já está instalado e atende ao `>=1.25.0`, então ele
fica como está (`Requirement already satisfied`, "requisito já atendido"); os outros dois são
baixados com as suas dependências. A saída termina com a lista do que foi instalado e o mesmo
aviso do pip:

```text
Successfully installed contourpy-1.4.0 cycler-0.12.1 fonttools-4.68.0 kiwisolver-1.5.1 matplotlib-3.11.2 packaging-26.3 pandas-3.1.1 pillow-13.0.0 pyparsing-3.3.3 python-dateutil-4.0.0 tzdata-2026.6

[notice] A new release of pip is available: 26.1.1 -> 26.3
[notice] To update, run: pip install --upgrade pip
```

As versões podem ser outras: o pip escolhe as mais novas que servem para o seu Python.

```bash
python3 loading.py
```

```text

LOADING STATUS: Loading programs...

Checking dependencies:
[OK] pandas (3.1.1) - Data manipulation ready
[OK] numpy (2.5.4) - Numerical computation ready
[OK] matplotlib (3.11.2) - Visualization ready

Analyzing Matrix data...
Processing 1000 data points...
Generating visualization...

Analysis complete!
Results saved to: matrix_analysis.png
```

```bash
echo $?
```

```text
0
```

Na primeira vez que o matplotlib roda numa máquina, ele monta uma lista das fontes do sistema;
se isso demorar mais de cinco segundos, ele avisa
`Matplotlib is building the font cache; this may take a moment.` antes da saída. É só na primeira
vez.

O gráfico apareceu na pasta:

```bash
ls
```

```text
loading.py
matrix_analysis.png
matrix_env
pyproject.toml
requirements.txt
```

## O que o pip instalou

`pip freeze` lista tudo o que está instalado no ambiente, com as versões exatas, no formato do
`requirements.txt`:

```bash
pip freeze
```

```text
contourpy==1.4.0
cycler==0.12.1
fonttools==4.68.0
kiwisolver==1.5.1
matplotlib==3.11.2
numpy==2.5.4
packaging==26.3
pandas==3.1.1
pillow==13.0.0
pyparsing==3.3.3
python-dateutil==4.0.0
tzdata==2026.6
```

São 12 pacotes para 3 dependências: os outros 9 são dependências delas. É essa lista que o pip
**não** guarda sozinho: amanhã, o mesmo `pip install -r requirements.txt` pode instalar versões
mais novas ([pip e Poetry](./02-pip-e-poetry.md)).

## Fora do venv

Desative o ambiente e rode o programa com o Python global:

```bash
deactivate
python3 loading.py
```

```text

LOADING STATUS: Loading programs...

Checking dependencies:
[MISSING] pandas - Data manipulation not available
[MISSING] numpy - Numerical computation not available
[MISSING] matplotlib - Visualization not available

Missing dependencies: pandas, numpy, matplotlib

With pip: installs the packages listed in requirements.txt
into the active environment (activate a venv first)
  pip install -r requirements.txt
  python3 loading.py

With Poetry: reads pyproject.toml, creates its own virtual
environment and records the exact versions in poetry.lock
  poetry install
  poetry run python loading.py
```

As bibliotecas continuam instaladas, mas no `site-packages` do `matrix_env`, que o Python global
não enxerga. Se o seu Python global tiver alguma delas instalada pelo sistema, a linha dela sai
com `[OK]`.

## No Python 3.10

No Python 3.10, o pip escolhe as versões mais novas que ainda aceitam o 3.10: pandas 2.3.3,
numpy 2.2.6 e matplotlib 3.10.9, mais dois pacotes, `pytz` e `six`, que essas versões mais
antigas pedem como dependência. As linhas `[OK]` mostram essas versões, e o aviso `[notice]` cita
o pip que veio com o Python 3.10 (`23.0.1 -> 26.3`); o resto da saída é igual.
