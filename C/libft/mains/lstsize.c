/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   lstsize.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/23 19:30:00 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/23 19:30:00 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <stdlib.h>
#include "libft.h"

static void	free_list(t_list *head)
{
	t_list	*tmp;

	while (head)
	{
		tmp = head->next;
		free(head);
		head = tmp;
	}
}

/* Monta uma lista com n nos (contents quaisquer) na frente, devolvendo a
   cabeca. Em falha de malloc devolve o que conseguiu montar. */
static t_list	*build(int n)
{
	t_list	*head;
	t_list	*node;

	head = NULL;
	while (n-- > 0)
	{
		node = ft_lstnew("x");
		if (!node)
			break ;
		ft_lstadd_front(&head, node);
	}
	return (head);
}

int	main(void)
{
	t_list	*head;
	int		falhas;

	falhas = 0;
	printf("<ft_lstsize>\n");
	/* caso 1: lista vazia (NULL) -> 0 */
	if (ft_lstsize(NULL) != 0)
		(printf("FALHA: size de NULL deveria ser 0\n"), falhas++);
	/* caso 2: um unico no -> 1 */
	head = build(1);
	if (ft_lstsize(head) != 1)
		(printf("FALHA: size de 1 no deveria ser 1\n"), falhas++);
	free_list(head);
	/* caso 3: varios nos -> conta exata */
	head = build(5);
	if (ft_lstsize(head) != 5)
		(printf("FALHA: size de 5 nos deveria ser 5\n"), falhas++);
	free_list(head);
	/* caso 4: lista maior, confirma que conta o ultimo (termina em NULL) */
	head = build(100);
	if (ft_lstsize(head) != 100)
		(printf("FALHA: size de 100 nos deveria ser 100\n"), falhas++);
	free_list(head);
	if (falhas == 0)
		printf("[OK] Passou em todos os casos.\n");
	else
		printf("[X] %d falha(s).\n", falhas);
	printf("</ft_lstsize>\n");
	return (falhas != 0);
}
