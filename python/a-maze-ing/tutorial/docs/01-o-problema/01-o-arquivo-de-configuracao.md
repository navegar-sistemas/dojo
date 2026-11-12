---
sidebar_position: 1
title: O arquivo de configuração
---

# O arquivo de configuração

Tudo o que o programa precisa saber vem de um arquivo de texto passado na linha de comando:

```bash
python3 a_maze_ing.py config.txt
```

## Formato

Uma chave por linha, no formato `CHAVE=valor`. Linhas que começam com `#` são comentários.

```ini
# Width of the maze, in cells (1 to 100)
WIDTH=20
# Height of the maze, in cells (1 to 100)
HEIGHT=15
# Entry cell as x,y (x = column, y = row, both from 0)
ENTRY=0,0
# Exit cell as x,y
EXIT=19,14
# File that receives the maze in hexadecimal
OUTPUT_FILE=maze.txt
# True: perfect maze (single path); False: Pac-Man board (default)
PERFECT=False
# Uncomment to get the same maze on every run
# SEED=42
```

## As chaves

| Chave | Obrigatória | Exemplo | Significado |
|---|---|---|---|
| `WIDTH` | sim | `20` | número de colunas, de 1 a 100 |
| `HEIGHT` | sim | `15` | número de linhas, de 1 a 100 |
| `ENTRY` | sim | `0,0` | célula de entrada, `x,y` |
| `EXIT` | sim | `19,14` | célula de saída, `x,y`, diferente da entrada |
| `OUTPUT_FILE` | sim | `maze.txt` | arquivo onde o labirinto é gravado |
| `PERFECT` | sim | `False` | `True` para labirinto perfeito, `False` para tabuleiro Pac-Man |
| `SEED` | não | `42` | semente do sorteio; com ela, o mesmo config gera o mesmo labirinto |

## Coordenadas `x,y`

`x` é a **coluna** e `y` é a **linha**, ambos contados a partir de 0, com a origem no canto de
cima à esquerda:

![Grade 6 por 4 com as coordenadas x,y de algumas células](/img/problema/coordenadas.svg)

Essa convenção vale em todo o projeto: no config, no arquivo de saída, nas mensagens de erro e no
código. Nunca existe `(linha, coluna)`.

## Regras de leitura

O arquivo é escrito por pessoas, então a leitura perdoa o que é inofensivo e recusa o que é
ambíguo:

| Situação | O que acontece |
|---|---|
| espaços em volta (`WIDTH = 20`) | ignorados |
| chave em minúsculas (`width=20`) | aceita: `WIDTH` e `width` são a mesma chave |
| linha vazia ou comentário | pulada |
| chave repetida | vale a última |
| chave desconhecida (`COLOR=red`) | ignorada |
| linha sem `=` (`HEIGHT 15`) | erro, citando o número da linha |
| chave obrigatória faltando | erro, listando todas as que faltam |
| valor inválido (`WIDTH=abc`) | erro, citando a chave e o valor |

## Erros

Todo erro termina o programa com **uma única linha** em stderr, começando com `Error: `, e
código de saída 1. Nunca aparece traceback:

```text
Error: config.txt: missing mandatory key(s): WIDTH, HEIGHT
Error: config.txt: WIDTH must be an integer, got 'abc'
Error: config.txt: ENTRY and EXIT must differ
```

A parte 11 implementa essa leitura. Por enquanto, basta saber o que entra no programa.
