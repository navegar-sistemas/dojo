/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   striteri.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/23 11:00:00 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/23 11:00:00 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void	ft_striteri(char *s, void (*f)(unsigned int, char *));

/* Copia s p/ buffer MUTAVEL no heap (literal de string seria read-only;
   escrever nele = crash). Tamanho exato -> over-read vira erro (asan). */
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

/* f's de teste. Como recebem char* (endereco), ALTERAM in-place:
   upper -> maiuscula                (prova que *c chega/escreve certo)
   index -> *c = 'a'+i               (prova que o INDICE vai 0,1,2,...)
   combo -> *c = *c + i              (prova c E i juntos) */
static void	f_upper(unsigned int i, char *c)
{
	(void)i;
	if (*c >= 'a' && *c <= 'z')
		*c -= 32;
}

static void	f_index(unsigned int i, char *c)
{
	*c = 'a' + i;
}

static void	f_combo(unsigned int i, char *c)
{
	*c = *c + i;
}

int	main(void)
{
	/* {s, f, esperado}. ft_striteri NAO aloca e retorna void: altera s.
	   f==NULL -> nao mexe (esperado == s). s==NULL -> nao crasha.
	   "" -> "" (no-op). Rode com asan/valgrind (make striteri ja faz). */
	struct s_caso
	{
		char const	*s;
		void		(*f)(unsigned int, char *);
		char const	*esperado;
	}	casos[] = {
	{"hello", f_upper, "HELLO"}, {"World!", f_upper, "WORLD!"},
	{"zzzzz", f_index, "abcde"}, {"AAAAA", f_combo, "ABCDE"},
	{"", f_upper, ""}, {"a", f_upper, "A"},
	{"42 Sao Paulo", f_upper, "42 SAO PAULO"},
	{"abc", NULL, "abc"}, {NULL, f_upper, NULL}};
	int		n = sizeof(casos) / sizeof(casos[0]);
	int		i;
	int		falhas;
	char	*buf;

	i = 0;
	falhas = 0;
	printf("<ft_striteri>\n");
	while (i < n)
	{
		if (casos[i].s == NULL)
		{
			ft_striteri(NULL, casos[i].f);
			printf("[ok] s=NULL nao crashou\n");
			i++;
			continue ;
		}
		buf = heapdup(casos[i].s);
		ft_striteri(buf, casos[i].f);
		if (strcmp(buf, casos[i].esperado) != 0)
			(printf("FALHA s=\"%s\" : ft=\"%s\" esperado=\"%s\"\n",
					casos[i].s, buf, casos[i].esperado), falhas++);
		free(buf);
		i++;
	}
	if (falhas == 0)
		printf("[OK] Passou em todos os casos.\n");
	else
		printf("[X] %d falha(s).\n", falhas);
	printf("</ft_striteri>\n");
	return (falhas != 0);
}
