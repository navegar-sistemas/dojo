/*
** Parte obrigatoria: conversao desconhecida e '%' no fim do formato.
** O padrao C deixa esses casos indefinidos, entao o esperado aqui e o
** contrato do proprio projeto, nao a saida da libc.
*/
#include <stdio.h>
#include "ft_printf.h"
#include "capture.h"

static int	run(const char *fmt, int arg, const char *want, int want_ret)
{
	char	out[CAP_SIZE];
	int		ret;

	cap_begin();
	ret = ft_printf(fmt, arg);
	cap_end(out);
	return (check(fmt, out, ret, want, want_ret));
}

int	main(void)
{
	int	fails;

	fails = 0;
	fails += run("%z", 0, "%z", 2);
	fails += run("a%zb", 0, "a%zb", 4);
	fails += run("%-5d|", 42, "%-5d|", 5);
	fails += run("%-5d %d", 42, "%-5d 42", 7);
	fails += run("abc%", 0, "abc", -1);
	fails += run("%", 0, "", -1);
	printf("%s (%d falha(s))\n", fails ? "FALHOU" : "PASSOU", fails);
	return (fails != 0);
}
