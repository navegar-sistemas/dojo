# Módulos

Uma responsabilidade por arquivo, respeitando o teto de 5 funções (contando `static`) e 25
linhas por corpo. As contagens abaixo são as da implementação de referência, que compila com
`-Wall -Wextra -Werror` e cabe nos dois limites.

| Arquivo | Funções | Maior corpo | Responsabilidade |
|---|---|---|---|
| `main.c` | 4 | 22 | orquestração e liberação |
| `parse.c` | 5 | 24 | argv → `t_conf` + `t_stack` |
| `parse_utils.c` | 5 | 22 | token, conversão, duplicatas, split, flags |
| `stack.c` | 5 | 17 | criar, destruir e consultar pilha |
| `emit.c` | 2 | 23 | nome da operação e gravação |
| `prog.c` | 5 | 14 | programa gravado: criar, crescer, liberar, imprimir |
| `ops_swap.c` | 4 | 7 | `sa`, `sb`, `ss` |
| `ops_push.c` | 3 | 8 | `pa`, `pb` |
| `ops_rotate.c` | 4 | 7 | `ra`, `rb`, `rr` |
| `ops_rrotate.c` | 4 | 7 | `rra`, `rrb`, `rrr` |
| `utils.c` | 5 | 13 | raiz inteira, rotação até o topo, zerar contagens, erro |
| `disorder.c` | 1 | 23 | métrica de desordem |
| `rank.c` | 3 | 23 | conversão valor → rank |
| `sort_tiny.c` | 2 | 23 | caso base n ≤ 3 |
| `sort_simple.c` | 1 | 19 | O(n²) |
| `sort_medium.c` | 5 | 20 | O(n√n) |
| `sort_complex.c` | 3 | 19 | O(n log n) |
| `sort_greedy.c` | 4 | 14 | guloso por custo: fases e saída antecipada |
| `greedy_cost.c` | 5 | 19 | custo de movimento, desempate, alvos em A e B |
| `greedy_pick.c` | 4 | 15 | varredura podada do melhor candidato |
| `greedy_exec.c` | 5 | 14 | execução do `t_move` com fusão `rr`/`rrr`; variantes de bias |
| `portfolio.c` | 4 | 14 | simulação de candidatos e escolha do mais curto |
| `sort_adaptive.c` | 1 | 16 | despacho por desordem + certificação do regime |
| `bench.c` | 3 | 22 | bloco de métricas |

Bônus:

| Arquivo | Funções | Maior corpo | Responsabilidade |
|---|---|---|---|
| `checker_bonus.c` | 5 | 23 | orquestração e veredito |
| `read_ops_bonus.c` | 2 | 25 | leitura de stdin até EOF |
| `apply_op_bonus.c` | 3 | 15 | sigla → operação |

`read_all` fecha em exatamente 25 linhas — o limite, sem folga.

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

/* prog.c */
t_prog	*prog_new(void);
void	prog_free(t_prog *p);
void	prog_push(t_ctx *c, t_op op);
void	prog_flush(t_ctx *c);

/* portfolio.c */
void	run_portfolio(t_ctx *c, t_conf *conf, t_sortfn alt);

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
void	ps_die(t_ctx *c);

/* disorder.c */
double	compute_disorder(t_stack *a);

/* rank.c */
int		build_ranks(t_stack *a);

/* estratégias */
void	sort_tiny(t_ctx *c);
void	sort_simple(t_ctx *c, t_conf *conf);
void	sort_medium(t_ctx *c, t_conf *conf);
void	sort_complex(t_ctx *c, t_conf *conf);
void	sort_adaptive(t_ctx *c, t_conf *conf, double d);

/* sort_greedy.c, greedy_exec.c */
void	sort_greedy_run(t_ctx *c, t_conf *conf);
void	sort_greedy(t_ctx *c, t_conf *conf);
void	sort_greedy_alt(t_ctx *c, t_conf *conf);

/* greedy_cost.c */
int		move_cost(t_move m);
t_move	move_better(t_ctx *c, t_move x, t_move y);
t_move	pair_best(t_ctx *c, int ia, int ib);
int		target_in_b(t_stack *b, int value);
int		target_in_a(t_stack *a, int value);

/* greedy_pick.c */
t_move	best_push(t_ctx *c);
t_move	best_insert(t_ctx *c);

/* greedy_exec.c */
void	exec_move(t_ctx *c, t_move m);

/* bench.c */
void	bench_print(t_ctx *c, t_conf *conf, double d);

