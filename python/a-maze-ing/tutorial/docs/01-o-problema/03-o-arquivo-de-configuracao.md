---
sidebar_position: 3
title: O arquivo de configuração
---

# O arquivo de configuração

O programa não pergunta nada ao usuário antes de gerar: tudo o que ele precisa saber (o tamanho
do labirinto, onde ficam a entrada e a saída, onde gravar o resultado) vem de um arquivo de
texto, o **arquivo de configuração**, passado na linha de comando:

```bash
python3 a_maze_ing.py config.txt
```

O nome `config.txt` é só um exemplo: o programa aceita qualquer nome de arquivo.

## Formato

Uma opção por linha, no formato `CHAVE=valor`. Linhas que começam com `#` são comentários,
ignorados pelo programa. Este é o `config.txt` que acompanha o projeto:

```ini
# Width of the maze, in cells (1 to 100)
WIDTH=20
# Height of the maze, in cells (1 to 100)
HEIGHT=15
# Entry cell as x,y (x = column, y = row, both from 0)
ENTRY=0,0
# Exit cell as x,y
EXIT=19,14
# File that receives the maze in hexadecimal
OUTPUT_FILE=maze.txt
# True: perfect maze (single path); False: Pac-Man board (default)
PERFECT=False
# Uncomment to get the same maze on every run
# SEED=42
```

Os comentários estão em inglês porque todos os textos do projeto (código, mensagens, arquivos)
estão em inglês.

## As opções

| Chave | Obrigatória | Exemplo | O que define |
|---|---|---|---|
| `WIDTH` | sim | `20` | quantas colunas a grade tem |
| `HEIGHT` | sim | `15` | quantas linhas a grade tem |
| `ENTRY` | sim | `0,0` | a célula de entrada, no formato `x,y` |
| `EXIT` | sim | `19,14` | a célula de saída, no formato `x,y`; diferente da entrada |
| `OUTPUT_FILE` | sim | `maze.txt` | o nome do arquivo onde o labirinto é gravado |
| `PERFECT` | sim | `False` | o tipo de labirinto: `True` para perfeito, `False` para tabuleiro de Pac-Man |
| `SEED` | não | `42` | a semente do sorteio (explicada abaixo) |

As seis primeiras são exigidas pelo enunciado. `SEED` é uma opção que este projeto acrescenta,
o que o enunciado permite.

Lembrando o endereço de uma célula: em `x,y`, o `x` é a coluna (posição na horizontal) e o `y` é
a linha (posição na vertical), contando de 0 a partir do canto de cima à esquerda. Em 20x15, a
entrada `0,0` é o canto de cima à esquerda e a saída `19,14` é o canto de baixo à direita.

## A semente (`SEED`)

O labirinto é **sorteado**: cada execução gera um labirinto diferente. Mas o enunciado exige que
dê para **repetir** um labirinto, por exemplo para mostrar o mesmo resultado na avaliação.

O sorteio de um computador não é aleatório de verdade: ele sai de uma conta que parte de um
número inicial, a **semente**. Mesma semente, mesma sequência de sorteios, mesmo labirinto.

- Sem `SEED`, o programa usa uma semente diferente a cada execução.
- Com `SEED=42`, toda execução gera exatamente o mesmo labirinto.

## Limites de tamanho

O enunciado não fixa limites para `WIDTH` e `HEIGHT`, só manda recusar valores impossíveis,
como tamanho negativo. Este projeto aceita de **1 a 100**:

- o mínimo 1 vem da lógica: não existe labirinto com 0 colunas;
- o máximo 100 é uma **escolha do projeto**: uma grade 200x100 já leva mais de 10 segundos
  para ser gerada, e valores enormes estouram a memória. Com o limite, um `WIDTH=1000000` dá
  uma mensagem de erro em vez de travar o computador.

## Regras de leitura

O arquivo é escrito por pessoas, então a leitura perdoa o que é inofensivo e recusa o que é
ambíguo:

| Situação | O que acontece |
|---|---|
| espaços em volta (`WIDTH = 20`) | ignorados |
| chave em minúsculas (`width=20`) | aceita: `WIDTH` e `width` são a mesma chave |
| linha vazia ou comentário | pulada |
| chave repetida | vale a última |
| chave desconhecida (`COLOR=red`) | ignorada |
| linha sem `=` (`HEIGHT 15`) | erro, citando o número da linha |
| chave obrigatória faltando | erro, listando todas as que faltam |
| valor inválido (`WIDTH=abc`) | erro, citando a chave e o valor |

As regras de perdoar ou recusar são escolhas do projeto: o enunciado só exige que todo erro
vire uma mensagem clara.

## Erros

Quando algo está errado, o programa termina com **uma única linha** de mensagem, começando com
`Error: `:

```text
Error: config.txt: missing mandatory key(s): WIDTH, HEIGHT
Error: config.txt: WIDTH must be an integer, got 'abc'
Error: config.txt: ENTRY and EXIT must differ
```

Três detalhes dessa mensagem:

- ela sai em **stderr**, a saída de erros do programa, separada da saída normal (**stdout**).
  Num terminal as duas aparecem juntas, mas um script consegue separá-las;
- o programa termina com **código de saída 1**. Todo programa devolve um número ao terminar:
  0 quer dizer sucesso e qualquer outro valor quer dizer erro. Esse número aparece no terminal
  com `echo $?`;
- nunca aparece **traceback**, a listagem de linhas de código que o Python imprime quando uma
  exceção não é tratada. O enunciado exige que o programa nunca quebre assim.

A [parte 11](../11-configuracao/01-o-value-object-maze-config.md) implementa a leitura e as
mensagens.
