---
sidebar_position: 5
title: O caminho em ciano
---

# O caminho em ciano

Quando o usuário escolhe a opção `2` do menu, o desenho mostra o caminho mais curto da entrada
à saída. Ele precisa aparecer como uma linha **contínua**. Pintar só as células do caminho
deixaria quadrados ciano soltos, separados pelas posições das passagens, que continuariam com o
fundo do terminal. A segunda passada pinta de ciano as células do caminho **e** as passagens
entre células seguidas.

## De onde vem o caminho

```python
        if state.show_path:
            path = maze.path()
```

A passada só roda quando o `ViewState` diz que o caminho está visível (`show_path` é `True`).

O caminho já vem pronto no retrato `GeneratedMaze`, no campo `solution`: uma letra por passo,
`N` (Norte, para cima), `E` (Leste, para a direita), `S` (Sul, para baixo) e `W` (Oeste, para a
esquerda). São as mesmas letras que o arquivo de saída grava na última linha. O método `path()`
([parte 12](../12-geracao-e-saida/02-o-caminho-em-celulas.md)) transforma as letras na lista de
células visitadas, começando na entrada.

No labirinto 4x3, `solution` é `EESES`. Partindo de `0,0`: Leste vai a `1,0`, Leste a `2,0`, Sul
a `2,1`, Leste a `3,1` e Sul a `3,2`, a saída. Cinco letras dão seis células:

```python
[(0, 0), (1, 0), (2, 0), (2, 1), (3, 1), (3, 2)]
```

![O caminho EESES no labirinto 4 por 3, com as células numeradas de 0 a 5](/img/tela/caminho-4x3.svg)

Na figura, magenta é a entrada, vermelho é a saída e a linha ciano é o caminho; o número em cada
célula é a posição dela na lista.

O `RenderService` não procura o caminho: quem acha o caminho mais curto é o gerador, com uma
busca em largura ([parte 7](../07-solver/01-busca-em-largura.md)). O desenho só mostra o que foi
gravado no arquivo, então o caminho da tela e o do arquivo são sempre o mesmo.

## Pares de células seguidas

```python
            for (x1, y1), (x2, y2) in zip(path, path[1:]):
```

`path[1:]` é a lista sem o primeiro item: `[(1, 0), (2, 0), (2, 1), (3, 1), (3, 2)]`.

`zip(a, b)` anda nas duas listas ao mesmo tempo e entrega pares: o primeiro item de `a` com o
primeiro de `b`, o segundo com o segundo, e assim por diante, até uma das listas acabar. Com
`path` e `path[1:]`, cada célula sai junto com a **seguinte**:

```python
[((0, 0), (1, 0)), ((1, 0), (2, 0)), ((2, 0), (2, 1)), ((2, 1), (3, 1)), ((3, 1), (3, 2))]
```

Um caminho de 5 passos dá 5 pares, um por passo.

O `(x1, y1), (x2, y2)` do `for` **desempacota** cada par: separa as duas tuplas e cada tupla nos
seus dois números. Na primeira volta, `x1 = 0, y1 = 0, x2 = 1, y2 = 0`.

## A passagem entre duas células

```python
                canvas[y1 + y2 + 1][x1 + x2 + 1] = Ansi.CYAN
```

A célula `x1,y1` fica na posição `2x1 + 1, 2y1 + 1` do desenho, e a célula `x2,y2` em
`2x2 + 1, 2y2 + 1`. A passagem entre elas fica exatamente no meio, na média das duas posições:

```text
px = ((2x1 + 1) + (2x2 + 1)) / 2 = x1 + x2 + 1
py = ((2y1 + 1) + (2y2 + 1)) / 2 = y1 + y2 + 1
```

Para as células `1,0` e `2,0`, que ficam nas posições `3,1` e `5,1`:

![Esquema de posições do labirinto 4 por 3 com as células 1,0 e 2,0 marcadas e a passagem 4,1 entre elas](/img/tela/passagem.svg)

É o esquema de posições da [página 3](./02-a-grade-de-posicoes.md), com as mesmas cores:
amarelo = célula, escuro = canto, azul = posição de parede fechada, verde = posição de parede
aberta (passagem). O `?` marca a passagem calculada pela conta, `4,1`.

A mesma conta vale para qualquer direção do passo, sem nenhum `if`:

| Passo | Células | Passagem | Qual parede é |
|---|---|---|---|
| Leste | `1,0` → `2,0` | `4,1` | a Leste de `1,0` |
| Sul | `2,0` → `2,1` | `5,2` | a Sul de `2,0` |
| Oeste | `2,0` → `1,0` | `4,1` | a mesma do passo Leste |
| Norte | `2,1` → `2,0` | `5,2` | a mesma do passo Sul |

Duas células seguidas do caminho sempre têm a parede entre elas aberta, porque o caminho só
anda por passagens. Pintar a posição não abre parede nenhuma: só colore um corredor que já
existe.

## A célula de chegada

```python
                canvas[2 * y2 + 1][2 * x2 + 1] = Ansi.CYAN
```

Cada par pinta a célula **de chegada** do passo, `x2,y2`. Assim, todas as células do caminho
ficam ciano, menos a primeira, a entrada, que nunca é chegada de nenhum passo. Ela não precisa:
a próxima passada pinta a entrada de magenta de qualquer jeito. A última célula, a saída, fica
ciano agora e vermelha logo depois.

## O resultado

A linha 1 do desenho (`py = 1`, a das células `x,0`) do 4x3, como o `render` a devolve, com o
caminho escondido e com o caminho visível. Cada `\x1b[` seguido de um número e de `m` é a
sequência que troca a cor de fundo ([parte 10](../10-utilitarios/08-sequencias-ansi.md)), e os dois
espaços depois dela são a posição pintada:

```python
# caminho escondido
'\x1b[47m  \x1b[45m  \x1b[49m  \x1b[49m  \x1b[49m  \x1b[49m  \x1b[47m  \x1b[49m  \x1b[47m  \x1b[0m'
# caminho visível
'\x1b[47m  \x1b[45m  \x1b[46m  \x1b[46m  \x1b[46m  \x1b[46m  \x1b[47m  \x1b[49m  \x1b[47m  \x1b[0m'
```

Lendo as nove posições da esquerda para a direita: borda (`47`, branco), entrada (`45`,
magenta), e depois quatro posições que trocaram `49` (fundo do terminal) por `46` (ciano): a
passagem `2,1`, a célula `1,0`, a passagem `4,1` e a célula `2,0`. Em seguida vêm a parede
fechada `6,1` (`47`), a célula `3,0` (`49`), que o caminho não visita porque desce antes de
chegar nela, e a borda. O `\x1b[0m` do fim devolve o terminal às cores normais
([última página desta parte](./06-as-linhas-de-texto.md)).
