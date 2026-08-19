#include "push_swap.h"

/*
** Despacho por desordem, o comportamento padrão. Cada regime roda um
** portfólio (run_portfolio): duas variantes de política de desempate
** do greedy e o algoritmo cuja contagem de operações certifica o
** limite do regime, mantendo o programa que saiu mais curto. Abaixo
** de 0.2 o certificador é o selection sort O(n²), até 0.5 o block
** sort O(n√n), a partir de 0.5 o radix O(n log n). O programa emitido
** nunca é mais longo que o do certificador, então o limite que o
** subject exige para o regime se sustenta por construção, enquanto o
** greedy fornece os programas curtos que os benchmarks pedem. cclass
** reporta a classe certificada do regime: é assim que o --bench
** mostra Adaptive / O(n√n) ou Adaptive / O(n log n) de acordo com a
** rota de fato tomada.
*/
void	sort_adaptive(t_ctx *c, t_conf *conf, double d)
{
	if (d < 0.2)
	{
		run_portfolio(c, conf, sort_simple);
		conf->cclass = "O(n²)";
	}
	else if (d < 0.5)
	{
		run_portfolio(c, conf, sort_medium);
		conf->cclass = "O(n√n)";
	}
	else
	{
		run_portfolio(c, conf, sort_complex);
		conf->cclass = "O(n log n)";
	}
	conf->name = "Adaptive";
}
