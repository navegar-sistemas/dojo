/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_calloc.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/22 13:33:07 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/22 13:33:07 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef PUSH_SWAP_H
# define PUSH_SWAP_H

# include "libft/libft.h"

typedef struct s_stack
{
	int	*data;
	int	size;
	int	cap;
}	t_stack;
t_stack	*stack_new(int cap);
void	stack_free(t_stack *s);
int		stack_is_sorted(t_stack *s);
int		stack_min_index(t_stack *s);
int		stack_max_index(t_stack *s);

#endif