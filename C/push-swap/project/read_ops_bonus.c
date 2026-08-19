#include "push_swap.h"

/*
** A realocação vive em sua própria função: embutida em read_all, o
** corpo chegaria a 27 linhas, acima do limite. Quatro parâmetros é
** o teto que a Norma permite.
*/
static char	*grow(char *buf, int total, char *tmp, int n)
{
	char	*dst;
	int		i;

	dst = malloc(total + n + 1);
	if (!dst)
	{
		free(buf);
		return (NULL);
	}
	i = 0;
	while (i < total)
	{
		dst[i] = buf[i];
		i++;
	}
	i = 0;
	while (i < n)
	{
		dst[total + i] = tmp[i];
		i++;
	}
	free(buf);
	return (dst);
}

/*
** Lê o stdin em blocos até o EOF. Ler tudo antes de aplicar qualquer
** coisa é o que o subject descreve, e isso faz uma instrução inválida
** abortar antes que uma única operação toque as pilhas.
*/
char	*read_all(int fd)
{
	char	tmp[1024];
	char	*buf;
	int		total;
	int		n;

	total = 0;
	buf = malloc(1);
	if (!buf)
		return (NULL);
	n = read(fd, tmp, 1024);
	while (n > 0)
	{
		buf = grow(buf, total, tmp, n);
		if (!buf)
			return (NULL);
		total += n;
		n = read(fd, tmp, 1024);
	}
	if (n < 0)
	{
		free(buf);
		return (NULL);
	}
	buf[total] = '\0';
	return (buf);
}
