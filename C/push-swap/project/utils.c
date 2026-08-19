#include "push_swap.h"

void	zero_counts(int *counts)
{
	int	i;

	i = 0;
	while (i < 11)
	{
		counts[i] = 0;
		i++;
	}
}

void	ps_die(t_ctx *c)
{
	ft_putendl_fd("Error", 2);
	while (c != NULL)
	{
		stack_free(c->a);
		stack_free(c->b);
		prog_free(c->prog);
		c = c->up;
	}
	exit(1);
}