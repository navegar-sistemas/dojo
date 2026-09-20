# T05 — Gramática do bônus

## Objetivo

A diretiva estendida vira `t_fmt`, e o build ganha a variante bônus.

## Depende de

T01.

## Arquivos

- `ft_printf_bonus.h` — guarda, `# include <stdarg.h>`,
  `# define PF_INT_MAX 2147483647`, `t_fmt`, protótipos de `parse_fmt`,
  `pf_putchar`, `pf_putn`, `pf_pad`, `pf_strlen`, `pf_strnlen`
- `parse_bonus.c` — `fmt_init` (static), `parse_flags` (static), `parse_num`
  (static), `parse_fmt`
- `put_bonus.c` — `pf_putchar`, `pf_putn`, `pf_pad`, `pf_strlen`,
  `pf_strnlen`
- `Makefile` — ganha `BSRCS = parse_bonus.c put_bonus.c`, `BOBJS`, a regra de
  padrão dos `BOBJS` (dependendo de `ft_printf_bonus.h`), `bonus`, `.bonus`,
  e o `clean`/`fclean` passam a remover `$(BOBJS)`/`.bonus` — forma final em
  [../02-restricoes/build.md](../02-restricoes/build.md)

## Especificação

- [../05-bonus/formato.md](../05-bonus/formato.md) — gramática e `parse_fmt`
- [../03-arquitetura/tipos.md](../03-arquitetura/tipos.md) — `t_fmt` e invariantes
- [../04-emissao/escritores.md](../04-emissao/escritores.md) — `pf_putn`, `pf_pad`
- [../02-restricoes/build.md](../02-restricoes/build.md) — marcador `.bonus`, `rm` antes do `ar`

## Implementação

`parse_fmt` segue o pseudocódigo de [formato.md](../05-bonus/formato.md) ao
pé da letra: `fmt_init` primeiro (é ela que põe `prec = -1` e `conv = '\0'`),
flags em laço com deduplicação natural (atribuir 1 duas vezes), largura e
precisão por `parse_num`, e `conv = *s` sem avançar. Quando `parse_num`
devolve −1, `parse_fmt` retorna na hora — `conv` fica `'\0'` e a diretiva
falha pelo caminho da incompleta.

`pf_pad` devolve 0 para contagem negativa, e `pf_strnlen` confere o limite
**antes** de ler o byte — os chamadores dependem das duas coisas
([escritores.md](../04-emissao/escritores.md)).

Neste ponto o `.a` do bônus contém só dois objetos e não linka um programa
que chame `ft_printf` — normal: o laço chega em T07.

## Pronto quando

`/tmp/ftpf-check/t_parse.c`:

```c
#include <stdio.h>
#include "ft_printf_bonus.h"

static void	ko(char *label, int ok)
{
	if (!ok)
		fprintf(stderr, "KO %s\n", label);
}

int	main(void)
{
	t_fmt		f;
	const char	*end;

	end = parse_fmt("-05d resto", &f);
	ko("flags", f.minus == 1 && f.zero == 1 && f.width == 5 && f.prec == -1);
	ko("conv", f.conv == 'd' && *end == 'd');
	parse_fmt("00500d", &f);
	ko("zero flag largura", f.zero == 1 && f.width == 500);
	parse_fmt("5.d", &f);
	ko("prec vazia", f.width == 5 && f.prec == 0);
	parse_fmt(".25r", &f);
	ko("prec 25", f.prec == 25 && f.conv == 'r');
	parse_fmt(" ", &f);
	ko("incompleta", f.space == 1 && f.conv == '\0');
	parse_fmt("++--  ##00x", &f);
	ko("dedup", f.plus && f.minus && f.space && f.hash && f.zero
		&& f.width == 0 && f.conv == 'x');
	parse_fmt("2147483647d", &f);
	ko("int max", f.width == 2147483647 && f.conv == 'd');
	parse_fmt("2147483648d", &f);
	ko("estouro largura", f.conv == '\0');
	parse_fmt(".4294967296d", &f);
	ko("estouro precisao", f.conv == '\0');
	ko("strnlen limite", pf_strnlen("abcdef", 3) == 3);
	ko("strnlen curta", pf_strnlen("ab", 9) == 2);
	ko("strnlen livre", pf_strnlen("abcdef", -1) == 6);
	ko("strnlen zero", pf_strnlen("abc", 0) == 0);
	ko("putn", pf_putn("abcdef", 3) == 3);
	ko("pad", pf_pad('.', 4) == 4);
	ko("pad neg", pf_pad('.', -3) == 0);
	ko("strlen", pf_strlen("(null)") == 6);
	pf_putchar('\n');
	return (0);
}
```

```bash
D=/tmp/ftpf-check
cc -Wall -Wextra -Werror -I. $D/t_parse.c parse_bonus.c put_bonus.c -o $D/t_par
$D/t_par > $D/par.out 2> $D/par.err
printf 'abc....\n' > $D/par.exp
cmp $D/par.out $D/par.exp && [ ! -s $D/par.err ] && echo T05 ok
make bonus && make bonus        # 2ª: Nothing to be done for 'bonus'.
ar t libftprintf.a              # parse_bonus.o put_bonus.o
make && make bonus              # transição nos dois sentidos sem erro
```
