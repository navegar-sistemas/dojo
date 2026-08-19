# T06 — Orquestração do `main`

## Objetivo

O programa liga parsing, contexto, programa gravado e despacho, com todos os caminhos de erro
e silêncio corretos. Nenhuma estratégia existe ainda.

## Depende de

T04, T05.

## Arquivos

- `main.c`

## Especificação

- [../03-arquitetura/fluxo.md](../03-arquitetura/fluxo.md) — sequência completa e as ordens fixas
- [../01-contrato/saida.md](../01-contrato/saida.md) — canais e códigos

## Implementação

Quatro funções:

| Função | Papel |
|---|---|
| `main` | sequência principal |
| `setup` (static) | zera `conf` e o contexto inteiro, lê flags, monta pilhas e programa |
| `run_strategy` (static) | cadeia de `if` sobre `conf.strategy` |
| `cleanup` (static) | libera pilhas e programa, devolve 0 |

[../03-arquitetura/fluxo.md](../03-arquitetura/fluxo.md) mostra o **estado final** de
`main.c`; `setup` e `cleanup` já nascem exatamente como estão lá. Pontos que decidem se
compila e se o erro é seguro:

**`setup` zera o contexto inteiro na entrada** — `a`, `b`, `counts`, `bias`, `prog`, `up` —
para que `ps_die(&c)` seja seguro a partir de qualquer ponto de falha. Cria `b` **e** `prog`
juntos e testa os dois.

**O erro mora em `ps_die`** (`utils.c`, T03), não aqui: `main.c` fecha em 4 funções.

**`cleanup` devolve `int`** para permitir `return (cleanup(&c));`.

**Zerar `counts`:** `int counts[11];` no topo e `zero_counts(counts)` — a norma proíbe
declaração com atribuição.

**`prog_flush` roda depois de `run_strategy` e antes de qualquer coisa condicionada a
`--bench`** — é ele que imprime a receita.

O `main` do fluxo final chama coisas que ainda não existem — `compute_disorder` (T08),
`build_ranks` (T09), as `sort_*` (T07 em diante), `bench_print` (T14). **Nenhum stub de função
é necessário**: o stub fica no ponto de chamada, e cada tarefa seguinte troca o seu.
`run_strategy` e `main` nascem assim:

```c
static void	run_strategy(t_ctx *c, t_conf *conf, double d)
{
	(void)c;
	(void)conf;
	(void)d;
}

int	main(int argc, char **argv)
{
	t_conf	conf;
	t_ctx	c;
	int		counts[11];
	double	d;

	if (!setup(argc, argv, &conf, &c))
		ps_die(&c);
	if (c.a->size == 0)
		return (cleanup(&c));
	zero_counts(counts);
	c.counts = counts;
	d = 0.0;
	run_strategy(&c, &conf, d);
	prog_flush(&c);
	return (cleanup(&c));
}
```

| Ponto do fluxo final | Em T06 | Vira real em |
|---|---|---|
| `d = compute_disorder(c.a);` | `d = 0.0;` | T08 |
| `if (!build_ranks(c.a)) ps_die(&c);` | linha ausente | T09 |
| corpo de `run_strategy` | `(void)` nos três parâmetros | T07, T10, T11, T12, T13 |
| `if (conf.bench) bench_print(&c, &conf, d);` | linha ausente | T14 |

O binário linka só com os arquivos de T01–T05 — se o link exigir qualquer `sort_*`, algo do
estado final entrou antes da hora.

## Pronto quando

```bash
make re
norminette *.c *.h
```

Todos os erros de [../06-aceitacao/casos.md](../06-aceitacao/casos.md) A5 (bateria registrada
em T05) e todos os casos silenciosos de A6, agora pelo binário completo:

```bash
./push_swap 0 one 2 3 2>&1 >/dev/null      # Error
./push_swap 0 one 2 3 2>/dev/null | wc -c  # 0
./push_swap; echo "exit=$?"                # nada, 0
./push_swap 42; echo "exit=$?"             # nada, 0
./push_swap --simple --medium 3 2 1; echo "exit=$?"   # Error, 1
./push_swap --simple --simple 3 2 1 ; echo "exit=$?"  # nada, 0 (estratégia é stub)
./push_swap --bench --bench 3 2 1   ; echo "exit=$?"  # nada, 0
```

Entrada válida e não ordenada ainda não imprime nada, porque nenhuma estratégia existe. Isso é
o esperado até T07.

```bash
valgrind --leak-check=full ./push_swap 3 2 1
valgrind --leak-check=full ./push_swap 0 one 2 3
```
