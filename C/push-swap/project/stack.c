#include "push_swap.h"

void	stack_free(t_stack *s)
{
	if (s == NULL)
		return ;
	if (s->data != NULL)
		free(s->data);
	free(s);
}

t_stack	*stack_new(int cap)
{
	t_stack	*s;

	s = malloc(sizeof(t_stack));
	if (!s)
		return (NULL);
	if (cap > 0)
		s->data = malloc(sizeof(int) * cap);
	else
		s->data = malloc(sizeof(int));
	if (!s->data)
	{
		free(s);
		return (NULL);
	}
	s->cap = cap;
	s->size = 0;
	return (s);
}

int	stack_is_sorted(t_stack *s)
{
	int	i;

	if (s->size <= 1)
		return (1);
	i = 1;
	while (i < s->size)
	{
		if (s->data[i] < s->data[i - 1])
			return (0);
		i++;
	}
	return (1);
}

int	stack_min_index(t_stack *s)
{
	int	i;
	int	min;

	min = 0;
	i = 1;
	while (i < s->size)
	{
		if (s->data[i] < s->data[min])
			min = i;
		i++;
	}
	return (min);
}

int	stack_max_index(t_stack *s)
{
	int	i;
	int	max;

	max = 0;
	i = 1;
	while (i < s->size)
	{
		if (s->data[i] > s->data[max])
			max = i;
		i++;
	}
	return (max);
}
