---
sidebar_position: 8
title: Cores ANSI
---

# Cores ANSI

Com as sequências SGR da [página anterior](./08-sequencias-ansi.md), o programa consegue
pintar o fundo de um trecho do terminal. Falta decidir como desenhar cada posição do labirinto
e quais cores usar, e guardar tudo num lugar só. Esta página cria a classe `Ansi`
(`amazeing/utils/ansi.py`) com as cores que o desenho usa
([parte 13](../13-tela/02-a-grade-de-posicoes.md)).

## Por que só fundo, e por que dois espaços

O desenho usa **só a cor de fundo**. Cada posição do desenho são dois espaços com fundo
colorido: o espaço não tem traço nenhum, então o que aparece é um bloco da cor do fundo.

São **dois** espaços porque o lugar de um caractere no terminal tem mais ou menos o dobro de
altura que de largura. Com um espaço por posição, cada bloco seria um retângulo alto; com dois
lado a lado, vira quase um quadrado:

![Um xadrez de 5 por 3 desenhado com 1 espaço por posição (retângulos altos) e com 2 espaços (quadrados)](/img/utilitarios/um-ou-dois-espacos.svg)

Cores do terminal: cada retângulo é o fundo de uma posição; o claro e o escuro só alternam para o
xadrez aparecer.

A alternativa seria pintar o **texto** de um caractere cheio, como `█`. O enunciado pede
"renderização ASCII", e o `█` não está na tabela ASCII, a dos 128 caracteres básicos
([página anterior](./08-sequencias-ansi.md)); o espaço está. Usar só espaços cumpre o pedido ao
pé da letra e funciona em qualquer terminal. Essa leitura do enunciado é escolha do projeto.

## As constantes

![As nove cores de Ansi: nome, sequência e uso](/img/utilitarios/paleta-ansi.svg)

Cores do terminal, num terminal de tema escuro: cada quadrado mostra o fundo que a sequência
produz, com o nome da constante, a sequência e o uso no desenho. O `DEFAULT` aparece escuro só
porque, num tema escuro, o fundo padrão do terminal é escuro; num terminal de tema claro, ele
sairia claro. Ele não escolhe cor nenhuma, como explica a seção
[Por que o corredor tem cor](#por-que-o-corredor-tem-cor).

| Constante | Número | Uso no desenho |
|---|---|---|
| `DEFAULT` | `49` | corredor (a passagem entre paredes) |
| `WHITE`, `YELLOW`, `GREEN`, `BLUE` | `47`, `43`, `42`, `44` | paredes: o menu troca entre as quatro |
| `GREY` | `100` | células do "42" |
| `MAGENTA` | `45` | entrada |
| `RED` | `41` | saída |
| `CYAN` | `46` | caminho mais curto |

As cores e o que cada uma pinta são escolha do projeto. São as cores básicas, que todo terminal
entende. Existem sequências para 256 cores e para cores RGB, mas nem todo terminal as aceita, e
o labirinto não precisa de mais do que isso. As quatro cores de parede são diferentes das
outras, para uma parede nunca ser confundida com a entrada, a saída, o caminho ou o "42".

### Por que o corredor tem cor

O corredor poderia ficar sem sequência nenhuma. Só que a cor de fundo **continua valendo** até
outro comando: um corredor impresso logo depois de uma parede branca sairia branco também. O
`DEFAULT = 49` existe para que **toda** posição comece com a sua própria sequência. O `49` não
escolhe uma cor: devolve o fundo que o terminal já usa, escuro ou claro, conforme o tema de quem
roda o programa.

## `RESET` e `background`

```python
RESET = "\x1b[0m"
```

Toda linha do desenho termina com o reset. Sem ele, a última cor da linha (a parede da borda)
"vazaria" para o resto da linha, para o menu e até para o terminal depois que o programa
termina.

```python
@staticmethod
def background(code: int) -> str:
    return f"\x1b[{code}m"
```

`background(41)` devolve `"\x1b[41m"`: a f-string troca `{code}` pelo número. `@staticmethod`
quer dizer que o método não usa nenhum dado de um objeto e se chama direto pela classe:
`Ansi.background(Ansi.RED)`.

As cores ficam guardadas como **números**, e a sequência só é montada na hora de desenhar. Assim
a lista das cores de parede é uma tupla de números (`Ansi.WHITE`, `Ansi.YELLOW`...), fácil de
comparar e de percorrer, e o formato `ESC [ número m` fica escrito num lugar só.

Uma linha do desenho é uma sequência por posição, cada uma seguida de dois espaços, e o reset no
fim:

![Uma linha do desenho: cada posição é uma sequência SGR e dois espaços](/img/utilitarios/linha-sgr.svg)

Cores do terminal, num tema escuro: branco é a parede (`47`), magenta a entrada (`45`) e os
quadrados escuros são corredor (`49`, o fundo padrão). Embaixo de cada quadrado, o texto que o
programa imprime para ele; o `\x1b[0m` do fim é o reset.

## O arquivo completo

```python title="amazeing/utils/ansi.py"
"""ANSI background colours of the terminal drawing."""


class Ansi:
    """SGR background codes and the reset sequence.

    Attributes:
        RESET: Sequence that restores the terminal colours.
        DEFAULT: Default terminal background, used for corridors.
        WHITE: White background.
        YELLOW: Yellow background.
        GREEN: Green background.
        BLUE: Blue background.
        MAGENTA: Magenta background, the entry.
        RED: Red background, the exit.
        CYAN: Cyan background, the shortest path.
        GREY: Grey background, the "42".
    """

    RESET = "\x1b[0m"
    DEFAULT = 49
    WHITE = 47
    YELLOW = 43
    GREEN = 42
    BLUE = 44
    MAGENTA = 45
    RED = 41
    CYAN = 46
    GREY = 100

    @staticmethod
    def background(code: int) -> str:
        """SGR sequence that sets a background colour.

        Args:
            code: SGR background code.

        Returns:
            The escape sequence.
        """
        return f"\x1b[{code}m"
```

## Experimente

Uma parede branca e a entrada magenta, lado a lado, com o reset no fim. Na raiz do projeto:

```bash
.venv/bin/python - <<'EOF'
from amazeing.utils.ansi import Ansi

line = Ansi.background(Ansi.WHITE) + "  " + Ansi.background(Ansi.MAGENTA) + "  " + Ansi.RESET
print(repr(line))
EOF
```

```text
'\x1b[47m  \x1b[45m  \x1b[0m'
```

O `repr` mostra os caracteres invisíveis escritos por extenso. Troque `print(repr(line))` por
`print(line)` para ver, no terminal, um quadrado branco e um magenta.
