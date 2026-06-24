/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   lstmap.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/24 11:00:00 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/24 11:00:00 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <stdlib.h>
#include "libft.h"

/* f: recebe um content (int*) e devolve um content NOVO (int*) = valor*10.
   Aloca -> a lista mapeada e independente da original. */
static void	*times10(void *content)
{
	int	*p;

	p = malloc(sizeof(int));
	if (p)
		*p = *(int *)content * 10;
	return (p);
}

static void	*heapint(int v)
{
	int	*p;

	p = malloc(sizeof(int));
	if (p)
		*p = v;
	return (p);
}

static void	free_all(t_list *head)
{
	t_list	*tmp;

	while (head)
	{
		tmp = head->next;
		free(head->content);
		free(head);
		head = tmp;
	}
}

static int	seq_ok(t_list *head, int *esp, int n)
{
	int	i;

	i = 0;
	while (i < n)
	{
		if (head == NULL || *(int *)head->content != esp[i])
			return (0);
		head = head->next;
		i++;
	}
	return (head == NULL);
}

int	main(void)
{
	t_list	*orig;
	t_list	*mapped;
	int		esp[5];
	int		ori[5];
	int		i;
	int		falhas;

	orig = NULL;
	falhas = 0;
	i = 0;
	while (i < 5)
	{
		ft_lstadd_back(&orig, ft_lstnew(heapint(i + 1)));
		esp[i] = (i + 1) * 10;
		ori[i] = i + 1;
		i++;
	}
	printf("<ft_lstmap>\n");
	/* caso 1: mapeia -> lista nova [10..50], mesmo tamanho, na ordem */
	mapped = ft_lstmap(orig, times10, free);
	if (ft_lstsize(mapped) != 5 || !seq_ok(mapped, esp, 5))
		(printf("FALHA: lista mapeada errada (tamanho/conteudo/ordem)\n"),
			falhas++);
	/* caso 2: a original NAO pode ser alterada */
	if (!seq_ok(orig, ori, 5))
		(printf("FALHA: a lista original foi modificada\n"), falhas++);
	/* caso 3: independencia -> nos e contents sao novos (ponteiros != ) */
	if (mapped == orig || (mapped && mapped->content == orig->content))
		(printf("FALHA: lista mapeada compartilha nos/contents com a orig\n"),
			falhas++);
	/* caso 4: guards -> NULL */
	if (ft_lstmap(NULL, times10, free) != NULL)
		(printf("FALHA: lstmap(NULL,..) deveria ser NULL\n"), falhas++);
	if (ft_lstmap(orig, NULL, free) != NULL)
		(printf("FALHA: lstmap(.,NULL,.) deveria ser NULL\n"), falhas++);
	free_all(orig);
	free_all(mapped);
	if (falhas == 0)
		printf("[OK] Passou em todos os casos.\n");
	else
		printf("[X] %d falha(s).\n", falhas);
	printf("</ft_lstmap>\n");
	return (falhas != 0);
}
