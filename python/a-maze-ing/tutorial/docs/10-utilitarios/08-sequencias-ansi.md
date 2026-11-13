---
sidebar_position: 7
title: Sequências ANSI
---

# Sequências ANSI

O enunciado exige mostrar o labirinto com as paredes, a entrada, a saída e o caminho bem
visíveis, e deixar o usuário trocar a cor das paredes. Este projeto desenha no terminal, com
quadradinhos coloridos. Para isso, o programa precisa mandar o terminal mudar de cor no meio do
texto. Esta página mostra como; a [próxima](./04-cores-ansi.md) cria a classe `Ansi`, com as
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
Neste projeto, ele tem sempre quatro peças: o ESC, um `[`, um número e a letra `m`. (O comando
aceita mais de um número, separados por `;`, para mudar várias coisas de uma vez; o desenho
nunca precisa disso.)

![As quatro peças da sequência de fundo vermelho: ESC avisa que vem um comando, o colchete abre o comando, 41 é o número do fundo vermelho e a letra m fecha](/img/utilitarios/sequencia-sgr.svg)

As caixas amarelas são as quatro peças, na ordem em que são impressas; o quadrado vermelho, à
direita, é a cor de fundo que o terminal passa a usar. O terminal não mostra nenhum desses
caracteres. A partir deles, tudo o que for impresso sai com fundo vermelho, até outro comando de
cor.

O número diz **o que** muda:

| Número | Muda | Exemplo |
|---|---|---|
| `30` a `37` | a cor do texto | `31`: texto vermelho |
| `40` a `47` | a cor do fundo | `41`: fundo vermelho |
| `100` a `107` | a cor do fundo, versão clara | `100`: fundo cinza |
| `49` | volta o fundo à cor padrão do terminal | |
| `0` | volta tudo ao padrão (o *reset*) | |
