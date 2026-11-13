---
sidebar_position: 7
title: Sem salões e o braiding
---

# Sem salões e o braiding

Um labirinto é feito de corredores, não de salões: o enunciado proíbe áreas abertas grandes, nos
dois modos. E o modo Pac-Man precisa abrir paredes extras num labirinto sem criar esses salões.
Esta página mostra a regra, o processo que transforma um labirinto perfeito num tabuleiro e os
tamanhos de grade em que esse tabuleiro não existe.

## Sem salões: nenhuma área aberta 3x3

O enunciado diz que os corredores não podem ter mais de 2 células de largura. A regra concreta é
que nenhum bloco de 3x3 células pode estar **totalmente aberto**, com as 12 paredes de dentro do
bloco removidas (6 entre colunas vizinhas e 6 entre linhas vizinhas). Blocos abertos de 2x2, 2x3
ou 3x2 são permitidos, e uma única parede por dentro já basta para um bloco 3x3 deixar de ser um
salão:

![Três blocos lado a lado: um 3 por 3 sem paredes por dentro, proibido; um 3 por 3 com uma parede, permitido; um 3 por 2 aberto, permitido](/img/problema/saloes-3x3.svg)

No modo perfeito, essa regra se cumpre sozinha. Um bloco 3x3 aberto tem ciclos (cada bloco 2x2
dentro dele é uma volta, como na [página anterior](./05-perfeito-e-pac-man.md)), e um labirinto
perfeito não tem nenhum. No modo Pac-Man, que abre paredes extras, ela precisa ser vigiada.

## Como o tabuleiro Pac-Man é gerado

Não existe um algoritmo separado para o Pac-Man. O gerador:

1. cria um labirinto **perfeito**;
2. abre uma parede em cada beco sem saída, ligando-o a uma vizinha;
3. abre mais paredes sorteadas até haver pelo menos 2 ciclos;
4. em cada parede que abre nos passos 2 e 3, confere se formou um bloco 3x3 aberto; se formou,
   fecha a parede de novo e tenta outra.

Esse processo se chama **braiding** ("trançar", em inglês): abrir paredes de um labirinto
perfeito para criar ciclos, como fios que se cruzam numa trança.

Os sorteios podem dar azar: um beco cujas paredes só formariam salões fica sem abrir. Por isso,
no fim, o gerador confere o resultado (no máximo 2 becos e pelo menos 2 ciclos). Se não deu, ele
descarta o labirinto e começa de novo, do passo 1, até 20 vezes. Se as 20 falharem, o gerador
desiste com um erro (na prática, a primeira tentativa já dá certo). O braiding é construído na
[parte 8](../08-braider/01-becos-sem-saida.md), e as tentativas na
[parte 9](../09-gerador/03-generate.md).

## Tamanhos impossíveis

O tabuleiro Pac-Man precisa de pelo menos dois ciclos (duas rotas independentes, como na
[página anterior](./05-perfeito-e-pac-man.md#duas-rotas-independentes)). Algumas grades não
comportam dois ciclos, mesmo sem nenhuma parede por dentro. Numa grade de 1 linha (ou de 1
coluna), as células ficam em fila, e uma fila não tem como dar a volta. Numa grade 2x2, só existe
uma volta possível, em torno do meio.

Para contar quantos ciclos independentes uma grade comporta, abra todas as paredes de dentro.
Cada bloco de 2x2 células vira um quadradinho com uma volta, como os dois da grade 3x2 da página
anterior, e qualquer outra volta é uma combinação desses quadradinhos. Basta então contar os
blocos 2x2: o canto de cima à esquerda de um bloco pode estar em qualquer coluna menos a última e
em qualquer linha menos a última. Numa grade `WIDTH x HEIGHT`, são `(WIDTH − 1) × (HEIGHT − 1)`
blocos, e portanto esse tanto de ciclos independentes. Na grade 3x2: `2 × 1 = 2`.

Quando essa conta dá menos de 2, o modo Pac-Man é impossível. Recusar o arquivo de configuração
antes de tentar é escolha do projeto: o gerador nunca conseguiria cumprir a regra, e a mensagem
explica o motivo em vez de gastar tentativas. Com `WIDTH=1`, `HEIGHT=10` e a saída dentro dessa
grade (`EXIT=0,9`), o programa pronto (o da
[parte 14](../14-menu-e-main/06-saidas-e-erros-inesperados.md)) mostra:

```text
Error: config.txt: PERFECT=False needs (WIDTH - 1) x (HEIGHT - 1) >= 2 for a Pac-Man board, got 1x10
```

O `1x10` no fim da mensagem é o tamanho pedido, `WIDTH` x `HEIGHT` (1 coluna por 10 linhas), e
não o resultado da conta, que daria `0 × 9 = 0`.

## O que vem depois

O "42" deixa dois becos que o braiding não abre e que não entram na conta do "no máximo 2
becos": a [próxima página](./06-o-padrao-42.md) mostra de onde eles vêm e por que não dá para
abri-los.
