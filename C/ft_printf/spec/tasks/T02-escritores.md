# T02 — Escritores da obrigatória

## Objetivo

Os quatro escritores públicos da parte obrigatória, com o contrato de retorno
comum.

## Depende de

T01.

## Arquivos

- `pf_put.c` — ganha `pf_putstr`, `pf_putnbr_base`, `pf_putptr`
- `ft_printf.h` — ganha os três protótipos

## Especificação

- [../04-emissao/escritores.md](../04-emissao/escritores.md) — `pf_putstr` e o contrato de retorno
- [../04-emissao/numeros.md](../04-emissao/numeros.md) — recursão de `pf_putnbr_base`, `pf_putptr`
- [../01-contrato/conversoes.md](../01-contrato/conversoes.md) — `(null)`, `(nil)`, bases

## Implementação

Na ordem do arquivo: `pf_putchar` (já existe), `pf_putstr` (NULL vira
`"(null)"` aqui mesmo), `pf_putnbr_base` (recursivo, alfabeto por parâmetro),
`pf_putptr` (`(nil)` para NULL; senão `0x` + hexadecimal minúsculo do
`(unsigned long)`). Toda falha de escrita devolve `-1` imediatamente —
inclusive no meio da recursão.

## Pronto quando

`/tmp/ftpf-check/t_escritores.c` (main temporário; não entra em `SRCS`):

```c
#include <stdio.h>
#include "ft_printf.h"

static void	ko(char *label, int ok)
{
	if (!ok)
		fprintf(stderr, "KO %s\n", label);
}

int	main(void)
{
	ko("putchar", pf_putchar('A') == 1);
	ko("putstr", pf_putstr("|abc|") == 5);
	ko("putstr vazia", pf_putstr("") == 0);
	ko("putstr NULL", pf_putstr(NULL) == 6);
	ko("dec 0", pf_putnbr_base(0, "0123456789") == 1);
	ko("dec max", pf_putnbr_base(4294967295u, "0123456789") == 10);
	ko("hex", pf_putnbr_base(255, "0123456789abcdef") == 2);
	ko("HEX", pf_putnbr_base(255, "0123456789ABCDEF") == 2);
	ko("ptr nil", pf_putptr(NULL) == 5);
	ko("ptr", pf_putptr((void *)0x1234) == 6);
	pf_putchar('\n');
	return (0);
}
```

```bash
D=/tmp/ftpf-check
make re
cc -I. $D/t_escritores.c -L. -lftprintf -o $D/t_esc
$D/t_esc > $D/esc.out 2> $D/esc.err
printf 'A|abc|(null)04294967295ffFF(nil)0x1234\n' > $D/esc.exp
cmp $D/esc.out $D/esc.exp && [ ! -s $D/esc.err ] && echo T02 ok
```

Silêncio em stderr é verde; qualquer `KO` é vermelho.
