# T03 — Programa gravado e emissão

## Objetivo

Toda operação será **gravada** num programa em vez de impressa na hora; `prog_flush` imprime
tudo de uma vez no fim.

## Por que isso existe — e por que vem antes das operações

O `--adaptive` (T13) gera até três programas candidatos e imprime só o mais curto. Para
comparar candidatos, eles precisam existir inteiros antes de qualquer byte sair em stdout —
então neste projeto **nada imprime durante a ordenação**: `emit` grava no `t_prog`, e quem
imprime é o `prog_flush`, uma vez, no fim
([../03-arquitetura/tipos.md](../03-arquitetura/tipos.md)).

E vem antes de T04 por um motivo simples: as operações chamam `emit`. Construindo o gravador
primeiro, os `op_*` já nascem gravando e nunca são reescritos. O preço é esta tarefa ser pura
infraestrutura — o primeiro comportamento visível de push_swap chega em T04.

## Depende de

T02.

## Arquivos

- `prog.c`
- `emit.c`
- `utils.c` (só `ps_die` e `zero_counts`; as rotações e `isqrt` vêm em T07)
- `push_swap.h` (ganha `t_op`, `t_prog`, `t_ctx` e os protótipos)

## Especificação

- [../03-arquitetura/tipos.md](../03-arquitetura/tipos.md) — `t_prog`, `t_ctx` e o significado de `prog`
- [../03-arquitetura/modulos.md](../03-arquitetura/modulos.md) — contratos
- [../02-restricoes/norma.md](../02-restricoes/norma.md) — por que a tabela de nomes é cadeia de `if`

## Implementação

### `t_ctx` já nasce completo

Dois campos só ganham uso mais adiante: `bias` (desempate do guloso, T12) e `up` (cadeia de
simulações do portfólio, T13). Declará-los agora evita mexer na struct depois; ficam zerados
até as tarefas deles.

### `prog.c`

```c
t_prog	*prog_new(void);
void	prog_free(t_prog *p);
void	prog_push(t_ctx *c, t_op op);
void	prog_flush(t_ctx *c);
```

`prog_new` aloca a struct e um buffer de 64 `t_op`; falha devolve `NULL` sem vazar.
`prog_free` aceita `NULL`. `prog_push` grava e delega o crescimento à `static prog_grow`, que
dobra a capacidade com `malloc` + `ft_memcpy` + `free` — falha de alocação aí dentro morre em
`ps_die(c)`. `prog_flush` percorre o programa imprimindo `op_name(op)` com
`ft_putendl_fd(_, 1)` e, se `c->counts` não for `NULL`, incrementa `counts[op]` na mesma
iteração.

### `emit.c`

`op_name` é a cadeia de 11 `if` devolvendo literais, terminada por `return ("")` — 23 linhas.

```c
void	emit(t_ctx *c, t_op op)
{
	if (c->prog == NULL)
		return ;
	prog_push(c, op);
}
```

`prog == NULL` é o modo executor do checker: aplica efeito, não grava nada.

### `utils.c` (parcial)

`zero_counts` zera um `int[11]`. `ps_die` imprime `Error` em stderr, percorre a cadeia `up`
liberando `a`, `b` e `prog` de cada contexto, e sai com 1. O laço sobre `up` parece exagero
agora — até T13 a cadeia tem um elo só — mas é o que deixa uma falha dentro de uma simulação
do portfólio liberar também o contexto real. `ps_die` mora aqui, e não em `main.c` ou
`prog.c`, porque esses dois fecham as próprias cotas de funções.

## Pronto quando

```bash
make re
norminette *.c *.h
```

`main` temporário (some em T06) — grava quatro operações, dá o flush e confere uma contagem:

```c
#include "push_swap.h"

int	main(void)
{
	t_ctx	c;
	int		counts[11];

	c.a = NULL;
	c.b = NULL;
	c.bias = 0;
	c.up = NULL;
	c.counts = counts;
	zero_counts(counts);
	c.prog = prog_new();
	if (!c.prog)
		return (1);
	emit(&c, OP_SA);
	emit(&c, OP_PB);
	emit(&c, OP_PB);
	emit(&c, OP_RRA);
	prog_flush(&c);
	ft_putnbr_fd(counts[OP_PB], 1);
	ft_putchar_fd('\n', 1);
	prog_free(c.prog);
	return (0);
}
```

Saída esperada:

```
sa
pb
pb
rra
2
```

Duas bordas para conferir à mão no mesmo `main`:

- com `c.prog = NULL` no lugar do `prog_new`, `emit` não grava nada — e `prog_flush` não é
  chamado nesse modo (o checker nunca chama);
- gravando 100+ operações num laço, o buffer dobra e a ordem se mantém.

```bash
valgrind --leak-check=full ./push_swap    # "All heap blocks were freed"
```
