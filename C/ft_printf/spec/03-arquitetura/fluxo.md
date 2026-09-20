# Fluxo

O mesmo esqueleto nas duas variantes: um laço sobre o formato, um despacho
por conversão, e o valor `r` carregando o resultado de cada passo.

| `r` | Significado | Efeito |
|---|---|---|
| > 0 | bytes escritos pelo passo | soma em `total` |
| 0 | passo válido que não escreveu nada (`%.0d` com 0) | nada a somar |
| −1 | `write` falhou, diretiva incompleta, **ou** um limite de `int` foi estourado | o laço para, retorno −1 |

Os bytes já escritos ficam escritos: `"abc%"` imprime `[abc]` e devolve −1.

## A soma, nas duas variantes

```c
static int	pf_add(int *total, int r);
```

```
pf_add(total, r):
    se r < 0 ou r > PF_INT_MAX - *total:
        devolve -1
    *total += r
    devolve r
```

O retorno de `ft_printf` é `int`, então a saída inteira tem que caber em
`INT_MAX` bytes. A comparação é feita **antes** da soma e do lado que não
estoura — `r > PF_INT_MAX - *total` em vez de `*total + r > PF_INT_MAX`, que
já seria o overflow. Como `r < 0` também devolve −1, o laço troca o par
`se r > 0: total += r` por uma chamada só.

A referência se comporta igual: quando o total passaria de `INT_MAX`, devolve
−1 com `errno = EOVERFLOW`, e o que já foi escrito fica escrito
([../06-aceitacao/casos.md](../06-aceitacao/casos.md)).

## Bônus: o laço

```c
int	ft_printf(const char *format, ...);
```

```
ft_printf(format, ...):
    va_start(ap, format)
    total = 0
    r = 0
    enquanto *format e r >= 0:
        se *format == '%':
            r = pf_directive(&format, &ap)
        senão:
            r = pf_putchar(*format++)
        r = pf_add(&total, r)
    va_end(ap)
    se r < 0:
        devolve -1
    devolve total
```

O laço não sabe o tamanho de uma diretiva — quem avança `format` sobre ela é
`pf_directive`, por isso o `&format`. No ramo literal o avanço é o `++` no
próprio argumento.

## Bônus: consumo de uma diretiva

```c
static int	pf_directive(const char **fmt, va_list *ap);
```

```
pf_directive(fmt, ap):
    f é t_fmt
    *fmt = parse_fmt(*fmt + 1, &f)
    se f.conv == '\0':
        devolve -1
    *fmt = *fmt + 1
    devolve pf_dispatch(&f, ap)
```

Contrato de avanço: recebe `*fmt` no `%` e o deixa **depois** da diretiva
inteira. O `+ 1` inicial pula o `%`; `parse_fmt` devolve o ponteiro parado no
byte de conversão ([../05-bonus/formato.md](../05-bonus/formato.md)); o `+ 1`
final o consome. No caso incompleto o retorno é imediato e a posição de
`*fmt` deixa de importar — o laço vai parar.

A ordem interna não pode ser trocada: **analisar antes de saber se a
conversão é conhecida**. `%-5r` precisa das flags e da largura mesmo sendo
desconhecida, porque a reimpressão sai da struct
([../05-bonus/conversoes.md](../05-bonus/conversoes.md)).

A `t_fmt` é local a esta função: nasce a cada diretiva e morre com ela. É o
que torna seguro `conv_ptr` escrever em `f->prec`.

## Bônus: despacho

```c
static int	pf_dispatch(t_fmt *f, va_list *ap);
```

```
pf_dispatch(f, ap):
    se f->conv == 'c':
        devolve conv_c(f, (char)va_arg(*ap, int))
    se f->conv == 's':
        devolve conv_s(f, va_arg(*ap, char *))
    se f->conv == 'p':
        devolve conv_ptr(f, va_arg(*ap, void *))
    se f->conv == 'd' ou f->conv == 'i':
        devolve conv_int(f, va_arg(*ap, int))
    se f->conv == 'u':
        devolve conv_uint(f, va_arg(*ap, unsigned int))
    se f->conv == 'x' ou f->conv == 'X':
        devolve conv_hex(f, va_arg(*ap, unsigned int))
    se f->conv == '%':
        devolve conv_percent()
    devolve conv_unknown(f)
```

