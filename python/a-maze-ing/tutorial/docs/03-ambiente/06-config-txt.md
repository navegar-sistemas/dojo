---
sidebar_position: 6
title: O config.txt padrão
---

# O `config.txt` padrão

## O que é

O arquivo de configuração que vai no repositório e que o `make run` usa. O formato e as chaves
estão na parte 1; aqui entra o conteúdo escolhido.

## As escolhas

| Linha | Por quê |
|---|---|
| `WIDTH=20`, `HEIGHT=15` | grande o bastante para o "42" (mínimo 9x7) e pequeno para caber num terminal comum |
| `ENTRY=0,0`, `EXIT=19,14` | cantos opostos: o caminho atravessa o labirinto inteiro |
| `OUTPUT_FILE=maze.txt` | o arquivo que o `.gitignore` ignora |
| `PERFECT=False` | o modo padrão do projeto, o tabuleiro Pac-Man |
| `# SEED=42` | comentada: cada execução gera um labirinto diferente |

### Um comentário antes de cada chave

Quem abre o arquivo pela primeira vez descobre, sem ler o README, o que cada chave faz e quais
valores aceita. O comentário é em inglês, como o resto do repositório.

### A `SEED` comentada

Sem `SEED`, o gerador sorteia uma semente nova a cada execução, e o `make run` mostra um
labirinto diferente toda vez. Para repetir um labirinto (para depurar, ou para mostrar o mesmo
desenho duas vezes), basta tirar o `#`:

```text
SEED=42
```

Com a `SEED` definida, o mesmo arquivo gera sempre a mesma grade e o mesmo caminho.

## O arquivo completo

```text title="config.txt"
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
