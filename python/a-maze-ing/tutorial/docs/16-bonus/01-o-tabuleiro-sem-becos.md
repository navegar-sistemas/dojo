---
sidebar_position: 1
title: O tabuleiro sem becos
---

# O tabuleiro sem becos

O projeto tem uma parte obrigatória e pode ter **bônus**: funcionalidades opcionais,
além do que o enunciado exige, que valem pontos extras. A folha de avaliação deste projeto (a
lista de perguntas que o avaliador segue na defesa) diz que os bônus só são considerados se
**todas** as perguntas da parte obrigatória tiverem sido bem-sucedidas. Um bônus em cima de uma parte obrigatória com defeito não conta.

O enunciado sugere três bônus:

- um labirinto do modo padrão (o tabuleiro de Pac-Man, `PERFECT=False`) **sem nenhum beco sem
  saída**;
- suportar **vários algoritmos** de geração;
- mostrar uma **animação** enquanto o labirinto é gerado.

Este projeto faz só o primeiro: um tabuleiro "perfeitamente trançado" (*perfectly braided*), em
que um jogador perseguido nunca fica preso em lugar nenhum. O modo Pac-Man construído na
[parte 8](../08-braider/02-abrir-os-becos.md) (o *braiding*, explicado abaixo) e na
[parte 9](../09-gerador/03-generate.md) (as tentativas do gerador) já entrega isso na prática,
em todos os labirintos medidos. Não é uma garantia: a
[próxima página](./02-por-que-nao-e-garantido.md) mostra a exceção. Esta parte não tem código
novo: explica por que o resultado sai assim, quando poderia não sair, e como prová-lo.

## Trançar: o que quer dizer "perfectly braided"

O tabuleiro Pac-Man é feito a partir de um labirinto perfeito, aquele em que existe um único
caminho entre duas células quaisquer ([parte 1](../01-o-problema/05-perfeito-e-pac-man.md)). O
gerador abre algumas paredes dele, criando ciclos, rotas alternativas que voltam ao mesmo lugar.
Esse processo se chama *braiding*, "trançar": os corredores, que eram galhos separados, passam a
se cruzar como os fios de uma trança ([parte 8](../08-braider/02-abrir-os-becos.md)).

"Perfeitamente trançado" é o caso extremo: um tabuleiro em que **nenhum** beco sobrou. Nele,
toda célula livre tem pelo menos duas passagens, exceto as poucas presas pelo "42", explicadas
abaixo.

## O que é um beco real

Um **beco sem saída** é uma célula com uma única passagem: quem entra só sai por onde veio. Num
tabuleiro de Pac-Man, é uma armadilha: o fantasma que vem atrás fecha a única saída.

Nem todo beco pode ser desfeito ([parte 8](../08-braider/01-becos-sem-saida.md)). Um beco é
**cercado** quando todas as suas paredes fechadas dão para a borda da grade ou para células do
"42". Abrir qualquer uma delas abriria o lado de fora da grade, ou uma célula que precisa ficar
fechada. Numa grade de 2x1 (sem "42") com a parede do meio aberta, por exemplo, as duas células
são becos cercados pela borda ([parte 5](../05-maze/05-passagens-e-becos.md)).

Um beco cercado tem uma única vizinha livre (a da sua passagem). Quando o "42" está desenhado,
só duas células ficam assim: as duas dentro das curvas do "2", fechadas pelo "42" em três lados.
O gerador deixa pelo menos uma célula livre entre o "42" e a borda, e por isso nenhuma célula
fica presa entre os dois. Esses são os becos **cercados pelo "42"**. Eles não contam: o
enunciado, ao descrever o que o `maze_analyzer.py` confere, fala de um tabuleiro "sem becos sem
saída além do padrão 42". O `maze_analyzer.py`, o programa que vem com o enunciado e confere o
arquivo de saída, conta esses becos à parte e os tolera.

Um beco **real** tem pelo menos uma parede fechada voltada para uma célula livre: uma parede que
poderia ser aberta. É esse que o bônus proíbe.

## Perfeito e Pac-Man, lado a lado

O labirinto perfeito do `config.txt` padrão (20x15, entrada `0,0`, saída `19,14`) com
`PERFECT=True` e `SEED=42`. Nesta figura e na seguinte, as cores são as da
[parte 8](../08-braider/01-becos-sem-saida.md): laranja = beco real, amarelo = beco cercado pelo
"42", cinza = célula do "42", magenta = entrada, vermelho = saída.

![Labirinto perfeito 20 por 15 com 32 becos reais em laranja e 2 cercados pelo 42 em amarelo](/img/bonus/perfeito-20x15.svg)

Um labirinto perfeito é uma **árvore**: os corredores se ramificam como galhos, sem nunca voltar
a se encontrar, e todo galho que sai do caminho principal termina num beco. São 32 becos reais.

O mesmo config com `PERFECT=False`, o padrão:

![Tabuleiro Pac-Man 20 por 15 sem becos reais e com 2 cercados pelo 42 em amarelo](/img/bonus/pacman-20x15.svg)

Nenhum laranja. Os dois becos amarelos continuam: são as duas células dentro das curvas do "2"
(a coluna 5 do desenho do "42", nas linhas 1 e 3; aqui, as células `11,6` e `11,8`), cercadas
por células do "42" e com uma única passagem para fora. Não há parede que possa ser aberta
nelas.

## Por que o Pac-Man sai assim

O *braiding* tem dois passos: (a) abrir uma parede em cada beco; (b) abrir paredes extras até
haver 2 ciclos ([parte 8](../08-braider/03-criar-ciclos.md)). O passo (a) é o que remove os
becos:

- `maze.dead_ends()` lista só os becos **reais**: para um beco cercado, `closed_sides` (a lista
  das paredes fechadas que dão para uma célula livre) vem vazia, e ele não entra na lista
  ([parte 5](../05-maze/05-passagens-e-becos.md));
- para cada beco da lista, em ordem sorteada, o passo abre uma das paredes fechadas que dão para
  uma vizinha livre;
- abrir uma parede só **aumenta** o número de passagens das duas células. Nenhuma abertura cria
  um beco novo, então uma única passada pela lista basta.

Na prática, isso remove todos os becos reais. A exceção é a regra do 3x3, outra regra
obrigatória do enunciado: nenhum bloco de 3x3 células pode ficar todo aberto, sem nenhuma parede
por dentro ([parte 8](../08-braider/04-a-regra-do-3x3.md)). Toda abertura passa por ela, e o
*braiding* recusa (fecha de novo) a parede que deixaria um 3x3 todo aberto. Se todas as paredes
de um beco forem recusadas, ele fica. A [próxima página](./02-por-que-nao-e-garantido.md) mostra
um caso assim.

A regra obrigatória do enunciado para o modo Pac-Man diz que os becos devem ser raros, com um ou
dois tolerados. O *braiding* vai além do mínimo porque abrir **todos** é tão simples quanto abrir
alguns: o mesmo laço, sem critério de parada.

## Não há chave para ligar

O bônus é o comportamento do modo padrão. Não existe opção no arquivo de configuração para
ligá-lo ou desligá-lo: `PERFECT=False` gera o tabuleiro sem becos, e `PERFECT=True` gera o
labirinto perfeito, com todos os seus becos. O README descreve o bônus na seção **Bonus**
([parte 15](../15-fechamento/04-time-bonus-e-recursos.md)).
