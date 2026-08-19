#include "push_swap.h"

/*
** Cadeia de ifs em vez de uma tabela de busca: um array local com
** inicializador quebra DECL_ASSIGN_LINE, e a mesma tabela em escopo
** de arquivo é uma variável global, proibida pelo subject. 23 linhas,
** dentro das 25 que a Norma permite.
*/
char	*op_name(t_op op)
{
	if (op == OP_SA)
		return ("sa");
	if (op == OP_SB)
		return ("sb");
	if (op == OP_SS)
		return ("ss");
	if (op == OP_PA)
		return ("pa");
	if (op == OP_PB)
		return ("pb");
	if (op == OP_RA)
		return ("ra");
	if (op == OP_RB)
		return ("rb");
	if (op == OP_RR)
		return ("rr");
	if (op == OP_RRA)
		return ("rra");
	if (op == OP_RRB)
		return ("rrb");
	if (op == OP_RRR)
		return ("rrr");
	return ("");
}

/*
** No gerador, toda operação cai no programa gravado e nada é
** impresso aqui: imprimir é trabalho do prog_flush, uma vez que o
** programa final é escolhido. prog == NULL é o checker: aplica o
** efeito, não grava nada.
*/
void	emit(t_ctx *c, t_op op)
{
	if (c->prog == NULL)
		return ;
	prog_push(c, op);
}
