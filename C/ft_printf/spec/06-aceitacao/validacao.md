# Validação

Comandos de `../project/`, salvo indicação. Arquivos de teste ficam **fora**
do diretório da implementação (aqui, `/tmp/ftpf-check/`): não são entregáveis.

## Estado limpo

```bash
make re                     # zero warning com -Wall -Wextra -Werror
make && make                # 2ª chamada: Nothing to be done for 'all'.
make bonus && make bonus    # 2ª chamada: Nothing to be done for 'bonus'.
```

Auditoria mecânica de estilo em
[../02-restricoes/estilo.md](../02-restricoes/estilo.md).

## O harness diferencial

O gabarito executável é a `printf` do sistema. Um mesmo lote de casos compila
duas vezes — uma chamando `printf`, outra chamando `ft_printf` — e as duas
execuções precisam produzir `stdout` **e** sequência de retornos idênticos.

`/tmp/ftpf-check/tdiff.c`:

```c
#include <stdio.h>
#include <limits.h>
int	ft_printf(const char *format, ...);
#ifdef USE_FT
# define PRINTF ft_printf
#else
# define PRINTF printf
#endif
static int g_i;
#define T(...) do { int r = PRINTF(__VA_ARGS__); \
	fprintf(stderr, "case %d ret %d\n", g_i++, r); } while (0);
int main(void)
{
#include CASES
	return 0;
}
```

Cada linha de um lote é `T(formato, argumentos…)` — as tabelas de
[casos.md](casos.md) transcrevem-se uma a uma. Amostra
(`/tmp/ftpf-check/lote_bonus.h`):

```c
T("%c|%s|%p|%d|%i|%u|%x|%X|%%", 'q', "str", (void *)0x42, -5, 6, 7u, 8u, 9u)
T("%08p", (void *)0)
T("%.3p", (void *)0)
T("% 015p", (void *)0x1234)
T("%.6s", (char *)0)
T("%.5s", (char *)0)
T("%+.0d", 0)
T("%020d", INT_MIN)
T("%#08x", 255u)
T("%0-5r")
T("abc%")
```

Rodada (o `-Wno-format` existe porque o lote exercita de propósito diretivas
que o compilador marca como suspeitas na `printf` real):

```bash
D=/tmp/ftpf-check
cc -Wno-format -DCASES='"lote_bonus.h"' $D/tdiff.c -o $D/t_ref
cc -DCASES='"lote_bonus.h"' -DUSE_FT $D/tdiff.c -L. -lftprintf -o $D/t_ft
$D/t_ref > $D/ref.out 2> $D/ref.ret
$D/t_ft  > $D/ft.out  2> $D/ft.ret
cmp $D/ref.out $D/ft.out && cmp $D/ref.ret $D/ft.ret && echo IDENTICO
```

O `cmp` de arquivos é o que permite comparar saídas com byte zero (`%c` com
`'\0'`) e espaços à direita sem ambiguidade.

**Lote da parte obrigatória** (`make` sem bônus): mesmas ferramentas, casos
**sem flag, largura ou precisão** — inclusive `"% "`, que parece literal mas
começa com a flag espaço
([../01-contrato/diretivas.md](../01-contrato/diretivas.md)). Desconhecidas de
um byte (`"%r"`), `"%%"` e formatos incompletos entram normalmente.

## Fuzz

Milhares de formatos válidos aleatórios, mesmo harness. Gerador
(`/tmp/ftpf-check/gera.py`):

```python
import random
random.seed()
ints = [0, 1, -1, 42, -42, 2147483647, -2147483648, 999999999]
uints = ["0u", "1u", "42u", "4294967295u", "2147483648u"]
chars = ["'a'", "'Z'", "' '", "127", "1"]
strs = ['"hi"', '""', '"hello world"', '(char *)0', '"abcdefghij"']
ptrs = ["(void *)0", "(void *)1", "(void *)0x1234",
        "(void *)0xffffffffffffffff"]
lits = ["", "x", "abc ", "%%", " fim"]
def diretiva():
    f = "".join(random.choice("-0# +") for _ in range(random.randint(0, 4)))
    w = "" if random.random() < 0.35 else str(random.randint(0, 50))
    p = ""
    if random.random() < 0.4:
        p = "." + (str(random.randint(0, 30)) if random.random() < 0.8 else "")
    c = random.choice("cspdiuxX%rk!w")
    return f + w + p + c, c
def arg(c):
    if c == "c": return random.choice(chars)
    if c == "s": return random.choice(strs)
    if c == "p": return random.choice(ptrs)
    if c in "di": return str(random.choice(ints))
    return random.choice(uints)
out = []
for _ in range(5000):
    fmt, args = random.choice(lits), []
    for _ in range(random.randint(1, 4)):
        d, c = diretiva()
        fmt += "%" + d
        if c in "cspdiuxX":
            args.append(arg(c))
        fmt += random.choice(lits)
    out.append('T("%s"%s)' % (fmt, (", " + ", ".join(args)) if args else ""))
open("lote_fuzz.h", "w").write("\n".join(out) + "\n")
```

Convenções do gerador: conversões desconhecidas só `r k ! w` (nunca `l`, `h`,
`*`, `'`, que a referência interpreta e o projeto declara fora do domínio —
[../01-contrato/api.md](../01-contrato/api.md)); diretivas sempre completas
(as incompletas já estão no lote curado); todo argumento consumível presente.
Para o lote da obrigatória, gerar sem flags/largura/precisão.

## Sanitizers

A biblioteca recompilada junto do harness, com ASan + UBSan:

```bash
cc -g -fsanitize=address,undefined -fno-sanitize-recover=all \
   -DCASES='"lote_bonus.h"' -DUSE_FT $D/tdiff.c *_bonus.c -o $D/t_san
$D/t_san > /dev/null 2> $D/san.err \
  && ! grep -qE 'runtime error|Sanitizer' $D/san.err && echo san-ok
cc -g -fsanitize=address,undefined -fno-sanitize-recover=all \
   -DCASES='"lote_obrig.h"' -DUSE_FT $D/tdiff.c ft_printf.c pf_put.c \
   -o $D/t_san2
$D/t_san2 > /dev/null 2> $D/san.err \
  && ! grep -qE 'runtime error|Sanitizer' $D/san.err && echo san-ok
```

`san-ok` nos dois, fuzz incluído. O veredito é o código de saída mais o
`grep`, nunca o silêncio de stderr: o stderr do harness sempre carrega o log
de retornos (`case N ret R`). O `-fno-sanitize-recover=all` faz o UBSan
abortar com status ≠ 0 em vez de só avisar e seguir.

## Memória

Não há alocação — o teste comprova a ausência:

```bash
valgrind --error-exitcode=42 --leak-check=full -q $D/t_ft > /dev/null
echo $?          # 0; e nenhuma linha de erro do valgrind
```

## A biblioteca em si

```bash
ar t libftprintf.a                    # objetos da variante corrente, e só
nm -g --defined-only libftprintf.a | grep -w T   # ft_printf presente
```

Após `make`: `ft_printf.o pf_put.o`. Após `make bonus`: os sete `*_bonus.o`.
Um `.a` com as duas variantes ao mesmo tempo é defeito de build
([../02-restricoes/build.md](../02-restricoes/build.md)).
