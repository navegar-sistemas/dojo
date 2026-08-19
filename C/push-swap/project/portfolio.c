#include "push_swap.h"

static t_stack	*stack_dup(t_stack *src)
{
	t_stack	*copy;

	copy = stack_new(src->cap);
	if (copy == NULL)
		return (NULL);
	ft_memcpy(copy->data, src->data, sizeof(int) * src->size);
	copy->size = src->size;
	return (copy);
}

/*
** Roda uma estratégia sobre cópias privadas das pilhas e retorna o
** programa que ela gerou. O contexto de simulação é encadeado ao seu
** pai através de up, para que uma falha de alocação em qualquer nível
** abaixo libere a árvore inteira antes de sair.
*/
static t_prog	*simulate(t_ctx *c, t_conf *conf, t_sortfn fn)
{
	t_ctx	sim;

	sim.counts = NULL;
	sim.bias = 0;
	sim.up = c;
	sim.a = stack_dup(c->a);
	sim.b = stack_dup(c->b);
	sim.prog = prog_new();
	if (sim.a == NULL || sim.b == NULL || sim.prog == NULL)
		ps_die(&sim);
	fn(&sim, conf);
	stack_free(sim.a);
	stack_free(sim.b);
	return (sim.prog);
}

static void	take_if_shorter(t_ctx *c, t_prog *cand)
{
	if (cand->len < c->prog->len)
	{
		prog_free(c->prog);
		c->prog = cand;
	}
	else
		prog_free(cand);
}

/*
** O portfólio no coração do --adaptive: gera as duas variantes do
** greedy e o programa certificador do regime a partir da mesma
** entrada, mantém o mais curto. A saída nunca pode superar o
** certificador, então o limite de complexidade de cada regime se
** sustenta não importa como o greedy se comporte; em entradas
** aleatórias um greedy vence quase sempre. Além de GREEDY_MAX_N
** elementos as varreduras de candidatos do greedy pesam na CPU
** enquanto os benchmarks param em 500, então o certificador roda
** sozinho.
*/
void	run_portfolio(t_ctx *c, t_conf *conf, t_sortfn alt)
{
	prog_free(c->prog);
	c->prog = NULL;
	if (c->a->size <= GREEDY_MAX_N)
	{
		c->prog = simulate(c, conf, sort_greedy);
		take_if_shorter(c, simulate(c, conf, sort_greedy_alt));
		take_if_shorter(c, simulate(c, conf, alt));
	}
	else
		c->prog = simulate(c, conf, alt);
}
