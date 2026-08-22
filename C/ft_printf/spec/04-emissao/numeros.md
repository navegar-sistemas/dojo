# Números

## Obrigatória — recursão que emite na ordem

```c
int	pf_putnbr_base(unsigned long n, const char *base)
```

```
pf_putnbr_base(n, base):
    b = comprimento de base
    len = 0
    se n >= b:
        len = pf_putnbr_base(n / b, base)
        se len < 0: devolve -1
    se pf_putchar(base[n % b]) < 0: devolve -1
    devolve len + 1
```

A recursão imprime o dígito mais significativo primeiro sem buffer nenhum.
Profundidade máxima: 20 chamadas (dígitos decimais de um `unsigned long` de
64 bits). A base é o alfabeto passado por literal — `"0123456789"`,
`"0123456789abcdef"`, `"0123456789ABCDEF"` — e o comprimento é medido dela
mesma, então uma base nova não pede código novo.

**Sinal e `INT_MIN`.** `pf_putnbr` (static em `ft_printf.c`) copia o `int`
para um `long`, imprime `-` se negativo e nega **no `long`** — `-INT_MIN` não
existe em `int`, mas existe em 64 bits. O valor segue como `unsigned long`
para a recursão.

**Ponteiro.** `pf_putptr`: `NULL` delega `pf_putstr("(nil)")`; senão `0x` e o
endereço convertido por `(unsigned long)` na base hexadecimal minúscula
(LP64: mesmo tamanho de ponteiro).

## Bônus — buffer preenchido de trás para a frente

```c
void	render_base(unsigned long n, const char *base, char *buf)
```

```
render_base(n, base, buf):
    b = comprimento de base
    len = 1
    tmp = n
    enquanto tmp >= b:                # conta os dígitos
        tmp = tmp / b
        len += 1
    buf[len] = '\0'
    enquanto len > 0:                 # preenche do fim
        len -= 1
        buf[len] = base[n % b]
        n = n / b
```

Duas passadas: contar, depois preencher do último dígito para o primeiro. O
resultado é uma string — o montador precisa medi-la (`pf_strlen`) antes de
decidir zeros e espaços, e é exatamente por isso que o bônus não usa a
recursão da obrigatória
([../03-arquitetura/decisoes.md](../03-arquitetura/decisoes.md)).

**Buffers.** `char buf[24]` nos chamadores: 20 dígitos decimais + `'\0'` com
folga. `n == 0` produz `"0"` (`len` parte de 1) — o caso "precisão 0 com valor
0 imprime vazio" é decidido **depois**, pelo chamador, esvaziando o buffer
(`buf[0] = '\0'`), nunca pelo renderizador.

**Sinal.** Igual à obrigatória: `conv_int` copia para `long`, nega no `long`,
e o sinal vira o **prefixo** do montador — os dígitos nunca sabem do sinal
([../05-bonus/montagem.md](../05-bonus/montagem.md)).
