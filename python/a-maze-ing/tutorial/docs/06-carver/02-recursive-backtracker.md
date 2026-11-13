---
sidebar_position: 2
title: O recursive backtracker
---

# O recursive backtracker

Uma grade tem muitas árvores geradoras possíveis (muitos jeitos de ligar todas as células sem
formar ciclo), e o programa precisa **sortear** uma diferente a cada execução. Esta página mostra
o algoritmo que faz esse sorteio, o *recursive backtracker*, e a estrutura que ele usa para
lembrar o caminho de volta: a **pilha**.

## A ideia: explorar uma caverna com um novelo

Imagine explorar uma caverna desenrolando um novelo de linha. Você anda sempre para um túnel
ainda não visitado, escolhido ao acaso. Quando chega a um ponto sem túnel novo, enrola a linha
e **volta** pelo mesmo caminho até achar uma bifurcação com um túnel ainda não visitado.

*Backtrack*, em inglês, quer dizer exatamente isso: voltar pelo caminho. Em passos:

1. comece na célula de entrada e marque-a como visitada;
2. olhe as vizinhas da célula atual que ainda **não** foram visitadas;
3. se houver alguma, sorteie uma, derrube a parede entre as duas, vá para ela e volte ao
   passo 2;
4. se não houver nenhuma, **recue** para a célula de onde veio e volte ao passo 2;
5. quando precisar recuar e não houver mais para onde recuar, acabou.

Andar sempre para a frente até não dar mais, e só então recuar, é o que se chama **busca em
profundidade** (*depth-first search*): o algoritmo vai fundo num caminho antes de tentar outro.

## A pilha: o novelo do algoritmo

O novelo é uma **pilha**: uma lista em que só se mexe numa ponta, o **topo**, como uma pilha de
pratos. Só duas operações:

- **empilhar** (em inglês, *push*): pôr um item no topo. Em Python, `lista.append(item)`;
- **desempilhar** (*pop*): tirar o item do topo. Em Python, `lista.pop()`.

O último item que entrou é o primeiro que sai. Ler o topo sem tirar nada é `lista[-1]` (o índice
`-1` é o último elemento da lista).

![Quatro estados de uma pilha: append de 0,0, de 1,0 e de 1,1, depois pop, que tira 1,1 do topo](/img/carver/pilha.svg)

Em cada quadro, a caixa laranja é o topo, as azuis são os itens de baixo e a caixa tracejada é o
item que acabou de sair.

No backtracker, a pilha guarda o caminho desde a entrada até a célula atual:

- **avançar** para uma célula nova = empilhar essa célula;
- **recuar** = desempilhar a célula do topo;
- a **célula atual** é sempre a do topo.

## Passo a passo numa grade 5x4

Os quadros abaixo são passos reais da escavação de uma grade de 5 colunas por 4 linhas, com a
semente de sorteio 3 (a semente é explicada na [página 5](./04-a-seed.md)). As cores:

- **laranja**: a célula atual, no topo da pilha;
- **azul**: as outras células da pilha;
- **número**: a posição da célula na pilha, contando do fundo: 1 é o fundo (a entrada), e o maior
  número é o topo;
- **verde**: células já visitadas que saíram da pilha;
- **branco**: células ainda não visitadas;
- **traço escuro**: parede ainda de pé.

![Oito quadros do backtracker numa grade 5 por 4, da pilha com uma célula até a pilha vazia](/img/carver/backtracker-passos.svg)

Os quadros mostram só alguns passos: entre o passo 11 e o 20 e entre o 20 e o 38, os passos
intermediários (12 a 19 e 21 a 37) foram omitidos. O número de uma célula muda quando a pilha
encolhe: no passo 11, a célula `2,3` tem o número 10 porque está na décima posição da pilha, logo
depois que `0,3` saiu.

Coordenadas no formato `x,y` (coluna, linha, contando de 0 a partir do canto de cima à esquerda):

- **Passos 0 e 1**: a pilha tem só a entrada `0,0`. O sorteio escolhe o Leste (a direita), a
  parede entre as duas é derrubada e a célula `1,0` entra na pilha.
- **Passo 9**: a escavação chegou a `0,3` andando para o Oeste (a esquerda), a partir de `1,3`.
  Todas as vizinhas dela já foram visitadas: é um beco.
- **Passo 10**: recua. `0,3` sai da pilha (fica verde) e a atual volta a ser `1,3`.
- **Passo 11**: `1,3` ainda tem uma vizinha não visitada, `2,3`. A escavação avança de novo por
  ali, abrindo um ramo novo.
- **Passo 20**: a pilha tem 19 células. As 20 células da grade já foram visitadas e só `0,3`
  saiu.
- **Passos 38 e 39**: ninguém mais tem vizinha nova, então as células saem da pilha uma a uma até
  ela ficar vazia. Todas estão verdes.

São 20 células, e cada uma entra e sai da pilha uma vez: 19 avanços (a entrada já começa na
pilha) e 20 recuos, 39 passos.

## Por que o resultado é uma árvore

- Cada parede derrubada liga a célula atual, já visitada, a uma célula **não visitada**. Nunca
  se abre parede entre duas células visitadas, que já estão ligadas; então nunca se forma um
  ciclo.
- O laço só termina quando nenhuma célula da pilha tem vizinha nova. As células livres formam um
  bloco só: de qualquer uma se chega a qualquer outra passando de vizinha livre em vizinha livre
  ([página 1](./01-labirinto-perfeito.md)). Suponha que sobrasse uma célula não
  visitada. Siga um caminho de células livres da entrada (visitada) até ela: em algum ponto desse
  caminho, uma célula visitada fica ao lado de uma não visitada. Quando essa visitada esteve no
  topo da pilha, ela teria visto a vizinha não visitada e avançado para lá. Então o laço só
  termina quando todas foram visitadas.

Liga tudo e não tem ciclo: é uma árvore geradora.

## Por que este algoritmo

O enunciado deixa a escolha do algoritmo livre; só pede que o `README.md` diga qual foi usado e
por quê. Há outros algoritmos clássicos que constroem árvores geradoras:

- **Kruskal**: embaralha todas as paredes e derruba cada uma que separa duas regiões ainda não
  ligadas. Precisa de uma estrutura chamada *union-find*, que responde rápido "estas duas células
  já estão ligadas?";
- **Prim**: cresce a árvore a partir de uma célula, sorteando a próxima parede numa lista de
  "fronteira" (as paredes entre a parte já escavada e o resto).

Medidos em grades 20x15, com as sementes de 1 a 100:

| Algoritmo | Estrutura auxiliar | Becos sem saída (fora os 2 becos cercados pelo "42") |
|---|---|---|
| backtracker | uma pilha (uma `list`) | 24 a 37 |
| Kruskal | union-find | 74 a 95 |
| Prim | lista de fronteira | 77 a 97 |

O backtracker anda o máximo que pode antes de recuar, então faz corredores longos e poucos becos.
Isso pesa no modo Pac-Man, que abre uma parede em **cada** beco
([parte 8](../08-braider/02-abrir-os-becos.md)): menos becos, menos paredes abertas, e o
tabuleiro continua parecendo um labirinto.

A escolha do backtracker é do projeto: Kruskal e Prim também cumpririam o enunciado, mas exigem
mais estrutura e deixam mais becos para abrir.
