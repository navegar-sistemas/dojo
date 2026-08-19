# T09 — Ranks

## Objetivo

`build_ranks` substituindo cada valor pela posição que ele ocuparia na lista ordenada.

## Depende de

T02. O `main` passa a chamá-la em T06 ou depois — ver
[../03-arquitetura/fluxo.md](../03-arquitetura/fluxo.md).

## Arquivos

- `rank.c`
- `main.c` (inserir `if (!build_ranks(c.a)) ps_die(&c);` — a linha marcada como ausente em T06)

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
e o índice é único.

**A escrita é in place**: `a->data[i]` é lido e sobrescrito na mesma iteração. Como o valor lido
é usado imediatamente na busca antes da escrita, não há corrupção.

**Retorno 0 só em falha de alocação**, e nesse caso a pilha fica intacta.

**Quem chama é o `main`**, entre `compute_disorder` e o despacho, para as quatro estratégias.
Dentro de uma `sort_*` não funcionaria: elas devolvem `void` e não têm como sinalizar a falha.
No `main` a falha cai no mesmo `ps_die` dos outros erros, e nada foi impresso ainda.

## Pronto quando

```bash
make re
norminette *.c *.h
```

Sonda temporária em `main.c`: depois de `build_ranks` os ranks estão em `a->data`, então basta
despejá-los no stderr. A sonda é a quinta função do arquivo (a cota é exatamente 5) mais uma
chamada no `main`. **Apague depois de conferir.**

```c
static void	probe_ranks(t_stack *a)
{
	int	i;

	i = -1;
	while (++i < a->size)
	{
		ft_putnbr_fd(a->data[i], 2);
		ft_putchar_fd(' ', 2);
	}
	ft_putchar_fd('\n', 2);
}
```

e no `main`, logo depois do `if (!build_ranks(c.a)) ps_die(&c);`:

```c
	probe_ranks(c.a);
```

Casos que cobrem negativos, esparsos e extremos de `int`:

| Entrada | Ranks esperados |
|---|---|
| `4 67 3 87 23` | `1 3 0 4 2` |
| `-5 1000000 3` | `0 2 1` |
| `1 2 3` | `0 1 2` |
| `3 2 1` | `2 1 0` |
| `-2147483648 0 2147483647` | `0 1 2` |
| `42` | `0` |

```bash
for arg in "4 67 3 87 23" "-5 1000000 3" "1 2 3" "3 2 1" "-2147483648 0 2147483647" "42"; do
  printf '%-28s -> %s\n' "$arg" "$(./push_swap $arg 2>&1 >/dev/null)"
done
```

Propriedades a verificar sobre entrada aleatória de 500 elementos:

- o conjunto de ranks resultante é exatamente `{0, 1, ..., 499}`, sem repetição e sem buraco;
- para todo par de posições, `valor[i] < valor[j]` se e somente se `rank[i] < rank[j]`.

As duas de uma vez — ordenando os pares (valor, rank) por valor, os ranks têm que sair
`0, 1, ..., 499` em sequência:

```bash
ARG=$(shuf -i 1-100000 -n 500 | tr '\n' ' ')
paste <(echo $ARG | tr ' ' '\n' | grep -v '^$') \
      <(./push_swap $ARG 2>&1 >/dev/null | tr ' ' '\n' | grep -v '^$') \
  | sort -n | awk '$2 != NR - 1 {bad = 1} END {if (bad) print "FALHOU"; else print "ranks ok"}'
```

```bash
valgrind --leak-check=full ./push_swap --simple $(shuf -i 1-10000 -n 50 | tr '\n' ' ')
```
