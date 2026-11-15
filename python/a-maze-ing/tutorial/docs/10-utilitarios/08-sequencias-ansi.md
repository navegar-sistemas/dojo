---
sidebar_position: 7
title: Sequências ANSI
---

# Sequências ANSI

O enunciado exige mostrar o labirinto com as paredes, a entrada, a saída e o caminho bem
visíveis, e deixar o usuário trocar a cor das paredes. Este projeto desenha no terminal, com
linhas e fundos coloridos. Para isso, o programa precisa mandar o terminal mudar de cor no meio
do texto. Esta página mostra como; a [próxima](./04-cores-ansi.md) cria a classe `Ansi`, com as
cores que o desenho usa.

## Caracteres que são comandos

Tudo o que um programa imprime vai para o terminal como uma sequência de caracteres. Cada
caractere tem um número: a tabela **ASCII** é a tabela básica que numera 128 caracteres, de 0 a
127 (letras sem acento, dígitos, pontuação, o espaço e alguns caracteres de controle, que não
têm desenho). O `A`, por exemplo, é o 65.

A maioria dos caracteres aparece na tela, mas alguns são **comandos** para o próprio terminal. O
principal é o **ESC**: o mesmo caractere que a tecla Esc produz, de número 27 na tabela ASCII.
Ele não tem desenho; serve para avisar "o que vem a seguir é um comando, não texto".

Em Python, o ESC se escreve `"\x1b"`: dentro de uma string, `\x` seguido de dois dígitos
hexadecimais é o caractere daquele número. **Hexadecimal** é o jeito de escrever números com 16
algarismos: `0` a `9` e depois `a` (10) a `f` (15)
([parte 1](../01-o-problema/02-paredes-em-bits.md)). Com dois dígitos, o da esquerda vale 16
vezes o seu valor, como as dezenas valem 10 vezes no sistema decimal. Em `1b`, o `1` vale
1 × 16 = 16 e o `b` vale 11: 16 + 11 = 27.

Esses comandos se chamam **sequências ANSI**, porque foram padronizadas pelo ANSI, o instituto
de normas técnicas dos Estados Unidos. Hoje praticamente todo terminal as entende.

## O comando de cor: SGR

O comando que muda a cor se chama **SGR** (*Select Graphic Rendition*, "escolher a aparência").
Ele começa com o ESC e um `[`, termina com a letra `m` e leva no meio números separados por
`;`. Os números dizem **o que** muda e **para qual cor**.

Cada caractere que o terminal mostra tem duas cores:

- a **cor do texto**: a do traço do caractere, como as linhas de uma letra `A`;
- a **cor do fundo**: a do retângulo atrás do caractere. Um espaço não tem traço nenhum, então
  só o fundo dele aparece.

### Cores de 24 bits

Uma tela mistura três luzes em cada ponto: vermelho, verde e azul. Uma cor **RGB** (de *red*,
*green*, *blue*) é a quantidade de cada uma, de 0 (apagada) a 255 (no máximo): `255, 255, 255`
é branco, `0, 0, 0` é preto, `239, 68, 68` é um vermelho. Cada quantidade cabe em 8 bits
(255 é o maior número de 8 bits), e as três juntas ocupam 24: por isso se fala em **cor de 24
bits**. São 256 × 256 × 256, mais de 16 milhões de cores.

O SGR escolhe uma cor RGB com cinco números:

| Números | Muda | Exemplo |
|---|---|---|
| `38;2;R;G;B` | a cor do texto | `38;2;31;41;55`: texto grafite |
| `48;2;R;G;B` | a cor do fundo | `48;2;255;255;255`: fundo branco |
| `0` | volta tudo ao padrão do terminal (o *reset*) | |

O `38` quer dizer "cor do texto", o `48` "cor do fundo", e o `2` que vem logo depois avisa que
os três números seguintes são R, G e B.

Um único comando pode mudar as duas cores de uma vez: basta pôr os dois grupos de números em
sequência, separados por mais um `;`. É assim que este projeto escreve toda cor, com o texto e
o fundo juntos:

![As peças da sequência de texto grafite e fundo branco: ESC, colchete, 38;2;31;41;55, ponto e vírgula, 48;2;255;255;255 e a letra m; à direita, o texto Ab em grafite sobre branco](/img/utilitarios/sequencia-sgr.svg)

As caixas amarelas são as peças, na ordem em que são impressas; à direita, o texto `Ab` como o
terminal passa a mostrá-lo, em grafite sobre branco. No desenho do labirinto, o mesmo grafite
pinta as paredes, feitas com os caracteres da [página 9](./09-caracteres-de-caixa.md). O terminal
não mostra nenhum caractere da sequência. A partir dela, tudo o que for impresso sai com essas
duas cores, até o próximo comando de cor.

### As cores com nome

O SGR também tem números curtos para oito cores com nome: `31` é "texto vermelho", `41` é
"fundo vermelho", e assim por diante. Esses números não fixam o tom: cada terminal tem um
**tema**, a sua tabela de cores, e um mesmo `41` sai num vermelho diferente em cada tema.

As cores de 24 bits saem iguais em qualquer terminal que as aceita. Usar só elas é escolha do
projeto: o desenho tem fundo branco e paredes escuras mesmo num terminal de tema escuro. Em
troca, o programa precisa de um terminal com cores de 24 bits, e o
[README](../15-fechamento/02-descricao-instrucoes-e-config.md) avisa isso nos requisitos.
