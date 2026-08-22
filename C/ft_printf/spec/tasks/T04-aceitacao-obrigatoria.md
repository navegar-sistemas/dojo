# T04 — Aceitação da obrigatória

## Objetivo

Parte obrigatória fechada: bateria completa, fuzz, sanitizers e valgrind,
tudo idêntico à referência.

## Depende de

T03.

## Arquivos

Nenhum novo — a tarefa é de verificação.

## Especificação

- [../06-aceitacao/validacao.md](../06-aceitacao/validacao.md) — harness, fuzz, sanitizers, valgrind
- [../06-aceitacao/casos.md](../06-aceitacao/casos.md) — linhas do encadeamento, desconhecidas de um byte, incompletas
- [../01-contrato/conversoes.md](../01-contrato/conversoes.md) — linhas por conversão

## Implementação

1. Montar `/tmp/ftpf-check/lote_obrig.h` transcrevendo em `T(...)`:
   os exemplos de [conversoes.md](../01-contrato/conversoes.md) (valores de
   borda incluídos: `INT_MIN`, `INT_MAX`, `UINT_MAX`, `'\0'`, `NULL`),
   o encadeamento de [casos.md](../06-aceitacao/casos.md), `"%r"`/`"%y"`
   (desconhecidas de um byte), `"%"`/`"abc%"` (incompletas) e literais puros.
   **Sem flag, largura ou precisão** — inclusive `"% "` fica de fora
   ([../01-contrato/diretivas.md](../01-contrato/diretivas.md)).
2. Gerar `/tmp/ftpf-check/lote_fuzz_obrig.h` com o gerador de
   [validacao.md](../06-aceitacao/validacao.md), com `diretiva()` reduzida a
   `"%" + conversao` (sem flags/largura/precisão).
3. Rodar os dois lotes no harness; depois sanitizers e valgrind.

## Pronto quando

```bash
D=/tmp/ftpf-check
make re
for L in lote_obrig.h lote_fuzz_obrig.h; do
  cc -Wno-format -DCASES="\"$L\"" $D/tdiff.c -o $D/t_ref
  cc -DCASES="\"$L\"" -DUSE_FT $D/tdiff.c -L. -lftprintf -o $D/t_ft
  $D/t_ref > $D/ref.out 2> $D/ref.ret
  $D/t_ft  > $D/ft.out  2> $D/ft.ret
  cmp $D/ref.out $D/ft.out && cmp $D/ref.ret $D/ft.ret && echo "$L identico"
done
cc -g -fsanitize=address,undefined -fno-sanitize-recover=all \
   -DCASES='"lote_obrig.h"' -DUSE_FT $D/tdiff.c ft_printf.c pf_put.c \
   -o $D/t_san
$D/t_san > /dev/null 2> $D/san.err \
  && ! grep -qE 'runtime error|Sanitizer' $D/san.err && echo san-ok
valgrind --error-exitcode=42 -q $D/t_ft > /dev/null; echo "valgrind: $?"
```

Dois `identico`, `san-ok`, `valgrind: 0` — o veredito do sanitizer é código
de saída + `grep`, porque o stderr do harness carrega o log de retornos
([../06-aceitacao/validacao.md](../06-aceitacao/validacao.md)).
