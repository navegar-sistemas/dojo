#include "push_swap.h"

static int	count_in_range(t_stack *s, int lo, int hi)
{
	int	i;
	int	n;

	i = 0;
	n = 0;
	while (i < s->size)
	{
		if (s->data[i] >= lo && s->data[i] <= hi)
			n++;
		i++;
	}
	return (n);
}

/*
** Fase 1, um bloco: varre a empurrando para b todo rank do bloco
** atual, mandando o topo para o fundo com ra quando ele não pertence.
** rest é a condição de parada, contada uma vez em CPU antes da
** varredura começar. Só ra, nunca rra: rotacionar para trás
** embaralha a ordem em que os elementos chegam a b e torna a fase 2
** mais cara do que economiza aqui.
*/
static void	collect_chunk(t_ctx *c, int lo, int hi)
{
	int	rest;

	rest = count_in_range(c->a, lo, hi);
	while (rest > 0)
	{
		if (c->a->data[0] >= lo && c->a->data[0] <= hi)
		{
			op_pb(c);
			rest--;
		}
		else
			op_ra(c);
	}
}

static void	collect_all(t_ctx *c, int n, int k, int width)
{
	int	block;
	int	lo;
	int	hi;

	block = 0;
	while (block < k)
	{
		lo = block * width;
		hi = lo + width - 1;
		if (hi > n - 1)
			hi = n - 1;
		collect_chunk(c, lo, hi);
		block++;
	}
}

/*
** Fase 2: b é aproximadamente decrescente a partir do topo, então a
** busca pelo máximo é curta. Procurar o extremo entre width elementos
** em vez de entre n é todo o ganho.
*/
static void	drain_b(t_ctx *c)
{
	int	i;

	while (c->b->size > 0)
	{
		i = stack_max_index(c->b);
		rotate_b_to_top(c, i);
		op_pa(c);
	}
}

/*
** Chunk sort sobre os ranks. k = max(2, isqrt(n / 2)) minimiza
** k/2 + n/(8k), a soma das duas fases; k = isqrt(n) é mensuravelmente
** pior. O piso de 2 mantém entradas pequenas funcionando.
*/
void	sort_medium(t_ctx *c, t_conf *conf)
{
	int	n;
	int	k;
	int	width;

	conf->name = "Medium";
	conf->cclass = "O(n√n)";
	if (c->a->size <= 3)
	{
		sort_tiny(c);
		return ;
	}
	if (stack_is_sorted(c->a))
		return ;
	n = c->a->size;
	k = isqrt(n / 2);
	if (k < 2)
		k = 2;
	width = (n + k - 1) / k;
	collect_all(c, n, k, width);
	drain_b(c);
}
