# T05 — Orquestração do `main`

## Objetivo

O programa liga parsing, contexto e despacho, com todos os caminhos de erro e silêncio
corretos. Nenhuma estratégia existe ainda.

## Depende de

T03, T04.

## Arquivos

- `main.c`

## Especificação

- [../03-arquitetura/fluxo.md](../03-arquitetura/fluxo.md) — sequência completa e as ordens fixas
- [../01-contrato/saida.md](../01-contrato/saida.md) — canais e códigos

## Implementação

Três funções:

| Função | Papel |
|---|---|
| `main` | os 11 passos do fluxo |
| `run_strategy` (static) | cadeia de `if` sobre `conf.strategy` |
| `fail` (static) | `Error` em stderr, liberação, `exit(1)` |

```c
static void	fail(t_stack *a, t_stack *b)
{
	ft_putendl_fd("Error", 2);
	stack_free(a);
	stack_free(b);
	exit(1);
}
```

`stack_free` aceitando `NULL` é o que permite chamar `fail` de qualquer ponto sem testar cada
ponteiro.

Sequência do `main`:

1. `conf` zerada com `strategy = STRAT_NONE`, `bench = 0`, `name`/`cclass` `NULL`.
2. `parse_flags` → falha chama `fail(NULL, NULL)`.
3. `strategy == STRAT_NONE` → `STRAT_ADAPTIVE`.
4. `parse_numbers` → `NULL` chama `fail(NULL, NULL)`.
5. `a->size == 0` → `stack_free(a)`, retorna 0.
6. `b = stack_new(a->size)` → `NULL` chama `fail(a, NULL)`.
7. `counts` local zerado, `ctx = {a, b, counts}`.
8. `d = compute_disorder(a)` — nesta tarefa ainda não existe; use `0.0` e substitua em T07.
9. `run_strategy(&ctx, &conf, d)`.
10. `conf.bench` → `bench_print` (T12).
11. Libera e retorna 0.

Nesta tarefa `run_strategy` chama funções ainda não implementadas. Duas saídas: declarar
protótipos vazios que retornam sem fazer nada, ou deixar `run_strategy` sem corpo útil e
preencher em T06. A primeira mantém o programa linkando e testável.

Zerar `counts`: `int counts[11];` no topo e um `while` de 11 posições — a norma proíbe
declaração com atribuição, então `= {0}` está fora.

## Pronto quando

```bash
make re
norminette *.c *.h
```

Todos os erros de [../06-aceitacao/casos.md](../06-aceitacao/casos.md) A5 e todos os casos
silenciosos de A6, agora pelo binário completo:

```bash
./push_swap 0 one 2 3 2>&1 >/dev/null    # Error
./push_swap 0 one 2 3 2>/dev/null | wc -c  # 0
./push_swap; echo "exit=$?"              # nada, 0
./push_swap 42; echo "exit=$?"           # nada, 0
./push_swap --simple --medium 3 2 1; echo "exit=$?"   # Error, 1
```

Entrada válida e não ordenada ainda não imprime nada, porque nenhuma estratégia existe. Isso é
o esperado até T06.

```bash
leaks --atExit -- ./push_swap 3 2 1
leaks --atExit -- ./push_swap 0 one 2 3
```
