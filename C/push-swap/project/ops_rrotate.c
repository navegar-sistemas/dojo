#include "push_swap.h"

static void	rotate_down(t_stack *s)
{
	int	tmp;

	if (s->size < 2)
		return ;
	tmp = s->data[s->size - 1];
	ft_memmove(s->data + 1, s->data, (s->size - 1) * sizeof(int));
	s->data[0] = tmp;
}

void	op_rra(t_ctx *c)
{
	rotate_down(c->a);
	emit(c, OP_RRA);
}

void	op_rrb(t_ctx *c)
{
	rotate_down(c->b);
	emit(c, OP_RRB);
}

void	op_rrr(t_ctx *c)
{
	rotate_down(c->a);
	rotate_down(c->b);
	emit(c, OP_RRR);
}
