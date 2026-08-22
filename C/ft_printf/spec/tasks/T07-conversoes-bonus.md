# T07 — Conversões e laço do bônus

## Objetivo

O bônus completo: espelho total da referência, flags incluídas.

## Depende de

T04, T06.

## Arquivos

- `conv_text_bonus.c` — `unk_head` (static), `conv_unknown`, `conv_c`,
  `conv_s`, `conv_percent`
- `conv_num_bonus.c` — `conv_int`, `conv_uint`
- `conv_hex_bonus.c` — `conv_hex`, `conv_ptr`
- `ft_printf_bonus.c` — `pf_dispatch` (static), `pf_directive` (static),
  `ft_printf`
- `ft_printf_bonus.h` — ganha os protótipos das oito `conv_*` e de
  `ft_printf`
- `Makefile` — `BSRCS` completo (7 arquivos)

## Especificação

- [../05-bonus/semantica.md](../05-bonus/semantica.md) — matriz flag × conversão, `(null)`, `(nil)`, canônica
- [../05-bonus/montagem.md](../05-bonus/montagem.md) — prefixo por conversão, campos de texto
- [../03-arquitetura/fluxo.md](../03-arquitetura/fluxo.md) — laço, diretiva, despacho, `va_list *`
- [../03-arquitetura/tipos.md](../03-arquitetura/tipos.md) — quem consome cada campo

## Implementação

Ordem sugerida: `conv_c`/`conv_s`/`conv_percent` (campos de texto) →
`conv_int`/`conv_uint`/`conv_hex`/`conv_ptr` (prefixo + `put_num`) →
`conv_unknown` (reconstrução canônica, largura e precisão via `render_base`
no próprio buffer) → `ft_printf_bonus.c` (laço idêntico ao de
[fluxo.md](../03-arquitetura/fluxo.md), `pf_directive` devolvendo −1 para
`conv == '\0'`).

Pontos que derrubam implementações apressadas, todos medidos:

- `conv_s`: o degrau do `NULL` é **antes** do truncamento — precisão < 6
  troca por `""`, senão por `"(null)"`; depois a precisão trunca normalmente.
- `conv_ptr` com `NULL`: `f->prec = -1` e delegar a `conv_s` — precisão
  ignorada, largura com espaços.
- `conv_hex`: prefixo só com `hash && n != 0`; o esvaziamento
  `prec == 0 && n == 0` vem **depois** de renderizar.
- `conv_int`: negar no `long`; o sinal nunca entra no buffer de dígitos.
- `unk_head`: `0` suprimida por `minus`, espaço por `plus` — ordem
  `# + espaço - 0`.
- `pf_dispatch`: `va_arg` só dentro do ramo — `%%` e desconhecida não tocam a
  lista.

## Pronto quando

Harness com o lote-amostra de
[../06-aceitacao/validacao.md](../06-aceitacao/validacao.md) e, na sequência,
um `lote_bonus.h` com **todas** as linhas de
[../06-aceitacao/casos.md](../06-aceitacao/casos.md) transcritas:

```bash
D=/tmp/ftpf-check
make bonus
cc -Wno-format -DCASES='"lote_bonus.h"' $D/tdiff.c -o $D/t_ref
cc -DCASES='"lote_bonus.h"' -DUSE_FT $D/tdiff.c -L. -lftprintf -o $D/t_ft
$D/t_ref > $D/ref.out 2> $D/ref.ret
$D/t_ft  > $D/ft.out  2> $D/ft.ret
cmp $D/ref.out $D/ft.out && cmp $D/ref.ret $D/ft.ret && echo T07 ok
ar t libftprintf.a              # os sete *_bonus.o, e só
make && make bonus && make bonus    # transições e no-relink de novo
```
