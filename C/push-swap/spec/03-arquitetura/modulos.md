# Módulos

Uma responsabilidade por arquivo, respeitando o teto de 5 funções (contando `static`) e 25
linhas por corpo. As contagens abaixo são as de uma implementação desta spec que compila com
`-Wall -Wextra -Werror` e cabe nos dois limites — não há folga onde está escrito 5.

| Arquivo | Funções | Maior corpo | Responsabilidade |
|---|---|---|---|
| `main.c` | 5 | 18 | orquestração, erro, liberação |
| `parse.c` | 5 | 24 | argv → `t_conf` + `t_stack` |
| `parse_utils.c` | 5 | 22 | token, conversão, duplicatas, split, flags |
| `stack.c` | 5 | 16 | criar, destruir e consultar pilha |
| `emit.c` | 2 | 23 | nome da operação e emissão |
| `ops_swap.c` | 4 | 7 | `sa`, `sb`, `ss` |
| `ops_push.c` | 3 | 7 | `pa`, `pb` |
| `ops_rotate.c` | 4 | 7 | `ra`, `rb`, `rr` |
| `ops_rrotate.c` | 4 | 7 | `rra`, `rrb`, `rrr` |
| `utils.c` | 4 | 13 | raiz inteira, rotação até o topo, zerar contagens |
| `disorder.c` | 1 | 23 | métrica de desordem |
| `rank.c` | 3 | 23 | conversão valor → rank |
| `sort_tiny.c` | 2 | 21 | caso base n ≤ 3 |
| `sort_simple.c` | 1 | 19 | O(n²) |
| `sort_medium.c` | 5 | 18 | O(n√n) |
| `sort_complex.c` | 3 | 19 | O(n log n) |
| `sort_adaptive.c` | 1 | 7 | despacho por desordem |
| `bench.c` | 3 | 20 | bloco de métricas |

Bônus:

| Arquivo | Funções | Maior corpo | Responsabilidade |
|---|---|---|---|
| `checker_bonus.c` | 4 | 23 | orquestração e veredito |
| `read_ops_bonus.c` | 2 | 22 | leitura de stdin até EOF |
| `apply_op_bonus.c` | 3 | 24 | sigla → operação |

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
int		flag_id(const char *s);

/* utils.c */
int		isqrt(int n);
void	rotate_a_to_top(t_ctx *c, int i);
void	rotate_b_to_top(t_ctx *c, int i);
void	zero_counts(int *counts);

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

