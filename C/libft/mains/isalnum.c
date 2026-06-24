/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   isalnum.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/18 06:55:22 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/18 06:55:22 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <ctype.h>

int	ft_isalnum(int c);

int	main(void)
{
	int	c;
	int	falhas;

	falhas = 0;
	c = -1;
	printf("<ft_isalnum>\n");
	while (c <= 255)
	{
		if ((ft_isalnum(c) != 0) != (isalnum(c) != 0))
		{
			printf("FALHA c=%d : ft=%d  libc=%d\n", c, ft_isalnum(c), isalnum(c));
			falhas++;
		}
		c++;
	}
	if (falhas == 0)
		printf("[OK] Passou nos 257 casos (-1..255).\n");
	else
		printf("[X] %d falha(s).\n", falhas);
	printf("</ft_isalnum>\n");
	return (falhas != 0);
}
