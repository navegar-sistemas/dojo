---
sidebar_position: 4
title: Cores ANSI
---

# Cores ANSI

O desenho do labirinto (parte 13) pinta cada posição com uma cor de fundo. A classe `Ansi`
(`amazeing/utils/ansi.py`) guarda os códigos dessas cores e monta a sequência que o terminal
entende.

## O que é uma sequência SGR

Um terminal não recebe só texto: alguns bytes especiais são comandos. O principal é o **ESC**,
caractere de código 27, escrito em Python como `"\x1b"`. Quando o terminal lê `ESC [`, ele entende
que vem um comando, e não texto para mostrar.

O comando de cor se chama **SGR** (*Select Graphic Rendition*) e tem a forma:

```text
ESC [ <número> m
```

Em Python: `"\x1b[41m"`. O terminal não mostra nada desses 5 caracteres; a partir deles, tudo o
que for escrito sai com fundo vermelho.

## Fundo × texto

Os números dizem **o quê** muda:

| Faixa | Muda | Exemplo |
|---|---|---|
| `30` a `37` | cor do texto | `31` texto vermelho |
| `40` a `47` | cor do fundo | `41` fundo vermelho |
| `100` a `107` | cor do fundo, versão clara | `100` fundo cinza |
| `49` | volta o fundo à cor padrão do terminal | |
| `0` | volta tudo ao padrão (o *reset*) | |

O desenho usa **só fundo**. Cada posição são dois espaços com fundo colorido: o espaço não tem
traço nenhum, então o que aparece é um bloco da cor do fundo. Dois espaços porque um caractere de
terminal é mais alto do que largo, e dois lado a lado formam um quadrado.

A alternativa, pintar o **texto** de um caractere cheio como `█`, exigiria um caractere fora do
ASCII, que nem todo terminal mostra igual. Espaços com fundo funcionam em qualquer terminal.

## As constantes

![As nove cores de Ansi: nome, sequência e uso](/img/utilitarios/paleta-ansi.svg)

| Constante | Código | Uso no desenho |
|---|---|---|
| `DEFAULT` | `49` | corredor |
| `WHITE`, `YELLOW`, `GREEN`, `BLUE` | `47`, `43`, `42`, `44` | paredes (a opção 3 do menu troca entre elas) |
| `GREY` | `100` | células do "42" |
| `MAGENTA` | `45` | entrada |
| `RED` | `41` | saída |
| `CYAN` | `46` | caminho mais curto |

São as 8 cores básicas (mais o cinza claro), que todo terminal entende. Há sequências para 256
cores e para cores RGB, mas nem todo terminal as aceita, e o labirinto não precisa de mais do que
isso.

### Por que o corredor tem cor

O corredor poderia ficar sem sequência nenhuma. O `DEFAULT = 49` existe para que **toda** posição
comece com a sua própria sequência: o corredor depois de uma parede branca precisa desligar o
fundo branco, senão herda a cor anterior. O `49` não escolhe uma cor: devolve o fundo que o
terminal já usa, escuro ou claro, conforme o tema de quem roda o programa.

## `RESET` e `background`

```python
RESET = "\x1b[0m"
```

Toda linha do desenho termina com o reset. Sem ele, a última cor da linha (a parede da borda)
"vazaria" para o resto da linha, para o menu e até para o prompt do shell depois que o programa
termina.

```python
@staticmethod
def background(code: int) -> str:
    return f"\x1b[{code}m"
```

As cores ficam guardadas como **números**, e a string só é montada na hora de desenhar. Assim a
paleta das paredes da parte 13 é uma tupla de inteiros (`Ansi.WHITE`, `Ansi.YELLOW`...), fácil de
comparar e de percorrer, e a sintaxe `ESC [ n m` fica escrita num lugar só.

Uma linha do desenho é uma sequência por posição, cada uma seguida de dois espaços, e o reset no
fim:

![Uma linha do desenho: cada posição é uma sequência SGR e dois espaços](/img/utilitarios/linha-sgr.svg)

## Experimente

```bash
.venv/bin/python -c '
from amazeing.utils.ansi import Ansi

line = Ansi.background(Ansi.WHITE) + "  " + Ansi.background(Ansi.MAGENTA) + "  " + Ansi.RESET
print(repr(line))
'
```

```text
'\x1b[47m  \x1b[45m  \x1b[0m'
```

Troque `print(repr(line))` por `print(line)` para ver, no terminal, um quadrado branco e um
magenta.

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
