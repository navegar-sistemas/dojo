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

#include "push_swap.h"

int	main(void)
{
	t_stack	*s;

	s = stack_new(5);
	s->data[0] = 3;
	s->data[1] = 1;
	s->data[2] = 2;
	s->size = 3;
	ft_putnbr_fd(stack_is_sorted(s), 1);
	ft_putnbr_fd(stack_min_index(s), 1);
	ft_putnbr_fd(stack_max_index(s), 1);
	s->size = 0;
	ft_putnbr_fd(stack_is_sorted(s), 1);
	ft_putchar_fd('\n', 1);
	stack_free(s);
	stack_free(NULL);
	return (0);
}
