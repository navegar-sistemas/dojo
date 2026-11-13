---
slug: /
sidebar_position: 1
title: O que vamos construir
---

# O que vamos construir

O **A-Maze-ing** é um programa em Python que **gera labirintos**. O
programa lê algumas opções de um arquivo de texto, sorteia um labirinto, grava esse labirinto
num arquivo e o desenha colorido no terminal. Este tutorial constrói esse programa do zero,
explicando cada decisão.

O programa é chamado assim no terminal (`config.txt` é o arquivo com as opções):

```bash
python3 a_maze_ing.py config.txt
```

Um labirinto de 20 colunas por 15 linhas gerado pelo programa:

![Um labirinto 20 por 15 gerado pelo programa, com o caminho mais curto em ciano](/img/problema/labirinto-20x15-caminho.svg)

Na figura:
- o quadrado **magenta**, no canto de cima à esquerda, é a **entrada**;
- o **vermelho**, no canto de baixo à direita, é a **saída**;
- a linha **ciano** é o caminho mais curto entre as duas;
- os quadrados **cinza** no meio desenham o número **42**, que o labirinto precisa mostrar
  sempre que ele cabe (num labirinto pequeno demais, o programa gera sem ele e avisa).

## O enunciado

O projeto vem com um documento oficial que diz o que precisa ser entregue, o **subject**; o
tutorial o chama de **enunciado do projeto**. Este
tutorial não pressupõe que você o leu: a [próxima página](./02-o-enunciado-em-linguagem-simples.md)
resume tudo o que ele pede, em linguagem simples, e cada regra é explicada de novo na página que
a implementa.

## Duas peças

O programa tem duas partes separadas:

| Peça | O que é |
|---|---|
| `mazegen` | o **gerador**: o código que sorteia o labirinto. O enunciado exige que ele possa ser reaproveitado em outro projeto, instalado com `pip` (o instalador de bibliotecas do Python), por isso vira um pacote próprio |
| `amazeing` e `a_maze_ing.py` | a **aplicação**: lê o arquivo de opções, chama o gerador, grava o resultado, desenha e mostra um menu |

## Como o tutorial avança

O tutorial tem 16 partes, que constroem o programa de dentro para fora: primeiro as peças
pequenas do gerador, depois a aplicação que as usa.

| Parte | O que ela faz |
|---|---|
| 1. Entendendo o problema | explica, sem código, do que um labirinto é feito, os arquivos de entrada e de saída e as regras |
| 2. Arquitetura | mostra como o código é dividido em pastas e camadas, e por quê |
| 3. Ambiente | cria as ferramentas e os arquivos de configuração do projeto (`Makefile`, `pyproject.toml`, `config.txt`) |
| 4. Value objects do gerador | constrói as peças mais simples: o erro do gerador, os quatro lados de uma célula, a posição de uma célula e o desenho do "42" |
| 5. A entidade Maze | constrói a grade de paredes e as perguntas que se faz a ela |
| 6. Carver: o labirinto perfeito | o algoritmo que cava o labirinto |
| 7. Solver: o caminho mais curto | o algoritmo que acha o caminho mais curto da entrada à saída |
| 8. Braider: o tabuleiro Pac-Man | o algoritmo que transforma o labirinto num tabuleiro com rotas alternativas |
| 9. MazeGenerator e o pacote | a classe que junta o gerador, a documentação, a licença e o pacote instalável |
| 10. Utilitários da aplicação | os erros da aplicação, a conversão de texto em número, em `True`/`False` e em coordenada, e as cores do terminal |
| 11. Configuração | a leitura e a validação do arquivo de opções |
| 12. Geração e arquivo de saída | gerar o labirinto e gravá-lo no arquivo |
| 13. Estado da tela e desenho | o desenho colorido no terminal |
| 14. Menu e main | o menu, o programa principal e o tratamento de erros |
| 15. Fechamento | o `README.md`, o pacote reconstruído e a lista do que entregar |
| 16. Bônus | o tabuleiro sem nenhum beco sem saída |

Cada página explica o problema e o raciocínio antes do código e termina com o arquivo
completo, pronto para copiar. Os termos novos são explicados onde aparecem e reunidos no
[glossário](./05-glossario.md).
