#include "push_swap.h"

static void	move_top(t_stack *from, t_stack *to)
{
	if (from->size == 0)
		return ;
	if (to->size > 0)
		ft_memmove(to->data + 1, to->data, to->size * sizeof(int));
	to->data[0] = from->data[0];
	to->size++;
	ft_memmove(from->data, from->data + 1, (from->size - 1) * sizeof(int));
	from->size--;
}

void	op_pa(t_ctx *c)
{
	move_top(c->b, c->a);
	emit(c, OP_PA);
}

void	op_pb(t_ctx *c)
{
	move_top(c->a, c->b);
	emit(c, OP_PB);
}
