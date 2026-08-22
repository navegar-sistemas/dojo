# T08 — Fechamento

## Objetivo

Tudo de [../06-aceitacao/validacao.md](../06-aceitacao/validacao.md) verde de
uma vez, nas duas variantes, a partir de um clone limpo.

## Depende de

T07.

## Arquivos

Nenhum novo.

## Implementação

1. `make fclean` e refazer o ciclo inteiro do zero.
2. Lote obrigatório (T04) na variante `make`; lote bônus (T07) e fuzz de
   5000 na variante `make bonus`.
3. Sanitizers nas duas variantes; valgrind no binário diferencial.
4. Auditoria mecânica de estilo e conferência das contagens de
   [../03-arquitetura/modulos.md](../03-arquitetura/modulos.md).

## Pronto quando

```bash
D=/tmp/ftpf-check
make re && make && make bonus && make bonus
python3 $D/gera.py                              # lote_fuzz.h, 5000 casos
for L in lote_bonus.h lote_fuzz.h; do
  cc -Wno-format -DCASES="\"$L\"" $D/tdiff.c -o $D/t_ref
  cc -DCASES="\"$L\"" -DUSE_FT $D/tdiff.c -L. -lftprintf -o $D/t_ft
  $D/t_ref > $D/ref.out 2> $D/ref.ret
  $D/t_ft  > $D/ft.out  2> $D/ft.ret
  cmp $D/ref.out $D/ft.out && cmp $D/ref.ret $D/ft.ret && echo "$L identico"
done
cc -g -fsanitize=address,undefined -fno-sanitize-recover=all \
   -DCASES='"lote_fuzz.h"' -DUSE_FT $D/tdiff.c *_bonus.c -o $D/t_san
$D/t_san > /dev/null 2> $D/san.err \
  && ! grep -qE 'runtime error|Sanitizer' $D/san.err && echo san-ok
valgrind --error-exitcode=42 -q $D/t_ft > /dev/null; echo "valgrind: $?"
make fclean && make \
  && cc -Wno-format -DCASES='"lote_obrig.h"' $D/tdiff.c -o $D/t_ref \
  && cc -DCASES='"lote_obrig.h"' -DUSE_FT $D/tdiff.c -L. -lftprintf \
     -o $D/t_ft \
  && $D/t_ref > $D/ref.out 2> $D/ref.ret && $D/t_ft > $D/ft.out 2> $D/ft.ret \
  && cmp $D/ref.out $D/ft.out && cmp $D/ref.ret $D/ft.ret \
  && echo "obrigatoria ainda identica"
grep -nE '\bfor\b|\bswitch\b|\bgoto\b|\bdo\b' *.c *.h; grep -n '?' *.c
expand -t4 *.c *.h | awk 'length > 80'
```

Dois `identico`, `san-ok`, `valgrind: 0`, `obrigatoria ainda identica`, e as
três auditorias mudas. A reverificação da obrigatória passa por
`make fclean && make` de propósito: um `make` seco depois do ciclo de bônus
não refaz nada — o `.a` corrente continua sendo o do bônus, como documenta a
tabela de sequências de [../02-restricoes/build.md](../02-restricoes/build.md)
— e o fechamento precisa testar a variante obrigatória de verdade.
