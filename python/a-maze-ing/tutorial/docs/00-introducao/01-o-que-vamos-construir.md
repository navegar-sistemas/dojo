---
slug: /
sidebar_position: 1
title: O que vamos construir
---

# O que vamos construir

O **A-Maze-ing** é um projeto da escola 42: um programa em Python que **gera labirintos**. O
programa lê algumas opções de um arquivo de texto, sorteia um labirinto, grava esse labirinto
num arquivo e o desenha colorido no terminal.

```bash
python3 a_maze_ing.py config.txt
```

![Um labirinto 20 por 15 gerado pelo programa, com o caminho mais curto em ciano](/img/problema/labirinto-20x15-caminho.svg)

Na figura:
- o quadrado **magenta**, no canto de cima à esquerda, é a **entrada**;
- o **vermelho**, no canto de baixo à direita, é a **saída**;
- a linha **ciano** é o caminho mais curto entre as duas;
- os quadrados **cinza** no meio desenham o número **42**, que todo labirinto do projeto
  precisa mostrar.

## O enunciado

Cada projeto da 42 vem com um documento oficial que diz o que precisa ser entregue. A escola
chama esse documento de **subject**. Este tutorial não pressupõe que você o leu: a próxima
página resume tudo o que ele pede, em linguagem simples, e cada regra é explicada de novo na
página que a implementa.

## Duas peças

O programa tem duas partes separadas:

| Peça | O que é |
|---|---|
| `mazegen` | o **gerador**: o código que sorteia o labirinto. O enunciado exige que ele seja reaproveitável em outro projeto, instalado com `pip`, por isso vira um pacote próprio |
| `amazeing` e `a_maze_ing.py` | a **aplicação**: lê o arquivo de opções, chama o gerador, grava o resultado, desenha e mostra um menu |

## Como o tutorial avança

As partes constroem o programa de dentro para fora:

1. o problema e a arquitetura, ainda sem código;
2. o ambiente: as ferramentas e os arquivos de configuração do projeto;
3. o gerador `mazegen`, peça por peça: posições na grade, paredes, os algoritmos que cavam o
   labirinto e que acham o caminho mais curto;
4. a aplicação `amazeing`: ler as opções, gravar o arquivo, desenhar e o menu;
5. o fechamento: a documentação, o pacote e a entrega.

Cada página explica o problema e o raciocínio antes do código e termina com o arquivo
completo, pronto para copiar. Os termos novos são explicados onde aparecem e reunidos no
[glossário](./05-glossario.md).
