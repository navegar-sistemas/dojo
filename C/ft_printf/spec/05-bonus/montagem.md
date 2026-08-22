# Montagem de campo numérico — `put_num`

Um único montador para `%d` `%i` `%u` `%x` `%X` `%p`(≠ NULL). Recebe a
`t_fmt`, o **prefixo** pronto (string) e os **dígitos** prontos (string, sem
sinal, saídos de `render_base`).

```c
int	put_num(t_fmt *f, char *pre, char *digits);
```

## As três contagens

```
zeros  = max(0, prec - strlen(digits))          # zeros de precisão
se zero e não minus e prec ausente:
    zeros = max(zeros, largura - strlen(pre) - strlen(digits))
                                                # zeros de largura
total  = strlen(pre) + zeros + strlen(digits)
espacos = max(0, largura - total)               # sempre espaços
```

A flag `0` é literalmente "precisão até encher a largura": entra na mesma
variável `zeros`, já descontando o prefixo. As condições de validade — não com
`-`, não com precisão — ficam no `se`, e o resto do montador não sabe que a
flag existe.

## Ordem de emissão

```
se não minus: espacos vezes ' '
pre, zeros vezes '0', digits
se minus:     espacos vezes ' '
devolve max(largura, total)      # na prática: total, ou largura se maior
```

Zeros **sempre** entre o prefixo e os dígitos — é o que produz `[+0042]` e
nunca `[0+042]`.

## As linhas medidas, explicadas pelas contagens

| Caso | pre | digits | zeros | espaços | Saída |
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
| `%.0d`, 0 | `` | `` (esvaziado) | 0 | 0 | `[]` |
| `%+.0d`, 0 | `+` | `` | 0 | 0 | `[+]` |

"Esvaziado": com precisão 0 e valor 0, o **chamador** faz `buf[0] = '\0'`
antes de entregar os dígitos ([../04-emissao/numeros.md](../04-emissao/numeros.md)).

## Quem monta o prefixo

| Chamador | Prefixos possíveis |
|---|---|
| `conv_int` | `-`, `+`, ` `, `` |
| `conv_uint` | `` |
| `conv_hex` | `0x`, `0X`, `` |
| `conv_ptr` | `0x`, `+0x`, ` 0x` |

## Campos de texto não passam por aqui

`conv_c` e `conv_s` alinham com espaços dos dois lados possíveis e nada mais —
sem zeros, sem prefixo:

```
se não minus: pad(' ', largura - len)
conteúdo
se minus:     pad(' ', largura - len)
devolve max(largura, len)
```

com `len` = 1 em `%c`, e em `%s` o comprimento já truncado pela precisão. O
`pf_pad` aceitando contagem negativa é o que dispensa o caso "conteúdo maior
que a largura" ([../04-emissao/escritores.md](../04-emissao/escritores.md)).
