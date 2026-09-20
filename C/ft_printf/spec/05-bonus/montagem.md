# Montagem do campo numérico — `put_num`

Um montador único para `%d`, `%i`, `%u`, `%x`, `%X` e `%p` não nulo. Recebe a
`t_fmt`, o **prefixo** pronto e os **dígitos** prontos, as duas coisas como
string; quem os produz são as conversões
([conversoes.md](conversoes.md)).

```c
int	put_num(t_fmt *f, char *pre, char *digits);
```

```
put_num(f, pre, digits):
    zeros = f->prec - pf_strlen(digits)
    se zeros < 0:
        zeros = 0
    se f->zero e não f->minus e f->prec < 0:
        total = pf_strlen(pre) + pf_strlen(digits)
        se f->width - total > zeros:
            zeros = f->width - total
    total = pf_strlen(pre) + zeros + pf_strlen(digits)
    se não f->minus e pf_pad(' ', f->width - total) < 0:
        devolve -1
    se pf_putn(pre, pf_strlen(pre)) < 0 ou pf_pad('0', zeros) < 0
       ou pf_putn(digits, pf_strlen(digits)) < 0:
        devolve -1
    se f->minus e pf_pad(' ', f->width - total) < 0:
        devolve -1
    se f->width > total:
        devolve f->width
    devolve total
```

## As duas contagens

**`zeros`** é a única variável que os dois tipos de preenchimento disputam:

| Origem | Quando | Valor |
|---|---|---|
| precisão | sempre | `prec - len(digits)`, nunca negativo |
| flag `0` | `zero` e não `minus` e `prec` ausente | `width - len(pre) - len(digits)`, se for maior |

A flag `0` é literalmente "precisão até encher a largura", já descontando o
prefixo — por isso entra na mesma variável. As três condições de validade
ficam no `se`, e o resto do montador não sabe que a flag existe. É daí que
saem, sem caso especial, as duas regras transversais: `-` vence `0`, e
precisão desliga `0`.

**`total`** aparece duas vezes com sentidos diferentes, para economizar uma
variável: dentro do `se` é o comprimento **sem** zeros, usado só para medir
quantos zeros a largura pede; na linha seguinte é recalculado como o
comprimento real do campo. Os espaços nunca ganham variável — são
`width - total`, entregues direto a `pf_pad`, que aceita negativo.

## Ordem de emissão

```
espaços à esquerda   se não minus
prefixo
zeros
dígitos
espaços à direita    se minus
```

Zeros **sempre** entre o prefixo e os dígitos: `[+0042]`, nunca `[0+042]`.
As três emissões do meio compartilham um único `se` com `ou` — não é estilo,
é o que mantém o corpo em 23 linhas
([../02-restricoes/estilo.md](../02-restricoes/estilo.md)).

O retorno é `max(width, total)`: quando a largura venceu, o campo tem
exatamente `width` bytes; quando não, tem `total`.

## As linhas medidas, explicadas pelas contagens

| Caso | `pre` | `digits` | `zeros` | espaços | Saída |
|---|---|---|---|---|---|
| `%+05d`, 42 | `+` | `42` | 2 (largura) | 0 | `[+0042]` |
| `% 05d`, 42 | ` ` | `42` | 2 (largura) | 0 | `[ 0042]` |
| `%05.3d`, 42 | `` | `42` | 1 (precisão; `0` desligada) | 2 | `[  042]` |
| `%5.3d`, −42 | `-` | `42` | 1 | 1 | `[ -042]` |
| `%020d`, INT_MIN | `-` | `2147483648` | 9 (largura) | 0 | `[-0000000002147483648]` |
| `%#08x`, 255 | `0x` | `ff` | 4 (largura) | 0 | `[0x0000ff]` |
| `%#5.3x`, 255 | `0x` | `ff` | 1 (precisão) | 0 | `[0x0ff]` |
| `% 015p`, 0x1234 | ` 0x` | `1234` | 8 (largura) | 0 | `[ 0x000000001234]` |
| `%+.8p`, 0x1234 | `+0x` | `1234` | 4 (precisão) | 0 | `[+0x00001234]` |
| `%-8.5d`, −42 | `-` | `42` | 3 | 2 à direita | `[-00042  ]` |
| `%.0d`, 0 | `` | `` | 0 | 0 | `[]` |
| `%+.0d`, 0 | `+` | `` | 0 | 0 | `[+]` |

Nas duas últimas, `digits` chega vazio: com precisão 0 e valor 0 o chamador
esvazia o buffer antes de entregá-lo
([../04-emissao/numeros.md](../04-emissao/numeros.md)). O prefixo sobrevive,
e é por isso que `%+.0d` escreve um byte.

## Campos de texto não passam por aqui

`conv_c` e `conv_s` alinham com espaços dos dois lados possíveis e nada mais
— sem prefixo, sem zeros, sem precisão de dígitos
([conversoes.md](conversoes.md)).
