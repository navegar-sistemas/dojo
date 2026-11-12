---
sidebar_position: 5
title: Glossário
---

# Glossário

Os termos que o tutorial usa, cada um com uma explicação curta e a página onde ele é explicado
em detalhe.

## O labirinto

| Termo | Significado |
|---|---|
| **grade** | o retângulo de células que forma o labirinto, com `WIDTH` colunas e `HEIGHT` linhas. [Veja](../01-o-problema/01-a-grade-e-as-celulas.md) |
| **célula** | um quadradinho da grade. [Veja](../01-o-problema/01-a-grade-e-as-celulas.md) |
| **lado** | cada uma das quatro bordas de uma célula: **Norte** (em cima), **Leste** (à direita), **Sul** (embaixo) e **Oeste** (à esquerda). [Veja](../01-o-problema/01-a-grade-e-as-celulas.md) |
| **parede** | um lado fechado: não dá para passar por ali. [Veja](../01-o-problema/01-a-grade-e-as-celulas.md) |
| **passagem** | um lado aberto entre duas células vizinhas: dá para andar de uma para a outra. [Veja](../01-o-problema/01-a-grade-e-as-celulas.md) |
| **coordenada `x,y`** | o endereço de uma célula: `x` é a posição na horizontal (a coluna) e `y` na vertical (a linha), contando de 0 a partir do canto de cima à esquerda. [Veja](../01-o-problema/01-a-grade-e-as-celulas.md) |
| **entrada e saída** | duas células escolhidas no arquivo de opções; o caminho mais curto vai de uma à outra. [Veja](../01-o-problema/03-o-arquivo-de-configuracao.md) |
| **coerência** | a regra de que duas células vizinhas concordam sobre a parede que dividem. [Veja](../01-o-problema/01-a-grade-e-as-celulas.md) |
| **o "42"** | o número 42 desenhado no meio do labirinto por células com as quatro paredes fechadas. [Veja](../01-o-problema/06-o-padrao-42.md) |
| **beco sem saída** | uma célula com uma única abertura: quem entra só sai por onde entrou. [Veja](../08-braider/01-becos-sem-saida.md) |
| **beco cercado** | um beco cujas paredes fechadas dão só para a borda ou para o "42", e que por isso não dá para abrir; não conta como beco real. [Veja](../08-braider/01-becos-sem-saida.md) |
| **ciclo** | um jeito de andar em círculo e voltar à mesma célula por outro caminho. [Veja](../01-o-problema/05-perfeito-e-pac-man.md) |
| **labirinto perfeito** | labirinto sem nenhum ciclo: entre duas células existe exatamente um caminho. [Veja](../01-o-problema/05-perfeito-e-pac-man.md) |
| **árvore geradora** | o nome, em teoria dos grafos, de um conjunto de ligações que conecta tudo sem formar ciclo; é a forma de um labirinto perfeito. [Veja](../06-carver/01-labirinto-perfeito.md) |
| **tabuleiro Pac-Man** | labirinto com ciclos e quase sem becos, onde quem foge sempre tem outra rota. [Veja](../01-o-problema/05-perfeito-e-pac-man.md) |
| **braiding** | ("trançar") transformar um labirinto perfeito num tabuleiro Pac-Man, abrindo paredes dos becos e criando ciclos. [Veja](../08-braider/02-abrir-os-becos.md) |
| **área aberta 3x3** | um bloco de 3x3 células sem nenhuma parede por dentro; proibido pelo enunciado. [Veja](../08-braider/04-a-regra-do-3x3.md) |
| **caminho mais curto** | a menor sequência de passos da entrada à saída, escrita com as letras `N`, `E`, `S`, `W`. [Veja](../07-solver/01-busca-em-largura.md) |

## Números e sorteio

