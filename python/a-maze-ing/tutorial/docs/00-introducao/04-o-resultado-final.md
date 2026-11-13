---
sidebar_position: 4
title: O resultado final
---

# O resultado final

Antes de construir peça por peça, ajuda ver aonde se quer chegar. Esta página mostra o programa
pronto, como ele fica no fim da [parte 14](../14-menu-e-main/06-saidas-e-erros-inesperados.md):
o que aparece na tela, o arquivo que ele grava e como outro projeto usa o gerador. Nada aqui é
para rodar agora.

## Na tela

O comando `make run` desenha o labirinto no terminal, com quadrados coloridos. Ele é um atalho,
criado na [parte 3](../03-ambiente/02-makefile-instalar-e-rodar.md), para
`.venv/bin/python a_maze_ing.py config.txt`: o `python3 a_maze_ing.py config.txt` do enunciado,
usando o Python do ambiente virtual do projeto (a pasta `.venv`, também criada na parte 3).

O labirinto muda a cada execução. Para ter sempre o mesmo, o `config.txt` traz a linha
`# SEED=42`, comentada (o `#` no começo faz o programa ignorá-la). Apagando o `#`, a semente do
sorteio fica fixa em 42, e o labirinto é sempre este, aqui com o caminho mais curto à mostra:

![Labirinto 20 por 15 com o caminho mais curto](/img/problema/labirinto-20x15-caminho.svg)

Magenta é a entrada, vermelho é a saída, ciano é o caminho mais curto e cinza é o "42". No
terminal, as paredes são quadrados coloridos sobre o fundo escuro; a figura usa linhas finas
para ficar legível.

Abaixo do desenho, o programa mostra um menu e espera o usuário digitar um número:

```text
=== A-Maze-ing ===
1. Re-generate a new maze
2. Show / Hide the shortest path
3. Rotate the wall colours
4. Quit
Choice? (1-4):
```

| Número | O que faz |
|---|---|
| `1` | sorteia outro labirinto, desenha e regrava o arquivo de saída |
| `2` | mostra ou esconde o caminho mais curto (em ciano) |
| `3` | troca a cor das paredes: branco, amarelo, verde, azul e de novo branco |
| `4` | encerra o programa |

## No arquivo

Ao mesmo tempo, o programa grava o labirinto num arquivo de texto, o `maze.txt` (o nome vem da
opção `OUTPUT_FILE` do `config.txt`). Cada caractere da grade descreve as paredes de uma célula
num código de `0` a `f`, explicado na
[parte 1](../01-o-problema/02-paredes-em-bits.md). Depois da grade vêm uma linha vazia, a
entrada, a saída e o caminho mais curto em letras (`N` = cima, `E` = direita, `S` = baixo, `W` =
esquerda):

```text
95395539555515513913
854693c69553c53c46aa
8153ac55695293a9556a
a852c3939696aac69552
ac3a92c045456a938556
c3aaaafa93fffaac4513
96aaaafc6857faa9396a
856c6afffafffac2aa92
81539053fafd5016a86a
ac3aaa92fafffaa9683a
a96aaaaa9695502c386a
c29046c069293c438692
9686953c52aaa93a83aa
83a943c13a86aaac6aaa
c4445456c44546c55446

0,0
19,14
SSEEESSSSSENNNESSSSEESSSSEESSEEEENNESSEEEEE
```

Os `f` no meio do bloco formam o "42": `f` é o código da célula com as quatro paredes fechadas.

## Em outro projeto

O gerador sai empacotado num arquivo, `mazegen-1.0.0-py3-none-any.whl`, que outro projeto
instala com `pip install mazegen-1.0.0-py3-none-any.whl`. Depois de instalado, basta importar a
classe e pedir um labirinto:

```python
from mazegen import MazeGenerator

# Os parâmetros omitidos ficam com o valor padrão: entrada em 0,0, saída no
# canto de baixo à direita (19,14 aqui) e perfect=False (tabuleiro Pac-Man).
gen = MazeGenerator(width=20, height=15, seed=42)
gen.generate()
print(gen.grid[0][0])   # o código das paredes da célula 0,0 (um número de 0 a 15)
print(gen.solution)     # o caminho mais curto, em letras N, E, S, W
```

Com a semente 42, o resultado é o mesmo labirinto da figura acima:

```text
9
SSEEESSSSSENNNESSSSEESSSSEESSEEEENNESSEEEEE
```

O `9` quer dizer paredes no Norte e no Oeste da célula `0,0`, como explicado na
[parte 1](../01-o-problema/02-paredes-em-bits.md). A classe `MazeGenerator` é construída na
[parte 9](../09-gerador/01-a-fachada.md).

## Os arquivos entregues

```text
a_maze_ing.py         o programa (o arquivo que se executa)
config.txt            o arquivo de opções padrão
Makefile              os atalhos install, run, debug, clean, lint, lint-strict e build
pyproject.toml        a descrição do pacote do gerador
.flake8               a configuração do flake8 (o verificador de estilo)
.gitignore            a lista de arquivos gerados que o git não guarda
mazegen/              o código do gerador (é o que vai para o pacote)
amazeing/             o código da aplicação: opções, arquivo, desenho, menu
README.md             a apresentação do projeto
LICENSE.md            a licença que permite reutilizar o gerador
mazegen-1.0.0-py3-none-any.whl, mazegen-1.0.0.tar.gz   o pacote do gerador
```
