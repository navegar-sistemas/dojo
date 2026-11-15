---
sidebar_position: 4
title: Paredes e cantos
---

# Paredes e cantos

Na base do desenho ([página anterior](./02-a-grade-de-caracteres.md)), a tabela `chars` só tem
espaços. A primeira camada desenha as paredes nela. Para isso o programa tem de descobrir, para
cada célula, quais lados estão fechados, e essa informação está nos bits do número de cada célula.
Depois, cada canto precisa do caractere que emenda as paredes que chegam nele. O método
`_draw_walls` faz as duas coisas, nessa ordem.

## Percorrer a grade

```python
        for y, row in enumerate(grid):
            for x, walls in enumerate(row):
                left = STEP * x
```

`grid` é a grade de paredes que o `render` passou (`maze.grid`). `enumerate` entrega cada item de
uma lista junto com o seu índice. No labirinto 4x3 da página anterior, a grade é
`((13, 5, 3, 11), (9, 7, 12, 2), (12, 5, 5, 6))`, então:

- a primeira volta do laço de fora dá `y = 0` e `row = (13, 5, 3, 11)`, a primeira linha;
- dentro dela, o laço de dentro dá `x = 0, walls = 13`, depois `x = 1, walls = 5`, e assim por
  diante.

Ao fim, cada célula `x,y` passou uma vez pelo corpo do laço, com `walls` igual a `grid[y][x]`:
o número que diz quais paredes da célula estão fechadas. `left` é a coluna do desenho onde a
célula começa, a da sua parede Oeste: `4x`.

Relembrando o formato desse número ([parte 1](../01-o-problema/02-paredes-em-bits.md)): cada
lado da célula ocupa um **bit** (um dígito 0 ou 1 da escrita binária do número), e o bit vale 1
quando há parede.

| Lado | Onde fica | Valor do bit |
|---|---|---|
| Norte | em cima | 1 |
| Leste | à direita | 2 |
| Sul | embaixo | 4 |
| Oeste | à esquerda | 8 |

## Como saber se uma parede está fechada

```python
                if walls & Direction.NORTH:
                    for column in range(left + 1, left + STEP):
                        chars[2 * y][column] = Box.HORIZONTAL
```

`Direction` é uma **enumeração** (um tipo com um conjunto fixo de valores, cada um com nome) dos
quatro lados de uma célula, criada na [parte 4](../04-value-objects/02-direction-bits.md). Cada
lado tem como valor o próprio bit: `Direction.NORTH` vale 1, `Direction.EAST` vale 2,
`Direction.SOUTH` vale 4 e `Direction.WEST` vale 8. Ela é um `IntEnum`, um tipo cujos membros se
comportam como números inteiros, então `walls & Direction.NORTH` faz a mesma conta que
`walls & 1`.

O `&` ("e" bit a bit) compara dois números bit a bit e só mantém os bits que valem 1 nos dois.
Com um dos lados sendo um bit só, o resultado responde se esse bit está ligado em `walls`:

- se a parede está **fechada**, o bit está ligado, e o resultado é o próprio valor do bit;
- se a parede está **aberta**, o bit está desligado, e o resultado é `0`.

Em Python, `0` conta como falso e qualquer outro número como verdadeiro. Então
`if walls & Direction.NORTH` quer dizer "se a parede Norte está fechada".

Para a célula `0,0` do 4x3, `walls` é `13`, `1101` em binário: Norte, Sul e Oeste fechados,
Leste aberto. Em Python, um número escrito com o prefixo `0b` está em binário: `0b1101` é o
mesmo número que `13`, e é assim que a figura abaixo o escreve.

![Os bits de 13: Oeste 1, Sul 1, Leste 0, Norte 1](/img/tela/bits-13.svg)

```text
13 & Direction.NORTH ->  1101 & 0001  ->  0001  ->  1   (Norte fechado)
13 & Direction.EAST  ->  1101 & 0010  ->  0000  ->  0   (Leste aberto)
```

O `Direction` vem do `mazegen` (`mazegen.value_objects.direction`), o mesmo usado para gerar o
labirinto e gravar o arquivo de saída. O `RenderService` não declara um `NORTH = 1` próprio: os
bits do desenho e os do arquivo vêm da mesma definição e não têm como divergir.

## Desenhar os quatro lados

```python
                if walls & Direction.NORTH:
                    for column in range(left + 1, left + STEP):
                        chars[2 * y][column] = Box.HORIZONTAL
                if walls & Direction.SOUTH:
                    for column in range(left + 1, left + STEP):
                        chars[2 * y + 2][column] = Box.HORIZONTAL
                if walls & Direction.WEST:
                    chars[2 * y + 1][left] = Box.VERTICAL
                if walls & Direction.EAST:
                    chars[2 * y + 1][left + STEP] = Box.VERTICAL
```

