---
sidebar_position: 1
title: O labirinto perfeito é uma árvore
---

# O labirinto perfeito é uma árvore

Todo labirinto do programa começa como uma grade em que **todas** as paredes estão fechadas:
cada célula é uma caixinha isolada. Para virar labirinto, algumas paredes precisam ser
derrubadas, e a escolha de quais derrubar decide se o resultado é bom. Esta página mostra que
paredes um **labirinto perfeito** precisa abrir; a classe que faz isso se chama `Carver`.

## Cavar: de tudo fechado a um labirinto

*Carve*, em inglês, quer dizer "cavar" ou "esculpir". A imagem é a de um bloco maciço de terra
em que se cavam túneis: no começo não há corredor nenhum, e cada parede derrubada abre um pedaço
de corredor entre duas células vizinhas.

![À esquerda, grade 6 por 4 com todas as paredes; à direita, o mesmo tamanho depois de cavado, com 23 paredes derrubadas](/img/carver/fechado-e-cavado.svg)

Nas duas grades, cada traço escuro é uma parede fechada e a célula magenta é a de entrada, `0,0`.

Relembrando os termos:

- **labirinto perfeito** (o modo `PERFECT=True` do arquivo de configuração): não tem nenhum
  **ciclo**, ou seja, nenhum jeito de andar em círculo e voltar à mesma célula por outro
  caminho. Por isso, entre duas células quaisquer existe exatamente um caminho
  ([parte 1](../01-o-problema/05-perfeito-e-pac-man.md));
- **`Maze`**: a classe que guarda as paredes de cada célula da grade e oferece métodos para
  abrir, fechar e consultar paredes ([parte 5](../05-maze/01-a-grade-de-paredes.md)). Um `Maze`
  recém-criado tem todas as paredes fechadas.

O `Carver` recebe esse `Maze` todo fechado e derruba paredes até ele virar um labirinto
perfeito. Ele é o primeiro passo de toda geração, nos dois modos: o tabuleiro Pac-Man
(`PERFECT=False`) também nasce de um labirinto perfeito, no qual depois se abrem paredes extras
([parte 8](../08-braider/01-becos-sem-saida.md)).

## O labirinto desenhado como pontos e linhas

Para enxergar quais paredes derrubar, troque cada célula por um ponto e cada **passagem** (um lado
aberto entre duas células) por uma linha ligando os dois pontos:

![Labirinto perfeito 6 por 4 com um ponto em cada célula e uma linha laranja em cada passagem](/img/carver/arvore-6x4.svg)

Cada ponto escuro é uma célula; cada linha laranja liga duas células vizinhas que têm uma passagem
entre si; os traços escuros em volta são as paredes que ficaram de pé.

Pontos ligados por linhas formam o que a matemática chama de **grafo**. O desenho laranja tem
duas propriedades:

- **liga tudo**: partindo de qualquer ponto, dá para chegar a qualquer outro seguindo linhas;
- **não fecha volta**: nenhuma sequência de linhas sai de um ponto e retorna a ele sem passar
  duas vezes pela mesma linha.

Um grafo com essas duas propriedades se chama **árvore**: como os galhos de uma árvore, ele se
ramifica, mas os galhos nunca se reencontram. Quando a árvore passa por **todos** os pontos, ela
se chama **árvore geradora** (*spanning tree*, em inglês).

| Propriedade da árvore | O que significa no labirinto |
|---|---|
| liga todos os pontos | toda célula é alcançável a partir da entrada |
| não fecha volta | não há ciclo, então existe um único caminho entre duas células |
| `C` pontos, `C − 1` linhas | `C` células, `C − 1` passagens |

Cavar um labirinto perfeito é, portanto, construir uma árvore geradora das células. No exemplo
acima, 24 células e 23 passagens.

## Por que exatamente `C − 1` passagens

