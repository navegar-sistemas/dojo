
#include "push_swap.h"

static void	rotate_up(t_stack *s)
{
	int	tmp;

	if (s->size < 2)
		return ;
	tmp = s->data[0];
	ft_memmove(s->data, s->data + 1, (s->size - 1) * sizeof(int));
	s->data[s->size - 1] = tmp;
}

void	op_ra(t_ctx *c)
{
	rotate_up(c->a);
	emit(c, OP_RA);
}

void	op_rb(t_ctx *c)
{
	rotate_up(c->b);
	emit(c, OP_RB);
}

void	op_rr(t_ctx *c)
{
	rotate_up(c->a);
	rotate_up(c->b);
	emit(c, OP_RR);
}