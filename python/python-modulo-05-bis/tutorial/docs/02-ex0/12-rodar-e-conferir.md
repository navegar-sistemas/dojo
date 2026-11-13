---
sidebar_position: 12
title: Rodar e conferir
---

# Rodar e conferir

Os comandos desta página chamam cada Python pelo caminho (`python3` para o global,
`lab_env/bin/python` para o do laboratório), e por isso funcionam com ou sem o `lab_env` ativado.

## Estilo e tipos

```bash
.venv/bin/flake8 ex0
.venv/bin/mypy --disallow-untyped-defs ex0
```

```text
Success: no issues found in 2 source files
```

O flake8 não imprime nada, e o mypy confere os dois arquivos `.py` sem achar problema.

## construct.py contra o enunciado

Os caminhos da saída mudam de máquina para máquina, e por isso a comparação troca as partes
variáveis pelas do enunciado antes de comparar. Fora do laboratório, a única linha variável é a
`Current Python`:

```bash
diff <(python3 ex0/construct.py | sed 's|^Current Python: .*|Current Python: /usr/bin/python3.11|') - <<'FIM'

LABORATORY STATUS: You are working in the open

Current Python: /usr/bin/python3.11
Virtual Environment: None detected

WARNING: You are in the global environment!
Every reagent you install here leaks into the whole system.

To seal the laboratory, run:
python3 -m venv lab_env
source lab_env/bin/activate # On Unix
lab_env\Scripts\activate  # On Windows

Then run this program again.
FIM
```

