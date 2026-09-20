# Conversões (bônus)

Cada `conv_*` recebe a `t_fmt` já analisada e o argumento com o tipo certo, e
devolve os bytes escritos — largura incluída — ou `-1`. Nenhuma toca a lista
variádica: o `va_arg` acontece no despacho
([../03-arquitetura/fluxo.md](../03-arquitetura/fluxo.md)).

| Diretiva | Função | Arquivo | Caminho |
|---|---|---|---|
| `%c` | `conv_c` | `conv_text_bonus.c` | campo de texto |
| `%s` | `conv_s` | `conv_text_bonus.c` | campo de texto |
| `%%` | `conv_percent` | `conv_text_bonus.c` | byte seco |
| desconhecida | `conv_unknown`, `unk_head` | `conv_text_bonus.c` | reconstrução |
| `%d` `%i` | `conv_int` | `conv_num_bonus.c` | campo numérico |
| `%u` | `conv_uint` | `conv_num_bonus.c` | campo numérico |
| `%x` `%X` | `conv_hex` | `conv_hex_bonus.c` | campo numérico |
| `%p` | `conv_ptr` | `conv_hex_bonus.c` | numérico, ou texto se `NULL` |

Duas formas de campo, e só duas:

- **Texto** — `conv_c` e `conv_s` alinham o conteúdo com espaços por conta
  própria.
- **Numérico** — `conv_int`, `conv_uint`, `conv_hex` e `conv_ptr` escolhem um
  prefixo, renderizam os dígitos e entregam os dois a `put_num`
  ([montagem.md](montagem.md)).

`conv_percent` e `conv_unknown` ficam fora das duas: escrevem uma sequência
fixa de bytes, sem campo nem alinhamento.

As regras de saída de cada combinação flag × conversão estão em
[semantica.md](semantica.md); aqui está como cada função as produz.

## Campos de texto

### `conv_c`

```c
int	conv_c(t_fmt *f, char c);
```

```
conv_c(f, c):
    se não f->minus e pf_pad(' ', f->width - 1) < 0:
        devolve -1
    se pf_putchar(c) < 0:
        devolve -1
    se f->minus e pf_pad(' ', f->width - 1) < 0:
        devolve -1
    se f->width > 1:
        devolve f->width
    devolve 1
```

O comprimento é sempre 1, inclusive para `'\0'` — o byte zero é escrito como
qualquer outro. `pf_pad` devolve 0 para contagem negativa, então largura 0 ou
1 dispensa teste ([../04-emissao/escritores.md](../04-emissao/escritores.md)).

Só `minus` e `width` são lidos, e é por isso que `%05c` alinha com espaços e
`%.3c` sai como `%c`: `zero` e `prec` não aparecem no corpo.

### `conv_s`

```c
int	conv_s(t_fmt *f, char *s);
```

```
conv_s(f, s):
    se s é NULL e f->prec >= 0 e f->prec < 6:
        s = ""
    senão se s é NULL:
        s = "(null)"
    len = pf_strlen(s)
    se f->prec >= 0 e f->prec < len:
        len = f->prec
    se não f->minus e pf_pad(' ', f->width - len) < 0:
        devolve -1
    se pf_putn(s, len) < 0:
        devolve -1
    se f->minus e pf_pad(' ', f->width - len) < 0:
        devolve -1
    se f->width > len:
        devolve f->width
    devolve len
```

A troca de `NULL` acontece **antes** do truncamento, e é isso que produz o
degrau do `(null)`: com precisão de 0 a 5 a string já virou `""` e não há o
que cortar; de 6 em diante `(null)` tem 6 bytes e o truncamento não morde.
`(null)` nunca sai pela metade.

`pf_putn` escreve exatamente `len` bytes, então o truncamento é o próprio
argumento da chamada — a string nunca é copiada nem modificada.

### `conv_percent`

```c
int	conv_percent(void);
```

```
conv_percent():
    devolve pf_putchar('%')
```

A `t_fmt` inteira é ignorada, largura inclusive: `%5%` escreve um byte.

## Diretiva desconhecida

Duas funções, porque a reconstrução não cabe em 25 linhas
([../02-restricoes/estilo.md](../02-restricoes/estilo.md)): `unk_head` monta o
`%` e as flags, `conv_unknown` acrescenta largura, precisão e a conversão.

### `unk_head`

```c
static int	unk_head(t_fmt *f, char *buf);
```

```
unk_head(f, buf):
    i = 1
    buf[0] = '%'
    se f->hash:
        buf[i++] = '#'
    se f->plus:
        buf[i++] = '+'
    se não f->plus e f->space:
        buf[i++] = ' '
    se f->minus:
        buf[i++] = '-'
    se f->zero e não f->minus:
        buf[i++] = '0'
    devolve i
```

A ordem das flags no buffer é fixa — `#`, `+` ou espaço, `-`, `0` — e
independe da ordem em que apareceram no formato. As duas supressões (`+`
engole o espaço, `-` engole o `0`) são os dois `se` compostos.

### `conv_unknown`

```c
int	conv_unknown(t_fmt *f);
```

