---
sidebar_position: 1
title: O problema
---

# O problema

Um programa que usa bibliotecas de fora só roda numa máquina onde elas estão instaladas, nas
versões certas. Quem recebe o programa precisa saber **quais** bibliotecas instalar, e o
programa precisa se comportar bem quando elas faltam. O exercício 1 escreve uma pequena análise
de dados com três bibliotecas e entrega, junto com ela, a lista do que instalar em dois formatos:
o do pip e o do Poetry.

## O que o enunciado pede

Três arquivos na pasta `ex1/`:

| Arquivo | O que é |
|---|---|
| `loading.py` | o programa de análise |
| `requirements.txt` | a lista de dependências no formato do pip ([O requirements.txt](./03-o-requirements-txt.md)) |
| `pyproject.toml` | a descrição do projeto e das dependências no formato do Poetry ([O pyproject.toml](./04-o-pyproject-toml.md)) |

O programa:

- usa o **numpy** para os cálculos e para **gerar** os dados simulados ("dados da Matrix"): os
  dados têm de vir do numpy, e não de uma lista escrita no código nem de `range()`;
- usa o **pandas** para manipular os dados;
- usa o **matplotlib** para desenhar um gráfico simples;
- detecta quais bibliotecas estão instaladas e, se faltar alguma, mostra uma mensagem útil, com
  as instruções de instalação pelo pip e pelo Poetry;
- tem uma **função de comparação** que mostra as versões dos pacotes instalados;
- mostra na própria saída as diferenças entre o pip e o Poetry.

Os módulos autorizados são `pandas`, `requests`, `matplotlib`, `numpy`, `sys` e `importlib`. O
`requests` serviria para buscar dados reais numa API; o enunciado deixa isso opcional, e o
tutorial não busca (os dados são gerados pelo numpy, como o enunciado pede por padrão).

## A saída do enunciado

```console
$> python loading.py

LOADING STATUS: Loading programs...

Checking dependencies:
[OK] pandas (2.1.0) - Data manipulation ready
[OK] numpy (1.25.0) - Numerical computation ready
[OK] requests (2.31.0) - Network access ready
[OK] matplotlib (3.7.2) - Visualization ready

Analyzing Matrix data...
Processing 1000 data points...
Generating visualization...

Analysis complete!
Results saved to: matrix_analysis.png
```

- os números entre parênteses são as versões instaladas na máquina de quem escreveu o enunciado;
- a linha do `requests` só aparece em quem busca dados numa API, diz o enunciado. Aqui ela não
  aparece;
- `matrix_analysis.png` é o arquivo do gráfico.

## Os testes pedidos

```console
$> python3 loading.py
# Should show missing dependencies and installation instructions for pip and Poetry
```

```console
$> pip install -r requirements.txt
$> python3 loading.py
# Should run analysis and create visualization
```

```console
$> poetry install
$> poetry run python loading.py
# Should run analysis and create visualization with Poetry environment
```

Sem as dependências, o programa mostra o que falta e como instalar pelos dois caminhos; com elas
instaladas pelo pip, ou pelo Poetry, ele roda a análise e cria o gráfico.

## O que fica a cargo de quem implementa

O enunciado pede que as diferenças entre o pip e o Poetry apareçam na saída do programa, mas a
saída de exemplo, a do caso em que tudo está instalado, não mostra nada sobre isso: rodada pelo
pip ou pelo Poetry, ela seria igual. A **escolha do tutorial** mantém todas as linhas da saída de
exemplo e mostra a diferença em dois lugares:

- no fim da saída de sucesso, uma linha a mais, `Environment:`, com a pasta do ambiente em que o
  programa rodou: o `matrix_env` criado à mão para o pip, ou o ambiente que o Poetry criou na
  pasta dele ([O main](./08-o-main.md#deu-tudo-certo));
- na saída do caso em que faltam bibliotecas, que explica o que cada ferramenta faz e quais
  comandos usar ([As instruções de instalação](./06-as-instrucoes-de-instalacao.md)).

## O aviso sobre flake8 e mypy

O enunciado permite, só neste exercício, avisos do flake8 e do mypy sobre `import`, e lembra que
há jeitos de evitá-los. O tutorial evita todos com `importlib.import_module`
([Importar pelo nome](../02-conceitos/03-importar-pelo-nome.md)), e o código fica sem aviso
nenhum.
