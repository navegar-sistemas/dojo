---
sidebar_position: 1
title: O problema
---

# O problema

Antes das classes, o primeiro exercício trata da estrutura de qualquer programa Python: **onde a
execução começa**. O programa é pequeno: guarda os dados de uma planta e os imprime.

## O que o enunciado pede

Um arquivo `ex0/ft_garden_intro.py`, que só pode chamar a função pronta `print()`, e que:

- roda quando chamado diretamente, com `python3 ft_garden_intro.py` de dentro da pasta `ex0`
  (ou `python3 ex0/ft_garden_intro.py` a partir da pasta do projeto);
- usa o bloco especial `if __name__ == "__main__":`;
- guarda o **nome**, a **altura** e a **idade** da planta em três variáveis simples;
- imprime esses dados com `print()`, imitando a saída abaixo.

O enunciado avisa que, neste exercício, a saída não será conferida letra por letra.

## A saída esperada

```text
=== Welcome to My Garden ===
Plant: Rose
Height: 25cm
Age: 30 days

=== End of Program ===
```

A saída tem um título, uma linha para cada dado da planta, uma **linha vazia** e uma linha de
encerramento. A altura vem em centímetros (`cm`, colado ao número) e a idade em dias.

## As duas perguntas da avaliação

O enunciado deixa duas tarefas para a avaliação:

- explicar **por que** a linha `if __name__ == "__main__":` é importante, o que leva ao conceito de
  *import* ([O ponto de partida](./03-o-ponto-de-partida.md));
- pesquisar o que faz a linha especial que começa com `#!`, chamada **shebang**, porque quem
  avalia vai pedir que você a acrescente ao programa, ao vivo
  ([O shebang](./06-o-shebang.md)).