/* bônus */
char	*read_all(int fd);
int		apply_line(t_ctx *c, const char *s, int len);
int		apply_rot(t_ctx *c, const char *s, int len);
```

## Funções `static` por arquivo

Não são detalhe de implementação: são o que faz cada corpo caber em 25 linhas, e ocupam a cota
de 5 funções do arquivo.

| Arquivo | `static` | Papel |
|---|---|---|
| `main.c` | `setup`, `run_strategy`, `cleanup` | ver [fluxo.md](fluxo.md) |
| `parse.c` | `count_tokens`, `add_tokens`, `fill_all` | contagem, preenchimento por argumento, laço |
| `prog.c` | `prog_grow` | dobra o buffer; falha cai em `ps_die` |
| `ops_swap.c` | `swap_top` | troca os dois do topo de uma pilha |
| `ops_push.c` | `move_top` | move o topo de uma pilha para outra |
| `ops_rotate.c` | `rotate_up` | gira uma pilha para cima |
| `ops_rrotate.c` | `rotate_down` | gira uma pilha para baixo |
| `rank.c` | `insert_sort`, `rank_of` | ordenação auxiliar e busca binária |
| `sort_tiny.c` | `sort_three` | os 5 casos de 3 elementos |
| `sort_medium.c` | `count_in_range`, `collect_chunk`, `collect_all`, `drain_b` | fases 1 e 2 |
| `sort_complex.c` | `bit_count`, `radix_pass` | bits necessários e uma passada |
| `sort_greedy.c` | `is_circular_sorted`, `push_phase`, `insert_phase` | saída antecipada e as duas fases |
| `greedy_pick.c` | `cand_push`, `cand_insert` | candidato de um índice |
| `greedy_exec.c` | `rot_a`, `rot_b` | sobras de rotação após a fusão |
| `portfolio.c` | `stack_dup`, `simulate`, `take_if_shorter` | cópia, execução isolada, escolha |
| `bench.c` | `put_percent`, `put_counts` | percentual e as duas linhas de contagem |
| `checker_bonus.c` | `reject_flags`, `fail_ck`, `run_all`, `cleanup_ck` | rejeição de `--`, erro, laço de linhas, liberação |
| `read_ops_bonus.c` | `grow` | realocação do buffer de leitura |
| `apply_op_bonus.c` | `same` | comparação exata de `len` bytes |

Dois deslocamentos são imposição direta da cota de 5: `ps_die` mora em `utils.c` (não em
`main.c`, que já tem 4 funções, nem em `prog.c`, que fecharia em 6), e as variantes
`sort_greedy`/`sort_greedy_alt` moram em `greedy_exec.c` porque `sort_greedy.c` fechou a cota
com as fases.

## Contratos

**`stack_new`** devolve `NULL` se qualquer `malloc` falhar, sem vazar o que já alocou. Aceita
`cap == 0`, alocando no mínimo um inteiro — é o caso de uma linha de comando só com flags.

**`stack_free`** aceita `NULL` e retorna sem fazer nada. É o que permite ao caminho de erro
liberar tudo sem testar cada ponteiro. `prog_free` tem o mesmo contrato.

**`stack_is_sorted`** devolve 1 para tamanhos 0 e 1.

**`stack_min_index` / `stack_max_index`** devolvem o índice (0 = topo). Não são chamadas com
pilha vazia.

**`op_*`** aplicam o efeito e chamam `emit` exatamente uma vez. Movimento sem efeito possível
(`sa` com menos de 2 elementos, `pa` com `b` vazia) não altera nada mas **ainda é gravado**.

**`op_ss`, `op_rr`, `op_rrr`** aplicam o efeito nas duas pilhas chamando os helpers `static`
de mutação, nunca as operações simples: `op_rr` que chamasse `op_ra` e `op_rb` gravaria duas
operações.

**`emit`** grava a operação no programa (`prog_push`) e não imprime nada — imprimir é papel do
`prog_flush`, uma vez escolhido o programa final. Com `prog == NULL` (checker), retorna sem
fazer nada.

**`prog_push`** é amortizado O(1); o crescimento dobra a capacidade e morre em `ps_die` se o
`malloc` falhar.

**`prog_flush`** imprime o programa em stdout, uma sigla por linha, e incrementa
`counts[op]` na mesma passada quando `counts` não é `NULL` — stdout e métricas não têm como
divergir.

**`flag_id`** devolve `STRAT_SIMPLE`..`STRAT_ADAPTIVE` para os seletores, `FLAG_BENCH` para
`--bench`, e 0 para qualquer outro token. A comparação usa o comprimento do literal **mais um**
(`ft_strncmp(s, "--simple", 9)`) para que `--simpleX` não seja aceito como prefixo.

**`parse_flags`** devolve 0 em erro. Ignora tokens que não começam com `--`.

**`parse_numbers`** devolve `NULL` em qualquer erro, já tendo liberado tudo o que alocou,
inclusive o array do `ft_split` em curso. Devolve uma pilha de tamanho 0 quando não há nenhum
token numérico — que não é erro.

**`token_to_int`** devolve 0 se o valor não couber em `int`. A conversão acumula em `long` com
o sinal aplicado e testa os limites **a cada dígito**, não só no fim: um token de 30 dígitos
estouraria o próprio `long` antes de terminar.

**`build_ranks`** devolve 0 se o `malloc` interno falhar; nesse caso a pilha fica intacta. É
chamada pelo `main`, não pelas estratégias — ver [fluxo.md](fluxo.md).

**`rotate_a_to_top(c, i)`** leva ao topo de `a` o elemento no índice `i` pelo caminho mais
curto: `ra` × `i` se `i <= size / 2`, senão `rra` × `(size - i)`. O empate escolhe `ra`, e essa
escolha é observável — ver [../04-algoritmos/simple.md](../04-algoritmos/simple.md).
`rotate_b_to_top` faz o mesmo em `b` com `rb`/`rrb`.

**`ps_die`** escreve `Error\n` em stderr, percorre a cadeia `up` liberando `a`, `b` e `prog`
de cada contexto, e sai com 1.

**`sort_*`** gravam `conf->name` e `conf->cclass` antes de qualquer retorno antecipado, e
delegam para `sort_tiny` quando `a->size <= 3`. Não alocam por conta própria — a única
alocação durante uma estratégia é o crescimento do `prog`, que morre em `ps_die`.

**`sort_greedy_run`** grava `"Greedy"` / `"O(n²)"` (rótulos sempre sobrescritos pelo
adaptativo — o guloso não é selecionável por flag), retorna cedo se a pilha já está ordenada,
delega n ≤ 3 para `sort_tiny` e roda as duas fases com alinhamento final. Contratos internos em
[../04-algoritmos/greedy.md](../04-algoritmos/greedy.md).

**`best_push` / `best_insert`** varrem os candidatos do topo para fora e podam: um candidato a
`k` passos do topo custa pelo menos `k`, então a varredura para quando `k` alcança o custo do
melhor já visto. A poda nunca muda a resposta.

**`exec_move`** funde as partes de mesmo sinal em `rr`/`rrr` e executa as sobras — exatamente
a fusão que `move_cost` precificou.

**`run_portfolio`** descarta o `c->prog` corrente e o substitui pelo programa mais curto entre
os candidatos: os dois gulosos e o certificador com até `GREEDY_MAX_N` elementos, só o
certificador acima disso. `simulate` roda cada candidato em cópias privadas das pilhas, com
`counts = NULL` e `up` apontando para o contexto real; `take_if_shorter` compara com `<`
estrito.

**`sort_adaptive`** despacha pelo valor da desordem, chama `run_portfolio` com o certificador
do regime e grava `cclass` com a classe **do regime** — não a do candidato vencedor — e
`name = "Adaptive"`.

**`apply_line`** devolve 0 se os `len` bytes não formarem exatamente uma das 11 siglas.
Comprimento 0 (linha vazia) devolve 0. Trata as cinco siglas que não são rotação e delega o
resto com `return (apply_rot(c, s, len));` — despachar as 11 numa função só fecharia em
exatamente 25 linhas.

**`reject_flags`** (static de `checker_bonus.c`) roda antes de `parse_numbers`: qualquer
`argv` com prefixo `--` imprime `Error` e sai com 255. Sem ela, o `parse_numbers`
compartilhado pularia o token e `./checker --simple 3 2 1` responderia `KO` onde a referência
responde `Error`.

## Direção das dependências

```
main
 ├── parse ── parse_utils ── (libft)
 ├── stack
 ├── disorder   rank
 ├── run_strategy ── sort_simple ──────────────┐
 │        ├─────────  sort_medium ─────────────┼── sort_tiny ──┐
 │        ├─────────  sort_complex ────────────┘               │
 │        └─────────  sort_adaptive ── portfolio ── sort_greedy ── greedy_pick ── greedy_cost
 │                                        │              └── greedy_exec ──┘
 │                                        └── (simula qualquer t_sortfn)
 ├── bench
 └── ops_* ── emit ── prog ── utils (ps_die)
```

Nenhuma seta aponta para trás: `emit` não conhece estratégia, `stack` não conhece operação,
operação não conhece estratégia, e o portfólio enxerga as estratégias só através de
`t_sortfn`. O `checker` do bônus reaproveita a metade de baixo do grafo (`parse`,
`parse_utils`, `stack`, `ops_*`, `emit`, `prog`, `utils`) sem tocar em nada acima.
