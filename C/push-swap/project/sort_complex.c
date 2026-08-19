#include "push_swap.h"

/*
** Bits necessários para o maior rank, n - 1. Usar n desperdiçaria uma
** passada inteira em potências de dois: com n = 256 o maior rank é
** 255, que cabe em 8 bits.
*/
static int	bit_count(int n)
{
	int	bits;

	bits = 0;
	while ((n - 1) >> bits)
		bits++;
	return (bits);
}

/*
** Uma partição estável. size é capturado antes do loop: a->size
** diminui a cada pb, e lê-lo na condição pararia a varredura cedo
** demais, deixando elementos não examinados.
*/
static void	radix_pass(t_ctx *c, int bit)
{
	int	i;
	int	size;

	i = 0;
	size = c->a->size;
	while (i < size)
	{
		if (((c->a->data[0] >> bit) & 1) == 0)
			op_pb(c);
		else
			op_ra(c);
		i++;
	}
	while (c->b->size > 0)
		op_pa(c);
}

/*
** Radix binário LSD sobre os ranks. Cada passada mantém a ordem
** fixada pelas anteriores dentro de cada grupo, então após
** ceil(log2 n) passadas a pilha está ordenada. A contagem é fechada:
** bits * n mais um pa por elemento com aquele bit zerado, a mesma
** para toda entrada de um dado tamanho (1084 para n = 100, 6784 para
** n = 500).
*/
void	sort_complex(t_ctx *c, t_conf *conf)
{
	int	bits;
	int	bit;

	conf->name = "Complex";
	conf->cclass = "O(n log n)";
	if (c->a->size <= 3)
	{
		sort_tiny(c);
		return ;
	}
	if (stack_is_sorted(c->a))
		return ;
	bits = bit_count(c->a->size);
	bit = 0;
	while (bit < bits)
	{
		radix_pass(c, bit);
		bit++;
	}
}
