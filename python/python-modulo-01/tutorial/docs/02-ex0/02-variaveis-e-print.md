---
sidebar_position: 2
title: Variáveis e print
---

# Variáveis e print

Os três dados da planta ficam em três variáveis, uma para cada informação:

```python
name: str = "Rose"
height: int = 25
age: int = 30
```

- `name` guarda um texto (`str`): o nome da planta;
- `height` guarda um inteiro (`int`): a altura em centímetros;
- `age` guarda um inteiro: a idade em dias.

O `: str` e o `: int` são **type hints** de variável
([Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md)). O enunciado só os
exige em funções e métodos, e o Python funcionaria sem eles aqui. Anotar estas três variáveis é
escolha do projeto: no exercício 0, guardar cada dado numa variável do tipo certo é o próprio
assunto. Do exercício 1 em diante, as variáveis do bloco main e dos experimentos ficam sem
anotação: o tipo já está no valor (`rose = Plant()` guarda uma `Plant`), e o mypy o deduz
sozinho.

Os nomes ficam em `snake_case` (minúsculas), a regra do enunciado para variáveis. Escrevê-los em
inglês, como o resto do código e a saída, é escolha do projeto.

## Imprimir

```python
print("=== Welcome to My Garden ===")
print(f"Plant: {name}")
print(f"Height: {height}cm")
print(f"Age: {age} days")
print()
print("=== End of Program ===")
```

- cada `print()` imprime uma linha;
- o `f` antes das aspas faz uma **f-string**: o que está entre `{}` é trocado pelo valor da
  variável, e `f"Height: {height}cm"` vira `Height: 25cm`. O `cm` vem colado ao `}`, sem espaço,
  porque a saída não tem espaço entre o número e a unidade;
- `print()` sem nada imprime a linha vazia antes do encerramento.
