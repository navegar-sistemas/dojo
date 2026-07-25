# `checker` (bônus)

Programa separado que **executa** a receita em vez de calculá-la. Espelha o comportamento do
binário de referência em `assets/`.

## Contrato

Recebe a pilha `a` como lista de inteiros (primeiro argumento no topo), lê movimentos de stdin
— um por linha, até EOF — aplica cada um e responde:

| Situação | stdout | stderr | exit |
|---|---|---|---|
| `a` ordenada **e** `b` vazia ao final | `OK\n` | — | 0 |
| qualquer outro estado final | `KO\n` | — | 0 |
| argumento inválido | — | `Error\n` | 255 |
| instrução inexistente ou mal formada | — | `Error\n` | 255 |
| nenhum argumento | — | — | 0 |

Lista de movimentos vazia é entrada válida: uma pilha já ordenada com zero operações responde
`OK`.

As regras de validação dos argumentos são as mesmas do `push_swap`
([../01-contrato/entrada.md](../01-contrato/entrada.md)), incluindo a divisão por espaços que
faz `./checker "" 1` ser erro.

Esses valores foram observados no binário de referência `assets/checker_Mac`, e são o alvo do
programa próprio.

## Instruções aceitas

As 11 siglas exatas, uma por linha: `sa sb ss pa pb ra rb rr rra rrb rrr`.

A comparação é exata. `ra` seguido de `\n` é válido; `ra ` com espaço, `RA` em maiúsculas,
`ra;` ou linha vazia no meio da entrada são erro. A última linha pode ou não terminar em `\n`.

## Módulos

| Arquivo | Funções | Responsabilidade |
|---|---|---|
| `checker_bonus.c` | `main` + statics | orquestração e veredito |
| `read_ops_bonus.c` | `read_all`, extração de linha | leitura de stdin até EOF |
| `apply_op_bonus.c` | `apply_line` | sigla → `t_op` → chamada da operação |

Reaproveita sem alteração: `parse.c`, `parse_utils.c`, `stack.c`, `emit.c` e os quatro
`ops_*.c`. A lista de objetos compartilhados está em
[../02-restricoes/build.md](../02-restricoes/build.md).

## Modo silencioso

O contexto é montado com `counts = NULL`:

```c
ctx.a = a;
ctx.b = b;
ctx.counts = NULL;
```

Com isso `emit` retorna sem imprimir nem contar, e as mesmas 11 operações do `push_swap`
aplicam o efeito nas pilhas sem produzir saída. É esse ponteiro que permite o reaproveitamento
— ver [../03-arquitetura/tipos.md](../03-arquitetura/tipos.md).

## Leitura de stdin

Sem `get_next_line` disponível, a leitura é feita com `read` em blocos até EOF, acumulando num
buffer que cresce por realocação:

```
read_all(fd):
    buf = malloc(tamanho inicial)
    total = 0
    enquanto (lidos = read(fd, temp, TAM)) > 0:
        garante espaço para total + lidos + 1
        copia temp para buf + total
        total += lidos
    buf[total] = '\0'
    devolve buf
```

Ler tudo antes de aplicar é o que o enunciado descreve ("depois que todas as instruções forem
lidas, o programa deve executá-las"). Também simplifica o tratamento de erro: uma instrução
inválida no meio aborta antes de qualquer aplicação.

`read` devolvendo `-1` é tratado como erro. `0` é o EOF normal.

## Fluxo

1. `parse_flags` não se aplica — o checker não tem flags. Um argumento começando com `--` é
   token numérico inválido, portanto erro.
2. `parse_numbers` monta `a`; erro → `Error`, saída 255.
3. Zero números → não imprime nada, saída 0.
4. `b = stack_new(a->size)`, contexto com `counts = NULL`.
5. `read_all(0)`; erro de leitura → `Error`, saída 255.
6. Para cada linha até o fim do buffer: traduz e aplica; linha inválida → `Error`, saída 255.
7. `stack_is_sorted(a) && b->size == 0` → `OK`, senão `KO`. Saída 0.
8. Libera tudo.

## Verificação contra a referência

O binário de referência é o gabarito executável: as mesmas entradas precisam produzir as mesmas
respostas nos dois.

```bash
for caso in "3 2 1|sa
rra" "3 2 1|sa" "1 2 3|" "3 2 one|" "|"; do
  args="${caso%%|*}"; ops="${caso#*|}"
  meu=$(printf '%s\n' "$ops" | ./checker $args 2>&1; echo "exit=$?")
  ref=$(printf '%s\n' "$ops" | ./assets/checker_Mac $args 2>&1; echo "exit=$?")
  [ "$meu" = "$ref" ] && echo "OK  $args" || echo "DIFERE  $args: meu=[$meu] ref=[$ref]"
done
```
