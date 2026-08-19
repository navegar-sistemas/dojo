#include "push_swap.h"

static void	ko(char *label, int ok)
{
	if (ok)
		return ;
	ft_putstr_fd("KO ", 2);
	ft_putendl_fd(label, 2);
}

static void	fill6(t_stack *s)
{
	s->data[0] = 2;
	s->data[1] = 1;
	s->data[2] = 3;
	s->data[3] = 6;
	s->data[4] = 5;
	s->data[5] = 8;
	s->size = 6;
}

static void	checks(t_ctx *c)
{
	int	i;

	i = -1;
	while (++i < 6)
		op_ra(c);
	ko("ra x6", c->a->data[0] == 2 && c->a->data[5] == 8);
	op_ra(c);
	op_rra(c);
	ko("ra+rra", c->a->data[0] == 2);
	op_rr(c);
	ko("rr", c->a->data[0] == 1 && c->prog->len == 9);
	op_pa(c);
	ko("pa vazia", c->a->size == 6 && c->b->size == 0);
	i = -1;
	while (++i < 5)
		op_pb(c);
	op_sa(c);
	ko("sa com 1", c->a->size == 1 && c->a->data[0] == 2);
	ko("grava sempre", c->prog->len == 16);
	prog_free(c->prog);
	c->prog = NULL;
	op_rb(c);
	ko("prog nulo", c->b->data[0] == 5);
}

static void	recipe(t_ctx *c)
{
	op_sa(c);
	op_pb(c);
	op_pb(c);
	op_pb(c);
	op_ra(c);
	op_rb(c);
	op_rra(c);
	op_rrb(c);
	op_sa(c);
	op_pa(c);
	op_pa(c);
	op_pa(c);
}

int	main(void)
{
	t_ctx	c;

	c.counts = NULL;
	c.bias = 0;
	c.up = NULL;
	c.a = stack_new(6);
	c.b = stack_new(6);
	c.prog = prog_new();
	if (c.a == NULL || c.b == NULL || c.prog == NULL)
		ps_die(&c);
	fill6(c.a);
	checks(&c);
	c.prog = prog_new();
	if (c.prog == NULL)
		ps_die(&c);
	c.b->size = 0;
	fill6(c.a);
	recipe(&c);
	prog_flush(&c);
	stack_free(c.a);
	stack_free(c.b);
	prog_free(c.prog);
	return (0);
}