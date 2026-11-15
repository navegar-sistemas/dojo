---
sidebar_position: 8
title: Cores ANSI
---

# Cores ANSI

Com as sequências SGR da [página anterior](./08-sequencias-ansi.md), o programa consegue escolher
a cor do texto e a do fundo de cada trecho do terminal. Falta decidir quais cores o desenho usa
e onde cada uma entra, e guardar tudo num lugar só, para que nenhuma outra classe precise
montar uma sequência à mão. Esta página cria a classe `Ansi` (`amazeing/utils/ansi.py`) com as
cores do desenho ([parte 13](../13-tela/02-a-grade-de-caracteres.md)) e o método que monta a
sequência.

## Texto e fundo

No desenho, as paredes são **linhas**: caracteres como `━` e `┃`, apresentados na
[próxima página](./09-caracteres-de-caixa.md). O que tem forma de linha usa a cor do **texto**;
o que tem forma de bloco usa a cor do **fundo**:

- no texto: as paredes e o caminho mais curto, que também é uma linha;
- no fundo: o branco de todo o desenho, o "42" e as células de entrada e de saída.

Todo caractere do desenho recebe um fundo, mesmo o espaço de um corredor, que fica branco. Pintar
o fundo inteiro é escolha do projeto: sem ele, o corredor teria a cor de fundo do terminal, e
uma parede grafite sumiria num terminal de tema escuro. Com o fundo branco, o desenho sai igual
em qualquer tema.

## As constantes

![As nove cores de Ansi: WHITE 255, 255, 255, fundo de tudo; CHARCOAL 31, 41, 55, ORANGE 194, 65, 12, GREEN 21, 128, 61 e BLUE 29, 78, 216, as quatro cores de parede; GREY 156, 163, 175, fundo do 42; MAGENTA 217, 70, 239, fundo da entrada; RED 239, 68, 68, fundo da saída; CYAN 34, 211, 238, linha do caminho](/img/utilitarios/paleta-ansi.svg)

