# T03 — Laço e despacho

## Objetivo

`ft_printf` completa na parte obrigatória: primeiro ponto comparável com a
referência.

## Depende de

T02.

## Arquivos

- `ft_printf.c` — `pf_putnbr` (static), `pf_conv` (static), `ft_printf`
- `ft_printf.h` — ganha `# include <stdarg.h>` e o protótipo de `ft_printf`
- `Makefile` — `SRCS` ganha `ft_printf.c`

## Especificação

- [../03-arquitetura/fluxo.md](../03-arquitetura/fluxo.md) — o laço obrigatório, `va_list` por ponteiro
- [../01-contrato/diretivas.md](../01-contrato/diretivas.md) — desconhecida, incompleta, consumo
- [../01-contrato/conversoes.md](../01-contrato/conversoes.md) — semântica das nove
- [../04-emissao/numeros.md](../04-emissao/numeros.md) — sinal em `long` (`pf_putnbr`)

## Implementação

Ordem no arquivo: `pf_putnbr` → `pf_conv` → `ft_printf` (statics definidas
antes do uso dispensam protótipos).

- `pf_putnbr(int n)`: copia para `long`, imprime `-` e nega no `long` se
  negativo, delega os dígitos a `pf_putnbr_base`; devolve sinal + dígitos ou
  `-1`.
- `pf_conv(char conv, va_list *ap)`: cadeia de `if` — `c s p d i u x X %` —
  cada ramo consome o argumento com o tipo certo **dentro** do ramo;
  desconhecida imprime `%` e o byte (2 bytes, nenhum argumento consumido).
- `ft_printf`: `va_start`, laço de
  [fluxo.md](../03-arquitetura/fluxo.md#o-laço-da-parte-obrigatória) —
  literal → `pf_putchar`; `%` com `format[1] == '\0'` → `r = -1`; senão
  `pf_conv(*(++format), &ap)` — soma `r > 0`, para em `r < 0`, `va_end`,
  devolve total ou `-1`.

## Pronto quando

Harness de [../06-aceitacao/validacao.md](../06-aceitacao/validacao.md)
(`tdiff.c` já em `/tmp/ftpf-check/`), com o lote inicial
`/tmp/ftpf-check/lote_inicial.h`:

```c
T("hello world")
T("%c", 'a')
T("%c", '\0')
T("%s", "hi")
T("%s", (char *)0)
T("%p", (void *)0x1234)
T("%p", (void *)0)
T("%d", INT_MIN)
T("%i", INT_MAX)
T("%u", 4294967295u)
T("%x", 0xabcdefu)
T("%X", 0xabcdefu)
T("100%%")
T("%r")
T("a%rb%d", 42)
T("abc%")
T("mix %s %d %x %p %c fim", "s", -7, 255u, (void *)0x1, 'k')
```

```bash
D=/tmp/ftpf-check
make re
cc -Wno-format -DCASES='"lote_inicial.h"' $D/tdiff.c -o $D/t_ref
cc -DCASES='"lote_inicial.h"' -DUSE_FT $D/tdiff.c -L. -lftprintf -o $D/t_ft
$D/t_ref > $D/ref.out 2> $D/ref.ret
$D/t_ft  > $D/ft.out  2> $D/ft.ret
cmp $D/ref.out $D/ft.out && cmp $D/ref.ret $D/ft.ret && echo T03 ok
```
