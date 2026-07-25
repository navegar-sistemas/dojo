# Módulos

Uma responsabilidade por arquivo, respeitando o teto de 5 funções (contando `static`) e 25
linhas por corpo.

| Arquivo | Funções | Responsabilidade |
|---|---|---|
| `main.c` | 3 | orquestração, caminhos de erro, liberação |
| `parse.c` | 4 | argv → `t_conf` + `t_stack` |
| `parse_utils.c` | 4 | validação de token, conversão, duplicatas, liberação do split |
| `stack.c` | 5 | criar, destruir e consultar pilha |
| `emit.c` | 2 | nome da operação e emissão |
| `ops_swap.c` | 4 | `sa`, `sb`, `ss` |
| `ops_push.c` | 3 | `pa`, `pb` |
| `ops_rotate.c` | 4 | `ra`, `rb`, `rr` |
| `ops_rrotate.c` | 4 | `rra`, `rrb`, `rrr` |
| `utils.c` | 3 | raiz inteira e rotação até o topo |
| `disorder.c` | 1 | métrica de desordem |
| `rank.c` | 3 | conversão valor → rank |
| `sort_tiny.c` | 2 | caso base n ≤ 3 |
| `sort_simple.c` | 1 | O(n²) |
| `sort_medium.c` | 4 | O(n√n) |
| `sort_complex.c` | 3 | O(n log n) |
| `sort_adaptive.c` | 1 | despacho por desordem |
| `bench.c` | 3 | bloco de métricas |

## Assinaturas públicas

```c
/* stack.c */
t_stack	*stack_new(int cap);
void	stack_free(t_stack *s);
int		stack_is_sorted(t_stack *s);
int		stack_min_index(t_stack *s);
int		stack_max_index(t_stack *s);

/* emit.c */
char	*op_name(t_op op);
void	emit(t_ctx *c, t_op op);

/* operações */
void	op_sa(t_ctx *c);
void	op_sb(t_ctx *c);
void	op_ss(t_ctx *c);
void	op_pa(t_ctx *c);
void	op_pb(t_ctx *c);
void	op_ra(t_ctx *c);
void	op_rb(t_ctx *c);
void	op_rr(t_ctx *c);
void	op_rra(t_ctx *c);
void	op_rrb(t_ctx *c);
void	op_rrr(t_ctx *c);

/* parse.c */
int		parse_flags(int argc, char **argv, t_conf *conf);
t_stack	*parse_numbers(int argc, char **argv);

/* parse_utils.c */
int		is_int_token(const char *s);
int		token_to_int(const char *s, int *out);
int		has_duplicates(t_stack *s);
void	free_split(char **parts);

/* utils.c */
int		isqrt(int n);
void	rotate_a_to_top(t_ctx *c, int i);
void	rotate_b_to_top(t_ctx *c, int i);

/* disorder.c */
double	compute_disorder(t_stack *a);

/* rank.c */
int		build_ranks(t_stack *a);

/* estratégias */
void	sort_tiny(t_ctx *c);
void	sort_simple(t_ctx *c, t_conf *conf);
void	sort_medium(t_ctx *c, t_conf *conf);
void	sort_complex(t_ctx *c, t_conf *conf);
void	sort_adaptive(t_ctx *c, t_conf *conf, double disorder);

/* bench.c */
void	bench_print(t_ctx *c, t_conf *conf, double disorder);
```

## Contratos

**`stack_new`** devolve `NULL` se qualquer `malloc` falhar, sem vazar o que já alocou.

**`stack_is_sorted`** devolve 1 para tamanhos 0 e 1.

**`stack_min_index` / `stack_max_index`** devolvem o índice (0 = topo). Não são chamadas com
pilha vazia; nenhum chamador precisa desse caso.

**`op_*`** aplicam o efeito e chamam `emit` exatamente uma vez. Movimento sem efeito possível
(`sa` com menos de 2 elementos, `pa` com `b` vazia) não altera nada mas **ainda é emitido** —
é o comportamento que o enunciado descreve e que o checker aceita.

**`op_ss`, `op_rr`, `op_rrr`** aplicam o efeito nas duas pilhas chamando os helpers `static` de
mutação, nunca as operações simples: `op_rr` que chamasse `op_ra` e `op_rb` emitiria duas
linhas em vez de uma.

**`parse_flags`** devolve 0 em erro. Ignora tokens que não começam com `--`. Deixa
`conf->strategy` em `STRAT_ADAPTIVE` quando nenhum seletor aparece.

**`parse_numbers`** devolve `NULL` em qualquer erro, já tendo liberado tudo o que alocou,
inclusive o array do `ft_split` em curso. Devolve uma pilha de tamanho 0 quando não há nenhum
token numérico — que não é erro.

**`token_to_int`** devolve 0 se o valor não couber em `int`. A conversão é feita em `long`.

**`build_ranks`** devolve 0 se o `malloc` interno falhar; nesse caso a pilha fica intacta.

**`rotate_a_to_top(c, i)`** leva ao topo de `a` o elemento no índice `i` pelo caminho mais
curto: `ra` × `i` se `i <= size / 2`, senão `rra` × `(size - i)`. O empate escolhe `ra`, e essa
escolha é observável — ver [../04-algoritmos/simple.md](../04-algoritmos/simple.md).
`rotate_b_to_top` faz o mesmo em `b` com `rb`/`rrb`.

**`sort_*`** gravam `conf->name` e `conf->cclass` antes de emitir qualquer movimento, e
delegam para `sort_tiny` quando `a->size <= 3`.

**`sort_adaptive`** não ordena: escolhe uma das outras três, chama, e sobrescreve
`conf->name` com `"Adaptive"` preservando o `cclass` gravado pela rota.

## Direção das dependências

```
main
 ├── parse ── parse_utils ── (libft)
 ├── stack
 ├── sort_adaptive ── sort_simple  ─┐
 │                    sort_medium  ─┼── sort_tiny ─┐
 │                    sort_complex ─┘              │
 │                         │                       │
 │                         ├── rank                │
 │                         └── utils               │
 ├── bench                                         │
 └── ops_* ── emit ─────────────────────────────────
```

Nenhuma seta aponta para trás: `emit` não conhece estratégia, `stack` não conhece operação,
operação não conhece estratégia. O `checker` do bônus reaproveita a metade de baixo do grafo
(`parse`, `stack`, `ops_*`, `emit`) sem tocar em nada acima.
