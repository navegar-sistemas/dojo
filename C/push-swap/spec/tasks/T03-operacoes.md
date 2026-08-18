# T03 — Operações e emissão

## Objetivo

As 11 operações aplicando o efeito nas pilhas e emitindo a sigla.

## Depende de

T02.

## Arquivos

- `emit.c`
- `ops_swap.c`, `ops_push.c`, `ops_rotate.c`, `ops_rrotate.c`

## Especificação

- [../01-contrato/saida.md](../01-contrato/saida.md) — formato da receita
- [../03-arquitetura/tipos.md](../03-arquitetura/tipos.md) — `t_ctx` e o significado de `counts`
- [../03-arquitetura/modulos.md](../03-arquitetura/modulos.md) — contratos
- [../02-restricoes/norma.md](../02-restricoes/norma.md) — por que a tabela de nomes é cadeia de `if`

## Implementação

### `emit.c`

```c
char	*op_name(t_op op);
void	emit(t_ctx *c, t_op op);
```

`op_name` é uma cadeia de 11 `if` devolvendo literais, terminada por `return ("")`. Array local
com inicializador viola a norma e tabela em escopo de arquivo é variável global.

```c
void	emit(t_ctx *c, t_op op)
{
	if (!c->counts)
		return ;
	c->counts[op]++;
	ft_putendl_fd(op_name(op), 1);
}
```

Contagem e impressão na mesma função é o que garante que `--bench` e stdout não divergem.

### Operações

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

static void	rotate_down(t_stack *s)
{
	int	tmp;

	if (s->size < 2)
		return ;
	tmp = s->data[s->size - 1];
	ft_memmove(s->data + 1, s->data, (s->size - 1) * sizeof(int));
	s->data[0] = tmp;
}
```

`ft_memmove` e não `ft_memcpy`: origem e destino se sobrepõem.

`move_top(t_stack *from, t_stack *to)` desloca `to->data` uma posição para a direita, grava
`from->data[0]` em `to->data[0]`, desloca `from->data` uma posição para a esquerda, ajusta os
dois `size`. Retorna sem fazer nada se `from->size == 0`.

**Regras que valem para todas:**

- Movimento sem efeito possível não altera nada mas **ainda chama `emit`**.
- `op_ss`, `op_rr` e `op_rrr` chamam os helpers `static` nas duas pilhas e emitem **uma** sigla.
  Chamar `op_ra` e `op_rb` dentro de `op_rr` emitiria duas linhas.

## Pronto quando

Um `main` temporário monta um contexto com `counts` apontando para um `int[11]` zerado, aplica
uma receita escrita à mão e o resultado é conferido contra o checker de referência.

```bash
make re
norminette *.c *.h
```

Sequência de verificação: partindo de `2 1 3 6 5 8`, a receita
`sa pb pb pb ra rb rra rrb sa pa pa pa` precisa deixar `a = 1 2 3 5 6 8` e `b` vazia.

```bash
./push_swap 2 1 3 6 5 8 | ../assets/checker_linux 2 1 3 6 5 8    # OK
./push_swap 2 1 3 6 5 8 | wc -l                                # 12
./push_swap 2 1 3 6 5 8 | cat -A                               # só siglas e $
```

Verificações pontuais no teste temporário:

| Cenário | Esperado |
|---|---|
| `op_ra` n vezes numa pilha de n | pilha idêntica à original |
| `op_ra` seguido de `op_rra` | pilha idêntica à original |
| `op_sa` com 1 elemento | não altera, mas emite `sa` |
| `op_pa` com `b` vazia | não altera, mas emite `pa` |
| `op_rr` | emite uma linha, gira as duas pilhas |
| contexto com `counts = NULL` | não imprime nada, pilhas mudam |

```bash
valgrind --leak-check=full ./push_swap 2 1 3 6 5 8
```
