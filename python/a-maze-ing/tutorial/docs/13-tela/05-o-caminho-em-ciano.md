---
sidebar_position: 6
title: O caminho em ciano
---

# O caminho em ciano

Quando o usuário escolhe a opção `2` do menu, o desenho mostra o caminho mais curto da entrada
à saída. Ele precisa aparecer como uma linha **contínua**, que passa pelo meio dos corredores sem
encostar nas paredes e faz a curva onde o caminho vira. A quarta e última camada do desenho
([página 3](./02-a-grade-de-caracteres.md#as-camadas-do-desenho)) escreve essa linha com
caracteres de caixa em ciano, do centro de uma célula ao centro da seguinte.

## De onde vem o caminho

```python
        if state.show_path:
            self._draw_path(maze.path(), chars, texts)
```

A camada só roda quando o `ViewState` diz que o caminho está visível (`show_path` é `True`).

O caminho já vem pronto no retrato `GeneratedMaze`, no campo `solution`: uma letra por passo,
`N` (Norte, para cima), `E` (Leste, para a direita), `S` (Sul, para baixo) e `W` (Oeste, para a
esquerda). São as mesmas letras que o arquivo de saída grava na última linha. O método `path()`
([parte 12](../12-geracao-e-saida/02-o-caminho-em-celulas.md)) transforma as letras na lista de
células visitadas, começando na entrada.

No labirinto 4x3 da [página 3](./02-a-grade-de-caracteres.md), `solution` é `EESES`. Partindo de
`0,0`: Leste vai a `1,0`, Leste a `2,0`, Sul a `2,1`, Leste a `3,1` e Sul a `3,2`, a saída.
Cinco letras dão seis células:

```python
[(0, 0), (1, 0), (2, 0), (2, 1), (3, 1), (3, 2)]
```

![O caminho EESES no labirinto 4 por 3, com as células numeradas de 0 a 5](/img/tela/caminho-4x3.svg)

Na figura, magenta é a entrada, vermelho é a saída e a linha ciano é o caminho; o número em cada
célula é a posição dela na lista.

O `RenderService` não procura o caminho: quem acha o caminho mais curto é o gerador, com uma
busca em largura ([parte 7](../07-solver/01-busca-em-largura.md)). O desenho só mostra o que foi
gravado no arquivo, então o caminho da tela e o do arquivo são sempre o mesmo.

## O centro de cada célula

A linha passa pelo **centro** de cada célula do caminho, a coluna `4x + 2` da linha `2y + 1`. O
caractere do centro precisa dos braços que levam às células vizinhas **no caminho**: à anterior e
à seguinte. Na célula `2,0`, que vem de `1,0` (Oeste) e segue para `2,1` (Sul), é o `┓`.

```python
        for index, (x, y) in enumerate(path):
            arms = 0
            for neighbour in path[max(index - 1, 0):index + 2]:
                for side in Direction:
                    if (x + side.dx, y + side.dy) == neighbour:
                        arms |= side
            chars[2 * y + 1][STEP * x + 2] = Box.glyph(arms)
            texts[2 * y + 1][STEP * x + 2] = Ansi.CYAN
```

- `path[max(index - 1, 0):index + 2]` é a fatia da lista com a célula anterior, a própria célula e
  a seguinte. Na primeira célula, `max(0 - 1, 0)` dá 0, e a fatia começa nela mesma, que não tem
  anterior; na última, a fatia passa do fim da lista, e o Python a corta sem erro.
- `for side in Direction` percorre os quatro lados. `side.dx` e `side.dy` dizem quanto `x` e `y`
  mudam num passo para aquele lado ([parte 4](../04-value-objects/03-direction-propriedades.md)):
  se a célula de um passo para aquele lado é a vizinha, o braço daquele lado entra em `arms`. A
  própria célula está na fatia, mas nunca fica a um passo de si mesma, então não acrescenta braço.
- O caractere vai para o centro, e a cor do **texto** dele vira ciano. O fundo não muda: na
  entrada e na saída continua magenta e vermelho.

As células do meio do caminho ganham dois braços: `━` ou `┃` onde o caminho segue reto, um canto
como `┓` onde ele vira. A entrada e a saída têm uma vizinha só no caminho e ganham um braço só,
uma meia linha que começa no centro: na entrada `0,0`, que segue para Leste, o `╺`.

## Os trechos entre duas células

Os centros sozinhos seriam pontos soltos: falta a linha que liga um centro ao seguinte.

```python
        for (x1, y1), (x2, y2) in zip(path, path[1:]):
            if y1 == y2:
                line = 2 * y1 + 1
                start = STEP * min(x1, x2) + 3
                for column in range(start, start + STEP - 1):
                    chars[line][column] = Box.HORIZONTAL
                    texts[line][column] = Ansi.CYAN
            else:
                line = 2 * min(y1, y2) + 2
                chars[line][STEP * x1 + 2] = Box.VERTICAL
                texts[line][STEP * x1 + 2] = Ansi.CYAN
```

`path[1:]` é a lista sem o primeiro item. `zip(a, b)` anda nas duas listas ao mesmo tempo e
entrega pares: o primeiro item de `a` com o primeiro de `b`, o segundo com o segundo, e assim por
diante, até uma das listas acabar. Com `path` e `path[1:]`, cada célula sai junto com a
**seguinte**: um caminho de 5 passos dá 5 pares. O `(x1, y1), (x2, y2)` do `for` **desempacota**
cada par em quatro números.

- **Passo na horizontal** (`y1 == y2`): os dois centros estão na mesma linha do desenho, a
  `2y + 1`, nas colunas `4x + 2` e `4x + 6`, com `x` a menor das duas colunas de célula. Entre
  eles ficam três caracteres, as colunas `4x + 3` a `4x + 5`: o último do interior da célula da
  esquerda, a parede (aberta) entre as duas e o primeiro do interior da da direita. Os três
  viram `━`. O `min` deixa a conta igual para um passo Leste e para um passo Oeste.
- **Passo na vertical**: os dois centros estão na mesma coluna, `4x + 2`, em linhas que diferem
  de 2. Entre eles fica um caractere só, na linha da parede (aberta) entre as duas células,
  `2y + 2` com `y` a menor das duas linhas. Ele vira `┃`.

No 4x3, os cinco passos de `EESES`:

| Passo | Células | Linha | Colunas | Caractere |
|---|---|---|---|---|
| Leste | `0,0` → `1,0` | 1 | 3 a 5 | `━` |
| Leste | `1,0` → `2,0` | 1 | 7 a 9 | `━` |
| Sul | `2,0` → `2,1` | 2 | 10 | `┃` |
| Leste | `2,1` → `3,1` | 3 | 11 a 13 | `━` |
| Sul | `3,1` → `3,2` | 4 | 14 | `┃` |

![O desenho do labirinto 4 por 3 com o caminho em ciano, com linhas e colunas numeradas e os centros das células do caminho contornados em laranja](/img/tela/caminho-linha-4x3.svg)

Na figura, os números de cima são as colunas do desenho, e os da esquerda, as linhas; contornados
em laranja, os centros das seis células do caminho, inclusive os da entrada e da saída. A linha
ciano liga um centro ao seguinte.

Duas células seguidas do caminho sempre têm a parede entre elas aberta, porque o caminho só anda
por passagens. Os caracteres que a camada escreve eram todos espaços: interior de célula ou
parede aberta. Ela não apaga parede nenhuma; só desenha dentro dos corredores. E o caminho
nunca entra nas células do "42": elas têm as quatro paredes fechadas.

## O resultado

A linha 1 do desenho do 4x3 (a das células `x,0`), como o `render` a devolve, com o caminho
escondido e com o caminho visível. Cada `\x1b[38;2;...;48;2;...m` é a sequência que escolhe a cor
do texto e a do fundo ([parte 10](../10-utilitarios/08-sequencias-ansi.md)):

```python
# caminho escondido
'\x1b[38;2;31;41;55;48;2;255;255;255m┃\x1b[38;2;31;41;55;48;2;217;70;239m   \x1b[38;2;31;41;55;48;2;255;255;255m        ┃   ┃\x1b[0m'
# caminho visível
'\x1b[38;2;31;41;55;48;2;255;255;255m┃\x1b[38;2;31;41;55;48;2;217;70;239m \x1b[38;2;34;211;238;48;2;217;70;239m╺━\x1b[38;2;34;211;238;48;2;255;255;255m━━━━━━┓\x1b[38;2;31;41;55;48;2;255;255;255m ┃   ┃\x1b[0m'
```

Com o caminho escondido, a linha tem a parede da borda, o interior da entrada (fundo magenta,
`217;70;239`), oito espaços, a parede entre as células `2,0` e `3,0`, os três espaços da célula
`3,0` e a parede da borda. Com o caminho visível, entram caracteres ciano
(`34;211;238`): o `╺━` ainda dentro da entrada, sobre o fundo magenta, e o `━━━━━━┓` sobre o
branco, até o centro da célula `2,0`, onde o caminho desce. A célula `3,0`, que o caminho não
visita, continua com três espaços. O `\x1b[0m` do fim devolve o terminal às cores normais
([próxima página](./06-as-linhas-de-texto.md)).
