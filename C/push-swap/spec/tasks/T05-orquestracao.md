# T05 — Orquestração do `main`

## Objetivo

O programa liga parsing, contexto e despacho, com todos os caminhos de erro e silêncio
corretos. Nenhuma estratégia existe ainda.

## Depende de

T03, T04.

## Arquivos

- `main.c`
- `utils.c` (só `zero_counts`; o resto do arquivo vem em T06)

## Especificação

- [../03-arquitetura/fluxo.md](../03-arquitetura/fluxo.md) — sequência completa e as ordens fixas
- [../01-contrato/saida.md](../01-contrato/saida.md) — canais e códigos

## Implementação

Cinco funções — a cota inteira do arquivo. Com menos, o `main` passa de 25 linhas:

| Função | Papel |
|---|---|
| `main` | sequência principal |
| `setup` (static) | zera `conf` e `ctx`, lê flags, monta as pilhas |
| `run_strategy` (static) | cadeia de `if` sobre `conf.strategy` |
| `fail` (static) | `Error` em stderr, liberação, `exit(1)` |
| `cleanup` (static) | liberação, devolve 0 |

`zero_counts` vai para `utils.c`, não cabe aqui.

O corpo completo das cinco funções está em
[../03-arquitetura/fluxo.md](../03-arquitetura/fluxo.md). Pontos que decidem se compila:

**`fail` recebe o `t_ctx`, não dois `t_stack *`.** Como `setup` zera `c->a` e `c->b` na primeira
linha, `fail(&c)` é seguro a partir de qualquer ponto de falha, inclusive antes de qualquer
alocação. Combinado com `stack_free(NULL)` sendo inofensivo, não há um único teste de ponteiro
no caminho de erro.

**`setup` tem 4 parâmetros** — o teto da norma. Não há espaço para um quinto.

**`cleanup` devolve `int`** para permitir `return (cleanup(&c));`, economizando duas linhas no
`main`.

**Zerar `counts`:** `int counts[11];` no topo e `zero_counts(counts)` — a norma proíbe
declaração com atribuição, então `= {0}` está fora.

Nesta tarefa, três chamadas ainda não têm implementação: `compute_disorder` (T07),
`build_ranks` (T08) e as `sort_*` (T06 em diante), além de `bench_print` (T12). Declare stubs
que retornam sem fazer nada — `compute_disorder` devolvendo `0.0` e `build_ranks` devolvendo 1
— para o programa linkar e os caminhos de erro ficarem testáveis. Cada tarefa seguinte troca um
stub pela versão real.

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

Flags repetidas não são erro:

```bash
./push_swap --simple --simple 3 2 1 ; echo "exit=$?"   # nada, 0
./push_swap --bench --bench 3 2 1   ; echo "exit=$?"   # nada, 0
```

```bash
valgrind --leak-check=full ./push_swap 3 2 1
valgrind --leak-check=full ./push_swap 0 one 2 3
```
