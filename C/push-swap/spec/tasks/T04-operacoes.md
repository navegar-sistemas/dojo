# T04 — Operações

## Objetivo

As 11 operações aplicando o efeito nas pilhas e gravando a sigla no programa.

## Depende de

T03.

## Arquivos

- `ops_swap.c`, `ops_push.c`, `ops_rotate.c`, `ops_rrotate.c`

## Especificação

- [../03-arquitetura/modulos.md](../03-arquitetura/modulos.md) — contratos
- [../01-contrato/saida.md](../01-contrato/saida.md) — formato da receita

## Implementação

Todas com assinatura `void op_xx(t_ctx *c)` — um parâmetro só, por causa de
`-Wunused-parameter`.

| Arquivo | Conteúdo |
|---|---|
| `ops_swap.c` | `swap_top` (static), `op_sa`, `op_sb`, `op_ss` |
| `ops_push.c` | `move_top` (static), `op_pa`, `op_pb` |
| `ops_rotate.c` | `rotate_up` (static), `op_ra`, `op_rb`, `op_rr` |
| `ops_rrotate.c` | `rotate_down` (static), `op_rra`, `op_rrb`, `op_rrr` |

```c
static void	rotate_up(t_stack *s)
{
	int	tmp;

	if (s->size < 2)
		return ;
	tmp = s->data[0];
	ft_memmove(s->data, s->data + 1, (s->size - 1) * sizeof(int));
	s->data[s->size - 1] = tmp;
}
```

`rotate_down` é o espelho (último vira primeiro). `ft_memmove` e não `ft_memcpy`: origem e
destino se sobrepõem.

`move_top(from, to)` abre espaço em `to` com `ft_memmove`, grava `from->data[0]` em
`to->data[0]` e fecha o buraco em `from`. Retorna sem fazer nada se `from->size == 0`.

**Regras que valem para todas:**

- Movimento sem efeito possível não altera nada mas **ainda chama `emit`** — a sigla entra no
  programa.
- `op_ss`, `op_rr` e `op_rrr` chamam os helpers `static` nas duas pilhas e emitem **uma**
  operação. Chamar `op_ra` e `op_rb` dentro de `op_rr` gravaria duas.

## Pronto quando

O `main` temporário de T03 passa a aplicar uma receita à mão e o resultado é conferido contra o
checker de referência. O parsing só existe em T05, então esse `main` **ignora `argv`** e monta
a pilha `2 1 3 6 5 8` escrevendo direto em `data` — os números na linha de comando abaixo
existem só para o `checker_linux` receber a lista dele.

```bash
make re
norminette *.c *.h
```

Sequência de verificação: partindo de `2 1 3 6 5 8`, a receita
`sa pb pb pb ra rb rra rrb sa pa pa pa` precisa deixar `a = 1 2 3 5 6 8` e `b` vazia.

```bash
./push_swap 2 1 3 6 5 8 | ../assets/checker_linux 2 1 3 6 5 8    # OK (main temporário)
./push_swap 2 1 3 6 5 8 | wc -l                                  # 12
./push_swap 2 1 3 6 5 8 | cat -A                                 # só siglas e $
```

Verificações pontuais embutidas no `main`:

| Cenário | Esperado |
|---|---|
| `op_ra` n vezes numa pilha de n | pilha idêntica à original |
| `op_ra` seguido de `op_rra` | pilha idêntica à original |
| `op_sa` com 1 elemento | não altera, mas grava `sa` |
| `op_pa` com `b` vazia | não altera, mas grava `pa` |
| `op_rr` | grava uma operação, gira as duas pilhas |
| contexto com `prog = NULL` | nada é gravado, pilhas mudam |

O `main` (substitui o de T03; some em T06). Cada linha da tabela vira um `ko(...)`: falha
imprime `KO <caso>` no stderr, silêncio é verde. As verificações rodam num primeiro programa
que é descartado; a receita roda num programa novo, então o stdout fica só com as 12 siglas —
é isso que os pipes acima medem.

```c
#include "push_swap.h"

static void	ko(char *label, int ok)
{
	if (ok)
		return ;
	ft_putstr_fd("KO ", 2);
	ft_putendl_fd(label, 2);
}

static void	fill6(t_stack *s)
{
	s->data[0] = 2;
	s->data[1] = 1;
	s->data[2] = 3;
	s->data[3] = 6;
	s->data[4] = 5;
	s->data[5] = 8;
	s->size = 6;
}

static void	checks(t_ctx *c)
{
	int	i;

	i = -1;
	while (++i < 6)
		op_ra(c);
	ko("ra x6", c->a->data[0] == 2 && c->a->data[5] == 8);
	op_ra(c);
	op_rra(c);
	ko("ra+rra", c->a->data[0] == 2);
	op_rr(c);
	ko("rr", c->a->data[0] == 1 && c->prog->len == 9);
	op_pa(c);
	ko("pa vazia", c->a->size == 6 && c->b->size == 0);
	i = -1;
	while (++i < 5)
		op_pb(c);
	op_sa(c);
	ko("sa com 1", c->a->size == 1 && c->a->data[0] == 2);
	ko("grava sempre", c->prog->len == 16);
	prog_free(c->prog);
	c->prog = NULL;
	op_rb(c);
	ko("prog nulo", c->b->data[0] == 5);
}

static void	recipe(t_ctx *c)
{
	op_sa(c);
	op_pb(c);
	op_pb(c);
	op_pb(c);
	op_ra(c);
	op_rb(c);
	op_rra(c);
	op_rrb(c);
	op_sa(c);
	op_pa(c);
	op_pa(c);
	op_pa(c);
}

int	main(void)
{
	t_ctx	c;

	c.counts = NULL;
	c.bias = 0;
	c.up = NULL;
	c.a = stack_new(6);
	c.b = stack_new(6);
	c.prog = prog_new();
	if (c.a == NULL || c.b == NULL || c.prog == NULL)
		ps_die(&c);
	fill6(c.a);
	checks(&c);
	c.prog = prog_new();
	if (c.prog == NULL)
		ps_die(&c);
	c.b->size = 0;
	fill6(c.a);
	recipe(&c);
	prog_flush(&c);
	stack_free(c.a);
	stack_free(c.b);
	prog_free(c.prog);
	return (0);
}
```

```bash
valgrind --leak-check=full ./push_swap 2 1 3 6 5 8    # All heap blocks were freed
```
