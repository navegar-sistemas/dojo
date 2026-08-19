#include "push_swap.h"

/*
** Raiz quadrada inteira, porque math.h não é uma dependência
** permitida.
*/
int	isqrt(int n)
{
	int	i;

	i = 1;
	while ((i + 1) * (i + 1) <= n)
		i++;
	return (i);
}

/*
** Traz a->data[i] ao topo pelo caminho mais curto. O empate em
** i == size / 2 escolhe ra, e essa escolha é observável: é o que
** reproduz a saída de --simple 5 4 3 2 1 publicada no subject.
*/
void	rotate_a_to_top(t_ctx *c, int i)
{
	int	size;

	size = c->a->size;
	if (i <= size / 2)
	{
		while (i-- > 0)
			op_ra(c);
	}
	else
	{
		while (size-- > i)
			op_rra(c);
	}
}

void	rotate_b_to_top(t_ctx *c, int i)
{
	int	size;

	size = c->b->size;
	if (i <= size / 2)
	{
		while (i-- > 0)
			op_rb(c);
	}
	else
	{
		while (size-- > i)
			op_rrb(c);
	}
}

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

/*
** Ponto único de saída por erro para falhas após o setup. Percorre a
** cadeia de simulação para que uma morte dentro das execuções
** candidatas do --adaptive também libere o contexto real. Libera o
** heap, reporta e sai com status 1.
*/
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
