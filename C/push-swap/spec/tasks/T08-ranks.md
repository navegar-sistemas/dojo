# T08 — Ranks

## Objetivo

`build_ranks` substituindo cada valor pela posição que ele ocuparia na lista ordenada.

## Depende de

T02.

## Arquivos

- `rank.c`

## Especificação

- [../04-algoritmos/ranks.md](../04-algoritmos/ranks.md)

## Implementação

```c
int	build_ranks(t_stack *a);
```

Três funções, duas `static`:

| Função | Papel |
|---|---|
| `insert_sort` (static) | ordena a cópia auxiliar |
| `rank_of` (static) | busca binária de um valor na cópia ordenada |
| `build_ranks` | aloca, ordena, mapeia, libera |

```
build_ranks(a):
    se a->size <= 0: devolve 1
    copia = malloc(a->size * sizeof(int))
    se copia == NULL: devolve 0
    copia recebe os valores de a->data
    insert_sort(copia, a->size)
    i = 0
    enquanto i < a->size:
        a->data[i] = rank_of(copia, a->size, a->data[i])
        i += 1
    free(copia)
    devolve 1
```

**`insert_sort`** com dois `while` aninhados. Para n = 500 são até 125 000 comparações em
memória, irrelevante em CPU e sem emitir movimento.

**`rank_of`** com busca binária. Funciona porque não há duplicatas — cada valor aparece uma vez
e o índice é único. Busca linear daria o mesmo resultado; a binária cabe no mesmo espaço.

**A escrita é in place**: `a->data[i]` é lido e sobrescrito na mesma iteração. Como o valor lido
é usado imediatamente na busca antes da escrita, não há corrupção.

**Retorno 0 só em falha de alocação**, e nesse caso a pilha fica intacta — o chamador ainda não
emitiu nenhum movimento, então pode encerrar por `Error` sem deixar meia receita.

## Pronto quando

```bash
make re
norminette *.c *.h
```

Teste temporário com casos que cobrem negativos, esparsos e extremos de `int`:

| Entrada | Ranks esperados |
|---|---|
| `4 67 3 87 23` | `1 3 0 4 2` |
| `-5 1000000 3` | `0 2 1` |
| `1 2 3` | `0 1 2` |
| `3 2 1` | `2 1 0` |
| `-2147483648 0 2147483647` | `0 1 2` |
| `42` | `0` |

Propriedades a verificar sobre entrada aleatória de 500 elementos:

- o conjunto de ranks resultante é exatamente `{0, 1, ..., 499}`, sem repetição e sem buraco;
- para todo par de posições, `valor[i] < valor[j]` se e somente se `rank[i] < rank[j]`.

```bash
leaks --atExit -- ./push_swap ...   # a cópia auxiliar precisa ser liberada
```
