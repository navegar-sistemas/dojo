#include "push_swap.h"

/*
** Verdadeiro quando uma única rotação final pode terminar o serviço:
** lidos ciclicamente, os ranks descem no máximo uma vez. É a saída
** antecipada da fase de push, e o que permite que entradas quase
** ordenadas mantenham a maioria de seus elementos totalmente fora
** de B.
*/
static int	is_circular_sorted(t_stack *s)
{
	int	i;
	int	descents;

	descents = 0;
	i = 0;
	while (i < s->size)
	{
		if (s->data[i] > s->data[(i + 1) % s->size])
			descents++;
		i++;
	}
	return (descents <= 1);
}

/*
** Envia elementos para B, o mais barato primeiro. B é mantida
** circularmente decrescente empurrando cada rank logo acima de seu
** sucessor, para que a fase de inserção possa colocar cada elemento
** direto em seu lugar. Para com 3 restantes, ou antes se o restante
** de A já estiver em ordem.
*/
static void	push_phase(t_ctx *c)
{
	t_move	m;

	while (c->a->size > 3 && !is_circular_sorted(c->a))
	{
		m = best_push(c);
		exec_move(c, m);
		op_pb(c);
	}
}

/*
** Coloca tudo de volta, o mais barato primeiro, mantendo A
** circularmente crescente. Uma única rotação de alinhamento no final
** termina o serviço.
*/
static void	insert_phase(t_ctx *c)
{
	t_move	m;

	while (c->b->size > 0)
	{
		m = best_insert(c);
		exec_move(c, m);
		op_pa(c);
	}
}

/*
** Inserção gulosa por custo sobre as duas pilhas. Isoladamente não
** tem limite de pior caso melhor que O(n²) operações; o --adaptive a
** executa através de run_portfolio contra um algoritmo certificador,
** que é o que limita o programa emitido dentro da classe declarada
** de cada regime.
*/
void	sort_greedy_run(t_ctx *c, t_conf *conf)
{
	conf->name = "Greedy";
	conf->cclass = "O(n²)";
	if (stack_is_sorted(c->a))
		return ;
	if (c->a->size <= 3)
	{
		sort_tiny(c);
		return ;
	}
	push_phase(c);
	if (c->a->size <= 3)
		sort_tiny(c);
	insert_phase(c);
	rotate_a_to_top(c, stack_min_index(c->a));
}
