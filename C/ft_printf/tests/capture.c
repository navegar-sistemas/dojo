#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "capture.h"

static int	g_pipe[2];
static int	g_saved;

/* Redireciona o fd 1 para um pipe; a saida deve caber no buffer do pipe. */
void	cap_begin(void)
{
	fflush(stdout);
	if (pipe(g_pipe) < 0)
	{
		perror("pipe");
		exit(2);
	}
	g_saved = dup(1);
	dup2(g_pipe[1], 1);
	close(g_pipe[1]);
}

int	cap_end(char *buf)
{
	int	n;

	fflush(stdout);
	dup2(g_saved, 1);
	close(g_saved);
	n = (int)read(g_pipe[0], buf, CAP_SIZE - 1);
	close(g_pipe[0]);
	if (n < 0)
		n = 0;
	buf[n] = '\0';
	return (n);
}

int	check(const char *label, const char *got, int got_ret,
		const char *want, int want_ret)
{
	if (strcmp(got, want) == 0 && got_ret == want_ret)
	{
		printf("OK     %-22s [%s] ret=%d\n", label, got, got_ret);
		return (0);
	}
	printf("FALHA  %-22s obtido [%s] ret=%d | esperado [%s] ret=%d\n",
		label, got, got_ret, want, want_ret);
	return (1);
}
