/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   strdup.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/22 16:30:00 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/22 16:30:00 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char	*ft_strdup(const char *s);

int	main(void)
{
	/* ft_strdup ALOCA: free() em cada retorno, checar NULL.
	   Checagens: (a) nao retorna NULL; (b) NAO retorna o mesmo ponteiro
	   (tem que ser COPIA nova, nao o proprio s); (c) conteudo == s
	   INCLUINDO o '\0' (strcmp pega truncamento, ex.: "hello"->"hell").
	   O '+1' do terminador e o size do strlcpy/memcpy sao os pegadinhas. */
	const char	*casos[] = {"", "a", "ab", "hello", "hello world",
		"42 Sao Paulo", "  spaces  ", "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"};
	int			n = sizeof(casos) / sizeof(casos[0]);
	int			i;
	int			falhas;
	char		*d;

	i = 0;
	falhas = 0;
	printf("<ft_strdup>\n");
	while (i < n)
	{
		d = ft_strdup(casos[i]);
		if (d == NULL)
		{
			printf("FALHA \"%s\" : retornou NULL\n", casos[i]);
			falhas++;
		}
		else if ((void *)d == (const void *)casos[i])
		{
			printf("FALHA \"%s\" : retornou o MESMO ponteiro (nao copiou)\n",
				casos[i]);
			falhas++;
			free(d);
		}
		else if (strcmp(d, casos[i]) != 0)
		{
			printf("FALHA \"%s\" : copia errada -> \"%s\"\n", casos[i], d);
			falhas++;
			free(d);
		}
		else
			free(d);
		i++;
	}
	if (falhas == 0)
		printf("[OK] Passou em todos os casos.\n");
	else
		printf("[X] %d falha(s).\n", falhas);
	printf("</ft_strdup>\n");
	return (falhas != 0);
}