/* bônus */
char	*read_all(int fd);
int		apply_line(t_ctx *c, const char *s, int len);
void	apply_rot(t_ctx *c, t_op op);
```

## Funções `static` por arquivo

Não são detalhe de implementação: são o que faz cada corpo caber em 25 linhas, e ocupam a cota
de 5 funções do arquivo.

| Arquivo | `static` | Papel |
|---|---|---|
| `main.c` | `fail`, `setup`, `run_strategy`, `cleanup` | ver [fluxo.md](fluxo.md) |
| `parse.c` | `count_tokens`, `add_tokens`, `fill_all` | contagem, preenchimento por argumento, laço |
| `stack.c` | — | as 5 públicas ocupam a cota |
| `ops_swap.c` | `swap_top` | troca os dois do topo de uma pilha |
| `ops_push.c` | `move_top` | move o topo de uma pilha para outra |
| `ops_rotate.c` | `rotate_up` | gira uma pilha para cima |
| `ops_rrotate.c` | `rotate_down` | gira uma pilha para baixo |
| `rank.c` | `insert_sort`, `rank_of` | ordenação auxiliar e busca binária |
| `sort_tiny.c` | `sort_three` | os 5 casos de 3 elementos |
| `sort_medium.c` | `count_in_range`, `collect_chunk`, `collect_all`, `drain_b` | fases 1 e 2 |
| `sort_complex.c` | `bit_count`, `radix_pass` | bits necessários e uma passada |
| `bench.c` | `put_percent`, `put_counts` | percentual e as duas linhas de contagem |
| `checker_bonus.c` | `fail_ck`, `run_all`, `cleanup_ck` | erro, laço de linhas, liberação |
| `read_ops_bonus.c` | `grow` | realocação do buffer de leitura |
| `apply_op_bonus.c` | `same` | comparação exata de `len` bytes |

## Contratos

**`stack_new`** devolve `NULL` se qualquer `malloc` falhar, sem vazar o que já alocou. Aceita
`cap == 0`, alocando no mínimo um inteiro — é o caso de uma linha de comando só com flags.

**`stack_free`** aceita `NULL` e retorna sem fazer nada. É o que permite ao caminho de erro
liberar tudo sem testar cada ponteiro.

**`stack_is_sorted`** devolve 1 para tamanhos 0 e 1.

**`stack_min_index` / `stack_max_index`** devolvem o índice (0 = topo). Não são chamadas com
pilha vazia.

**`op_*`** aplicam o efeito e chamam `emit` exatamente uma vez. Movimento sem efeito possível
(`sa` com menos de 2 elementos, `pa` com `b` vazia) não altera nada mas **ainda é emitido**.

**`op_ss`, `op_rr`, `op_rrr`** aplicam o efeito nas duas pilhas chamando os helpers `static` de
mutação, nunca as operações simples: `op_rr` que chamasse `op_ra` e `op_rb` emitiria duas
linhas.

**`flag_id`** devolve `STRAT_SIMPLE`..`STRAT_ADAPTIVE` para os seletores, `FLAG_BENCH` para
`--bench`, e 0 para qualquer outro token. A comparação usa o comprimento do literal **mais um**
(`ft_strncmp(s, "--simple", 9)`) para que `--simpleX` não seja aceito como prefixo.

**`parse_flags`** devolve 0 em erro. Ignora tokens que não começam com `--`.

**`parse_numbers`** devolve `NULL` em qualquer erro, já tendo liberado tudo o que alocou,
inclusive o array do `ft_split` em curso. Devolve uma pilha de tamanho 0 quando não há nenhum
token numérico — que não é erro.

**`token_to_int`** devolve 0 se o valor não couber em `int`. A conversão acumula em `long` e
testa os limites **a cada dígito**, não só no fim: um token de 30 dígitos estouraria o próprio
`long` antes de terminar.

**`build_ranks`** devolve 0 se o `malloc` interno falhar; nesse caso a pilha fica intacta. É
chamada pelo `main`, não pelas estratégias — ver [fluxo.md](fluxo.md).

**`rotate_a_to_top(c, i)`** leva ao topo de `a` o elemento no índice `i` pelo caminho mais
curto: `ra` × `i` se `i <= size / 2`, senão `rra` × `(size - i)`. O empate escolhe `ra`, e essa
escolha é observável — ver [../04-algoritmos/simple.md](../04-algoritmos/simple.md).
`rotate_b_to_top` faz o mesmo em `b` com `rb`/`rrb`.

**`sort_*`** gravam `conf->name` e `conf->cclass` **antes** de qualquer retorno antecipado, e
delegam para `sort_tiny` quando `a->size <= 3`. Nunca alocam.

**`sort_adaptive`** não ordena: escolhe uma das outras três, chama, e sobrescreve `conf->name`
com `"Adaptive"` preservando o `cclass` gravado pela rota.

**`apply_line`** devolve 0 se os `len` bytes não formarem exatamente uma das 11 siglas.
Comprimento 0 (linha vazia) devolve 0.

## Direção das dependências

```
main
 ├── parse ── parse_utils ── (libft)
 ├── stack
 ├── rank
 ├── sort_adaptive ── sort_simple  ─┐
 │                    sort_medium  ─┼── sort_tiny ─┐
 │                    sort_complex ─┘              │
 │                         └── utils               │
 ├── bench                                         │
 └── ops_* ── emit ─────────────────────────────────
```

Nenhuma seta aponta para trás: `emit` não conhece estratégia, `stack` não conhece operação,
operação não conhece estratégia. O `checker` do bônus reaproveita a metade de baixo do grafo
(`parse`, `parse_utils`, `stack`, `ops_*`, `emit`) sem tocar em nada acima.