| Termo | Significado |
|---|---|
| **bit** | um dígito binário, 0 ou 1. Cada lado de uma célula ocupa um bit: 1 = parede, 0 = passagem. [Veja](../01-o-problema/02-paredes-em-bits.md) |
| **binário** | o jeito de escrever números só com 0 e 1; cada casa, da direita para a esquerda, vale o dobro da anterior (1, 2, 4, 8). [Veja](../01-o-problema/02-paredes-em-bits.md) |
| **hexadecimal** | o jeito de escrever números de 0 a 15 com um só caractere: `0` a `9` e depois `a` (10) a `f` (15). [Veja](../01-o-problema/02-paredes-em-bits.md) |
| **semente (seed)** | um número que fixa o sorteio: com a mesma semente, o programa gera sempre o mesmo labirinto. [Veja](../06-carver/04-a-seed.md) |
| **BFS** | busca em largura: o algoritmo que acha o caminho mais curto explorando primeiro as células mais próximas. [Veja](../07-solver/01-busca-em-largura.md) |
| **backtracker** | o algoritmo que cava o labirinto perfeito: anda sorteando caminhos e volta atrás quando fica sem saída. [Veja](../06-carver/02-recursive-backtracker.md) |

## Python e ferramentas

| Termo | Significado |
|---|---|
| **ambiente virtual (venv)** | uma pasta `.venv` com um Python e bibliotecas só deste projeto, separados do resto do computador. [Veja](../03-ambiente/01-o-ambiente-virtual.md) |
| **Makefile** | arquivo com atalhos de comandos: `make install`, `make run`, `make lint`... [Veja](../03-ambiente/02-makefile-instalar-e-rodar.md) |
| **flake8** | ferramenta que confere o estilo do código (PEP 8). [Veja](../03-ambiente/05-flake8-e-gitignore.md) |
| **mypy** | ferramenta que confere as anotações de tipo do código. [Veja](../03-ambiente/04-pyproject.md) |
| **docstring** | o texto entre `"""` logo no começo de um módulo, classe ou função, que documenta o que ele faz. [Veja](../03-ambiente/07-pacotes-do-mazegen.md) |
| **pacote** | uma pasta com `__init__.py`, que o Python importa como um módulo. [Veja](../03-ambiente/07-pacotes-do-mazegen.md) |
| **wheel (`.whl`) e sdist (`.tar.gz`)** | os dois formatos de arquivo em que um pacote Python é distribuído e instalado com `pip`. [Veja](../09-gerador/08-o-pacote.md) |
| **traceback** | a listagem de erro que o Python imprime quando uma exceção não é tratada; o programa nunca deve mostrá-la ao usuário. [Veja](../14-menu-e-main/05-a-barreira-de-erros.md) |
| **stdout e stderr** | as duas saídas de texto de um programa: a normal e a de erros. [Veja](../14-menu-e-main/05-a-barreira-de-erros.md) |
| **código de saída** | o número que o programa devolve ao terminar: 0 é sucesso, outro valor é erro. [Veja](../14-menu-e-main/05-a-barreira-de-erros.md) |
| **ANSI** | as sequências de caracteres especiais que mandam o terminal mudar de cor. [Veja](../10-utilitarios/04-cores-ansi.md) |

## Arquitetura

| Termo | Significado |
|---|---|
| **camada** | um grupo de classes com o mesmo papel; uma camada só usa as camadas mais internas. [Veja](../02-arquitetura/01-por-que-camadas.md) |
| **value object** | um objeto que é só um valor: não muda depois de criado e é comparado pelo conteúdo (ex.: uma coordenada). [Veja](../02-arquitetura/04-papeis-das-classes.md) |
| **entidade** | um objeto cujo estado muda, mas que protege as próprias regras (ex.: a grade de paredes). [Veja](../02-arquitetura/04-papeis-das-classes.md) |
| **service** | uma classe que só executa uma operação, sem guardar estado (ex.: o algoritmo que cava). [Veja](../02-arquitetura/04-papeis-das-classes.md) |
| **use case** | uma operação completa da aplicação, num único método `execute`. [Veja](../02-arquitetura/04-papeis-das-classes.md) |
| **porta (port)** | a descrição do que uma classe precisa de outra (os métodos e os tipos), sem dizer quem vai fornecer. [Veja](../12-geracao-e-saida/03-a-porta-maze-repository.md) |
| **repository** | a classe que lê ou grava arquivos; a única camada que mexe em disco. [Veja](../02-arquitetura/04-papeis-das-classes.md) |
| **composition root** | o ponto do programa que cria todas as peças e as liga; aqui, o `a_maze_ing.py`. [Veja](../14-menu-e-main/04-o-composition-root.md) |
