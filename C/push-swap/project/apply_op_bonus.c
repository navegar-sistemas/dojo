#include "push_swap.h"

/*
** Correspondência exata de len bytes: o literal também precisa
** terminar ali, senão "r" combinaria com "ra". "ra" é válido; "ra "
** com espaço, "RA" e "ra;" não são.
*/
static int	same(const char *s, int len, char *lit)
{
	int	i;

	i = 0;
	while (i < len)
	{
		if (lit[i] == '\0' || s[i] != lit[i])
			return (0);
		i++;
	}
	return (lit[len] == '\0');
}

int	apply_rot(t_ctx *c, const char *s, int len)
{
	if (same(s, len, "ra"))
		op_ra(c);
	else if (same(s, len, "rb"))
		op_rb(c);
	else if (same(s, len, "rr"))
		op_rr(c);
	else if (same(s, len, "rra"))
		op_rra(c);
	else if (same(s, len, "rrb"))
		op_rrb(c);
	else if (same(s, len, "rrr"))
		op_rrr(c);
	else
		return (0);
	return (1);
}

/*
** Despachar as 11 instruções em uma única função fecha em exatamente
** 25 linhas, o limite sem folga; as seis rotações vão para apply_rot
** e ambos os corpos ficam bem abaixo disso. Uma linha vazia, len ==
** 0, não é uma instrução válida.
*/
int	apply_line(t_ctx *c, const char *s, int len)
{
	if (len == 0)
		return (0);
	if (same(s, len, "sa"))
		op_sa(c);
	else if (same(s, len, "sb"))
		op_sb(c);
	else if (same(s, len, "ss"))
		op_ss(c);
	else if (same(s, len, "pa"))
		op_pa(c);
	else if (same(s, len, "pb"))
		op_pb(c);
	else
		return (apply_rot(c, s, len));
	return (1);
}
