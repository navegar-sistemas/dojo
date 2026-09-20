# Fluxo

O mesmo esqueleto nas duas variantes: um laço sobre o formato, um despacho
por conversão, e o valor `r` carregando o resultado de cada passo.

| `r` | Significado | Efeito |
|---|---|---|
| > 0 | bytes escritos pelo passo | soma em `total` |
| 0 | passo válido que não escreveu nada (`%.0d` com 0) | nada a somar |
| −1 | `write` falhou **ou** diretiva incompleta | o laço para, retorno −1 |

Os bytes já escritos ficam escritos: `"abc%"` imprime `[abc]` e devolve −1.

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
        se r > 0:
            total += r
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

Cadeia de `if`, não tabela: um vetor de ponteiros para função seria variável
global em escopo de arquivo, ou inicialização na declaração em escopo local —
as duas proibidas ([../02-restricoes/estilo.md](../02-restricoes/estilo.md)).

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
        se r > 0:
            total += r
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
acontece via `*ap`, dentro do despacho. O motivo é de ABI:

- no x86-64 (SysV), `va_list` é um array de uma struct; passá-lo "por valor"
  na prática passa um ponteiro, e o cursor avança para o chamador — funciona
  por acidente;
- no ARM64 da Apple, `va_list` é um `char *` simples. Por valor, a função
  chamada avança uma **cópia**, o chamador não vê nada, e o segundo `%d` relê
  o primeiro argumento.

`&ap` elimina a diferença: existe um só `va_list` vivo, o do laço, e todos o
avançam através do ponteiro. Vale nas duas variantes — `pf_conv` e
`pf_dispatch` recebem `va_list *`.

## Caminho de erro

Não há limpeza a fazer: nenhuma alocação, nenhum estado fora da pilha.
Propagar o `-1` **é** o caminho de erro inteiro. Cada escritor devolve `-1`
assim que um `write` falha; montadores e conversões testam cada escrita e
repassam; o laço para na primeira falha e a `ft_printf` devolve `-1`.