- `<(comando)` entrega ao `diff` a saída do comando como se fosse um arquivo;
- o `|` (*pipe*) liga a saída de um programa à entrada do seguinte. `sed 's|antes|depois|'` troca,
  em cada linha, o texto que casa com `antes` por `depois`; aqui, `^Current Python: .*` casa com a
  linha inteira que começa com `Current Python: ` (o `^` é o começo da linha, e `.*` é "qualquer
  coisa até o fim");
- o `-` diz ao `diff` para ler o segundo texto da entrada do comando, e `<<'FIM'` escreve nessa
  entrada as linhas seguintes, até a linha `FIM`: a saída copiada do enunciado. Cole o bloco
  inteiro, até a linha `FIM`; sem ela, o terminal fica esperando mais linhas;
- o `diff` compara os dois textos linha a linha e só imprime as diferenças.

Sem nenhuma linha impressa, tudo o que não é caminho é igual ao enunciado, inclusive a linha vazia
do começo e os dois espaços da linha do Windows.

Dentro do laboratório, o Python chamado como `lab_env/bin/python` termina o caminho em
`bin/python`, como o enunciado. A comparação troca o caminho da pasta do projeto (`$PWD`, a
variável do terminal com a pasta atual) por `/path/to` e a versão do Python por `3.11`:

```bash
diff <(lab_env/bin/python ex0/construct.py | sed -e "s|$PWD|/path/to|" -e 's|python3\.[0-9]*/|python3.11/|') - <<'FIM'

LABORATORY STATUS: The laboratory is sealed

Current Python: /path/to/lab_env/bin/python
Virtual Environment: lab_env
Environment Path: /path/to/lab_env

SUCCESS: You are working in an isolated environment!
Safe to install reagents without affecting
the global system.

Reagent installation path:
/path/to/lab_env/lib/python3.11/site-packages
FIM
```

Sem nenhuma linha impressa. Os dois `-e` passam duas trocas ao mesmo `sed`; na segunda,
`python3\.[0-9]*/` casa com `python3.`, os números da versão e a barra (o `\.` é um ponto de
verdade, e `[0-9]*` é "zero ou mais algarismos"). Se a pasta do projeto estiver dentro de um
caminho com atalhos (*links*), o `$PWD` pode não bater com o caminho que o Python mostra, e o
`diff` aponta as três linhas com caminho; o resto continua valendo.

## Os dois locais de pacotes

O mesmo pedido, `site.getsitepackages()[0]`, feito ao Python global e ao do laboratório:

```bash
python3 -c 'import site; print(site.getsitepackages()[0])'
lab_env/bin/python -c 'import site; print(site.getsitepackages()[0])'
```

```text
/path/to/lib/python3.15/site-packages
/path/to/the-codex/lab_env/lib/python3.15/site-packages
```

A primeira é a pasta do Python global, compartilhada por todos os programas da máquina; o começo
dela muda com o sistema e com o jeito como o Python foi instalado (no Debian e no Ubuntu, costuma
ser `/usr/local/lib/python3.X/dist-packages`). A segunda fica dentro do `lab_env` e só ele a
enxerga. É a diferença de locais que o enunciado pede para `construct.py` mostrar: o programa
imprime a segunda dentro do laboratório e, fora dele, avisa que tudo vai para a primeira.

## construct.py no ambiente do Poetry

O ambiente que o Poetry criou também é um ambiente virtual, e `construct.py` o reconhece:

```bash
.venv/bin/poetry -P ex0 run python ex0/construct.py
```

```text

LABORATORY STATUS: The laboratory is sealed

Current Python: /path/to/virtualenvs/sealed-laboratory-YaXe80qZ-py3.15/bin/python
Virtual Environment: sealed-laboratory-YaXe80qZ-py3.15
Environment Path: /path/to/virtualenvs/sealed-laboratory-YaXe80qZ-py3.15

SUCCESS: You are working in an isolated environment!
Safe to install reagents without affecting
the global system.

Reagent installation path:
/path/to/virtualenvs/sealed-laboratory-YaXe80qZ-py3.15/lib/python3.15/site-packages
```

O nome do ambiente é o que o Poetry escolheu; o teste `sys.prefix != sys.base_prefix` vale para
qualquer ambiente virtual.

## loading.py contra o enunciado

As versões mudam com o tempo, e a comparação as troca por `(VERSION)` dos dois lados:

```bash
diff <(lab_env/bin/python ex0/loading.py | sed -E 's/\([0-9.]+\)/(VERSION)/') - <<'FIM'

REAGENT STATUS: Loading reagents...

Checking dependencies:
[OK] pandas (VERSION) - Data manipulation ready
[OK] numpy (VERSION) - Numerical computation ready

pip vs Poetry:
  requirements.txt declares what to install; pip resolves it at install time.
  pyproject.toml declares the same constraints, and Poetry pins the resolved
  versions in poetry.lock so every install is identical.

All reagents present and accounted for.
FIM
```

Sem nenhuma linha impressa. O `-E` deixa o `sed` entender os parênteses de `\([0-9.]+\)` como
caracteres de verdade (com a barra antes) e o `+` como "um ou mais"; o padrão casa com um número
de versão entre parênteses, como `(3.1.1)`.

## Só um reagente faltando

Um ambiente com o `numpy` e sem a `pandas` mostra o caso em que falta só um:

```bash
python3 -m venv half_env
half_env/bin/python -m pip install numpy
half_env/bin/python ex0/loading.py
```

A instalação termina com `Successfully installed numpy-2.5.4` (e, num ambiente novo, com o aviso
`[notice]` de versão nova do `pip`, que não atrapalha). O programa:

```text

REAGENT STATUS: Loading reagents...

Checking dependencies:
[MISSING] pandas - Data manipulation unavailable
[OK] numpy (2.5.4) - Numerical computation ready

pip vs Poetry:
  requirements.txt declares what to install; pip resolves it at install time.
  pyproject.toml declares the same constraints, and Poetry pins the resolved
  versions in poetry.lock so every install is identical.

Missing reagents: pandas
Install them with pip:
  pip install -r ex0/requirements.txt
Or with Poetry:
  poetry -P ex0 install
  poetry -P ex0 run python ex0/loading.py
```

Depois, apague o ambiente de teste:

```bash
rm -rf half_env
```
