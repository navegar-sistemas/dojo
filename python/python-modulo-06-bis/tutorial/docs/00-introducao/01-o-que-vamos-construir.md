---
slug: /
sidebar_position: 1
title: O que vamos construir
---

# O que vamos construir

Um programa costuma receber dados de vários tipos: números, textos, registros de log. Cada tipo
pede um tratamento diferente, mas o resto do programa não quer saber de cada detalhe: quer
entregar um dado e receber o resultado. Duas ferramentas da programação orientada a objetos
resolvem isso:

- a **classe abstrata**, uma classe que serve só de molde: não gera objetos, lista os métodos que
  toda classe filha precisa escrever e pode já trazer pronto o que é igual para todas;
- o **polimorfismo**, que permite chamar o mesmo método em objetos de classes diferentes e
  deixar cada um responder do seu jeito.

Com essas duas peças prontas, aparecem perguntas de **arquitetura** (a organização das classes
de um programa): quem cria os objetos, como dar uma habilidade a só algumas classes de uma
família, e como trocar o jeito de agir de um objeto sem mexer no código que o usa. Cada pergunta
tem uma resposta conhecida, um **padrão de projeto**: uma solução de organização de classes com
nome, usada em muitos programas.

O projeto se chama **Code Nexus**. O tema é uma central de dados do ano de 2087, em Neo-Tokyo,
com uma arena onde criaturas sintéticas lutam para testar o sistema. O tema só dá nome às coisas;
o assunto de verdade é herança, classes abstratas, polimorfismo e três padrões de projeto.

## Cinco programas, em dois movimentos

O projeto tem cinco **exercícios**. Os três primeiros são a **fundação**: cada um é um arquivo
só, e cada um copia o código do anterior e acrescenta uma peça. Os dois últimos são a
**arquitetura**: cada um é um **pacote** (uma pasta de arquivos de código que funciona como uma
peça só) com scripts de teste ao lado.

| Exercício | Arquivos | O que constrói |
|---|---|---|
| 0 | `data_processor.py` | uma classe abstrata `DataProcessor` e três **processadores**, um para números, um para textos e um para logs, que guardam os dados recebidos e os devolvem um de cada vez |
| 1 | `data_stream.py` | uma classe `DataStream` que recebe uma lista com dados misturados e entrega cada um ao processador certo, sem saber de que classe ele é |
| 2 | `data_pipeline.py` | a saída do sistema: **plugins** que exportam os dados processados em CSV ou em JSON |
| 3 | pacote `ex3/`, `battle.py` e `capacitor.py` | criaturas de duas famílias, criadas por **fábricas**, e uma **capacidade** de transformação que só uma das famílias tem |
| 4 | pacote `ex4/` e `tournament.py` | **estratégias** de luta intercambiáveis e um torneio que põe as criaturas para lutar sem saber de que família cada uma é |

Um trecho da saída do exercício 4. Cada criatura entra no torneio com uma estratégia, e a
segunda recebeu uma estratégia que ela não consegue seguir:

```text
* Battle *
Shiftling is a Normal type Creature
 vs.
Flameling is a Fire type Creature
 now fight!
Shiftling shifts into a sharper form!
Shiftling performs a boosted strike!
Shiftling returns to normal.
Battle error, aborting tournament: Invalid Creature 'Flameling' for this aggressive strategy
```

O `Shiftling` se transformou, atacou e voltou ao normal; o `Flameling` não sabe se transformar, e
o torneio parou com uma mensagem de erro. As mensagens são em inglês porque o enunciado do projeto
mostra a saída de cada programa, e essa saída é em inglês.

## O enunciado

O projeto vem com um documento oficial que diz o que precisa ser entregue: o **enunciado** (em
inglês, *subject*). A [próxima página](./02-o-enunciado-em-linguagem-simples.md) resume tudo o
que ele pede.

## As partes

| Parte | Conteúdo |
|---|---|
| Ambiente | prepara o Python, a pasta do projeto e as duas ferramentas que conferem o código (flake8 e mypy) |
| Classes abstratas e polimorfismo | explica, com experimentos pequenos, sobrescrita de métodos, classes abstratas, os type hints `Any` e `int \| float`, polimorfismo e a fila que guarda os dados |
| Exercícios 0 a 2 | constroem os três programas da fundação, um por parte |
| Pacotes e herança múltipla | explica, com experimentos, o pacote com `__init__.py` e a classe com duas classes mães |
| Exercícios 3 e 4 | constroem as fábricas, a capacidade e as estratégias, um exercício por parte |
| Fechamento | confere tudo, mostra como entregar e responde às perguntas que o enunciado deixa para a avaliação |

Cada exercício termina com os arquivos completos. Os termos novos estão reunidos no
[glossário](./05-glossario.md).