```
conv_unknown(f):
    buf é char[40]
    i = unk_head(f, buf)
    se f->width ≠ 0:
        render_base(f->width, "0123456789", buf + i)
        i = i + pf_strlen(buf + i)
    se f->prec >= 0:
        buf[i++] = '.'
        render_base(f->prec, "0123456789", buf + i)
        i = i + pf_strlen(buf + i)
    buf[i] = f->conv
    devolve pf_putn(buf, i + 1)
```

| Detalhe | Razão |
|---|---|
| `char buf[40]` | pior caso: `%` + 5 flags + 10 dígitos de largura + `.` + 10 de precisão + a conversão = 28 bytes, mais o `'\0'` de `render_base` |
| largura 0 não é escrita | largura 0 é indistinguível de ausente ([../03-arquitetura/tipos.md](../03-arquitetura/tipos.md)) |
| precisão 0 **é** escrita | `%.r` vira `[%.0r]`; o sentinela de ausente é −1 |
| `render_base` escreve no meio do buffer | recebe `buf + i` e termina em `'\0'`; `pf_strlen(buf + i)` mede o que ela pôs |
| o `'\0'` é sobrescrito | pelo `.` ou pela conversão; a emissão é por contagem (`pf_putn`), não por terminador |
| nenhum argumento é consumido | `%` é reconstruído a partir da struct, não do texto original |

## Campos numéricos

Os quatro seguem a mesma sequência: escolher o prefixo, renderizar os dígitos
num buffer de 24 bytes, esvaziar o buffer no caso "precisão 0 com valor 0" e
chamar `put_num`. Nenhum deles emite byte por conta própria.

### `conv_int`

```c
int	conv_int(t_fmt *f, int n);
```

```
conv_int(f, n):
    buf é char[24], v é long
    v = n
    pre = ""
    se v < 0:
        pre = "-"
        v = -v
    senão se f->plus:
        pre = "+"
    senão se f->space:
        pre = " "
    render_base(v, "0123456789", buf)
    se f->prec == 0 e n == 0:
        buf[0] = '\0'
    devolve put_num(f, pre, buf)
```

A negação acontece em `long`: `-INT_MIN` não existe em `int`
([../04-emissao/numeros.md](../04-emissao/numeros.md)). O sinal nunca entra no
buffer — vai como prefixo, e é por isso que os zeros caem entre ele e os
dígitos.

A cadeia `senão se` implementa a precedência `-` > `+` > espaço com três
atribuições e nenhum ternário.

### `conv_uint`

```c
int	conv_uint(t_fmt *f, unsigned int n);
```

```
conv_uint(f, n):
    buf é char[24]
    render_base(n, "0123456789", buf)
    se f->prec == 0 e n == 0:
        buf[0] = '\0'
    devolve put_num(f, "", buf)
```

O prefixo é sempre vazio, e é só isso que faz `%+u`, `% u` e `%#u` saírem
como `%u` — as flags nem são lidas.

### `conv_hex`

```c
int	conv_hex(t_fmt *f, unsigned int n);
```

```
conv_hex(f, n):
    buf é char[24]
    pre = ""
    se f->hash e n ≠ 0 e f->conv == 'x':
        pre = "0x"
    se f->hash e n ≠ 0 e f->conv == 'X':
        pre = "0X"
    se f->conv == 'X':
        render_base(n, "0123456789ABCDEF", buf)
    senão:
        render_base(n, "0123456789abcdef", buf)
    se f->prec == 0 e n == 0:
        buf[0] = '\0'
    devolve put_num(f, pre, buf)
```

`f->conv` é lido duas vezes — para a caixa do prefixo e para a do alfabeto —
e é o que permite uma função só para `%x` e `%X`. A condição `n ≠ 0` no
prefixo é o que faz `%#x` com 0 imprimir `[0]`, e ela se compõe com o
esvaziamento: `%#.0x` com 0 fica sem prefixo **e** sem dígitos, saída vazia.

### `conv_ptr`

```c
int	conv_ptr(t_fmt *f, void *p);
```

```
conv_ptr(f, p):
    buf é char[24]
    se p é NULL:
        f->prec = -1
        devolve conv_s(f, "(nil)")
    pre = "0x"
    se f->plus:
        pre = "+0x"
    senão se f->space:
        pre = " 0x"
    render_base(p, "0123456789abcdef", buf)
    devolve put_num(f, pre, buf)
```

**`NULL`** vira texto: apagar a precisão e delegar a `conv_s` entrega de uma
vez as quatro regras medidas — `(nil)` inteiro, largura com espaços mesmo com
a flag `0`, precisão e sinais sem efeito. A escrita em `f->prec` é segura
porque a struct é local a `pf_directive` e morre com a diretiva
([../03-arquitetura/fluxo.md](../03-arquitetura/fluxo.md)).

**Não nulo** é o único caso em que o prefixo tem três formas compostas
(`0x`, `+0x`, ` 0x`) — o sinal vem antes do `0x`, e os zeros de largura
depois dos dois. Não há esvaziamento por precisão: um ponteiro não nulo nunca
rende valor 0.
