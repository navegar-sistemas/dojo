/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   lstlast.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/23 20:00:00 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/23 20:00:00 by macoelho         ###   ########.fr       */
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

int	main(void)
{
	t_list	*head;
	t_list	*cauda;
	t_list	*r;
	int		i;
	int		falhas;

	head = NULL;
	falhas = 0;
	printf("<ft_lstlast>\n");
	/* caso 1: lista vazia -> NULL */
	if (ft_lstlast(NULL) != NULL)
		(printf("FALHA: lstlast(NULL) deveria ser NULL\n"), falhas++);
	/* caso 2: um unico no -> o proprio no (head == last) */
	head = ft_lstnew("unico");
	if (ft_lstlast(head) != head)
		(printf("FALHA: 1 no -> deveria devolver o proprio no\n"), falhas++);
	/* a 'cauda' e o 1o no criado; add_front empurra os outros pra frente,
	   entao esse no fica no fim (->next == NULL) o tempo todo. */
	cauda = head;
	i = 0;
	while (i < 5)
	{
		ft_lstadd_front(&head, ft_lstnew("x"));
		i++;
	}
	/* caso 3: lista com 6 nos -> devolve EXATAMENTE a cauda, e ela termina.
	   Guarda o retorno antes de desreferenciar (uma impl bugada pode
	   devolver NULL; nao queremos crashar a propria main). */
	r = ft_lstlast(head);
	if (r != cauda)
		(printf("FALHA: nao devolveu o ultimo no (esperado cauda)\n"), falhas++);
	else if (r->next != NULL)
		(printf("FALHA: o no devolvido nao e o fim (next != NULL)\n"), falhas++);
	free_list(head);
	if (falhas == 0)
		printf("[OK] Passou em todos os casos.\n");
	else
		printf("[X] %d falha(s).\n", falhas);
	printf("</ft_lstlast>\n");
	return (falhas != 0);
}