Cada quadrado mostra a cor, com o nome da constante, os valores de vermelho, verde e azul e o que
ela pinta no desenho. O menu troca a cor das paredes entre `CHARCOAL`, `ORANGE`, `GREEN` e
`BLUE`. As cores e o que cada uma pinta são escolha do projeto; o critério das quatro cores de
parede está na [paleta da parte 13](../13-tela/01-o-estado-da-tela.md#a-paleta).

## O tipo `Rgb`

```python
Rgb = tuple[int, int, int]
```

Cada cor é uma tupla de três números: vermelho, verde e azul. `tuple[int, int, int]` é a
anotação de tipo de uma tupla com **exatamente** três inteiros. A linha dá um nome curto a esse
tipo, um **apelido de tipo** (*type alias*): `Rgb` pode ser usado em qualquer anotação no lugar
de `tuple[int, int, int]`, e o mypy entende os dois como o mesmo tipo.

```python
    WHITE: Rgb = (255, 255, 255)
```

Dentro da classe, cada cor é um atributo anotado com o apelido: `WHITE` vale a tupla
`(255, 255, 255)`. O `ViewState` e o `RenderService`, da parte 13, importam o `Rgb` deste mesmo
arquivo para anotar as cores que guardam.

## `RESET` e `colours`

```python
    RESET = "\x1b[0m"
```

Toda linha do desenho termina com o reset. Sem ele, as últimas cores da linha continuariam
valendo para o menu e até para o terminal depois que o programa termina.

```python
    @staticmethod
    def colours(text: Rgb, background: Rgb) -> str:
        return "\x1b[38;2;{};{};{};48;2;{};{};{}m".format(*text, *background)
```

`colours(text, background)` monta a sequência que escolhe as duas cores de uma vez: a do texto
e a do fundo. `@staticmethod` quer dizer que o método não usa nenhum dado de um objeto e se chama
direto pela classe: `Ansi.colours(Ansi.CHARCOAL, Ansi.WHITE)`.

O `format` troca cada `{}` da string, da esquerda para a direita, por um argumento. O `*` na
frente de uma tupla a **desempacota**: `*text` passa os três números da tupla como três
argumentos separados. Com `*text, *background`, o `format` recebe seis números e preenche os
seis `{}`:

```python
"{};{};{}".format(*(31, 41, 55))    # '31;41;55', o mesmo que .format(31, 41, 55)
```

Escrita como f-string com os índices, `{text[0]}` a `{background[2]}`, a mesma linha do `return`
teria 111 caracteres, acima do limite de 79 do flake8; com o `format` e o `*`, ela cabe.

As cores ficam guardadas como **tuplas**, e a sequência só é montada na hora de desenhar. Assim
a lista das cores de parede é uma tupla de cores (`Ansi.CHARCOAL`, `Ansi.ORANGE`...), fácil de
comparar e de percorrer, e o formato `ESC [ 38;2;R;G;B;48;2;R;G;B m` fica escrito num lugar só.

Uma linha real do desenho, a segunda do labirinto 3x2 da
[parte 1](../01-o-problema/07-o-desenho-e-o-menu.md), separada nos trechos de cada sequência:

![Uma linha do desenho em três trechos: a parede da borda, grafite sobre fundo branco, a entrada em magenta e o resto da linha sobre fundo branco, cada trecho com a sua sequência](/img/utilitarios/linha-sgr.svg)

Em cima, a linha como o terminal a mostra; embaixo, o texto que o programa imprime para cada
trecho. Uma sequência só aparece onde o par de cores muda: o trecho 3 pinta oito espaços e uma
parede com uma sequência só.

## O arquivo completo

```python title="amazeing/utils/ansi.py"
"""24-bit ANSI colours of the terminal drawing."""

Rgb = tuple[int, int, int]


class Ansi:
    """Colours of the drawing and the escape sequences that apply them.

    Attributes:
        RESET: Sequence that restores the terminal colours.
        WHITE: Background of the whole drawing.
        CHARCOAL: Wall colour, the first of the rotation.
        ORANGE: Wall colour.
        GREEN: Wall colour.
        BLUE: Wall colour, the last of the rotation.
        MAGENTA: Background of the entry.
        RED: Background of the exit.
        CYAN: Lines of the shortest path.
        GREY: Background of the "42".
    """

    RESET = "\x1b[0m"
    WHITE: Rgb = (255, 255, 255)
    CHARCOAL: Rgb = (31, 41, 55)
    ORANGE: Rgb = (194, 65, 12)
    GREEN: Rgb = (21, 128, 61)
    BLUE: Rgb = (29, 78, 216)
    MAGENTA: Rgb = (217, 70, 239)
    RED: Rgb = (239, 68, 68)
    CYAN: Rgb = (34, 211, 238)
    GREY: Rgb = (156, 163, 175)

    @staticmethod
    def colours(text: Rgb, background: Rgb) -> str:
        """SGR sequence that sets the text and the background colour.

        Args:
            text: Colour of the characters.
            background: Colour behind the characters.

        Returns:
            The escape sequence.
        """
        return "\x1b[38;2;{};{};{};48;2;{};{};{}m".format(*text, *background)
```

## Experimente

Uma parede grafite sobre branco e o interior da entrada, em magenta, lado a lado, com o reset no
fim. Na raiz do projeto:

```bash
.venv/bin/python - <<'EOF'
from amazeing.utils.ansi import Ansi

wall = Ansi.colours(Ansi.CHARCOAL, Ansi.WHITE) + "┃"
entry = Ansi.colours(Ansi.CHARCOAL, Ansi.MAGENTA) + "   "
print(repr(wall + entry + Ansi.RESET))
EOF
```

```text
'\x1b[38;2;31;41;55;48;2;255;255;255m┃\x1b[38;2;31;41;55;48;2;217;70;239m   \x1b[0m'
```

O `repr` mostra os caracteres invisíveis escritos por extenso. Troque `print(repr(...))` por
`print(wall + entry + Ansi.RESET)` para ver, no terminal, a parede e o bloco magenta.
