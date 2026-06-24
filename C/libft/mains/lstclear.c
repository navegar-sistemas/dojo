/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   lstclear.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/23 21:30:00 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/23 21:30:00 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <stdlib.h>
#include "libft.h"

/* del instrumentado: conta chamadas e libera o content. asan acusa se algum
   no/content nao for liberado; o contador acusa se nem todos forem deletados. */
static int	g_del_calls;

static void	count_del(void *content)
{
	g_del_calls++;
	free(content);
}

static void	*heapint(int v)
{
	int	*p;

	p = malloc(sizeof(int));
	if (p)
		*p = v;
	return (p);
}

/* monta uma lista com n nos (content no heap) e devolve a cabeca. */
static t_list	*build(int n)
{
	t_list	*head;
	int		i;

	head = NULL;
	i = 0;
	while (i < n)
	{
		ft_lstadd_back(&head, ft_lstnew(heapint(i)));
		i++;
	}
	return (head);
}

int	main(void)
{
	t_list	*head;
	int		falhas;

	falhas = 0;
	printf("<ft_lstclear>\n");
	/* caso 1: limpa lista de 5 nos -> del 5x, *lst == NULL, asan sem leak */
	g_del_calls = 0;
	head = build(5);
	ft_lstclear(&head, count_del);
	if (head != NULL)
		(printf("FALHA: *lst deveria virar NULL apos clear\n"), falhas++);
	if (g_del_calls != 5)
		(printf("FALHA: del deveria ser chamado 5x (foi %d)\n", g_del_calls),
			falhas++);
	/* caso 2: lista vazia -> nao crasha, continua NULL */
	g_del_calls = 0;
	head = NULL;
	ft_lstclear(&head, count_del);
	if (head != NULL || g_del_calls != 0)
		(printf("FALHA: clear de lista vazia nao deveria fazer nada\n"),
			falhas++);
	/* caso 3: lst == NULL -> so retorna, nao crasha */
	ft_lstclear(NULL, count_del);
	/* caso 4: del == NULL -> nao crasha e NAO limpa; limpamos depois */
	g_del_calls = 0;
	head = build(3);
	ft_lstclear(&head, NULL);
	if (head == NULL || g_del_calls != 0)
		(printf("FALHA: del==NULL nao deveria limpar a lista\n"), falhas++);
	ft_lstclear(&head, count_del);
	if (falhas == 0)
		printf("[OK] Passou em todos os casos.\n");
	else
		printf("[X] %d falha(s).\n", falhas);
	printf("</ft_lstclear>\n");
	return (falhas != 0);
}
