#include "push_swap.h"

static void	put(char *label, int n)
{
	ft_putstr_fd(label, 1);
	ft_putnbr_fd(n, 1);
	ft_putchar_fd('\n', 1);
}

static void	fill3(t_stack *s, int a, int b, int c)
{
	s->data[0] = a;
	s->data[1] = b;
	s->data[2] = c;
	s->size = 3;
}

int	main(void)
{
	t_stack	*s;
	int		i;

	stack_free(NULL);
	s = stack_new(5);
	put("new size: ", s->size);
	put("new cap: ", s->cap);
	put("sorted vazia: ", stack_is_sorted(s));
	s->size = 1;
	s->data[0] = 7;
	put("sorted {7}: ", stack_is_sorted(s));
	put("min {7}: ", stack_min_index(s));
	fill3(s, 1, 2, 3);
	put("sorted {1 2 3}: ", stack_is_sorted(s));
	fill3(s, 1, 3, 2);
	put("sorted {1 3 2}: ", stack_is_sorted(s));
	i = 0;
	while (i < 5)
	{
		s->data[i] = 5 - i;
		i++;
	}
	s->size = 5;
	put("min {5 4 3 2 1}: ", stack_min_index(s));
	put("max {5 4 3 2 1}: ", stack_max_index(s));
	stack_free(s);
	return (0);
}