#ifndef PUSH_SWAP_H
# define PUSH_SWAP_H

# include "libft/libft.h"

typedef struct s_stack
{
	int	*data;
	int	size;
	int	cap;
}	t_stack;

/* stack.c */
t_stack	*stack_new(int cap);
void	stack_free(t_stack *s);
int		stack_is_sorted(t_stack *s);
int		stack_min_index(t_stack *s);
int		stack_max_index(t_stack *s);

#endif