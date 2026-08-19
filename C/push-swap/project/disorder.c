#include "push_swap.h"

double	compute_disorder(t_stack *a)
{
	long	mistakes;
	long	pairs;
	int		i;
	int		j;

	mistakes = 0;
	pairs = 0;
	i = 0;
	while (i < a->size)
	{
		j = i + 1;
		while (j < a->size)
		{
			pairs++;
			if (a->data[i] > a->data[j])
				mistakes++;
			j++;
		}
		i++;
	}
	if (pairs == 0)
		return (0.0);
	return ((double)mistakes / (double)pairs);
}
