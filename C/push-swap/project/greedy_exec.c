#include "push_swap.h"

static void	rot_a(t_ctx *c, int n)
{
	while (n > 0)
	{
		op_ra(c);
		n--;
	}
	while (n < 0)
	{
		op_rra(c);
		n++;
	}
}

static void	rot_b(t_ctx *c, int n)
{
	while (n > 0)
	{
		op_rb(c);
		n--;
	}
	while (n < 0)
	{
		op_rrb(c);
		n++;
	}
}

/*
** Executa o par de rotações, fundindo primeiro as partes de mesma
** direção em rr / rrr: a fusão é exatamente o que move_cost
** precificou com um max() em vez de uma soma.
*/
void	exec_move(t_ctx *c, t_move m)
{
	while (m.a > 0 && m.b > 0)
	{
		op_rr(c);
		m.a--;
		m.b--;
	}
	while (m.a < 0 && m.b < 0)
	{
		op_rrr(c);
		m.a++;
		m.b++;
	}
	rot_a(c, m.a);
	rot_b(c, m.b);
}

void	sort_greedy(t_ctx *c, t_conf *conf)
{
	c->bias = 0;
	sort_greedy_run(c, conf);
}

/*
** Mesmo greedy, política de desempate oposta. Sua trajetória se
** descorrelaciona da de sort_greedy após o primeiro empate, então o
** mínimo do portfólio corta a cauda da distribuição de contagem de
** operações.
*/
void	sort_greedy_alt(t_ctx *c, t_conf *conf)
{
	c->bias = 1;
	sort_greedy_run(c, conf);
}
