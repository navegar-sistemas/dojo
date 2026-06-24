/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   strmapi.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/23 10:00:00 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/23 10:00:00 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char	*ft_strmapi(char const *s, char (*f)(unsigned int, char));

/* Fonte no HEAP de tamanho exato -> over-read de s vira erro detectavel
   (valgrind/asan). */
static char	*heapdup(const char *s)
{
	size_t	n;
	char	*d;

	n = strlen(s) + 1;
	d = malloc(n);
	if (d)
		memcpy(d, s, n);
	return (d);
}

/* f's de teste. Cada uma prova algo:
   ident  -> ignora i, devolve c  (resultado == s)
   upper  -> maiuscula letras     (prova que c chega certo)
   index  -> devolve 'a'+i        (prova que o INDICE chega 0,1,2,...)
   combo  -> devolve c+i          (prova que c E i chegam juntos) */
static char	f_ident(unsigned int i, char c)
{
	(void)i;
	return (c);
}

static char	f_upper(unsigned int i, char c)
{
	(void)i;
	if (c >= 'a' && c <= 'z')
		return (c - 32);
	return (c);
}

static char	f_index(unsigned int i, char c)
{
	(void)c;
	return ('a' + i);
}

static char	f_combo(unsigned int i, char c)
{
	return (c + i);
}

int	main(void)
{
	/* {s, f, esperado}. ft_strmapi ALOCA: free() + checar NULL.
	   s==NULL ou f==NULL -> NULL. "" -> "". Rode com asan/valgrind
	   (make strmapi ja faz) p/ leak e over-read. */
	struct s_caso
	{
		char const	*s;
		char		(*f)(unsigned int, char);
		char const	*esperado;
	}	casos[] = {
	{"hello", f_ident, "hello"}, {"hello", f_upper, "HELLO"},
	{"World!", f_upper, "WORLD!"}, {"zzzzz", f_index, "abcde"},
	{"AAAAA", f_combo, "ABCDE"}, {"", f_ident, ""}, {"a", f_upper, "A"},
	{"42 Sao Paulo", f_ident, "42 Sao Paulo"},
	{NULL, f_ident, NULL}, {"x", NULL, NULL}};
	int		n = sizeof(casos) / sizeof(casos[0]);
	int		i;
	int		falhas;
	char	*src;
	char	*got;

	i = 0;
	falhas = 0;
	printf("<ft_strmapi>\n");
	while (i < n)
	{
		if (casos[i].s)
			src = heapdup(casos[i].s);
		else
			src = NULL;
		got = ft_strmapi(src, casos[i].f);
		if (casos[i].esperado == NULL && got != NULL)
			(printf("FALHA s=\"%s\" : esperava NULL, veio \"%s\"\n",
					casos[i].s, got), falhas++);
		else if (casos[i].esperado != NULL && (got == NULL
				|| strcmp(got, casos[i].esperado) != 0))
			(printf("FALHA s=\"%s\" : ft=\"%s\" esperado=\"%s\"\n",
					casos[i].s, got, casos[i].esperado), falhas++);
		free(got);
		free(src);
		i++;
	}
	if (falhas == 0)
		printf("[OK] Passou em todos os casos.\n");
	else
		printf("[X] %d falha(s).\n", falhas);
	printf("</ft_strmapi>\n");
	return (falhas != 0);
}
