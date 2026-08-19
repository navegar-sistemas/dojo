#ifndef PUSH_SWAP_H
# define PUSH_SWAP_H

# include "libft/libft.h"

# define STRAT_NONE 0
# define STRAT_SIMPLE 1
# define STRAT_MEDIUM 2
# define STRAT_COMPLEX 3
# define STRAT_ADAPTIVE 4
# define FLAG_BENCH 5
//# define GREEDY_MAX_N 1500

/*
** Pilha apoiada em um array fixo. data[0] é o TOPO, data[size - 1] é
** o fundo. cap é definido uma vez na criação e nunca muda: as duas
** pilhas juntas nunca guardam mais que os n elementos iniciais,
** então nenhuma realocação é necessária.
*/
typedef struct s_stack
{
	int	*data;
	int	size;
	int	cap;
}	t_stack;

/*
** As 11 operações do push_swap. A ordem dos membros importa: é a
** ordem das colunas do --bench, e op_name() indexa sua tabela com
** ela.
*/
typedef enum e_op
{
	OP_SA,
	OP_SB,
	OP_SS,
	OP_PA,
	OP_PB,
	OP_RA,
	OP_RB,
	OP_RR,
	OP_RRA,
	OP_RRB,
	OP_RRR
}	t_op;

/*
** Um fluxo de operações gravado. As operações são bufferizadas aqui
** em vez de impressas conforme são geradas, para que o --adaptive
** possa construir vários programas candidatos e imprimir apenas o
** mais curto.
*/
typedef struct s_prog
{
	t_op	*ops;
	int		len;
	int		cap;
}	t_prog;

/*
** Um par de rotações a executar antes de um push: contagens
** positivas significam rotações para frente (ra / rb), contagens
** negativas significam rotações reversas (rra / rrb). exec_move
** funde as partes de mesmo sinal em rr / rrr.
*/
typedef struct s_move
{
	int	a;
	int	b;
}	t_move;

/*
** Contexto de execução compartilhado por toda operação. prog
** seleciona o modo:
**   não-NULL -> gerador (push_swap): aplica e registra a operação;
**   NULL     -> executor (checker):    aplica apenas, em silêncio.
** counts é um int[11] indexado por t_op, preenchido por prog_flush
** para o --bench. bias escolhe a política de desempate do greedy. up
** encadeia uma simulação ao contexto que a originou, para que ps_die
** possa liberar toda alocação viva a partir de qualquer profundidade.
*/
typedef struct s_ctx
{
	t_stack			*a;
	t_stack			*b;
	int				*counts;
	int				bias;
	t_prog			*prog;
	struct s_ctx	*up;
}	t_ctx;

/*
** name e cclass são char *, não const char *: ft_putstr_fd recebe um
** char *, e descartar o qualificador é erro sob -Werror. Ambos são
** escritos pela estratégia que roda, para que o --adaptive possa
** reportar a classe da rota que de fato tomou.
*/
typedef struct s_conf
{
	int		strategy;
	int		bench;
	char	*name;
	char	*cclass;
}	t_conf;

//typedef void	(*t_sortfn)(t_ctx *c, t_conf *conf);

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

///* portfolio.c */
//void	run_portfolio(t_ctx *c, t_conf *conf, t_sortfn alt);

/* ops_swap.c */
void	op_sa(t_ctx *c);
void	op_sb(t_ctx *c);
void	op_ss(t_ctx *c);

/* ops_push.c */
void	op_pa(t_ctx *c);
void	op_pb(t_ctx *c);

/* ops_rotate.c */
void	op_ra(t_ctx *c);
void	op_rb(t_ctx *c);
void	op_rr(t_ctx *c);

/* ops_rrotate.c */
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

/* sort_tiny.c, sort_simple.c, sort_medium.c, sort_complex.c */
void	sort_tiny(t_ctx *c);
void	sort_simple(t_ctx *c, t_conf *conf);
void	sort_medium(t_ctx *c, t_conf *conf);
void	sort_complex(t_ctx *c, t_conf *conf);

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

void	exec_move(t_ctx *c, t_move m);

///* sort_adaptive.c */
//void	sort_adaptive(t_ctx *c, t_conf *conf, double d);

///* bench.c */
//void	bench_print(t_ctx *c, t_conf *conf, double d);

///* read_ops_bonus.c, apply_op_bonus.c */
//char	*read_all(int fd);
//int		apply_line(t_ctx *c, const char *s, int len);
//int		apply_rot(t_ctx *c, const char *s, int len);

#endif
