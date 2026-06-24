/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   strchr.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/19 16:00:38 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/19 16:00:38 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <string.h>

char *ft_strchr(const char *s, int c);

int main(void)
{
	/* "banana": repeticao -> testa "primeira ocorrencia" */
	const char *casos_s[] = {"", "a", "hello world", "banana",
		"42 São Paulo", "abcdefghij"};
	/* '\0': term | 'a'+256: trunca p/ 'a' | -1: (char)0xFF | 'z': ausente
	   0xC3: byte ALTO presente em "São" -> testa achar high byte */
	int casos_c[] = {'a', 'j', '1', '*', '-', '\0', 'a' + 256, -1, 'z', 0xC3};
	int n1 = sizeof(casos_s) / sizeof(casos_s[0]);
	int n2 = sizeof(casos_c) / sizeof(casos_c[0]);
	int i1 = 0;
	int falhas = 0;

	printf("<ft_strchr>\n");
	while (i1 < n1)
	{
		int i2 = 0;
		while (i2 < n2)
		{
			const char *r_ft = ft_strchr(casos_s[i1], casos_c[i2]);
			const char *r_libc = strchr(casos_s[i1], casos_c[i2]);
			if (r_ft != r_libc)
			{
				printf("FALHA s=\"%s\" c=%d : ft=%p  libc=%p\n",
					casos_s[i1], casos_c[i2], (void *)r_ft, (void *)r_libc);
				falhas++;
			}
			i2++;
		}
		i1++;
	}

	if (falhas == 0)
		printf("[OK] Passou em todos os casos.\n");
	else
		printf("[X] %d falha(s).\n", falhas);
	printf("</ft_strchr>\n");
	return (falhas != 0);
}
