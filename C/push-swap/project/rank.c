#include "push_swap.h"

static void	insert_sort(int *t, int n)
{
	int	i;
	int	j;
	int	v;

	i = 1;
	while (i < n)
	{
		v = t[i];
		j = i - 1;
		while (j >= 0 && t[j] > v)
		{
			t[j + 1] = t[j];
			j--;
		}
		t[j + 1] = v;
		i++;
	}
}

/*
** Busca binária: é exata porque não há duplicatas, então cada valor
** aparece uma vez na cópia ordenada.
*/
static int	rank_of(int *t, int n, int v)
{
	int	lo;
	int	hi;
	int	mid;

	lo = 0;
	hi = n - 1;
	while (lo < hi)
	{
		mid = (lo + hi) / 2;
		if (t[mid] < v)
			lo = mid + 1;
		else
			hi = mid;
	}
	return (lo);
}

/*
** Substitui cada valor pela posição que ele ocuparia na lista
** ordenada, 0..n-1. Ordenar os ranks é o mesmo problema que ordenar
** os valores, e é o intervalo denso que permite ao --medium dividir
** em blocos parelhos e ao --complex usar ceil(log2 n) passadas.
*/
int	build_ranks(t_stack *a)
{
	int	*copy;
	int	i;

	if (a->size <= 0)
		return (1);
	copy = malloc(sizeof(int) * a->size);
	if (!copy)
		return (0);
	i = 0;
	while (i < a->size)
	{
		copy[i] = a->data[i];
		i++;
	}
	insert_sort(copy, a->size);
	i = 0;
	while (i < a->size)
	{
		a->data[i] = rank_of(copy, a->size, a->data[i]);
		i++;
	}
	free(copy);
	return (1);
}
