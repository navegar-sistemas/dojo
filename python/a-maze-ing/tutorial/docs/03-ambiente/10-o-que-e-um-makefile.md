---
sidebar_position: 2
title: O que é um Makefile
---

# O que é um `Makefile`

O projeto tem comandos longos que se repetem: criar o ambiente virtual, instalar as ferramentas,
rodar o programa, verificar o código. O enunciado exige que eles fiquem num arquivo `Makefile`,
cada um com um nome curto. Esta página explica o que é esse arquivo, como se lê uma regra e
quais regras o projeto escreve.

## O que é o `make`

O `make` é um programa de linha de comando. Ele costuma vir instalado; se não estiver, os
[pré-requisitos](../00-introducao/03-pre-requisitos.md#ferramentas) mostram como instalar. Ele
lê um arquivo chamado `Makefile`, na pasta atual, e executa os comandos de uma **regra** pelo
nome dela. Digitar `make run` executa os comandos da regra `run`.

## Como ler uma regra

Uma regra tem um nome (o **alvo**), dois-pontos e, nas linhas de baixo, os comandos:

![Uma regra do Makefile: o alvo lint, os dois-pontos, e dois comandos começando com TAB](/img/ambiente/regra-makefile.svg)

O `$(PY)` e o `$(MYPY_FLAGS)` da figura são **variáveis** do `Makefile`: na hora de rodar, o
`make` troca `$(PY)` pelo caminho do Python do projeto, `.venv/bin/python`. O `$(PY)` é
explicado na [próxima página](./02-makefile-instalar-e-rodar.md#as-variáveis), e o
`$(MYPY_FLAGS)` na [página da regra `lint`](./03-makefile-limpar-verificar-empacotar.md#lint-a-regra).

- o **alvo** é o nome usado no terminal: `make lint`;
- os **dois-pontos** fecham o nome;
- cada linha de comando começa com um caractere **TAB** (a tecla Tab), nunca com espaços. Com
  espaços, o `make` não reconhece a linha como comando e para com o erro `missing separator`.
  Muitos editores trocam o TAB por espaços sem avisar; para conferir, o comando
  `cat -et Makefile` mostra cada TAB como `^I` e o fim de cada linha como `$`:

  ```text
  install:$
  ^Ipython3 -m venv $(VENV)$
  ```

  Uma linha de comando que começa com espaços em vez de `^I` está errada;
- os comandos rodam em ordem, um por linha, como se fossem digitados no terminal. Se um falha, o
  `make` para ali e não roda os seguintes.

## As regras que o enunciado exige

O enunciado pede estas regras, cada uma com um trabalho:

| Regra | O que o enunciado pede |
|---|---|
| `install` | instalar as dependências do projeto com `pip` (ou outro instalador) |
| `run` | executar o programa principal |
| `debug` | executar o programa principal com o depurador do Python, como o `pdb` |
| `clean` | apagar arquivos temporários e caches, como `__pycache__` e `.mypy_cache` |
| `lint` | rodar o `flake8 .` e o `mypy .` com cinco opções que ele fixa, listadas na [página da regra `lint`](./03-makefile-limpar-verificar-empacotar.md#lint-a-regra) |
| `lint-strict` | opcional e "fortemente recomendada": o `flake8 .` e o `mypy . --strict` |

O projeto acrescenta uma regra por escolha própria, `build`, que monta o pacote do `mazegen`. O
motivo: na avaliação, o enunciado pede para reconstruir o pacote a partir do código-fonte, e um
`make build` faz isso com um comando só.

As regras ficam em três páginas: [instalar e rodar](./02-makefile-instalar-e-rodar.md)
(`install`, `run`, `debug`), [verificar](./03-makefile-limpar-verificar-empacotar.md) (`lint`,
`lint-strict`) e [limpar e empacotar](./09-makefile-empacotar.md) (`clean`, `build` e o arquivo
completo).

## Criando o arquivo

Crie, na raiz do projeto, um arquivo de texto chamado exatamente `Makefile`, sem extensão. Cada
trecho de código das três páginas seguintes entra nesse arquivo, colado no fim, na ordem em que
aparece. O [arquivo completo](./09-makefile-empacotar.md#o-arquivo-completo) tem os mesmos
trechos em outra ordem: a variável `MYPY_FLAGS` fica no topo, junto das outras, e a regra
`clean` vem antes de `lint`. A ordem não muda o que cada regra faz, e quem preferir pode copiar
só o arquivo completo.
