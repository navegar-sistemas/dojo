---
sidebar_position: 3
title: Índices e fatias
---

# Índices e fatias

O programa precisa pegar o nome do programa, que está na primeira posição de `sys.argv`, e os
argumentos, que estão em todas as outras. Uma lista dá acesso a um elemento pela **posição**, e a
um pedaço dela pela **fatia**.

```python title="experimentos/indices.py"
words = ["ft_command_quest.py", "hello", "world", "42"]
print(words[0])
print(words[1])
print(words[-1])
print(words[1:])
print(words[1:3])
print(words[4:])
try:
    print(words[4])
except IndexError as error:
    print(f"IndexError: {error}")
```

```bash
python3 experimentos/indices.py
```

```text
ft_command_quest.py
hello
42
['hello', 'world', '42']
['hello', 'world']
[]
IndexError: list index out of range
```

## Índices

A posição de um elemento se chama **índice** e começa em **0**: numa lista de quatro elementos,
os índices vão de 0 a 3. `words[0]` é o primeiro elemento, `words[1]` o segundo.

Um índice negativo conta do fim: `words[-1]` é o último, `words[-2]` o penúltimo.

Um índice que não existe lança `IndexError` ("erro de índice"), com a mensagem
`list index out of range` ("índice da lista fora do intervalo"). `words` não tem posição 4.

## Fatias

Uma **fatia** (*slice*) é uma lista nova com um pedaço da original. `words[a:b]` pega do índice
`a` até **antes** do índice `b`:

| Fatia | Pega os índices | Resultado |
|---|---|---|
| `words[1:3]` | 1 e 2 | `['hello', 'world']` |
| `words[1:]` | do 1 até o fim | `['hello', 'world', '42']` |
| `words[:2]` | do começo até o 1 | `['ft_command_quest.py', 'hello']` |
| `words[4:]` | do 4 até o fim; não há nenhum | `[]` |

Sem o número da esquerda, a fatia começa no início; sem o da direita, vai até o fim. Uma fatia
nunca lança erro: além do fim da lista, ela só fica vazia. `[]` é a **lista vazia**.

Para o exercício, `sys.argv[0]` é o nome do programa e `sys.argv[1:]` é a lista só com os
argumentos. Sem argumentos, `sys.argv[1:]` é `[]`, e `len(sys.argv[1:])` é 0.