Pense na árvore sendo montada aos poucos, como um grupo de células ligadas que cresce. O grupo
começa com uma única célula. Numa árvore, toda passagem nova liga o grupo a uma célula que ainda
estava **de fora**: se ligasse duas células que já estão no grupo, ela criaria um segundo caminho
entre elas, ou seja, um ciclo. Então cada passagem traz exatamente uma célula nova para o grupo.

Para o grupo ir de 1 célula até as `C` células, entram `C − 1` células novas, uma por passagem:
`C − 1` passagens, nem uma a mais, nem uma a menos.

- uma passagem a mais ligaria duas células que já estavam ligadas por outro caminho. Os dois
  caminhos juntos formariam um ciclo;
- uma a menos deixaria alguma célula de fora, isolada.

Com 4 células, por exemplo: a primeira começa sozinha e cada uma das outras 3 entra com uma
passagem, 3 no total.

O `Maze` tem um método que mede isso, `loop_count()`, que conta os ciclos com a conta
`passagens − células + 1` ([parte 5](../05-maze/06-contar-ciclos.md)). Numa árvore, passagens =
células − 1, e a conta dá sempre 0.

## O "42" fica fora da árvore

O enunciado exige um "42" desenhado no meio do labirinto por células com as quatro paredes
fechadas ([parte 1](../01-o-problema/06-o-padrao-42.md)). Essas 18 células não fazem parte da
árvore: a árvore liga só as **células livres**, as que não são do "42".

O `Carver` não precisa saber disso. Para descobrir as vizinhas de uma célula, ele chama
`maze.neighbour(cell, side)`, que devolve a célula vizinha daquele lado, ou `None` quando o lado
dá para fora da grade ou para uma célula do "42" ([parte 5](../05-maze/03-vizinhos.md)). Uma
célula que nunca aparece como vizinha nunca é escavada, e uma parede que dá para fora nunca é
derrubada: a borda continua fechada sem esforço nenhum.

Mesmo com o "42" no caminho, as células livres continuam todas ligadas entre si, por dois
motivos:

- o desenho ocupa um bloco de 7 colunas por 5 linhas, centralizado, com pelo menos uma célula de
  corredor entre o bloco e cada borda. Essa margem dá a volta inteira no bloco, então as células
  de fora do bloco se alcançam umas às outras por ela;
- dentro do bloco, cada célula livre (os buracos entre os traços do "4" e do "2") tem uma vizinha
  livre, e seguindo de vizinha em vizinha se chega à margem. As mais apertadas são as duas células
  dentro das curvas do "2" (coluna 5 do desenho, linhas 1 e 3): o "42" as fecha em três lados e
  sobra uma vizinha livre só, que já basta para ligá-las ao resto. Elas são os **becos cercados**
  que a [parte 8](../08-braider/01-becos-sem-saida.md) explica.

Nenhuma célula livre fica presa atrás do desenho.

## O que vem de graça com uma árvore

- **Um único caminho entre a entrada e a saída**: é o que o enunciado exige com `PERFECT=True`.
- **Becos sem saída**: um beco é uma célula com uma única abertura. Numa árvore, todo ramo que sai
  do caminho principal termina num beco, como cada galho termina numa ponta (que os matemáticos
  chamam de **folha**).
- **Nenhum bloco 3x3 aberto**: o enunciado proíbe um bloco de 3x3 células sem nenhuma parede por
  dentro. Um bloco desses tem 9 células e 12 passagens internas (6 entre colunas vizinhas e 6
  entre linhas vizinhas). Num pedaço qualquer de uma árvore também não há ciclo, então a conta de
  cima vale para ele: 9 células ligadas sem ciclo têm no máximo 9 − 1 = 8 passagens entre si.
  Como 12 é mais que 8, um bloco todo aberto teria ciclos, e o modo perfeito cumpre essa regra
  sem conferir nada.

Falta decidir **em que ordem** derrubar as paredes para formar a árvore. A
[próxima página](./02-recursive-backtracker.md) mostra o algoritmo.
