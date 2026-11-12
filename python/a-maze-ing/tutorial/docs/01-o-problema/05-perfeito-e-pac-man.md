---
sidebar_position: 5
title: Labirinto perfeito e tabuleiro Pac-Man
---

# Labirinto perfeito e tabuleiro Pac-Man

O enunciado pede dois tipos de labirinto, e a opção `PERFECT` do arquivo de configuração
escolhe qual gerar. Para entender a diferença, são necessárias duas palavras: **beco sem saída**
e **ciclo**.

## Beco sem saída

Um **beco sem saída** é uma célula com uma única abertura: três lados têm parede e só um é
passagem. Quem entra num beco só consegue sair por onde entrou. No labirinto abaixo, os becos
estão em amarelo:

![Labirinto 6 por 4 com três becos sem saída em amarelo](/img/problema/perfeito-6x4-becos.svg)

## Ciclo

Um **ciclo** é um caminho que dá a volta e termina na célula onde começou, sem passar duas
vezes pelo mesmo trecho. Um ciclo existe quando há duas rotas diferentes entre duas células: dá
para ir por uma e voltar pela outra.

![Tabuleiro 6 por 4 com um ciclo destacado em ciano](/img/problema/pacman-6x4-ciclo.svg)

## Labirinto perfeito (`PERFECT=True`)

Um labirinto **perfeito** não tem nenhum ciclo. Por isso, entre quaisquer duas células existe
**exatamente um** caminho: se houvesse dois, juntos eles formariam um ciclo.

Um labirinto perfeito 6x4 gerado pelo programa (com a semente 7), com a entrada em magenta e a
saída em vermelho:

![Labirinto perfeito 6 por 4](/img/problema/perfeito-6x4.svg)

Consequências:

- todo corredor que se afasta do caminho entre a entrada e a saída termina num beco sem saída;
- numa grade de `C` células, o labirinto tem exatamente `C − 1` passagens: é o mínimo para ligar
  tudo. Uma passagem a mais criaria um ciclo; uma a menos deixaria alguma célula isolada.

## Tabuleiro de Pac-Man (`PERFECT=False`, o padrão)

Pac-Man é um jogo de fliperama em que o jogador anda por um labirinto comendo pontos e fugindo
de fantasmas. Num labirinto perfeito, o jogador perseguido entraria num beco e seria pego. Por
isso o enunciado pede, para esse modo, um labirinto que funcione como **tabuleiro do jogo**:

| Regra do enunciado | Por quê |
|---|---|
| toda célula é alcançável | o jogo espalha pontos por todos os corredores, e todos precisam poder ser comidos |
| os quatro cantos e o centro são corredores | os fantasmas começam nos cantos e o jogador começa no centro |
| pelo menos **duas rotas independentes** (dois ciclos) | quem foge sempre tem um caminho alternativo; um ciclo só não basta |
| becos sem saída raros: no máximo um ou dois | num beco o jogador fica encurralado; o ideal é nenhum |

"Duas rotas independentes" quer dizer dois ciclos que não são o mesmo ciclo dado de outro jeito:
abrir **uma** parede num labirinto perfeito cria exatamente um ciclo, e o enunciado diz que isso
não basta.

O centro, quando a grade tem número par de colunas ou de linhas, não é uma célula só: este
projeto aceita qualquer uma das células em volta do meio.

O mesmo labirinto 6x4 da figura anterior, gerado no modo Pac-Man (mesma semente):

![Tabuleiro Pac-Man 6 por 4](/img/problema/pacman-6x4.svg)

As paredes que fechavam os becos foram abertas, e o tabuleiro ganhou rotas alternativas.

## Sem salões: nenhuma área aberta 3x3

Nos dois modos, o enunciado proíbe áreas abertas grandes: um labirinto é feito de corredores,
não de salões. A regra concreta é que nenhum bloco de 3x3 células pode estar totalmente aberto,
com todas as paredes de dentro do bloco removidas. Blocos abertos de 2x2, 2x3 ou 3x2 são
permitidos. No modo perfeito essa regra se cumpre sozinha, porque um bloco 3x3 aberto teria
ciclos; no modo Pac-Man, que abre paredes extras, ela precisa ser vigiada.

## Como o Pac-Man é gerado

Não existe um algoritmo separado para ele. O gerador:

1. cria um labirinto **perfeito**;
2. abre uma parede em cada beco sem saída, ligando-o a uma vizinha;
3. abre mais paredes sorteadas até haver pelo menos 2 ciclos;
4. desfaz qualquer abertura que formaria um bloco 3x3 aberto.

Esse processo se chama **braiding** ("trançar", em inglês) e é construído na
[parte 8](../08-braider/01-becos-sem-saida.md).

## Tamanhos impossíveis

Algumas grades não comportam dois ciclos, por menor que seja a quantidade de paredes. Numa
grade de 1 linha (ou 1 coluna) as células ficam em fila, e uma fila não tem como dar a volta.
Numa grade 2x2, mesmo sem nenhuma parede por dentro, só existe uma volta possível.

A conta geral: uma grade `WIDTH x HEIGHT` com todas as paredes de dentro abertas tem
`(WIDTH − 1) × (HEIGHT − 1)` ciclos independentes. Quando essa conta dá menos de 2, o modo
Pac-Man é impossível e o programa recusa o arquivo de configuração:

```text
Error: config.txt: PERFECT=False needs (WIDTH - 1) x (HEIGHT - 1) >= 2 for a Pac-Man board, got 1x10
```
