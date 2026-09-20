# Escritores

O andar de baixo das duas variantes: as únicas funções que tocam o descritor
1. Todas devolvem os bytes que escreveram, ou `-1` se um `write` falhou
([../03-arquitetura/modulos.md](../03-arquitetura/modulos.md)).

| Função | Variante | Arquivo | Devolve | Pré-condição |
|---|---|---|---|---|
| `pf_putchar` | as duas | `pf_put.c`, `put_bonus.c` | 1 | — |
| `pf_putstr` | obrigatória | `pf_put.c` | comprimento escrito, ou −1 se passar de `INT_MAX` | `NULL` é aceito |
| `pf_putn` | bônus | `put_bonus.c` | `n`, em `long` | `n ≥ 0`, `s` com ao menos `n` bytes |
| `pf_pad` | bônus | `put_bonus.c` | `n`, ou 0 se `n < 0` | — |
| `pf_strlen` | bônus | `put_bonus.c` | comprimento | só strings do projeto, sempre curtas |
| `pf_strnlen` | bônus | `put_bonus.c` | comprimento limitado a `max`, em `long` | `max < 0` = sem limite |

## `pf_putchar` — as duas variantes

```c
int	pf_putchar(char c);
```

```
pf_putchar(c):
    se write(1, &c, 1) < 0:
        devolve -1
    devolve 1
```

Todo byte do projeto sai por aqui, um `write` por byte. Junto com `pf_add`,
é o único código idêntico nas duas variantes
([../03-arquitetura/decisoes.md](../03-arquitetura/decisoes.md)).

## Obrigatória: `pf_putstr`

```c
int	pf_putstr(char *s);
```

```
pf_putstr(s):
    i é long
    se s é NULL:
        s = "(null)"
    i = 0
    enquanto s[i]:
        se pf_putchar(s[i]) < 0:
            devolve -1
        i += 1
    se i > PF_INT_MAX:
        devolve -1
    devolve i
```

O contador é `long` porque uma string pode ter mais de `INT_MAX` bytes, e um
`int` estouraria no meio do laço. A referência escreve a string inteira e só
então devolve −1; aqui é igual — a conferência vem depois do laço.

A substituição de `NULL` é incondicional porque na parte obrigatória não
existe precisão. No bônus a mesma regra depende dela e mora em `conv_s`
([../05-bonus/conversoes.md](../05-bonus/conversoes.md)).

Escreve até o `'\0'`, que fica de fora: `pf_putstr("")` devolve 0 sem
escrever nada.

## Bônus: `pf_putn`

```c
long	pf_putn(const char *s, long n);
```

```
pf_putn(s, n):
    i é long
    i = 0
    enquanto i < n:
        se pf_putchar(s[i]) < 0:
            devolve -1
        i += 1
    devolve n
```

Escreve por contagem, não por terminador — é o truncamento de `%.3s` e a
emissão da diretiva desconhecida, que carrega bytes depois do `'\0'` deixado
por `render_base`. Os chamadores nunca passam `n` negativo: `conv_s` limita
`len` à precisão, e `conv_unknown` conta o que montou.

`n` e o retorno são `long` porque `conv_s` pode mandar escrever uma string de
mais de `INT_MAX` bytes; devolver esse `n` como `int` o transformaria num
número negativo, que o chamador leria como falha de escrita.

## Bônus: `pf_pad`

```c
int	pf_pad(char c, int n);
```

```
pf_pad(c, n):
    i = 0
    enquanto i < n:
        se pf_putchar(c) < 0:
            devolve -1
        i += 1
    se n < 0:
        devolve 0
    devolve n
```

Repete um byte `n` vezes e **aceita `n` negativo devolvendo 0**. É o que
permite escrever `pf_pad(' ', f->width - len)` sem testar se a largura já foi
vencida: o caso "conteúdo maior que a largura" desaparece de todos os
chamadores em vez de aparecer em cada um.

## Bônus: `pf_strlen`

```c
int	pf_strlen(const char *s);
```

```
pf_strlen(s):
    i = 0
    enquanto s[i]:
        i += 1
    devolve i
```

Comprimento de string do projeto — nenhuma função de biblioteca entra no
build ([../02-restricoes/build.md](../02-restricoes/build.md)). Só mede
strings que o próprio projeto montou: prefixos de até 3 bytes, dígitos de até
20, o buffer da diretiva desconhecida. `put_num` a chama cinco vezes. A
string do usuário, em `%s`, passa por `pf_strnlen`.

## Bônus: `pf_strnlen`

```c
long	pf_strnlen(const char *s, long max);
```

```
pf_strnlen(s, max):
    i é long
    i = 0
    enquanto (max < 0 ou i < max) e s[i]:
        i += 1
    devolve i
```

Comprimento que **para em `max`**. `conv_s` a chama com a precisão, e o −1 de
"precisão ausente" vira "sem limite" sem nenhum teste extra.

A ordem da condição é o ponto: o limite é conferido **antes** de `s[i]` ser
lido. Em C é legal passar a `%.3s` um array de 3 bytes sem terminador — a
linguagem só exige o `'\0'` quando a precisão é ausente ou maior que o array
— e um `strlen` comum andaria pela memória vizinha até achar um zero. Com
ASan, essa leitura é `heap-buffer-overflow`; sem ele, pode ser um segfault,
que o subject pune com nota 0.