Cadeia de `if` por escolha, não por imposição: a Norma permitiria uma tabela
`static const` de ponteiros para função
([../02-restricoes/estilo.md](../02-restricoes/estilo.md)), mas nove ramos não
pagam uma tabela de 256 entradas, e a cadeia mantém o `va_arg` de cada tipo
visível no ponto em que acontece.

Cada ramo faz o `va_arg` com o tipo da sua conversão, **dentro** do ramo. É
assim que `%%` e as desconhecidas não consomem argumento: o caminho delas não
passa por nenhum `va_arg`.

## Obrigatória: laço e despacho

A diretiva tem dois bytes fixos, então não existe `pf_directive` — o laço
avança sozinho.

```
ft_printf(format, ...):
    va_start(ap, format)
    total = 0
    r = 0
    enquanto *format e r >= 0:
        se *format == '%' e format[1] == '\0':
            r = -1
        senão se *format == '%':
            r = pf_conv(*(++format), &ap)
        senão:
            r = pf_putchar(*format)
        format += 1
        r = pf_add(&total, r)
    va_end(ap)
    se r < 0:
        devolve -1
    devolve total
```

Uma diretiva avança dois bytes: o `++format` dentro da chamada e o
`format += 1` do fim da iteração. Um literal avança um.

```
pf_conv(conv, ap):
    se conv == 'c':
        devolve pf_putchar((char)va_arg(*ap, int))
    se conv == 's':
        devolve pf_putstr(va_arg(*ap, char *))
    se conv == 'p':
        devolve pf_putptr(va_arg(*ap, void *))
    se conv == 'd' ou conv == 'i':
        devolve pf_putnbr(va_arg(*ap, int))
    se conv == 'u':
        devolve pf_putnbr_base(va_arg(*ap, unsigned int), "0123456789")
    se conv == 'x':
        devolve pf_putnbr_base(va_arg(*ap, unsigned int), "0123456789abcdef")
    se conv == 'X':
        devolve pf_putnbr_base(va_arg(*ap, unsigned int), "0123456789ABCDEF")
    se conv == '%':
        devolve pf_putchar('%')
    se pf_putchar('%') < 0 ou pf_putchar(conv) < 0:
        devolve -1
    devolve 2
```

A desconhecida é o fim da cadeia: dois bytes literais, nenhum argumento
consumido.

### As duas variantes lado a lado

| | Obrigatória | Bônus |
|---|---|---|
| tamanho da diretiva | 2 bytes | variável |
| quem avança `format` | o laço | `pf_directive` |
| diretiva incompleta | `format[1] == '\0'`, testado antes | `f.conv == '\0'`, depois da análise |
| desconhecida | 2 bytes literais em `pf_conv` | reconstrução canônica em `conv_unknown` |
| estado | nenhum | `t_fmt` por diretiva |

## `va_list` por ponteiro

O laço declara `va_list ap` e passa `&ap` adiante; **todo** `va_arg`
acontece via `*ap`, dentro do despacho. Passar o `va_list` por valor a uma
função que faz `va_arg` e depois continuar usando-o no chamador dá resultados
diferentes por plataforma — medido com dois `int` variádicos, 1 e 2:

| Plataforma | `sizeof(va_list)` | Por valor, o chamador lê | Por ponteiro |
|---|---|---|---|
| x86-64 SysV | 24 (array de uma struct) | 2 — o array decai em ponteiro e o cursor avança "por acidente" | 2 |
| ARM64 Linux (AAPCS64) | 32 (struct) | **1** — a struct foi copiada, o chamador relê o primeiro | 2 |
| ARM64 Apple | 8 (`char *`) | **1** — o ponteiro foi copiado, idem | 2 |

Por valor, o segundo `%d` de um formato imprimiria o primeiro argumento de
novo em duas das três. `&ap` elimina a diferença: existe um só `va_list`
vivo, o do laço, e todos o avançam através do ponteiro. Vale nas duas
variantes — `pf_conv` e `pf_dispatch` recebem `va_list *`.

## Caminho de erro

Não há limpeza a fazer: nenhuma alocação, nenhum estado fora da pilha.
Propagar o `-1` **é** o caminho de erro inteiro. Cada escritor devolve `-1`
assim que um `write` falha; montadores e conversões testam cada escrita e
repassam; o laço para na primeira falha e a `ft_printf` devolve `-1`.
