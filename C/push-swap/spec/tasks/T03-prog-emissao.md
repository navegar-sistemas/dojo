# T03 — Programa gravado e emissão

## Objetivo

Operações entram num `t_prog` em vez de irem para stdout; `prog_flush` imprime tudo de uma vez.

## Depende de

T02.

## Arquivos

- `prog.c`
- `emit.c`
- `utils.c` (só `ps_die` e `zero_counts`; as rotações e `isqrt` vêm em T07)

## Especificação

- [../03-arquitetura/tipos.md](../03-arquitetura/tipos.md) — `t_prog`, `t_ctx` e o significado de `prog`
- [../03-arquitetura/modulos.md](../03-arquitetura/modulos.md) — contratos
- [../02-restricoes/norma.md](../02-restricoes/norma.md) — por que a tabela de nomes é cadeia de `if`

## Implementação

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
`ps_die(c)`, não tem como devolver erro. `prog_flush` percorre o programa imprimindo
`op_name(op)` com `ft_putendl_fd(_, 1)` e, se `c->counts` não for `NULL`, incrementa
`counts[op]` na mesma iteração.

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

Nada é impresso aqui: `prog == NULL` é o modo executor do checker.

### `utils.c` (parcial)

`zero_counts` zera um `int[11]`. `ps_die` imprime `Error` em stderr, percorre a cadeia `up`
liberando `a`, `b` e `prog` de cada contexto, e sai com 1. Mora aqui — e não em `main.c` ou
`prog.c` — porque esses dois fecham as próprias cotas de funções.

## Pronto quando

Um `main` temporário monta um contexto com um `prog_new` e um `int[11]` zerado, grava uma
sequência à mão com `emit`, e confere flush e contagens. Não faz parte da entrega — some em T06.

```bash
make re
norminette *.c *.h
```

| Cenário | Esperado |
|---|---|
| `emit` de `OP_SA`, `OP_PB`, `OP_RRA` + `prog_flush` | stdout `sa\npb\nrra\n`, counts com 1 em cada |
| 100 `emit` seguidos | buffer cresce sem perder a ordem |
| contexto com `prog = NULL` | `emit` não grava; flush de um prog vazio não imprime nada |

```bash
./push_swap | cat -A          # só as siglas do teste, cada uma com $
valgrind --leak-check=full ./push_swap    # "All heap blocks were freed"
```
