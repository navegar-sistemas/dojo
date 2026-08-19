#include "push_swap.h"

static void	swap_top(t_stack *s)
{
	int	tmp;

	if (s->size < 2)
		return ;
	tmp = s->data[0];
	s->data[0] = s->data[1];
	s->data[1] = tmp;
}

void	op_sa(t_ctx *c)
{
	swap_top(c->a);
	emit(c, OP_SA);
}

void	op_sb(t_ctx *c)
{
	swap_top(c->b);
	emit(c, OP_SB);
}

void	op_ss(t_ctx *c)
{
	swap_top(c->a);
	swap_top(c->b);
	emit(c, OP_SS);
}
