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

- [../05-bonus/conversoes.md](../05-bonus/conversoes.md) — algoritmo de cada `conv_*` e de `unk_head`
- [../05-bonus/semantica.md](../05-bonus/semantica.md) — matriz flag × conversão, `(null)`, `(nil)`, canônica
- [../05-bonus/montagem.md](../05-bonus/montagem.md) — o que `put_num` espera receber
- [../03-arquitetura/fluxo.md](../03-arquitetura/fluxo.md) — laço, diretiva, despacho, `va_list *`
- [../03-arquitetura/tipos.md](../03-arquitetura/tipos.md) — quem lê cada campo

## Implementação

Cada função tem o algoritmo em
[conversoes.md](../05-bonus/conversoes.md); a ordem sugerida é campos de
texto (`conv_c`, `conv_s`, `conv_percent`) → numéricos (`conv_int`,
`conv_uint`, `conv_hex`, `conv_ptr`) → `conv_unknown` com `unk_head` →
`ft_printf_bonus.c`.

Os seis pontos onde uma implementação apressada diverge da referência:

| Função | Armadilha |
|---|---|
| `conv_s` | a troca do `NULL` vem **antes** da medição, senão `(null)` sai cortado; a medição é `pf_strnlen(s, prec)`, nunca `pf_strlen` — `%.3s` sobre 3 bytes sem terminador é entrada válida |
| `conv_ptr` | `NULL` precisa de `f->prec = -1` antes de delegar a `conv_s` |
| `conv_hex` | o prefixo exige `hash` **e** valor ≠ 0; o esvaziamento vem **depois** de renderizar |
| `conv_int` | negar em `long`, e o sinal nunca entra no buffer de dígitos |
| `unk_head` | `-` suprime o `0` e `+` suprime o espaço; a ordem é fixa |
| `pf_dispatch` | `va_arg` só dentro do ramo, senão `%%` e desconhecida consomem argumento |

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
