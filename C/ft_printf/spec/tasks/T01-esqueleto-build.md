# T01 — Esqueleto de build

## Objetivo

`make` produz `libftprintf.a` com um objeto dentro, sem relinkar na segunda
chamada.

## Depende de

Nada.

## Arquivos

- `Makefile`
- `ft_printf.h`
- `pf_put.c` contendo só `pf_putchar`

## Especificação

- [../02-restricoes/build.md](../02-restricoes/build.md) — Makefile completo e propriedades
- [../04-emissao/escritores.md](../04-emissao/escritores.md) — `pf_putchar`

## Implementação

1. Copiar o Makefile de [build.md](../02-restricoes/build.md) **sem** a parte
   do bônus: `BSRCS`, `BOBJS`, a regra de padrão dos `BOBJS`, `bonus` e
   `.bonus` entram em T05; `clean`/`fclean` ainda não mencionam `BOBJS` nem
   `.bonus`. `SRCS` começa contendo só `pf_put.c`.
2. `ft_printf.h` mínimo: guarda de inclusão e o protótipo de `pf_putchar`.
   O header cresce tarefa a tarefa
   ([README.md](README.md#header-incremental)).
3. `pf_put.c` com `pf_putchar` exatamente como em
   [escritores.md](../04-emissao/escritores.md).

## Pronto quando

```bash
make                        # compila sem warning, cria libftprintf.a
make                        # Nothing to be done for 'all'.
ar t libftprintf.a          # pf_put.o
touch ft_printf.h && make   # recompila (dependência do header)
make fclean                 # remove .o e .a
make re                     # do zero, zero warning
```
