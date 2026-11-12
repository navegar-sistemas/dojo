---
sidebar_position: 2
title: O recursive backtracker
---

# O recursive backtracker

## A ideia

O **recursive backtracker** é uma busca em profundidade com sorteio:

1. comece na entrada e marque-a como visitada;
2. olhe as vizinhas da célula atual que ainda **não** foram visitadas;
3. se há alguma, sorteie uma, derrube a parede entre as duas, vá para ela e volte ao passo 2;
4. se não há nenhuma, **recue** para a célula de onde veio e volte ao passo 2;
5. quando recuar da entrada, acabou.

O caminho de volta fica guardado numa **pilha**: avançar empilha a célula nova, recuar
desempilha a do topo. A célula atual é sempre o topo da pilha.

## Passo a passo numa grade 5x4

Os quadros abaixo são passos reais da escavação de uma grade 5x4 com `random.Random(3)`:

- **laranja**: a célula atual, topo da pilha;
- **azul**: células na pilha, numeradas na ordem em que entraram;
- **verde**: células visitadas que já saíram da pilha;
- **branco**: células ainda não visitadas.

![Oito quadros do backtracker numa grade 5 por 4, da pilha com uma célula até a pilha vazia](/img/carver/backtracker-passos.svg)

- **Passos 0 e 1**: a pilha tem só a entrada; o sorteio escolhe Leste e a célula `(1, 0)` entra
  na pilha.
- **Passo 9**: a escavação desceu até `(0, 3)`. As vizinhas dela já foram visitadas: é um beco.
- **Passo 10**: recua. `(0, 3)` sai da pilha (verde) e a atual volta a ser `(1, 3)`.
- **Passo 11**: `(1, 3)` ainda tem uma vizinha nova, `(2, 3)`. A escavação avança de novo por
  ali, abrindo um ramo novo.
- **Passo 20**: a pilha chega a 19 células: todas as 20 foram visitadas e só `(0, 3)` saiu.
- **Passos 38 e 39**: sem vizinhas novas em lugar nenhum, a pilha esvazia até a entrada e o
  laço termina. Todas as células estão verdes.

São 20 células, cada uma entra e sai da pilha uma vez: 19 avanços e 20 recuos, 39 passos.

## Por que o resultado é uma árvore

- Cada parede derrubada liga a célula atual (visitada) a uma célula **não visitada**. Nunca se
  abre parede entre duas visitadas, então nunca se fecha um ciclo.
- O laço só termina quando nenhuma célula na pilha tem vizinha nova. Como as células livres
  estão todas ligadas, isso só acontece quando todas foram visitadas.

Conexo e sem ciclo: árvore geradora.

## Por que este algoritmo

Há outros algoritmos que constroem árvores geradoras. Os dois clássicos:

- **Kruskal**: embaralha todas as paredes e derruba cada uma que liga duas regiões ainda
  separadas. Precisa de uma estrutura *union-find* para saber quais células já estão na mesma
  região.
- **Prim**: cresce a árvore a partir de uma célula, sorteando a próxima parede numa lista de
  "fronteira".

Medidos em grades 20x15, seeds de 1 a 100:

| Algoritmo | Estrutura auxiliar | Becos reais |
|---|---|---|
| backtracker | uma pilha (lista) | 24 a 37 |
| Kruskal | union-find | 74 a 95 |
| Prim | lista de fronteira | 77 a 97 |

O backtracker anda o máximo que pode antes de recuar, então faz corredores longos e poucos becos.
Isso pesa no modo Pac-Man, que abre uma parede em **cada** beco (parte 8): menos becos, menos
paredes abertas, e o tabuleiro continua parecendo um labirinto.

Kruskal e Prim não acrescentam nada ao que o subject pede e exigem mais estrutura. Ficam de
fora.
