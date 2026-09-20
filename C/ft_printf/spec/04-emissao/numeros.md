# Números

Dois caminhos para a mesma tarefa, e a diferença não é de gosto: a parte
obrigatória escreve os dígitos assim que os descobre, o bônus precisa
**contá-los antes** do primeiro byte sair, porque largura e precisão dependem
do comprimento.

| Variante | Função | Estratégia | Saída |
|---|---|---|---|
| obrigatória | `pf_putnbr_base` | recursão | bytes no descritor 1 |
| bônus | `render_base` | buffer preenchido de trás para a frente | string em `buf` |

## Obrigatória: `pf_putnbr_base`

```c
int	pf_putnbr_base(unsigned long n, const char *base);
```

```
pf_putnbr_base(n, base):
    b = 0
    enquanto base[b]:
        b += 1
    len = 0
    se n >= b:
        len = pf_putnbr_base(n / b, base)
        se len < 0:
            devolve -1
    se pf_putchar(base[n % b]) < 0:
        devolve -1
    devolve len + 1
```

A recursão emite o dígito mais significativo primeiro sem buffer nenhum: a
chamada de baixo escreve o resto da divisão depois que a de cima já escreveu
o seu. Profundidade máxima 20 — os dígitos decimais de um `unsigned long` de
64 bits.

A base é o alfabeto, passado por literal: `"0123456789"`,
`"0123456789abcdef"`, `"0123456789ABCDEF"`. O comprimento sai da própria
string, então uma base nova não pede código novo.

## Obrigatória: `pf_putnbr`

```c
static int	pf_putnbr(int n);
```

```
pf_putnbr(n):
    v é long
    v = n
    len = 0
    se v < 0:
        se pf_putchar('-') < 0:
            devolve -1
        len = 1
        v = -v
    r = pf_putnbr_base(v, "0123456789")
    se r < 0:
        devolve -1
    devolve len + r
```

O `int` é copiado para um `long` antes da negação: `-INT_MIN` estoura em
`int`, mas cabe em 64 bits. O valor chega a `pf_putnbr_base` como
`unsigned long`, já positivo.

## Obrigatória: `pf_putptr`

```c
int	pf_putptr(void *ptr);
```

```
pf_putptr(ptr):
    se ptr é NULL:
        devolve pf_putstr("(nil)")
    se pf_putstr("0x") < 0:
        devolve -1
    r = pf_putnbr_base(ptr, "0123456789abcdef")
    se r < 0:
        devolve -1
    devolve r + 2
```

O ponteiro passa por `(unsigned long)`, que tem o tamanho de um endereço nas
plataformas-alvo (LP64). Sem zeros à esquerda: `0x1234` sai com 6 bytes.

## Bônus: `render_base`

```c
void	render_base(unsigned long n, const char *base, char *buf);
```

```
render_base(n, base, buf):
    b = 0
    enquanto base[b]:
        b += 1
    len = 1
    tmp = n
    enquanto tmp >= b:
        tmp = tmp / b
        len += 1
    buf[len] = '\0'
    enquanto len > 0:
        len -= 1
        buf[len] = base[n % b]
        n = n / b
```

Duas passadas: a primeira conta os dígitos sem escrever, a segunda preenche
do último para o primeiro. Não devolve nada — quem chama mede o resultado com
`pf_strlen`.

| Detalhe | Consequência |
|---|---|
| `len` parte de 1 | `n == 0` produz `"0"`, nunca string vazia |
| o `'\0'` é escrito antes dos dígitos | `buf` é uma string válida assim que a função retorna |
| `char buf[24]` nos chamadores | 20 dígitos decimais de 64 bits + `'\0'`, com folga |

O caso "precisão 0 com valor 0 imprime vazio" **não** é decidido aqui: o
chamador esvazia o buffer depois (`buf[0] = '\0'`), já sabendo a precisão
([../05-bonus/conversoes.md](../05-bonus/conversoes.md)).

## Sinal, nas duas variantes

O sinal nunca entra no buffer de dígitos. Na obrigatória ele é escrito antes
da recursão; no bônus vira o **prefixo** que `put_num` recebe
([../05-bonus/montagem.md](../05-bonus/montagem.md)). É o que produz
`[+0042]` e nunca `[0+042]`, e o que faz o `-` não contar como dígito de
precisão: `%.5d` com −42 dá `[-00042]`, seis bytes.
