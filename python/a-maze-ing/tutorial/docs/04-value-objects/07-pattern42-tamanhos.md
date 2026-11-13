---
sidebar_position: 6
title: "Pattern42: três tamanhos"
---

# `Pattern42`: três tamanhos

O `for_size` da [página anterior](./05-pattern42-posicao.md) recebe o tamanho da grade e devolve
as células do "42": calcula o canto `x0,y0` do bloco 7x5 (`x0 = (width - 7) // 2`,
`y0 = (height - 5) // 2`) e desloca cada `X` do desenho até ali. Esta página mostra onde o bloco
cai em três tamanhos de grade, e por que nenhum tamanho permitido deixa o "42" colado na borda.

## Três tamanhos

Em 9x7, o tamanho mínimo, sobra exatamente uma célula de corredor em volta do bloco (tracejado):

![O 42 numa grade 9 por 7](/img/value-objects/pattern42-9x7.svg)

Em 20x15, o tamanho do `config.txt`:

![O 42 numa grade 20 por 15](/img/value-objects/pattern42-20x15.svg)

Em 8x7, `x0 = (8 - 7) // 2 = 0`: o bloco começaria na coluna 0, colado na borda esquerda, sem
nenhuma célula livre entre o "4" e a borda. Isso quebra a folga escolhida na
[parte 1](../01-o-problema/06-o-padrao-42.md) (pelo menos uma célula livre entre o "42" e cada
borda). Por isso o padrão fica vazio:

![Em 8 por 7 o bloco encostaria na borda](/img/value-objects/pattern42-8x7.svg)

### A margem vale em todo tamanho permitido

Com `width >= 9`, sobram pelo menos 2 colunas fora do bloco. A sobra da esquerda,
`x0 = (width - 7) // 2`, é a metade arredondada para baixo: pelo menos 1. A sobra da direita é o
resto, igual à da esquerda ou uma coluna maior: também pelo menos 1. Por isso a última coluna do
bloco, `x0 + 6`, fica no máximo em `width - 2`. O mesmo raciocínio vale para as linhas com `height >= 7`. Então
sempre há pelo menos uma célula livre entre o "42" e cada borda, e os quatro cantos da grade
nunca são do "42".

Os cantos importam por causa do modo Pac-Man: o enunciado exige que os quatro cantos e o centro
sejam corredores abertos e explica o motivo: os fantasmas e as *super-pac-gums* (as pastilhas
especiais do jogo) ficam nos cantos, e o jogador começa no centro. Uma célula do "42" nunca é
corredor, então o "42" não pode ocupar um canto.

## O que falta

O `Pattern42` já sabe **quais** células formam o "42". Falta responder à pergunta que o resto do
gerador faz, "esta célula é do 42?". A [próxima página](./06-pattern42-consulta.md) escreve essa
resposta e mostra o arquivo completo, com um exemplo para rodar.
