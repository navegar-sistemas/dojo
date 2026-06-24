/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   lstiter.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/24 10:00:00 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/24 10:00:00 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <stdlib.h>
#include "libft.h"

/* f de teste: conta chamadas e MODIFICA o content no lugar (+1).
   Se aplicar no content errado / pular nos / nao aplicar, a checagem pega. */
static int	g_calls;

static void	inc(void *content)
{
	g_calls++;
	*(int *)content += 1;
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

/* confere que cada content == base+i (cada no incrementado UMA vez) */
static int	seq_ok(t_list *head, int base, int n)
{
	int	i;

	i = 0;
	while (i < n)
	{
		if (head == NULL || *(int *)head->content != base + i)
			return (0);
		head = head->next;
		i++;
	}
	return (head == NULL);
}

int	main(void)
{
	t_list	*head;
	int		i;
	int		falhas;

	falhas = 0;
	head = NULL;
	i = 0;
	while (i < 5)
	{
		ft_lstadd_back(&head, ft_lstnew(heapint(10 + i)));
		i++;
	}
	printf("<ft_lstiter>\n");
	/* caso 1: aplica f em todos -> contents viram 11..15, f chamado 5x */
	g_calls = 0;
	ft_lstiter(head, inc);
	if (g_calls != 5)
		(printf("FALHA: f deveria ser chamado 5x (foi %d)\n", g_calls),
			falhas++);
	if (!seq_ok(head, 11, 5))
		(printf("FALHA: f nao foi aplicado em todos os contents na ordem\n"),
			falhas++);
	/* caso 2: lst == NULL -> nao crasha */
	ft_lstiter(NULL, inc);
	/* caso 3: f == NULL -> nao crasha e nao toca nos contents */
	g_calls = 0;
	ft_lstiter(head, NULL);
	if (g_calls != 0 || !seq_ok(head, 11, 5))
		(printf("FALHA: f==NULL nao deveria alterar nada\n"), falhas++);
	free_all(head);
	if (falhas == 0)
		printf("[OK] Passou em todos os casos.\n");
	else
		printf("[X] %d falha(s).\n", falhas);
	printf("</ft_lstiter>\n");
	return (falhas != 0);
}
