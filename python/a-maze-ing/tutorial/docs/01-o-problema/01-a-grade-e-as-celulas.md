---
sidebar_position: 1
title: A grade e as células
---

# A grade e as células

Antes de gerar qualquer labirinto, é preciso saber do que um labirinto é feito. Esta página
define as palavras que o resto do tutorial usa o tempo todo: grade, célula, lado, parede,
passagem e coordenada.

## A grade

O labirinto é uma **grade** retangular de quadradinhos iguais, como um tabuleiro de xadrez.
Cada quadradinho é uma **célula**. A grade tem `WIDTH` células na horizontal (a largura) e
`HEIGHT` células na vertical (a altura). Um labirinto 6x4 tem 6 colunas, 4 linhas e
6 × 4 = 24 células.

## Os quatro lados de uma célula

Cada célula é um quadrado, então tem quatro **lados**. O enunciado dá a cada lado o nome de um
ponto cardeal, como num mapa em que o Norte fica para cima:

![Uma célula com os quatro lados: Norte em cima, Leste à direita, Sul embaixo, Oeste à esquerda](/img/problema/lados-da-celula.svg)

| Lado | Onde fica na tela | Letra usada no código e nos arquivos |
|---|---|---|
| Norte | em cima | `N` |
| Leste | à direita | `E` (de *East*, leste em inglês) |
| Sul | embaixo | `S` |
| Oeste | à esquerda | `W` (de *West*, oeste em inglês) |

## Parede e passagem

Cada lado de uma célula está num de dois estados:

- **fechado**: há uma **parede** ali, e não dá para atravessar;
- **aberto**: não há parede, e dá para andar até a célula vizinha. Um lado aberto entre duas
  células é uma **passagem**.

Na figura, as linhas escuras são paredes. Entre A e B não há linha: é uma passagem, e dá para
ir de A para B. Entre A e C há uma linha: é uma parede, e para ir de A até C é preciso dar a
volta.

![Labirinto 3 por 2: A e B ligadas por uma passagem, A e C separadas por uma parede](/img/problema/parede-e-passagem.svg)

Gerar um labirinto é decidir, para cada lado de cada célula, se ele é parede ou passagem.

## Vizinhas dividem a mesma parede

A parede que fica à direita (Leste) de uma célula é **a mesma** parede que fica à esquerda
(Oeste) da vizinha da direita. Não são duas paredes coladas, é uma só.

![Duas células vizinhas, A e B, compartilhando a parede do meio](/img/problema/parede-compartilhada.svg)

Mesmo assim, o programa guarda as paredes **por célula**: cada célula anota o estado dos seus
quatro lados. A parede do meio aparece duas vezes: na célula A, à esquerda, como o lado Leste, e
na célula B, à direita, como o lado Oeste. O enunciado exige que as duas anotações
**concordem**: é proibido A dizer "parede fechada no Leste" e B dizer "passagem no Oeste". Essa regra se chama **coerência**, e quebrá-la é o erro mais
fácil de cometer ao abrir passagens. Por isso, toda abertura de passagem mexe nas duas células
ao mesmo tempo.

## A borda é sempre fechada

Os lados que dão para fora da grade (o Norte da primeira linha, o Sul da última, o Oeste da
primeira coluna e o Leste da última) são sempre paredes, inclusive nas células de entrada e de
saída. A entrada e a saída são células marcadas **dentro** da grade, não buracos na borda.

## O endereço de uma célula: `x,y`

Para dizer qual célula é qual, cada uma tem um endereço com dois números, escrito `x,y`:

- `x` é a posição na **horizontal**: em qual **coluna** a célula está;
- `y` é a posição na **vertical**: em qual **linha** a célula está;
- os dois começam em **0**, no canto de **cima à esquerda**.

![Grade 6 por 4 com as coordenadas x,y de algumas células](/img/problema/coordenadas.svg)

É a mesma ordem do plano cartesiano da escola (primeiro o horizontal, depois o vertical), com
uma diferença: aqui o `y` cresce **para baixo**, porque a linha 0 é a de cima, como nas linhas de
um texto.

Numa grade de 20 colunas por 15 linhas, as células vão de `0,0` (canto de cima à esquerda) até
`19,14` (canto de baixo à direita): o `x` vai de 0 a 19 e o `y` de 0 a 14.

No código, a grade é uma lista de linhas, e cada linha uma lista de células. Para pegar a célula
`x,y`, primeiro se escolhe a linha e depois a coluna: `grid[y][x]`. É a mesma célula, só que a
lista pede a linha antes: a célula `5,3` da figura é `grid[3][5]`.
