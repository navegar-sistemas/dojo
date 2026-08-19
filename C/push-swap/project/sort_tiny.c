#include "push_swap.h"

/*
** As 6 permutações de 3 elementos, cada uma resolvida em no máximo
** 2 movimentos. data não se move com as rotações, então todo teste
** lê os valores capturados no início da função.
*/
static void	sort_three(t_ctx *c)
{
	int	x;
	int	y;
	int	z;

	x = c->a->data[0];
	y = c->a->data[1];
	z = c->a->data[2];
	if (x > y && y < z && x < z)
		op_sa(c);
	else if (x > y && y > z)
	{
		op_sa(c);
		op_rra(c);
	}
	else if (x > y && x > z)
		op_ra(c);
	else if (x < y && y > z && x < z)
	{
		op_sa(c);
		op_ra(c);
	}
	else if (x < y && y > z && x > z)
		op_rra(c);
}

/*
** Caso base das quatro estratégias. O limite é 3 e não 5 porque o
** subject publica a saída exata de --simple 5 4 3 2 1, que um caso
** especial em n = 5 alteraria.
*/
void	sort_tiny(t_ctx *c)
{
	if (c->a->size < 2)
		return ;
	if (c->a->size == 2)
	{
		if (c->a->data[0] > c->a->data[1])
			op_sa(c);
		return ;
	}
	sort_three(c);
}
