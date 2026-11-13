---
sidebar_position: 4
title: O resultado final
---

# O resultado final

Esta é a saída de cada programa pronto. Os programas não recebem argumentos nem leem o teclado. Os
comandos são rodados **dentro da pasta de cada exercício** (`ex0`, `ex1` ou `ex2`), como nos
exemplos do enunciado, e só funcionam depois que os arquivos e os ambientes existirem: a página
de rodar e conferir de cada exercício faz tudo, passo a passo.

Parte das saídas depende da máquina: caminhos de pastas e números de versão. Nos caminhos,
`/…` marca o trecho que muda de máquina para máquina (o lugar onde o Python está instalado, ou
onde fica a pasta do projeto); o resto aparece como no terminal.

## Exercício 0

Fora de qualquer ambiente virtual:

```bash
python3 construct.py
```

```text

MATRIX STATUS: You're still plugged in

Current Python: /…/bin/python3.15
Virtual Environment: None detected

WARNING: You're in the global environment!
The machines can see everything you install.

To enter the construct, run:
python -m venv matrix_env
source matrix_env/bin/activate # On Unix
matrix_env\Scripts\activate  # On Windows

Then run this program again.

Package installation path:
/…/lib/python3.15/site-packages
```

Dentro do ambiente virtual `matrix_env`, já ativado:

```bash
python3 construct.py
```

```text

MATRIX STATUS: Welcome to the construct

Current Python: /…/the-matrix/ex0/matrix_env/bin/python3
Virtual Environment: matrix_env
Environment Path: /…/the-matrix/ex0/matrix_env

SUCCESS: You're in an isolated environment!
Safe to install packages without affecting
the global system.

Package installation path:
/…/the-matrix/ex0/matrix_env/lib/python3.15/site-packages
```

O `3.15` é a versão do Python; com outra versão, o número muda.

## Exercício 1

Com as bibliotecas instaladas:

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

Environment: /…/the-matrix/ex1/matrix_env
```

Os números entre parênteses são as versões instaladas, e podem ser outros. A última linha não está
na saída do enunciado: é a pasta do ambiente onde o programa rodou, aqui o venv do pip; rodado pelo
Poetry, ela mostra o ambiente que o Poetry criou. O programa grava o
gráfico no arquivo `matrix_analysis.png`:

![Gráfico de linhas com 1000 pontos: o sinal, em azul, sobe e desce entre cerca de -21 e 26, e a tendência, em laranja, é a média dos 50 pontos até cada um, uma linha suave que acompanha o sinal a partir do ponto 49](/img/ex1/matrix_analysis.png)

## Exercício 2

Com o arquivo `.env` de desenvolvimento:

```bash
python3 oracle.py
```

```text

ORACLE STATUS: Reading the Matrix...

Configuration loaded:
Mode: development
Database: Connected to local instance
API Access: Authenticated
Log Level: DEBUG
Zion Network: Online

Environment security check:
[OK] No hardcoded secrets detected
[OK] .env file properly configured
[OK] Production overrides available

The Oracle sees all configurations.
```

Esta saída é igual, linha por linha, à do enunciado.
