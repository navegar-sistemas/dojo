---
sidebar_position: 1
title: Por que separar em camadas
---

# Por que separar em camadas

O A-Maze-ing faz cinco trabalhos bem diferentes: lê o arquivo de opções, gera o labirinto, grava
o resultado num arquivo, desenha o labirinto no terminal e conversa com o usuário por um menu.
Esta página mostra por que esses trabalhos ficam em pedaços de código separados, e não todos
misturados num arquivo só.

## O problema do arquivo único

Dá para escrever o programa inteiro num `a_maze_ing.py` de 600 linhas. Funciona, mas cria três
problemas.

**O gerador não pode ser reaproveitado.** O enunciado exige que a geração do labirinto fique numa
classe que **outro projeto** consiga instalar com `pip` e usar (por exemplo, um jogo futuro que
só quer um labirinto pronto). Se o código que gera também lê o `config.txt` e chama `print`, o
jogo que o reutilizar vai precisar de um `config.txt` e vai ter a tela suja de mensagens que não
pediu.

**Uma mudança quebra o que não devia.** Com tudo no mesmo arquivo, o desenho e a geração usam as
mesmas variáveis. Trocar a cor das paredes pode, por descuido, mudar uma variável de que o
gerador depende.

**Fica difícil explicar.** Na avaliação, o avaliador pergunta "onde está a regra de que a borda
é sempre fechada?". Num arquivo de 600 linhas, a resposta vira uma caça ao tesouro.

## A ideia: um trabalho por classe

O código é separado por **responsabilidade**: cada classe cuida de um único trabalho e responde
a uma única pergunta. A coluna "Quem responde" traz as classes que o tutorial constrói, cada uma
na sua parte; a coluna "Camada" é a pasta onde cada uma mora, explicada logo abaixo:

| Pergunta | Quem responde | Camada |
|---|---|---|
| Como representar a posição `x,y` de uma célula? | `Cell` | `mazegen` |
| Como guardar as paredes e mexer nelas sem que duas vizinhas discordem? | `Maze` | `mazegen` |
| Como cavar os corredores de um labirinto perfeito? | `Carver` | `mazegen` |
| Como achar o caminho mais curto da entrada à saída? | `Solver` | `mazegen` |
| Como ler o `config.txt`? | `FileConfigRepository` | `repositories` |
| Como gravar o arquivo de saída? | `FileMazeRepository` | `repositories` |
| Como transformar o labirinto em linhas coloridas para o terminal? | `RenderService` | `services` |
| Como mostrar o menu e ler a escolha do usuário? | `Menu` | `ui` |
| Quem cria todas essas peças e as liga? | `a_maze_ing.py` | o arquivo `a_maze_ing.py`, sozinho |

## Camadas

Uma **camada** é um grupo de classes com o mesmo tipo de trabalho, guardadas numa mesma pasta.
Por exemplo, as duas classes que mexem em arquivos (`FileConfigRepository` e
`FileMazeRepository`) formam a camada `repositories`; as regras do labirinto (`Cell`, `Maze`...)
ficam no `mazegen`.

As camadas se organizam como anéis, do centro para a borda:

![As camadas como anéis, da borda para o centro: a_maze_ing.py, ui, services e repositories, use_cases, domain, utils e errors, e o mazegen no centro, com as suas subpastas](/img/arquitetura/camadas.svg)

O que cada nome quer dizer, da borda para o centro:

| Camada | O que guarda |
|---|---|
| `a_maze_ing.py` | o arquivo que se executa: cria as peças e liga umas às outras |
| `ui` | a interface com o usuário (*user interface*): o menu |
| `services` | o desenho do labirinto em texto colorido (`RenderService`) |
| `repositories` | a leitura do `config.txt` e a gravação do arquivo de saída |
| `use_cases` | a operação "gerar um labirinto e gravá-lo" (`GenerateMaze`) |
| `domain` | os dados do programa: as opções lidas, o labirinto pronto, o estado da tela |
| `utils` | funções de apoio, como converter o texto `"20"` no número 20 |
| `errors` | os tipos de erro da aplicação |
| `mazegen` | o gerador de labirintos inteiro |

As camadas de `ui` a `utils` são pastas do pacote da aplicação, o `amazeing` (apresentado na
[próxima página](./02-dois-pacotes.md)), e `errors` é um arquivo dele, o `amazeing/errors.py`; a camada `services`, por exemplo, é a pasta
`amazeing/services/`. O `mazegen` tem as suas próprias subpastas (`entities/`,
`value_objects/`, `services/`), todas no anel central: o `Carver` e o `Solver` moram em
`mazegen/services/`, que faz parte do gerador. A camada `services` do anel de fora é só a
`amazeing/services/`, a do `RenderService`.

- No **centro** ficam as regras: o que é uma célula, uma parede, um labirinto. Essas regras valem
  com ou sem terminal, com ou sem arquivo.
- Na **borda** fica o que fala com o mundo de fora: ler e gravar arquivos, imprimir, ler o
  teclado.

A regra que faz isso funcionar: o código de uma camada só **importa** (usa) código da própria
camada ou de anéis **mais para dentro**. Dentro do `mazegen`, por exemplo, o `Maze` importa a
`Cell`: os dois são do mesmo pacote. Duas camadas que dividem o mesmo anel, como `services` e `repositories`, são
camadas distintas que ficam à mesma distância do centro, e uma não importa a outra. O gerador, no
centro, não sabe que existe menu nem arquivo. Os anéis dão o limite máximo; a
[página da regra de dependência](./03-regra-de-dependencia.md) lista, camada por camada, o que
cada uma pode importar no projeto, com algumas proibições a mais.

Esse jeito de organizar tem nome: **Clean Architecture** ("arquitetura limpa"), um estilo
descrito pelo programador Robert C. Martin. A ideia central é a dos anéis: as regras no centro,
os detalhes (arquivos, telas) na borda, e o centro sem depender de nenhum detalhe.

## O que se ganha

- **Leitura**: para entender o desenho, abre-se só o `RenderService`; para entender a geração,
  só os arquivos do gerador.
- **Reuso**: o gerador vive num pacote próprio (o `mazegen`, explicado na
  [próxima página](./02-dois-pacotes.md)), que não sabe que existe configuração, terminal ou
  menu. Outro projeto o instala e usa sem levar nada disso junto.
- **Erros fáceis de achar**: só os `repositories` leem e gravam arquivos, e só a `ui` imprime
  na tela (além do `a_maze_ing.py`, que imprime a mensagem de erro final). Um `print` dentro do
  gerador está, por definição, no lugar errado.
- **Papéis conhecidos**: cada classe tem um papel (value object, entidade, service...,
  explicados na [página dos papéis](./04-papeis-das-classes.md)), e o papel já diz o que ela pode
  e o que não pode fazer.

## O preço

Mais arquivos, mais `import`, e algumas classes pequenas, de dez ou vinte linhas. Para um
projeto deste tamanho o preço é baixo, e a organização se paga na hora de explicar o código a um
avaliador ou de mudar uma parte sem medo de quebrar outra.
