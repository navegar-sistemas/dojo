---
sidebar_position: 8
title: O config.txt padrão
---

# O `config.txt` padrão

O enunciado exige que o repositório traga um arquivo de opções pronto, e o `make run` precisa de
um para rodar o programa. Esta página escolhe o conteúdo desse arquivo, o `config.txt`.

## Relembrando o formato

O arquivo de opções tem uma opção por linha, no formato `CHAVE=valor`, e as linhas que começam
com `#` são comentários, que o programa ignora. As chaves estão explicadas na
[parte 1](../01-o-problema/03-o-arquivo-de-configuracao.md):

| Chave | O que define |
|---|---|
| `WIDTH`, `HEIGHT` | a largura e a altura do labirinto, em células |
| `ENTRY`, `EXIT` | as células de entrada e de saída, como `x,y` (`x` é a coluna, `y` a linha, os dois a partir de 0) |
| `OUTPUT_FILE` | o arquivo onde o labirinto é gravado |
| `PERFECT` | `True` para labirinto perfeito (um único caminho entre duas células), `False` para tabuleiro Pac-Man (com rotas alternativas e quase sem becos) |
| `SEED` | opcional: a semente do sorteio; mesmo número, mesmo labirinto |

## As escolhas

Os valores são escolhas do projeto:

| Linha | Por quê |
|---|---|
| `WIDTH=20`, `HEIGHT=15` | grande o bastante para o "42" (que precisa de pelo menos 9x7) e pequeno o bastante para caber num terminal comum |
| `ENTRY=0,0`, `EXIT=19,14` | cantos opostos: o caminho atravessa o labirinto inteiro |
| `OUTPUT_FILE=maze.txt` | um nome curto, na raiz do projeto; como o arquivo é regravado a cada execução, ele fica fora do git (o `.gitignore` da [página anterior](./05-flake8-e-gitignore.md) o lista) |
| `PERFECT=False` | o tabuleiro Pac-Man, que o enunciado chama de modo padrão (o "default" do comentário). Mesmo assim, a chave `PERFECT` é obrigatória no arquivo, então o valor fica escrito; só no `MazeGenerator` ([parte 9](../09-gerador/01-a-fachada.md)) o `perfect=False` é usado quando o parâmetro é omitido |
| `# SEED=42` | comentada: cada execução gera um labirinto diferente |

### Um comentário antes de cada chave

Quem abre o arquivo pela primeira vez descobre, sem ler o README, o que cada chave faz e quais
valores aceita. Os comentários são em inglês, como todo o resto do repositório.

O "1 to 100" dos comentários de `WIDTH` e `HEIGHT` também é escolha do projeto: o enunciado não
fixa um limite, mas grades grandes ficam lentas de gerar (uma 200x100 já leva mais de 10
segundos) e valores enormes estouram a memória. A
[parte 11](../11-configuracao/03-a-ordem-das-validacoes.md) mostra o programa recusando valores
fora desse intervalo.

### A `SEED` comentada

Sem `SEED`, o gerador sorteia uma semente nova a cada execução, e o `make run` mostra um
labirinto diferente toda vez. Para repetir um labirinto (para depurar um problema, ou para
mostrar o mesmo desenho duas vezes), basta tirar o `#`:

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
