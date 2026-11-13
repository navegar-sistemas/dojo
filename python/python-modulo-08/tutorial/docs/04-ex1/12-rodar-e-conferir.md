---
sidebar_position: 12
title: Rodar e conferir
---

# Rodar e conferir

As duas páginas anteriores já rodaram o programa em todas as situações que o enunciado pede: sem
ambiente virtual, com um ambiente vazio, com parte das bibliotecas, com todas pelo pip e com todas
pelo Poetry. Falta conferir o código e o caso de erro na gravação. Os comandos continuam na pasta
`ex1`.

## Conferir estilo e tipos

```bash
../.venv/bin/flake8 loading.py
../.venv/bin/mypy --disallow-untyped-defs loading.py
```

```text
Success: no issues found in 1 source file
```

O flake8 não imprime nada, e o mypy não acha problema, mesmo rodando no `.venv` das ferramentas,
onde não há numpy, pandas nem matplotlib: o programa não tem nenhum `import` dessas bibliotecas
para ele procurar ([Importar pelo nome](../02-conceitos/03-importar-pelo-nome.md)). O enunciado
aceitaria avisos de `import` neste exercício, mas aqui não há nenhum.

## Quando o gráfico não pode ser gravado

Para provocar o erro de gravação, troque o arquivo do gráfico por uma **pasta** com o mesmo nome:
o programa não consegue gravar uma imagem no lugar de uma pasta.

```bash
rm matrix_analysis.png
mkdir matrix_analysis.png
../.venv/bin/poetry run python loading.py
echo $?
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
Analysis failed: [Errno 21] Is a directory: 'matrix_analysis.png'
1
```

O `savefig` lançou `IsADirectoryError` ("é uma pasta"), um tipo filho de `OSError`; o `except` do
`main` o capturou, e a mensagem do erro saiu numa linha só, sem traceback
([O main](./08-o-main.md#não-deu-para-gravar-o-gráfico)). O código de saída é `1`.

Apague a pasta e gere o gráfico de novo:

```bash
rmdir matrix_analysis.png
../.venv/bin/poetry run python loading.py > /dev/null
echo $?
```

```text
0
```

`rmdir` apaga uma pasta vazia, e `> /dev/null` descarta a saída do programa, já conferida antes
(`/dev/null` é um arquivo especial que joga fora tudo o que recebe).

## Resumo das situações

| Situação | Comando | Resultado | Código de saída |
|---|---|---|---|
| Python global, sem as bibliotecas | `python3 loading.py` | `[MISSING]` nas três e as instruções | `1` |
| venv vazio | `python3 loading.py` (venv ativado) | `[MISSING]` nas três e as instruções | `1` |
| venv só com numpy | `python3 loading.py` (venv ativado) | `[OK]` no numpy, `[MISSING]` nas outras | `1` |
| venv com o `requirements.txt` | `python3 loading.py` (venv ativado) | análise e gráfico | `0` |
| ambiente do Poetry | `../.venv/bin/poetry run python loading.py` | análise e gráfico | `0` |
| gráfico sem poder ser gravado | `../.venv/bin/poetry run python loading.py` | `Analysis failed: ...` | `1` |

Volte para a pasta do projeto:

```bash
cd ..
```
