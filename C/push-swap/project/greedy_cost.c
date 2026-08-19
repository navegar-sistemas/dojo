#include "push_swap.h"

/*
** Rotações que compartilham direção rodam como rr / rrr, então um
** par de mesmo sinal custa a perna mais longa e um par misto custa a
** soma.
*/
int	move_cost(t_move m)
{
	int	ca;
	int	cb;

	ca = m.a;
	if (ca < 0)
		ca = -ca;
	cb = m.b;
	if (cb < 0)
		cb = -cb;
	if ((m.a >= 0 && m.b >= 0) || (m.a <= 0 && m.b <= 0))
	{
		if (ca > cb)
			return (ca);
		return (cb);
	}
	return (ca + cb);
}

/*
** O menor custo vence. bias inverte qual lado fica com o empate:
** duas execuções do mesmo greedy com políticas de desempate opostas
** divergem rapidamente, e o portfólio do --adaptive fica com o mais
** curto dos dois programas.
*/
t_move	move_better(t_ctx *c, t_move x, t_move y)
{
	int	cx;
	int	cy;

	cx = move_cost(x);
	cy = move_cost(y);
	if (cy < cx)
		return (y);
	if (cy == cx && c->bias == 1)
		return (y);
	return (x);
}

/*
** O melhor das quatro combinações de direção para trazer o índice ia
** ao topo de A e o índice ib ao topo de B: cada índice pode viajar
** para frente (o próprio índice) ou para trás (índice menos size,
** negativo).
*/
t_move	pair_best(t_ctx *c, int ia, int ib)
{
	t_move	m;
	t_move	best;

	m.a = ia;
	m.b = ib;
	best = m;
	m.b = ib - c->b->size;
	best = move_better(c, best, m);
	m.a = ia - c->a->size;
	best = move_better(c, best, m);
	m.b = ib;
	best = move_better(c, best, m);
	return (best);
}

/*
** B é mantida circularmente decrescente. Um novo valor se encaixa
** logo acima de seu sucessor (o maior rank abaixo dele); um valor
** menor que todo rank em B vai acima do máximo atual, que é também
** onde um novo máximo global cai. Ambos mantêm a ordem circular
** intacta.
*/
int	target_in_b(t_stack *b, int value)
{
	int	i;
	int	succ;
	int	maxi;

	succ = -1;
	maxi = 0;
	i = 0;
	while (i < b->size)
	{
		if (b->data[i] > b->data[maxi])
			maxi = i;
		if (b->data[i] < value
			&& (succ == -1 || b->data[i] > b->data[succ]))
			succ = i;
		i++;
	}
	if (succ == -1)
		return (maxi);
	return (succ);
}

/*
** Espelho de target_in_b para a A circularmente crescente: um valor
** vai logo acima de seu teto (o menor rank acima dele), e acima do
** mínimo quando não tem teto ou é o novo mínimo.
*/
int	target_in_a(t_stack *a, int value)
{
	int	i;
	int	up;
	int	mini;

	up = -1;
	mini = 0;
	i = 0;
	while (i < a->size)
	{
		if (a->data[i] < a->data[mini])
			mini = i;
		if (a->data[i] > value
			&& (up == -1 || a->data[i] < a->data[up]))
			up = i;
		i++;
	}
	if (up == -1)
		return (mini);
	return (up);
}
