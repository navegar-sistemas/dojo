---
sidebar_position: 1
title: Por que separar em camadas
---

# Por que separar em camadas

## O problema do arquivo único

Dá para escrever o A-Maze-ing inteiro num `a_maze_ing.py` de 600 linhas: ler o config, gerar,
gravar, desenhar e ler o menu, tudo misturado. Funciona, mas:

- o gerador fica preso ao programa, e o subject exige que ele seja **reutilizável** num projeto
  futuro, instalado com `pip`;
- uma mudança no desenho pode quebrar a geração, porque tudo compartilha as mesmas variáveis;
- na avaliação, explicar "onde fica" cada regra vira caça ao tesouro.

## A ideia: cada coisa no seu lugar

Separar o código por **responsabilidade**. Cada arquivo responde a uma pergunta só:

| Pergunta | Quem responde |
|---|---|
| Como representar uma posição na grade? | `Cell` |
| Como guardar e mexer nas paredes sem quebrar a coerência? | `Maze` |
| Como cavar um labirinto perfeito? | `Carver` |
| Como achar o caminho mais curto? | `Solver` |
| Como ler o `config.txt`? | `FileConfigRepository` |
| Como gravar o arquivo de saída? | `FileMazeRepository` |
| Como transformar o labirinto em linhas coloridas? | `RenderService` |
| Como conversar com o usuário? | `Menu` |
| Quem liga tudo isso? | `a_maze_ing.py` |

## O que se ganha

- **Leitura**: para entender o desenho, abre-se só o `RenderService`.
- **Reuso**: o gerador vive num pacote próprio, sem saber que existe config, terminal ou menu.
- **Erros localizados**: só uma camada lê e grava arquivos; só uma imprime na tela. Se aparece
  um `print` no gerador, está no lugar errado.
- **Tipos claros**: cada classe tem um papel conhecido (próximas páginas), e o papel diz o que
  ela pode e o que não pode fazer.

## O preço

Mais arquivos, mais `import`s, e algumas classes pequenas. Para um projeto deste tamanho o
preço é baixo, e a organização paga a conta na hora de explicar o código a um avaliador.

A estrutura segue a ideia de **Clean Architecture**: o núcleo (as regras) no centro, e o que
fala com o mundo de fora (arquivos, terminal) na borda.
