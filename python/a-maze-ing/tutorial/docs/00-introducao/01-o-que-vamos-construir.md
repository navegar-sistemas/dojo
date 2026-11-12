---
slug: /
sidebar_position: 1
title: O que vamos construir
---

# O que vamos construir

O **A-Maze-ing** é um programa em Python que lê um arquivo de configuração, gera um labirinto
aleatório, grava esse labirinto num arquivo de texto e o desenha colorido no terminal.

```bash
python3 a_maze_ing.py config.txt
```

Ao rodar, o programa:

1. lê o `config.txt` (tamanho, entrada, saída, nome do arquivo de saída, tipo de labirinto);
2. gera o labirinto, com um **"42"** desenhado no meio por células fechadas;
3. grava o labirinto em hexadecimal no arquivo de saída;
4. desenha o labirinto no terminal e abre um menu para gerar outro, mostrar o caminho mais curto,
   trocar a cor das paredes ou sair.

## Duas peças

O projeto tem duas partes bem separadas:

| Peça | O que é |
|---|---|
| `mazegen` | o **gerador**: uma biblioteca reutilizável, empacotada como `mazegen-1.0.0-py3-none-any.whl`, que qualquer outro projeto pode instalar com `pip` |
| `amazeing` + `a_maze_ing.py` | a **aplicação**: lê o config, chama o gerador, grava o arquivo, desenha e mostra o menu |

O subject pede essa separação: a geração do labirinto tem de ser uma classe única, dentro de um
módulo independente, pronta para ser reaproveitada num projeto futuro.

## Como o tutorial avança

Cada parte constrói uma camada, de dentro para fora:

1. o problema e a arquitetura, sem código;
2. o ambiente: `Makefile`, `pyproject.toml`, lint;
3. o gerador `mazegen`, peça por peça: coordenadas, grade, algoritmos de geração e solução;
4. a aplicação `amazeing`: configuração, arquivo de saída, desenho e menu;
5. o fechamento: `README.md`, pacote e entrega.

Toda página explica o raciocínio antes do código e termina com o arquivo completo, pronto para
copiar.
