/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   isascii.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/18 17:39:28 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/18 17:39:28 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <ctype.h>

int	ft_isascii(int c);

int	main(void)
{
	int	c;
	int	falhas;

	falhas = 0;
	c = -1;
	printf("<ft_isascii>\n");
	while (c <= 255)
	{
		if ((ft_isascii(c) != 0) != (isascii(c) != 0))
		{
			printf("FALHA c=%d : ft=%d  libc=%d\n", c, ft_isascii(c), isascii(c));
			falhas++;
		}
		c++;
	}
	if (falhas == 0)
		printf("[OK] Passou nos 257 casos (-1..255).\n");
	else
		printf("[X] %d falha(s).\n", falhas);
	printf("</ft_isascii>\n");
	return (falhas != 0);
}
