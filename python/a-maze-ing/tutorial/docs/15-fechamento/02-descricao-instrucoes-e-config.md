---
sidebar_position: 2
title: Descrição, instruções e config
---

# Descrição, instruções e config

As três primeiras seções respondem ao que qualquer leitor pergunta primeiro: o que é, como roda
e como se configura.

## Description

O objetivo em uma frase, depois a visão geral em tópicos curtos:

```markdown
A-Maze-ing generates a maze from a configuration file, writes it to an
output file in hexadecimal and shows it in the terminal.
```

Os tópicos cobrem cada peça visível do projeto, uma linha de **o que é** e, quando cabe, **a
regra** que a define:

- **Perfect mode** e **Pac-Man mode**, com a chave que liga cada um e qual é o padrão;
- **The "42"**: 18 células fechadas, o tamanho mínimo (9x7) e o aviso quando não cabe;
- **Output file**: um dígito hexadecimal por célula, a entrada, a saída e o caminho;
- **Display**: as cores e as quatro opções do menu;
- **Reusable module**: o pacote `mazegen` e os dois arquivos que o distribuem.

O avaliador usa essa lista como roteiro: cada item é algo que ele vai ver funcionando.

## Instructions

Tudo que alguém precisa para sair de um clone limpo e ver o labirinto:

- o requisito: Python 3.10 ou posterior e `make`;
- `make install` e `make run`, num bloco `sh`, com um comentário do que cada um faz;
- que `make run` é o mesmo que `python3 a_maze_ing.py config.txt`, com o Python do `.venv`;
- como rodar com outro arquivo: `.venv/bin/python a_maze_ing.py my_config.txt`;
- a tabela das opções do menu, de `1` a `4`;
- a tabela das outras regras do `Makefile`: `lint`, `lint-strict`, `debug`, `clean` e `build`.

O comando `python3 a_maze_ing.py config.txt` aparece escrito por extenso: é o que o subject
manda executar, e o avaliador procura por ele.

O README fala em `.venv/bin/python`, e não em `python3`, porque o `make install` cria o `.venv`
e todas as regras do `Makefile` usam o Python de lá. Quem roda `python3` do sistema pode estar
numa versão anterior à 3.10.

## Configuration file

O subject pede "a estrutura e o formato completos" do arquivo. Isso é mais do que listar as
chaves: inclui as regras de leitura que um usuário só descobriria errando.

- **Formato:** um `KEY=VALUE` por linha, comentários com `#`, linhas em branco ignoradas,
  coordenadas `x,y` com `x` coluna e `y` linha, origem no canto superior esquerdo.
- **Tabela das chaves:** `WIDTH`, `HEIGHT`, `ENTRY`, `EXIT`, `OUTPUT_FILE`, `PERFECT` (obrigatórias)
  e `SEED` (opcional), cada uma com o valor aceito.
- **Regras de leitura:** chaves e booleanos em qualquer caixa; espaços em volta ignorados;
  divisão no primeiro `=`; chave desconhecida ignorada; chave repetida vale a última; `#` depois
  de um valor faz parte dele; todas as chaves ausentes listadas num só erro; os limites de
  tamanho, entrada diferente da saída e fora do "42", e o mínimo de tamanho do Pac-Man.
- **O formato dos erros:** uma linha `Error: <causa>` em stderr e código 1.
- **O `config.txt` do repositório**, inteiro, num bloco `text`.

Cada regra dessa lista corresponde a uma decisão tomada na parte 11. O README é o lugar onde o
usuário as encontra sem ler o código.
