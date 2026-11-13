---
sidebar_position: 2
title: Pais, letras e desempate
---

# Pais, letras e desempate

A busca em largura da [página anterior](./01-busca-em-largura.md) descobre **a que distância**
cada célula está da entrada. Mas o arquivo de saída precisa do caminho em letras, um passo por
letra, e a distância sozinha não diz por onde ir. Para montar o caminho, a busca precisa lembrar
**de onde** veio cada célula. Esta página mostra como ela anota isso, como lê o caminho de volta
e como escolhe entre dois caminhos do mesmo tamanho.

## O dicionário `parents`

Quando uma célula é descoberta, o `Solver` anota num dicionário chamado `parents` ("pais"):

- a **chave** é a célula descoberta;
- o **valor** é um par (uma tupla) `(célula anterior, lado do passo)`: a célula de onde se chegou
  e o lado pelo qual se andou;
- a entrada tem valor `None`: ela não veio de lugar nenhum.

A célula anterior é chamada de **pai** da célula descoberta, como numa árvore genealógica: cada
célula tem um pai, e seguindo os pais se chega sempre à entrada, a origem de todas.

O mesmo dicionário também responde se uma célula já foi descoberta: `nxt not in parents` quer
dizer "ainda não". Não é preciso um conjunto de visitadas à parte.

## Um exemplo pequeno

O labirinto 3x2 da [parte 1](../01-o-problema/04-o-arquivo-de-saida.md), com a entrada em `0,0`
(magenta) e a saída em `0,1` (vermelho). Em cada célula, a letra do lado pelo qual ela foi
descoberta: `E` em `1,0` quer dizer "cheguei aqui andando para o Leste a partir de `0,0`".

![Labirinto 3 por 2 com a letra do passo de descoberta em cada célula e o caminho EESWW em ciano](/img/solver/pais-3x2.svg)

A célula magenta é a entrada, a vermelha é a saída e a faixa ciano é o caminho; os traços escuros
são paredes.

O dicionário, ao fim da busca. Cada valor é um par: primeiro a célula pai, entre parênteses, e
depois a letra do lado. `((0,0), E)` quer dizer "pai `0,0`, passo para o Leste".

| Célula (chave) | Valor: (pai, lado) |
|---|---|
| `0,0` | `None` |
| `1,0` | `((0,0), E)` |
| `2,0` | `((1,0), E)` |
| `2,1` | `((2,0), S)` |
| `1,1` | `((2,1), W)` |
| `0,1` | `((1,1), W)` |

## Do fim para o começo

Com `parents` pronto, o caminho sai **de trás para a frente**: só a saída sabe de onde veio, então
a leitura começa por ela.

1. começa na saída e lê o par `(pai, lado)`;
2. anota a letra do lado e passa para o pai;
3. repete até chegar à entrada, cujo valor é `None`;
4. inverte a lista de letras, que foi lida da saída para a entrada.

No exemplo:

| Célula atual | Valor lido | Letra anotada |
|---|---|---|
| `0,1` | `((1,1), W)` | `W` |
| `1,1` | `((2,1), W)` | `W` |
| `2,1` | `((2,0), S)` | `S` |
| `2,0` | `((1,0), E)` | `E` |
| `1,0` | `((0,0), E)` | `E` |
| `0,0` | `None` | fim |

As letras lidas são `W W S E E`. Invertidas, dão `EESWW`: dois passos para a direita, um para
baixo e dois para a esquerda, o caminho da entrada até a saída. A letra de cada lado vem de
`Direction.letter`, uma propriedade dos lados que devolve `"N"`, `"E"`, `"S"` ou `"W"`
([parte 4](../04-value-objects/03-direction-propriedades.md)).

Num labirinto perfeito 6x4 (semente 7), a mesma leitura, da saída `5,3` até a entrada, e depois
invertida, dá `SEESENNEESWSES`:

![Labirinto 6 por 4 com a letra do passo de descoberta em cada célula e o caminho em ciano](/img/solver/pais.svg)

As cores são as do exemplo 3x2: magenta é a entrada `0,0`, vermelho é a saída `5,3`, e a faixa
ciano é o caminho.

## Vários caminhos do mesmo tamanho

No modo Pac-Man pode haver mais de um caminho mais curto. Numa grade 3x2 sem paredes por dentro,
de `0,0` até `2,1`, há três caminhos de 3 passos:

![Três quadros da grade 3 por 2: EES, o escolhido; ESE e SEE, do mesmo tamanho](/img/solver/empate-3x2.svg)

Em cada quadro, magenta é a entrada, vermelho é a saída, a faixa ciano é o caminho e as linhas
tracejadas são as passagens.

Qualquer um seria aceito pelo enunciado, mas o programa precisa escolher **sempre o mesmo**: a
mesma semente precisa dar sempre o mesmo arquivo de saída. O `Solver` desempata por duas regras:

- **vizinhas na ordem N, E, S, W.** O `Solver` pega os lados abertos de uma célula com
  `maze.passages(cell)`, que os devolve sempre na ordem Norte, Leste, Sul, Oeste
  ([parte 5](../05-maze/05-passagens-e-becos.md)). As vizinhas entram na fila sempre nessa ordem;
- **vale o pai da primeira descoberta.** Uma célula que já está em `parents` nunca é reescrita,
  mesmo que outra célula da mesma camada também chegue a ela.

Na grade 3x2, de `0,0` até `2,1`, a busca anda assim (a fila é lida da frente para o fim):

| Tirada da frente | Vizinhas descobertas agora, na ordem N, E, S, W | Fila depois |
|---|---|---|
| `0,0` | `1,0` (pai `0,0`, `E`) e `0,1` (pai `0,0`, `S`) | `1,0`, `0,1` |
| `1,0` | `2,0` (pai `1,0`, `E`) e `1,1` (pai `1,0`, `S`); `0,0` já foi descoberta | `0,1`, `2,0`, `1,1` |
| `0,1` | nenhuma: `0,0` e `1,1` já foram descobertas | `2,0`, `1,1` |
| `2,0` | `2,1` (pai `2,0`, `S`) | `1,1`, `2,1` |
| `1,1` | nenhuma: `2,1` já tem pai e ele não muda | `2,1` |
| `2,1` | é a saída: a busca para | |

A saída foi descoberta por `2,0`, e não por `1,1`, porque `2,0` entrou na fila antes: ao tratar
`1,0`, o Leste (`2,0`) veio antes do Sul (`1,1`). Seguindo os pais a partir da saída: `2,1` veio
de `2,0` por `S`, `2,0` de `1,0` por `E`, `1,0` de `0,0` por `E`. Invertido, `EES`.

No sentido contrário, de `2,1` para `0,0`, o Norte é o primeiro lado da ordem, e a mesma conta dá
`NWW`. As [páginas 3](./04-a-busca-do-solver.md) e [4](./03-o-codigo-do-solver.md) escrevem o
`Solver`, e o fim da página 4 confere esses dois resultados.
