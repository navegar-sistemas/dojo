# T02 — Pilha

## Objetivo

Criar, destruir e consultar `t_stack`.

## Depende de

T01.

## Arquivos

- `stack.c`

## Especificação

- [../03-arquitetura/tipos.md](../03-arquitetura/tipos.md) — `t_stack` e seus invariantes
- [../03-arquitetura/modulos.md](../03-arquitetura/modulos.md) — contratos das cinco funções

## Implementação

```c
t_stack	*stack_new(int cap);
void	stack_free(t_stack *s);
int		stack_is_sorted(t_stack *s);
int		stack_min_index(t_stack *s);
int		stack_max_index(t_stack *s);
```

**`stack_new`** aloca a `struct` e o vetor `data` com `cap` inteiros, zera `size`, grava `cap`.
Se qualquer `malloc` falhar, libera o que já alocou e devolve `NULL`. `cap == 0` é chamada
válida — o `malloc` de zero bytes pode devolver `NULL` sem ser erro, então trate esse caso
explicitamente ou aloque no mínimo 1.

**`stack_free`** aceita `NULL` e retorna sem fazer nada. Libera `data` e depois a `struct`.
Sem essa tolerância, o caminho de erro do `main` precisaria testar cada ponteiro.

**`stack_is_sorted`** devolve 1 se `size <= 1`. Caso contrário percorre com `while` verificando
`data[i] < data[i + 1]` para todo `i`.

**`stack_min_index` / `stack_max_index`** devolvem o índice do menor/maior valor, com 0 sendo o
topo. Percorrem uma vez guardando índice e valor do extremo. Não são chamadas com pilha vazia.

Cinco funções: o arquivo está na cota exata, sem espaço para helper `static`.

## Pronto quando

Um `main` temporário exercita as cinco funções e imprime os resultados. Não faz parte da
entrega — apague ou substitua em T05.

```bash
make re
norminette *.c *.h
```

Casos que o teste temporário precisa cobrir:

| Chamada | Esperado |
|---|---|
| `stack_new(5)` | não-`NULL`, `size == 0`, `cap == 5` |
| `stack_free(NULL)` | não quebra |
| `stack_is_sorted` com `{}` e `{7}` | 1 |
| `stack_is_sorted` com `{1,2,3}` | 1 |
| `stack_is_sorted` com `{1,3,2}` | 0 |
| `stack_min_index` com `{5,4,3,2,1}` | 4 |
| `stack_max_index` com `{5,4,3,2,1}` | 0 |
| `stack_min_index` com `{7}` | 0 |

```bash
valgrind --leak-check=full ./push_swap    # "All heap blocks were freed"
```
