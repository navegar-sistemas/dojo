/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   lstadd_front.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/23 17:30:00 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/23 17:30:00 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <stdlib.h>
#include "libft.h"

/* Anda a lista e confere que os contents batem, na ordem de 'esp', e que
   a lista tem EXATAMENTE n nos (termina em NULL depois do n-esimo). */
static int	seq_ok(t_list *head, void **esp, int n)
{
	int	i;

	i = 0;
	while (i < n)
	{
		if (head == NULL || head->content != esp[i])
			return (0);
		head = head->next;
		i++;
	}
	return (head == NULL);
}

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
	t_list	*solto;
	void	*a = "a";
	void	*b = "b";
	void	*c = "c";
	int		falhas;

	head = NULL;
	falhas = 0;
	printf("<ft_lstadd_front>\n");
	/* caso 1: lista vazia -> o no vira a cabeca, next == NULL */
	ft_lstadd_front(&head, ft_lstnew(a));
	if (!seq_ok(head, (void *[]){a}, 1))
		(printf("FALHA: add em lista vazia\n"), falhas++);
	/* caso 2 e 3: insere na frente -> ordem LIFO (c, b, a) */
	ft_lstadd_front(&head, ft_lstnew(b));
	ft_lstadd_front(&head, ft_lstnew(c));
	if (!seq_ok(head, (void *[]){c, b, a}, 3))
		(printf("FALHA: ordem/encadeamento apos 3 inserts\n"), falhas++);
	/* caso 4: new == NULL -> nao mexe na lista, nao crasha */
	ft_lstadd_front(&head, NULL);
	if (!seq_ok(head, (void *[]){c, b, a}, 3))
		(printf("FALHA: new==NULL alterou a lista\n"), falhas++);
	/* caso 5: lst == NULL -> so retorna, nao crasha */
	solto = ft_lstnew("solto");
	ft_lstadd_front(NULL, solto);
	free(solto);
	free_list(head);
	if (falhas == 0)
		printf("[OK] Passou em todos os casos.\n");
	else
		printf("[X] %d falha(s).\n", falhas);
	printf("</ft_lstadd_front>\n");
	return (falhas != 0);
}