Cada lado fechado vira caracteres no lugar dele
([página anterior](./02-a-grade-de-caracteres.md#onde-cada-pedaço-cai)):

| Lado fechado | Linha | Colunas | Caractere |
|---|---|---|---|
| Norte | `2y`, logo acima da célula | `4x + 1` a `4x + 3` | `━` (`Box.HORIZONTAL`) |
| Sul | `2y + 2`, logo abaixo | `4x + 1` a `4x + 3` | `━` |
| Oeste | `2y + 1`, a da célula | `4x` | `┃` (`Box.VERTICAL`) |
| Leste | `2y + 1` | `4x + 4` | `┃` |

`range(left + 1, left + STEP)` são as colunas `4x + 1`, `4x + 2` e `4x + 3`: o `range` para
**antes** do segundo número. Uma parede horizontal ocupa a largura do interior da célula, três
caracteres; a vertical, um caractere só. Uma parede **aberta** não escreve nada, e o lugar dela
continua um espaço.

Para a célula `0,0` (`13`), o Norte, o Sul e o Oeste estão fechados, e o Leste aberto:

![Os caracteres em volta da célula 0,0: linha horizontal em cima e embaixo, linha vertical à esquerda, nada à direita](/img/tela/paredes-0-0.svg)

A figura mostra as linhas 0 a 2 e as colunas 0 a 4 do desenho, já com os cantos da próxima seção;
em amarelo, o interior da célula. A coluna 4 da linha 1, a parede Leste, ficou vazia: é a
passagem para a célula `1,0`.

### Cada parede escrita duas vezes

Uma parede de dentro do labirinto pertence a duas células: a parede Leste de `x,y` é a parede
Oeste de `x + 1, y`. O laço olha os quatro lados de toda célula, então essa parede é escrita duas
vezes, uma por célula, com o mesmo caractere no mesmo lugar. A segunda escrita não muda nada.

As duas células sempre **concordam** sobre a parede que dividem: é a regra de **coerência** do
enunciado ([parte 1](../01-o-problema/01-a-grade-e-as-celulas.md)). O `Maze`, a classe que
guarda as paredes durante a geração, garante isso: o único jeito de abrir uma parede é o
`open_wall`, que abre os dois lados de uma vez ([parte 5](../05-maze/04-abrir-e-fechar.md)).
Olhar os quatro lados de cada célula também desenha a borda sem nenhuma regra a mais: o Norte da
primeira linha, o Oeste da primeira coluna, o Leste da última e o Sul da última estão sempre
fechados.

## Os cantos

Depois do primeiro laço, as paredes estão desenhadas, mas os cantos continuam espaços. Um canto
precisa do caractere de caixa que emenda as paredes que chegam nele: `┏` onde uma parede desce e
outra vai para a direita, `┳` onde três se encontram, `━` no meio de uma parede reta, um espaço
onde nenhuma parede chega.

Os braços de um canto são as paredes que saem dele, e a classe `Box`
([parte 10](../10-utilitarios/09-caracteres-de-caixa.md)) dá o caractere certo para cada soma
de braços: Norte = 1, Leste = 2, Sul = 4, Oeste = 8, os mesmos bits das paredes.

```python
        last_line = len(chars) - 1
        last_column = len(chars[0]) - 1
        for line in range(0, last_line + 1, 2):
            for column in range(0, last_column + 1, STEP):
                arms = 0
                if line > 0 and chars[line - 1][column] == Box.VERTICAL:
                    arms |= Direction.NORTH
                if (column < last_column
                        and chars[line][column + 1] == Box.HORIZONTAL):
                    arms |= Direction.EAST
                if (line < last_line
                        and chars[line + 1][column] == Box.VERTICAL):
                    arms |= Direction.SOUTH
                if column > 0 and chars[line][column - 1] == Box.HORIZONTAL:
                    arms |= Direction.WEST
                chars[line][column] = Box.glyph(arms)
```

- `range(0, last_line + 1, 2)` dá as linhas pares, `0, 2, 4...`, e
  `range(0, last_column + 1, STEP)` as colunas múltiplas de 4: exatamente os cantos.
- Para cada canto, `arms` começa em 0 e ganha um bit para cada parede que encosta nele: um `┃`
  logo acima (Norte), um `━` logo à direita (Leste), um `┃` logo abaixo (Sul), um `━` logo à
  esquerda (Oeste). `arms |= Direction.NORTH` liga o bit do Norte em `arms`: o `|=` faz o "ou"
  bit a bit e guarda o resultado na própria variável
  ([parte 1](../01-o-problema/08-ler-e-mudar-paredes.md)).
- As condições `line > 0`, `column < last_column` e as outras duas impedem de olhar para fora
  das tabelas: o canto da primeira linha não tem nada acima dele.
- `Box.glyph(arms)` dá o caractere com exatamente esses braços.

O canto lê o **desenho**, e não a grade de bits. Um canto fica entre até quatro células, e cada
parede que chega nele já está nas tabelas, escrita pelo primeiro laço; olhar os quatro vizinhos
do desenho é mais curto do que perguntar às quatro células. Por isso os cantos vêm **depois** das
paredes.

Os 20 cantos do 4x3, em amarelo:

![O desenho das paredes do labirinto 4 por 3 com os 20 cantos destacados em amarelo](/img/tela/cantos-4x3.svg)

Alguns deles, com os braços e o caractere escolhido:

| Linha, coluna | Braços | Soma | Caractere |
|---|---|---|---|
| 0, 0 | Leste + Sul | 6 | `┏` |
| 0, 12 | Leste + Sul + Oeste | 14 | `┳` |
| 2, 0 | Norte + Leste + Sul | 7 | `┣` |
| 2, 4 | Leste + Oeste | 10 | `━` |
| 2, 8 | Sul + Oeste | 12 | `┓` |
| 2, 12 | Norte | 1 | `╹` |
| 4, 4 | Leste | 2 | `╺` |
| 4, 8 | Norte + Leste + Oeste | 11 | `┻` |

O canto da linha 2, coluna 12 tem um braço só: a parede vertical que desce da borda de cima
termina ali, e o `╹` é uma meia linha que para no centro do caractere. Num tabuleiro Pac-Man,
onde há blocos de 2x2 células sem parede por dentro, o canto do meio do bloco não tem braço
nenhum e fica um espaço.

## Depois da primeira camada

Todas as paredes fechadas e todos os cantos já estão em `chars`. As cores continuam as do começo:
texto na cor das paredes e fundo branco. Com o caminho escondido, só faltam o "42", a entrada e a
saída para o desenho ficar pronto.
