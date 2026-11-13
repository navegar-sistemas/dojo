---
sidebar_position: 6
title: Labirinto perfeito e tabuleiro Pac-Man
---

# Labirinto perfeito e tabuleiro Pac-Man

O enunciado pede dois tipos de labirinto, e a opção `PERFECT` do arquivo de configuração
escolhe qual gerar. Para entender a diferença, são necessárias duas palavras: **beco sem saída**
e **ciclo**.

## Beco sem saída

Um **beco sem saída** é uma célula com uma única abertura: três lados têm parede e só um é
passagem. Quem entra num beco só consegue sair por onde entrou.

O labirinto abaixo, de 6 colunas por 4 linhas, foi gerado pelo programa com a semente 7. Ele tem
três becos, em laranja: as células `0,0`, `1,0` e `0,3`. A `0,0` é também a entrada do
labirinto; qualquer célula pode ser um beco.

![Labirinto 6 por 4 com três becos sem saída em laranja](/img/problema/perfeito-6x4-becos.svg)

## Ciclo

Um **ciclo** é um caminho que dá a volta e termina na célula onde começou, sem passar duas
vezes pelo mesmo trecho. Um ciclo existe quando há duas rotas diferentes entre duas células: dá
para ir por uma e voltar pela outra.

Numa grade de 3 colunas por 2 linhas em que só a parede entre `1,0` e `1,1` está fechada, dá
para sair de `0,0`, andar pela linha de cima, descer pela direita, voltar pela linha de baixo e
chegar de novo a `0,0`:

![Grade 3 por 2 com um ciclo em ciano em volta da parede do meio](/img/problema/ciclo-3x2.svg)

## Labirinto perfeito (`PERFECT=True`)

Um labirinto **perfeito** não tem nenhum ciclo. Por isso, entre quaisquer duas células existe
**exatamente um** caminho: se houvesse dois, juntos eles formariam um ciclo.

O labirinto dos becos, acima, é perfeito. Aqui está ele de novo, com a entrada em `0,0` e a
saída em `5,3`:

![Labirinto perfeito 6 por 4, com a entrada em magenta e a saída em vermelho](/img/problema/perfeito-6x4.svg)

Duas consequências:

- todo corredor que se afasta do caminho entre a entrada e a saída termina num beco sem saída;
- numa grade de `C` células, o labirinto tem exatamente `C − 1` passagens. Partindo de uma
  célula, cada passagem aberta liga no máximo **uma** célula nova ao grupo das que já se
  alcançam; para juntar as outras `C − 1` células, são precisas pelo menos `C − 1` passagens.
  E uma passagem a mais ligaria duas células que já se alcançavam, criando uma segunda rota
  entre elas: um ciclo. O 6x4 acima tem 24 células e 23 passagens.

## Tabuleiro de Pac-Man (`PERFECT=False`)

Pac-Man é um jogo de fliperama em que o jogador anda por um labirinto comendo pontos e fugindo
de fantasmas. Num labirinto perfeito, o jogador perseguido entraria num beco e seria pego. Por
isso o enunciado pede, para esse modo, um labirinto que funcione como **tabuleiro do jogo**:

| Regra do enunciado | Por quê |
|---|---|
| toda célula é alcançável | o jogo espalha pontos por todos os corredores, e todos precisam poder ser comidos |
| os quatro cantos e o centro são corredores | o próprio enunciado explica: os fantasmas e as *super-pac-gums* (as pastilhas especiais) ficam nos cantos, e o jogador começa no centro |
| pelo menos **duas rotas independentes** (dois ciclos) | quem foge sempre tem um caminho alternativo; um ciclo só não basta |
| becos sem saída raros: no máximo um ou dois | num beco o jogador fica encurralado; o ideal é nenhum |

O enunciado chama este modo de **"o padrão"** (*default*). Isso não dispensa a chave no arquivo
de configuração, onde `PERFECT` continua obrigatória; na classe `MazeGenerator`
([parte 9](../09-gerador/01-a-fachada.md)), quem não informa o parâmetro `perfect` recebe
`perfect=False`.

### Cantos e centro

"Corredor" aqui quer dizer uma célula livre do labirinto, que dá para alcançar andando. As únicas
células que não são corredores são as do "42", que ficam fechadas e fora do labirinto
([página do "42"](./06-o-padrao-42.md)). A regra, então, é que os cantos e o centro não podem
ser células do "42":

- os cantos nunca são: o "42" só é desenhado com pelo menos uma célula livre entre ele e cada
  borda;
- o centro também não: o "42" fica no meio, mas deixa uma coluna livre entre o "4" e o "2", e o
  centro da grade cai sempre nela.

Quando a grade tem número par de colunas (ou de linhas), o centro não é uma célula só, e sim as
duas (ou quatro) em volta do meio. Este projeto, como o verificador que acompanha o
enunciado, exige que pelo menos uma delas seja corredor; a da coluna livre do "42" sempre é.

### Duas rotas independentes

"Duas rotas independentes" quer dizer dois ciclos que não são o mesmo ciclo dado de outro jeito.
Na grade 3x2 com todas as paredes de dentro abertas, cada quadrado de 2x2 células é um ciclo:

![A grade 3 por 2 sem paredes por dentro, com os dois ciclos destacados lado a lado](/img/problema/ciclos-3x2-dois.svg)

Há também a volta grande, pela borda da grade inteira. Ela não conta como terceira rota: é só
os dois quadrados juntos, e não traz nenhum caminho alternativo que eles já não deem. Esta grade
tem duas rotas independentes. O labirinto de um ciclo só, como o da seção "Ciclo", tem uma, e o
enunciado diz que isso não basta: um labirinto perfeito com uma única parede aberta não serve
como tabuleiro.

### Um tabuleiro de verdade

O labirinto 6x4 dos becos, gerado no modo Pac-Man com a mesma semente:

![Tabuleiro Pac-Man 6 por 4, com a entrada em magenta e a saída em vermelho](/img/problema/pacman-6x4.svg)

O gerador abriu duas paredes: uma entre `0,0` e `1,0`, que acaba com dois becos de uma vez, e
outra entre `0,3` e `1,3`. Cada parede aberta liga duas células que já se alcançavam por outro
caminho, e por isso cria um ciclo:

![Os dois ciclos do tabuleiro 6 por 4, cada um criado por uma parede aberta](/img/problema/pacman-6x4-ciclos.svg)

O resultado tem dois ciclos e nenhum beco: cumpre as regras do modo.

A [próxima página](./09-sem-saloes-e-o-braiding.md) mostra uma regra que vale para os dois
modos, a proibição de salões, como o gerador transforma um labirinto perfeito num tabuleiro e
quais tamanhos de grade não comportam os dois ciclos que o tabuleiro exige.
