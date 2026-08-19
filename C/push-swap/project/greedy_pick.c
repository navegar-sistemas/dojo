#include "push_swap.h"

static t_move	cand_push(t_ctx *c, int i)
{
	return (pair_best(c, i, target_in_b(c->b, c->a->data[i])));
}

/*
** Varre os candidatos para fora a partir do topo de A (índices 0,
** depois 1 e n-1, depois 2 e n-2, ...). Um candidato a k passos de
** distância custa pelo menos k rotações, então a varredura para
** assim que k alcança o melhor custo encontrado: nada mais distante
** pode vencer. A poda mantém o greedy rápido sem nunca mudar sua
** resposta.
*/
t_move	best_push(t_ctx *c)
{
	t_move	best;
	int		k;
	int		size;

	size = c->a->size;
	best = cand_push(c, 0);
	k = 1;
	while (k <= size - k && k < move_cost(best))
	{
		best = move_better(c, best, cand_push(c, k));
		if (size - k != k)
			best = move_better(c, best, cand_push(c, size - k));
		k++;
	}
	return (best);
}

static t_move	cand_insert(t_ctx *c, int i)
{
	return (pair_best(c, target_in_a(c->a, c->b->data[i]), i));
}

/*
** Mesma varredura para fora e poda de best_push, sobre os índices
** de B.
*/
t_move	best_insert(t_ctx *c)
{
	t_move	best;
	int		k;
	int		size;

	size = c->b->size;
	best = cand_insert(c, 0);
	k = 1;
	while (k <= size - k && k < move_cost(best))
	{
		best = move_better(c, best, cand_insert(c, k));
		if (size - k != k)
			best = move_better(c, best, cand_insert(c, size - k));
		k++;
	}
	return (best);
}
