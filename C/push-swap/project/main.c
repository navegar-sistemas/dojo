#include "push_swap.h"

int	main(void)
{
	t_ctx	c;
	int		counts[11];

	c.a = NULL;
	c.b = NULL;
	c.bias = 0;
	c.up = NULL;
	c.counts = counts;
	zero_counts(counts);
	c.prog = prog_new();
	if (!c.prog)
		return (1);
	emit(&c, OP_SA);
	emit(&c, OP_PB);
	emit(&c, OP_PB);
	emit(&c, OP_RRA);
	prog_flush(&c);
	ft_putnbr_fd(counts[OP_PB], 1);
	ft_putchar_fd('\n', 1);
	prog_free(c.prog);
	return (0);
}