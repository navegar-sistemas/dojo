---
sidebar_position: 9
title: Caracteres de caixa
---

# Caracteres de caixa

No desenho do labirinto, uma parede é uma **linha** fina, e as linhas precisam se encontrar sem
falha: uma parede horizontal que chega a uma vertical forma um canto, três paredes que se
encontram formam um T. O terminal só mostra caracteres, então o desenho precisa de caracteres que
sejam pedaços de linha. Esta página apresenta esses caracteres e cria a classe `Box`
(`amazeing/utils/box.py`), que escolhe o caractere certo para cada encontro de paredes.

## O que é um caractere de caixa

Num terminal, cada caractere ocupa um retângulo do mesmo tamanho, e os retângulos ficam colados
uns nos outros, em linhas e colunas. A tabela **Unicode** numera os caracteres de todas as
escritas do mundo; os 128 primeiros são os da tabela ASCII
([página 7](./08-sequencias-ansi.md)), e entre os outros há um grupo feito para desenhar
molduras: os **caracteres de caixa** (*box-drawing characters*).

Um caractere de caixa é desenhado de modo que as suas linhas encostem nas bordas do retângulo.
Um `━` vai da borda esquerda à direita; um `┃`, da borda de cima à de baixo. Postos lado a lado,
os traços de um continuam nos do vizinho, e a sequência `┏━━━┓` vira uma linha só, com os dois
cantos.

O grupo tem versões finas (`─`, `│`, `┌`) e grossas (`━`, `┃`, `┏`). O projeto usa as grossas,
para as paredes aparecerem bem; é escolha do projeto.

### E a "renderização ASCII"?

O enunciado lista, como uma das formas de mostrar o labirinto, a "Renderização ASCII no
terminal", sem dizer o que conta como renderização ASCII. A segunda figura de exemplo do mesmo
capítulo mostra um labirinto com paredes finas e contínuas, e nenhum caractere da tabela ASCII
desenha uma linha assim. O projeto lê "ASCII" como "desenho feito de texto no terminal", e não
como "só os 128 caracteres da tabela"; é uma escolha, e os caracteres de caixa são o que deixa
as paredes finas.

## Os braços

Um **braço** é uma linha que sai do centro do caractere e vai até uma das bordas. Há quatro
bordas, então um caractere de caixa tem de zero a quatro braços: o `━` tem os braços Leste e
Oeste, o `┏` tem Leste e Sul, o `╋` tem os quatro.

Cada braço recebe um bit, na mesma convenção das paredes de uma célula
([parte 1](../01-o-problema/02-paredes-em-bits.md)): Norte = 1, Leste = 2, Sul = 4, Oeste = 8.
A soma dos bits dos braços dá um número de 0 a 15, e cada número corresponde a exatamente um
caractere:

![Os 16 caracteres de caixa, um para cada soma de braços de 0 a 15](/img/utilitarios/caixa-bracos.svg)

Cada retângulo tracejado é o lugar de um caractere; embaixo, a soma dos braços e quais são eles.
Os de um braço só (1, 2, 4 e 8) são meias linhas, que param no centro: aparecem na ponta de uma
parede solta e na ponta do caminho mais curto. O 0 é o espaço: nenhum braço.

## A tabela

```python
    _BY_ARMS = " ╹╺┗╻┃┏┣╸┛━┻┓┫┳╋"
```

Os 16 caracteres estão numa string só, em ordem: o caractere da posição `n` é o que tem os braços
cujos bits somam `n`. Uma string se indexa como uma lista, então `_BY_ARMS[6]` é o sétimo
caractere, `┏`: 6 = Leste (2) + Sul (4).

| Soma | Braços | Caractere |
|---|---|---|
| 0 | nenhum | espaço |
| 5 | Norte + Sul | `┃` |
| 6 | Leste + Sul | `┏` |
| 10 | Leste + Oeste | `━` |
| 11 | Norte + Leste + Oeste | `┻` |
| 15 | os quatro | `╋` |

O `_` no começo do nome marca o atributo como interno da classe: quem usa a `Box` pede um
caractere pelo método `glyph`, e não lê a string direto.

## As duas paredes e o método `glyph`

```python
    HORIZONTAL = "━"
    VERTICAL = "┃"
```

São os caracteres de uma parede fechada: `━` numa parede horizontal (a Norte ou a Sul de uma
célula), `┃` numa vertical (a Leste ou a Oeste). Os dois também estão na tabela, nas posições 10
e 5; as constantes dão nome a eles, para o desenho escrever `Box.HORIZONTAL` em vez de
`Box.glyph(10)`.

```python
    @staticmethod
    def glyph(arms: int) -> str:
        return Box._BY_ARMS[arms]
```

*Glyph* é o desenho de um caractere. `glyph(arms)` recebe a soma dos braços e devolve o
caractere. O desenho do labirinto usa o método em dois lugares:

- nos **cantos**: em cada canto, ele soma os bits das paredes que saem dali e pede o caractere
  com esses braços ([parte 13](../13-tela/03-paredes-e-cantos.md));
- no **centro** de cada célula do caminho mais curto: os braços são os lados que levam à célula
  anterior e à seguinte do caminho ([parte 13](../13-tela/05-o-caminho-em-ciano.md)).

## O arquivo completo

```python title="amazeing/utils/box.py"
"""Box-drawing characters chosen by the lines that leave their centre."""


class Box:
    """Heavy box-drawing characters indexed by their arms.

    An arm is a line from the centre of the character to one of its
    edges. The bit of each arm follows the wall bits of the output file:
    north 1, east 2, south 4 and west 8.

    Attributes:
        HORIZONTAL: Line from the west edge to the east edge.
        VERTICAL: Line from the north edge to the south edge.
    """

    HORIZONTAL = "━"
    VERTICAL = "┃"
    _BY_ARMS = " ╹╺┗╻┃┏┣╸┛━┻┓┫┳╋"

    @staticmethod
    def glyph(arms: int) -> str:
        """Character whose lines are exactly the given arms.

        Args:
            arms: Sum of the arm bits, 0 to 15.

        Returns:
            The character; a space when there is no arm.
        """
        return Box._BY_ARMS[arms]
```

## Experimente

Na raiz do projeto, o trecho pede alguns caracteres pela soma dos braços e monta uma caixa com
os quatro cantos. O `|` é o "ou" bit a bit ([parte 1](../01-o-problema/08-ler-e-mudar-paredes.md)):
`2 | 4` liga os bits de Leste e de Sul, e dá 6.

```bash
.venv/bin/python - <<'EOF'
from amazeing.utils.box import Box

print([Box.glyph(arms) for arms in (0, 5, 6, 10, 15)])
print(Box.glyph(10) == Box.HORIZONTAL, Box.glyph(5) == Box.VERTICAL)
print(Box.glyph(2 | 4) + Box.HORIZONTAL * 3 + Box.glyph(4 | 8))
print(Box.glyph(1 | 2) + Box.HORIZONTAL * 3 + Box.glyph(1 | 8))
EOF
```

```text
[' ', '┃', '┏', '━', '╋']
True True
┏━━━┓
┗━━━┛
```

As duas últimas linhas são uma caixa fechada: os cantos de cima têm o braço Sul, que encosta nos
de baixo, e os de baixo têm o braço Norte.
