/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   strlen.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/18 06:55:22 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/18 06:55:22 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <string.h>

size_t	ft_strlen(const char *s);

int	main(void)
{
	const char	*casos[] = {"", "a", "hello world", "42 São Paulo",
		"abcdefghij", "   ", "1234567890",
		"linha longa para verificar contagem alem de buffers pequenos"};
	int			n = sizeof(casos) / sizeof(casos[0]);
	int			i = 0;
	int			falhas = 0;

	printf("<ft_strlen>\n");
	while (i < n)
	{
		if (ft_strlen(casos[i]) != strlen(casos[i]))
		{
			printf("FALHA s=\"%s\" : ft=%zu  libc=%zu\n",
				casos[i], ft_strlen(casos[i]), strlen(casos[i]));
			falhas++;
		}
		i++;
	}
	if (falhas == 0)
		printf("[OK] Passou em todos os casos.\n");
	else
		printf("[X] %d falha(s).\n", falhas);
	printf("</ft_strlen>\n");
	return (falhas != 0);
}
