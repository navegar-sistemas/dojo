/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   lstdelone.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/23 21:00:00 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/23 21:00:00 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <stdlib.h>
#include "libft.h"

/* del de teste: marca quantas vezes foi chamado e libera o content.
   Assim o asan acusa se o content NAO for liberado, e o contador acusa
   se o del nao for chamado (ou for chamado demais). */
static int	g_del_calls;

static void	count_del(void *content)
{
	g_del_calls++;
	free(content);
}

/* content no heap (int): se o no/content nao forem liberados, asan vaza. */
static void	*heapint(int v)
{
	int	*p;

	p = malloc(sizeof(int));
	if (p)
		*p = v;
	return (p);
}

int	main(void)
{
	t_list	*a;
	t_list	*b;
	int		falhas;

	falhas = 0;
	printf("<ft_lstdelone>\n");
	/* caso 1: deleta UM no -> del chamado 1x; content + no liberados (asan) */
	g_del_calls = 0;
	a = ft_lstnew(heapint(42));
	ft_lstdelone(a, count_del);
	if (g_del_calls != 1)
		(printf("FALHA: del deveria ser chamado 1x (foi %d)\n", g_del_calls),
			falhas++);
	/* caso 2: delone(a) com a->next=b -> NAO pode mexer no b. */
	g_del_calls = 0;
	b = ft_lstnew(heapint(2));
	a = ft_lstnew(heapint(1));
	a->next = b;
	ft_lstdelone(a, count_del);
	if (g_del_calls != 1)
		(printf("FALHA: delone deletou mais de 1 no (del=%d)\n", g_del_calls),
			falhas++);
	else if (b->content == NULL || *(int *)b->content != 2 || b->next != NULL)
		(printf("FALHA: o resto da lista (b) foi corrompido/liberado\n"),
			falhas++);
	ft_lstdelone(b, count_del);
	/* caso 3: lst == NULL -> nao crasha, nao chama del */
	g_del_calls = 0;
	ft_lstdelone(NULL, count_del);
	if (g_del_calls != 0)
		(printf("FALHA: delone(NULL,..) nao deveria chamar del\n"), falhas++);
	/* caso 4: del == NULL -> nao crasha (e nao libera; limpamos na mao) */
	a = ft_lstnew(heapint(7));
	ft_lstdelone(a, NULL);
	free(a->content);
	free(a);
	if (falhas == 0)
		printf("[OK] Passou em todos os casos.\n");
	else
		printf("[X] %d falha(s).\n", falhas);
	printf("</ft_lstdelone>\n");
	return (falhas != 0);
}
