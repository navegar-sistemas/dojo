/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   lstnew.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/23 17:00:00 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/23 17:00:00 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <stdlib.h>
#include "libft.h"

/* Um no valido tem: content == o MESMO ponteiro que entrou (por referencia,
   nao copia) e next == NULL. Devolve 0 se algo estiver errado. */
static int	check_node(t_list *node, void *esperado)
{
	if (node == NULL)
		return (0);
	if (node->content != esperado)
		return (0);
	if (node->next != NULL)
		return (0);
	return (1);
}

int	main(void)
{
	int		falhas;
	char	*str;
	int		valor;
	char	*buf;
	t_list	*n;

	falhas = 0;
	str = "42 Sao Paulo";
	valor = 7;
	printf("<ft_lstnew>\n");
	/* caso 1: content = ponteiro pra string */
	n = ft_lstnew(str);
	if (!check_node(n, str))
		(printf("FALHA: content!=str ou next!=NULL\n"), falhas++);
	free(n);
	/* caso 2: content = ponteiro pra int */
	n = ft_lstnew(&valor);
	if (!check_node(n, &valor))
		(printf("FALHA: content!=&valor ou next!=NULL\n"), falhas++);
	free(n);
	/* caso 3: content = NULL -> tem que CRIAR o no (nao devolver NULL) */
	n = ft_lstnew(NULL);
	if (n == NULL)
		(printf("FALHA: lstnew(NULL) devolveu NULL (devia criar o no)\n"),
			falhas++);
	else if (n->content != NULL || n->next != NULL)
		(printf("FALHA: lstnew(NULL): content/next errado\n"), falhas++);
	free(n);
	/* caso 4: prova que e por REFERENCIA, nao copia. Altera o buffer depois
	   de criar o no; se for o mesmo ponteiro, o no enxerga a mudanca. */
	buf = malloc(4);
	if (buf)
	{
		buf[0] = 'a';
		buf[1] = '\0';
		n = ft_lstnew(buf);
		buf[0] = 'X';
		if (n == NULL || n->content != buf || ((char *)n->content)[0] != 'X')
			(printf("FALHA: content nao e por referencia (copiou?)\n"),
				falhas++);
		free(n);
		free(buf);
	}
	if (falhas == 0)
		printf("[OK] Passou em todos os casos.\n");
	else
		printf("[X] %d falha(s).\n", falhas);
	printf("</ft_lstnew>\n");
	return (falhas != 0);
}
