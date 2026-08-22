# T06 — Montagem numérica

## Objetivo

Dígitos em buffer e o montador único de campo numérico.

## Depende de

T05.

## Arquivos

- `num_render_bonus.c` — `render_base`, `put_num`
- `ft_printf_bonus.h` — ganha os dois protótipos
- `Makefile` — `BSRCS` ganha `num_render_bonus.c`

## Especificação

- [../04-emissao/numeros.md](../04-emissao/numeros.md) — `render_base` em duas passadas
- [../05-bonus/montagem.md](../05-bonus/montagem.md) — as três contagens e a ordem de emissão

## Implementação

`render_base` conta os dígitos, escreve o `'\0'` e preenche de trás para a
frente — o pseudocódigo de [numeros.md](../04-emissao/numeros.md) é literal.

`put_num` calcula `zeros` (precisão; largura se `zero && !minus && prec`
ausente), `total` e emite: espaços à esquerda se não-`minus`, prefixo, zeros,
dígitos, espaços à direita se `minus`; devolve a largura se ela venceu, senão
`total`. As três emissões centrais compartilham um único `if` de erro com
`||` — é o que mantém o corpo em 23 linhas
([../02-restricoes/estilo.md](../02-restricoes/estilo.md)).

## Pronto quando

`/tmp/ftpf-check/t_montagem.c`:

```c
#include <stdio.h>
#include "ft_printf_bonus.h"

static void	ko(char *label, int ok)
{
	if (!ok)
		fprintf(stderr, "KO %s\n", label);
}

static t_fmt	fmt(int minus, int zero, int width, int prec)
{
	t_fmt	f;

	f.minus = minus;
	f.zero = zero;
	f.hash = 0;
	f.plus = 0;
	f.space = 0;
	f.width = width;
	f.prec = prec;
	f.conv = 'd';
	return (f);
}

int	main(void)
{
	char	buf[24];
	t_fmt	f;

	render_base(0, "0123456789", buf);
	ko("render 0", buf[0] == '0' && buf[1] == '\0');
	render_base(4294967295u, "0123456789", buf);
	ko("render max", pf_strlen(buf) == 10 && buf[0] == '4' && buf[9] == '5');
	render_base(255, "0123456789ABCDEF", buf);
	ko("render FF", buf[0] == 'F' && buf[1] == 'F' && buf[2] == '\0');
	f = fmt(0, 1, 5, -1);
	ko("largura zeros", put_num(&f, "+", "42") == 5);
	pf_putchar('|');
	f = fmt(0, 0, 5, 3);
	ko("prec espacos", put_num(&f, "", "42") == 5);
	pf_putchar('|');
	f = fmt(1, 0, 8, 5);
	ko("minus direita", put_num(&f, "-", "42") == 8);
	pf_putchar('|');
	f = fmt(0, 1, 15, -1);
	ko("prefixo composto", put_num(&f, " 0x", "1234") == 15);
	pf_putchar('|');
	f = fmt(0, 0, 0, 0);
	ko("vazio", put_num(&f, "+", "") == 1);
	pf_putchar('\n');
	return (0);
}
```

```bash
D=/tmp/ftpf-check
cc -Wall -Wextra -Werror -I. $D/t_montagem.c num_render_bonus.c put_bonus.c \
   -o $D/t_mon
$D/t_mon > $D/mon.out 2> $D/mon.err
printf '+0042|  042|-00042  | 0x000000001234|+\n' > $D/mon.exp
cmp $D/mon.out $D/mon.exp && [ ! -s $D/mon.err ] && echo T06 ok
make bonus                      # três objetos no .a
```

As cinco saídas entre `|` são, na ordem, as linhas `%+05d`/42,
`%05.3d`/42, `%-8.5d`/−42, `% 015p`/`0x1234` e `%+.0d`/0 da tabela de
[montagem.md](../05-bonus/montagem.md) — o montador reproduz a referência
antes mesmo de existir uma conversão.
