/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   lstadd_back.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/23 20:30:00 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/23 20:30:00 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <stdlib.h>
#include "libft.h"

/* Anda a lista e confere os contents na ordem de 'esp', e que ela tem
   EXATAMENTE n nos (termina em NULL depois do n-esimo). */
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
	printf("<ft_lstadd_back>\n");
	/* caso 1: lista vazia -> o no vira a cabeca */
	ft_lstadd_back(&head, ft_lstnew(a));
	if (!seq_ok(head, (void *[]){a}, 1))
		(printf("FALHA: add_back em lista vazia\n"), falhas++);
	/* caso 2 e 3: insere no FIM -> ordem FIFO (a, b, c) */
	ft_lstadd_back(&head, ft_lstnew(b));
	ft_lstadd_back(&head, ft_lstnew(c));
	if (!seq_ok(head, (void *[]){a, b, c}, 3))
		(printf("FALHA: ordem/encadeamento apos 3 add_back\n"), falhas++);
	/* caso 4: new == NULL -> nao mexe na lista, nao crasha */
	ft_lstadd_back(&head, NULL);
	if (!seq_ok(head, (void *[]){a, b, c}, 3))
		(printf("FALHA: new==NULL alterou a lista\n"), falhas++);
	/* caso 5: lst == NULL -> so retorna, nao crasha */
	solto = ft_lstnew("solto");
	ft_lstadd_back(NULL, solto);
	free(solto);
	free_list(head);
	if (falhas == 0)
		printf("[OK] Passou em todos os casos.\n");
	else
		printf("[X] %d falha(s).\n", falhas);
	printf("</ft_lstadd_back>\n");
	return (falhas != 0);
}
