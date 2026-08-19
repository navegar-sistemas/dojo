#include "push_swap.h"

/*
** Selection sort por extração do mínimo. O que sai de a é sempre o
** menor restante, então b recebe os valores crescendo do fundo para
** cima; empurrá-los de volta com pa inverte de novo e a termina
** ordenado.
**
** name e cclass são escritos antes dos retornos antecipados: o
** --bench precisa do rótulo mesmo quando nada é emitido.
*/
void	sort_simple(t_ctx *c, t_conf *conf)
{
	int	i;

	conf->name = "Simple";
	conf->cclass = "O(n²)";
	if (c->a->size <= 3)
	{
		sort_tiny(c);
		return ;
	}
	if (stack_is_sorted(c->a))
		return ;
	while (c->a->size > 0)
	{
		i = stack_min_index(c->a);
		rotate_a_to_top(c, i);
		op_pb(c);
	}
	while (c->b->size > 0)
		op_pa(c);
}
