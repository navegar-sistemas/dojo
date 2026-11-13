---
sidebar_position: 10
title: Instalar com o pip
---

# Instalar com o pip

O roteiro do enunciado testa o `loading.py` duas vezes: antes e depois de instalar os reagentes
com o `pip`. Todos os comandos desta página rodam com o `lab_env` **ativado** (o prompt mostra
`(lab_env)`; se não mostrar, rode `source lab_env/bin/activate`).

## Sem os reagentes

O `lab_env` ainda está vazio:

```bash
python3 ex0/loading.py
```

```text

REAGENT STATUS: Loading reagents...

Checking dependencies:
[MISSING] pandas - Data manipulation unavailable
[MISSING] numpy - Numerical computation unavailable

pip vs Poetry:
  requirements.txt declares what to install; pip resolves it at install time.
  pyproject.toml declares the same constraints, and Poetry pins the resolved
  versions in poetry.lock so every install is identical.

Missing reagents: pandas, numpy
Install them with pip:
  pip install -r ex0/requirements.txt
Or with Poetry:
  poetry -P ex0 install
  poetry -P ex0 run python ex0/loading.py
```

O programa não travou: terminou normalmente, depois de mostrar o que falta e como instalar. Um
programa que termina normalmente devolve ao terminal o **código de saída** `0`; um que para com um
erro devolve outro número. `$?` guarda o código de saída do último comando:

```bash
echo $?
```

```text
0
```

## Instalar

```bash
pip install -r ex0/requirements.txt
```

O `-r` manda o `pip` ler a lista de um arquivo. Ele baixa e instala as bibliotecas, mostrando cada
passo, e a última linha da saída lista o que foi instalado:

```text
Successfully installed numpy-2.5.4 pandas-3.1.1 python-dateutil-4.0.0 tzdata-2026.6
```

Os números são as versões que o `pip` escolheu, as mais novas que cumprem os especificadores no
dia da instalação; na sua máquina podem ser outros. Com Python 3.10, o `pip` escolhe versões mais
antigas, as últimas que funcionam nele (a `pandas` 2.3.3 e o `numpy` 2.2.6, aqui), e a lista de
dependências transitivas muda junto. `python-dateutil` e `tzdata` são dependências transitivas:
vieram porque a `pandas` precisa delas.

## Com os reagentes

```bash
python3 ex0/loading.py
```

```text

REAGENT STATUS: Loading reagents...

Checking dependencies:
[OK] pandas (3.1.1) - Data manipulation ready
[OK] numpy (2.5.4) - Numerical computation ready

pip vs Poetry:
  requirements.txt declares what to install; pip resolves it at install time.
  pyproject.toml declares the same constraints, and Poetry pins the resolved
  versions in poetry.lock so every install is identical.

All reagents present and accounted for.
```

É a saída do enunciado, com as versões instaladas aqui no lugar de `2.1.0` e `1.25.0`.

## O que está no laboratório

`pip list` mostra tudo o que está instalado no ambiente:

```bash
pip list
```

```text
Package         Version
--------------- -------
numpy           2.5.4
pandas          3.1.1
pip             26.3
python-dateutil 4.0.0
tzdata          2026.6
```

Só o que foi instalado aqui, e mais nada: as bibliotecas do Python global não aparecem, e nada
foi instalado fora do `lab_env`. É o laboratório selado. Com Python 3.10, a lista também tem
`pytz` e `six`, dependências transitivas da `pandas` 2.3.3. No 3.10 e no 3.11, ela também tem o
`setuptools`, que o ambiente dessas versões traz de nascença.
