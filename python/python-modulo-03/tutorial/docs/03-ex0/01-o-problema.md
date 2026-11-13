---
sidebar_position: 1
title: O problema
---

# O problema

Um programa precisa receber instruções de quem o roda. O jeito mais simples é escrevê-las na
mesma linha do comando, depois do nome do programa:

```bash
python3 ft_command_quest.py hello world 42
```

`hello`, `world` e `42` são os **argumentos** desse comando. O primeiro programa do projeto
mostra o que recebeu: o próprio nome, quantos argumentos vieram e cada um deles.

## O que o enunciado pede

Um arquivo `ex0/ft_command_quest.py` que só pode usar `import sys`, `sys.argv`, `len()` e
`print()`. Ele imprime:

- um título, `=== Command Quest ===`;
- o nome do programa;
- se não veio nenhum argumento, a frase `No arguments provided!`; se vieram, quantos foram e
  cada um, numerado a partir de 1;
- o total de itens recebidos, contando o nome do programa.

## A saída esperada

Rodado sem argumentos, com três, e com um argumento entre aspas:

```text
=== Command Quest ===
Program name: ft_command_quest.py
No arguments provided!
Total arguments: 1
```

```text
=== Command Quest ===
Program name: ft_command_quest.py
Arguments received: 3
Argument 1: hello
Argument 2: world
Argument 3: 42
Total arguments: 4
```

```text
=== Command Quest ===
Program name: ft_command_quest.py
Arguments received: 1
Argument 1: Data Quest
Total arguments: 2
```

Os números contam coisas diferentes: `Arguments received` conta só os argumentos, e
`Total arguments` conta também o nome do programa, por isso é sempre um a mais: o Python entrega
tudo numa lista só, com o nome do programa na primeira posição
([A linha de comando](./02-a-linha-de-comando.md)).

![A lista sys.argv do comando com hello world 42: quatro caixas numeradas de 0 a 3, com ft_command_quest.py na posição 0 e hello, world e 42 nas posições 1 a 3. As posições 1 a 3 são os argumentos; as quatro juntas são o total](/img/ex0/argv.svg)
