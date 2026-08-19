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

O corpo completo está em [../03-arquitetura/fluxo.md](../03-arquitetura/fluxo.md). Pontos que
decidem se compila e se o erro é seguro:

**`setup` zera o contexto inteiro na entrada** — `a`, `b`, `counts`, `bias`, `prog`, `up` —
para que `ps_die(&c)` seja seguro a partir de qualquer ponto de falha. Cria `b` **e** `prog`
juntos e testa os dois.

**O erro mora em `ps_die`** (`utils.c`, T03), não aqui: `main.c` fecha em 4 funções.

**`cleanup` devolve `int`** para permitir `return (cleanup(&c));`.

**Zerar `counts`:** `int counts[11];` no topo e `zero_counts(counts)` — a norma proíbe
declaração com atribuição.

**`prog_flush` roda depois de `run_strategy` e antes de qualquer coisa condicionada a
`--bench`** — é ele que imprime a receita.

Nesta tarefa, quatro chamadas ainda não têm implementação: `compute_disorder` (T08),
`build_ranks` (T09), as `sort_*` (T07 em diante) e `bench_print` (T14). Declare stubs que
retornam sem fazer nada — `compute_disorder` devolvendo `0.0` e `build_ranks` devolvendo 1 —
para o programa linkar e os caminhos de erro ficarem testáveis. Cada tarefa seguinte troca um
stub pela versão real.

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
