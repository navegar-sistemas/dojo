# `checker` (bônus)

Programa separado que **executa** a receita em vez de calculá-la. Espelha o comportamento do
binário de referência em `../assets/`.

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

Esses valores foram observados no binário de referência `../assets/checker_linux`, e são o
alvo do programa próprio.

## Instruções aceitas

As 11 siglas exatas, uma por linha: `sa sb ss pa pb ra rb rr rra rrb rrr`.

A comparação é exata. `ra` seguido de `\n` é válido; `ra ` com espaço, `RA` em maiúsculas e
`ra;` são erro.

**Toda linha precisa terminar em `\n`, inclusive a última.** Uma sigla no fim da entrada sem a
quebra é `Error`, não uma instrução válida. Linha vazia em qualquer posição também é `Error`.
Entrada completamente vazia, por outro lado, é válida: zero instruções.

Comportamento do binário de referência, que é o alvo:

| Entrada em stdin | `3 2 1` | `1 2 3` |
|---|---|---|
| `sa\nrra\n` | `OK` | — |
| `ra\n` | `KO` | — |
| `ra` sem quebra | `Error` | `Error` |
| `sa\nrra` sem quebra final | `Error` | `Error` |
| `\n` (linha vazia) | `Error` | `Error` |
| `sa\n\nrra\n` (vazia no meio) | `Error` | `Error` |
| nenhum byte | `KO` | `OK` |

## Módulos

| Arquivo | Funções | Responsabilidade |
|---|---|---|
| `checker_bonus.c` | `reject_flags`, `fail_ck`, `run_all`, `cleanup_ck` (static) + `main` | rejeição de `--`, erro, laço de linhas, veredito |
| `read_ops_bonus.c` | `grow` (static) + `read_all` | leitura de stdin até EOF |
| `apply_op_bonus.c` | `same` (static) + `apply_line`, `apply_rot` | sigla → operação |

A separação não é estética: `read_all` fecha em exatamente 25 linhas de corpo — o limite da
norma, sem folga — mesmo com a realocação extraída para `grow`; embutida, passaria. E
`apply_line` despachando as 11 siglas numa função só também fecharia em 25: as seis rotações
vão para `apply_rot` (`apply_line` termina em `return (apply_rot(c, s, len));`).

Reaproveita sem alteração: `parse.c`, `parse_utils.c`, `stack.c`, `emit.c`, `prog.c`,
`utils.c` e os quatro `ops_*.c`. A lista de objetos compartilhados e o motivo de `prog.o` e
`utils.o` entrarem nela estão em [../02-restricoes/build.md](../02-restricoes/build.md).

## Modo silencioso

O contexto inteiro é zerado com `ft_memset(&c, 0, sizeof(t_ctx))`, o que deixa
**`prog == NULL`**: `emit` retorna sem gravar nada, e as mesmas 11 operações do `push_swap`
aplicam o efeito nas pilhas sem produzir saída nem alocação. É esse ponteiro que permite o
reaproveitamento — ver [../03-arquitetura/tipos.md](../03-arquitetura/tipos.md).

## Leitura de stdin

Sem `get_next_line` disponível, a leitura é feita com `read` em blocos de 1024 bytes até EOF,
acumulando num buffer que cresce por realocação:

```
grow(buf, total, tmp, n):
    novo = malloc(total + n + 1)
    se novo == NULL: libera buf; devolve NULL
    copia buf[0..total) e tmp[0..n) para novo
    libera buf
    devolve novo

read_all(fd):
    total = 0
    buf = malloc(1)
    se buf == NULL: devolve NULL
    n = read(fd, tmp, 1024)
    enquanto n > 0:
        buf = grow(buf, total, tmp, n)
        se buf == NULL: devolve NULL
        total += n
        n = read(fd, tmp, 1024)
    se n < 0: libera buf; devolve NULL
    buf[total] = '\0'
    devolve buf
```

`grow` tem 4 parâmetros — o teto da norma.

Ler tudo antes de aplicar simplifica o tratamento de erro: uma instrução inválida no meio
aborta antes de qualquer aplicação.

`read` devolvendo `-1` é tratado como erro. `0` é o EOF normal.

## Fluxo

1. O contexto é zerado com `ft_memset` e `buf` começa `NULL` — `fail_ck(&c, buf)` é seguro a
   partir de qualquer ponto.
2. `reject_flags`: qualquer `argv` com prefixo `--` imprime `Error` e sai com 255, **antes**
   de `parse_numbers` — o parser compartilhado pula tokens com esse prefixo, e sem a rejeição
   `./checker --simple 3 2 1` responderia `KO` onde a referência responde `Error`.
3. `parse_numbers` monta `a`; erro → `Error`, saída 255.
4. Zero números → não imprime nada, saída 0, sem ler stdin.
5. `b = stack_new(a->size)` e `read_all(0)`; falha em qualquer um → `Error`, saída 255.
6. Percorre o buffer separando por `\n` e aplicando cada linha; linha inválida → `Error`,
   saída 255. Sobra de bytes sem `\n` final também é `Error`:

   ```
   run_all(c, buf):
       ini = 0
       i = 0
       enquanto buf[i]:
           se buf[i] == '\n':
               se não apply_line(c, buf + ini, i - ini):
                   devolve 0
               ini = i + 1
           i += 1
       devolve (i == ini)
   ```

   O `i == ini` final é o que rejeita a última linha sem quebra. Sem ele, `printf 'ra'`
   responderia `KO` onde a referência responde `Error`.

7. `stack_is_sorted(a) && b->size == 0` → `OK`, senão `KO`. Saída 0.
8. `fail_ck` e `cleanup_ck` liberam tudo, inclusive o buffer.

## Verificação contra a referência

O binário de referência é o gabarito executável: as mesmas entradas precisam produzir as mesmas
respostas nos dois.

```bash
for caso in "3 2 1|sa
rra" "3 2 1|sa" "1 2 3|" "3 2 one|" "|"; do
  args="${caso%%|*}"; ops="${caso#*|}"
  meu=$(printf '%s\n' "$ops" | ./checker $args 2>&1; echo "exit=$?")
  ref=$(printf '%s\n' "$ops" | ../assets/checker_linux $args 2>&1; echo "exit=$?")
  [ "$meu" = "$ref" ] && echo "OK  $args" || echo "DIFERE  $args: meu=[$meu] ref=[$ref]"
done
```
