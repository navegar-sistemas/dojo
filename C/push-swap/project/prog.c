#include "push_swap.h"

/*
** 64 é um início confortável: entradas minúsculas nunca crescem, e a
** duplicação alcança os poucos milhares de operações de n = 500 em
** uma dezena de realocações.
*/
t_prog	*prog_new(void)
{
	t_prog	*p;

	p = malloc(sizeof(t_prog));
	if (!p)
		return (NULL);
	p->ops = malloc(sizeof(t_op) * 64);
	if (!p->ops)
	{
		free(p);
		return (NULL);
	}
	p->len = 0;
	p->cap = 64;
	return (p);
}

void	prog_free(t_prog *p)
{
	if (p == NULL)
		return ;
	free(p->ops);
	free(p);
}

/*
** A duplicação mantém prog_push amortizado O(1). Falha de alocação
** aborta via ps_die, que libera todo contexto ao longo da cadeia de
** simulação.
*/
static void	prog_grow(t_ctx *c)
{
	t_op	*next;
	t_prog	*p;

	p = c->prog;
	next = malloc(sizeof(t_op) * p->cap * 2);
	if (next == NULL)
		ps_die(c);
	ft_memcpy(next, p->ops, sizeof(t_op) * p->len);
	free(p->ops);
	p->ops = next;
	p->cap = p->cap * 2;
}

void	prog_push(t_ctx *c, t_op op)
{
	if (c->prog->len == c->prog->cap)
		prog_grow(c);
	c->prog->ops[c->prog->len] = op;
	c->prog->len++;
}

/*
** Imprime o programa escolhido e preenche os contadores do --bench
** na mesma passada, para que os contadores nunca possam divergir do
** stdout.
*/
void	prog_flush(t_ctx *c)
{
	int	i;

	i = 0;
	while (i < c->prog->len)
	{
		if (c->counts != NULL)
			c->counts[c->prog->ops[i]]++;
		ft_putendl_fd(op_name(c->prog->ops[i]), 1);
		i++;
	}
}
