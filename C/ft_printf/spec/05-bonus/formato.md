# Gramática da diretiva (bônus)

## Forma

```
diretiva  := '%' flag* largura? precisao? conversao
flag      := '-' | '0' | '#' | '+' | ' '
largura   := digito+
precisao  := '.' digito*
conversao := qualquer byte — ou nenhum, se o formato acabar
```

| Regra | Efeito |
|---|---|
| flags em qualquer ordem, com repetição | repetir não acumula: `%--5d` ≡ `%-5d` |
| `0` à esquerda da largura é flag | o laço de flags consome todos os bytes do conjunto antes de a largura começar |
| precisão vazia vale 0 | `%.d` ≡ `%.0d`, `%.s` ≡ `%.0s` |
| largura e precisão vão até `INT_MAX`, inclusive | um dígito a mais e a diretiva inteira falha: nada dela é impresso, retorno −1 |

Em `%007r` os dois `0` são flags e a largura é 7. Em `%00500d` o primeiro `0`
é flag e a largura é 500 — o laço de flags para no `5`, e daí em diante todo
dígito é largura, zeros incluídos.

## As quatro funções

`parse_bonus.c` inteiro: uma para zerar, uma para as flags, uma para os
números, uma que costura as três.

### `fmt_init`

```c
static void	fmt_init(t_fmt *f);
```

```
fmt_init(f):
    f->minus = 0
    f->zero = 0
    f->hash = 0
    f->plus = 0
    f->space = 0
    f->width = 0
    f->prec = -1
    f->conv = '\0'
```

Existe porque as regras de estilo proíbem inicializar na declaração
([../02-restricoes/estilo.md](../02-restricoes/estilo.md)). Os dois valores
que não são zero carregam significado: `prec = -1` é "precisão ausente" e
`conv = '\0'` é "diretiva incompleta"
([../03-arquitetura/tipos.md](../03-arquitetura/tipos.md)).

### `parse_flags`

```c
static const char	*parse_flags(const char *s, t_fmt *f);
```

```
parse_flags(s, f):
    enquanto *s é um de "-0#+ ":
        se *s == '-': f->minus = 1
        se *s == '0': f->zero = 1
        se *s == '#': f->hash = 1
        se *s == '+': f->plus = 1
        se *s == ' ': f->space = 1
        s += 1
    devolve s
```

A deduplicação é de graça: atribuir 1 duas vezes dá 1. Os cinco testes são
independentes — nenhum `senão` —, mas só um pode casar por iteração.

### `parse_num`

```c
static int	parse_num(const char **s, int *n);
```

```
parse_num(s, n):
    *n = 0
    enquanto **s é dígito:
        se *n > (PF_INT_MAX - (**s - '0')) / 10:
            devolve -1
        *n = *n * 10 + (**s - '0')
        *s += 1
    devolve 0
```

Lê um número decimal, avança o ponteiro do chamador e devolve −1 se o valor
passaria de `INT_MAX`. Serve à largura e à precisão — o mesmo laço, com
destinos diferentes.

A conta `*n * 10 + dígito` monta o número da esquerda para a direita: a cada
dígito novo, o que já foi lido vale dez vezes mais. `**s - '0'` transforma o
caractere no valor — os dígitos são contíguos na tabela ASCII, de `'0'` = 48
a `'9'` = 57.

A guarda vem **antes** da multiplicação, e está escrita do lado que não
estoura: `*n * 10 + d <= INT_MAX` equivale a `*n <= (INT_MAX - d) / 10`.
Conferir depois seria tarde — overflow de `int` com sinal é comportamento
indefinido, e o compilador tem licença para assumir que não acontece. Sem a
guarda, `%4294967296d` dava a volta exata em 32 bits e imprimia como `%d`.

| Formato | Resultado |
|---|---|
| `%2147483647d` | largura `INT_MAX`, aceita |
| `%2147483648d` | −1 |
| `%4294967296d` | −1 |
| `%.99999999999d` | −1 |

### `parse_fmt`

```c
const char	*parse_fmt(const char *s, t_fmt *f);
```

Recebe `s` no primeiro byte **depois** do `%`, preenche `f` e devolve o
ponteiro parado no byte de conversão, sem consumi-lo — quem avança é
`pf_directive` ([../03-arquitetura/fluxo.md](../03-arquitetura/fluxo.md)).

```
parse_fmt(s, f):
    fmt_init(f)
    s = parse_flags(s, f)
    se parse_num(&s, &f->width) < 0:
        devolve s
    se *s == '.':
        s += 1
        se parse_num(&s, &f->prec) < 0:
            devolve s
    f->conv = *s
    devolve s
```

`parse_num` começa pondo 0 no destino, e é isso que faz a precisão vazia
valer 0 sem caso especial: depois do `.`, `%.d` não tem dígito nenhum e
`prec` fica no 0 inicial — deixando de ser o −1 de "ausente".

**Os dois retornos antecipados reaproveitam o mecanismo da diretiva
incompleta.** `fmt_init` deixou `conv = '\0'`; quem sai antes de
`f->conv = *s` devolve a struct com essa marca, e `pf_directive` a converte em
−1 ([../03-arquitetura/fluxo.md](../03-arquitetura/fluxo.md)). Nenhum campo
novo, nenhum código de erro novo — e o efeito é o da referência: nada da
diretiva é impresso, os literais anteriores ficam.

O ponteiro devolvido nesse caso aponta para o dígito que estouraria — dentro
da string, portanto seguro de desreferenciar na condição do laço, que então
para por `r < 0`.

Quando o formato acaba no meio, `*s` é `'\0'` e `f->conv` recebe `'\0'` pelo
caminho normal: a mesma marca, o mesmo tratamento.

## Casos de análise que enganam

| Formato | flags | `width` | `prec` | `conv` |
|---|---|---|---|---|
| `%-05d` | `minus`, `zero` | 5 | −1 | `d` |
| `%00500d` | `zero` | 500 | −1 | `d` |
| `%5.d` | — | 5 | 0 | `d` |
| `%.5` | — | 0 | 5 | `'\0'` → incompleta, retorno −1 |
| `% ` | `space` | 0 | −1 | `'\0'` → incompleta, retorno −1 |
| `%5.2r` | — | 5 | 2 | `r` → desconhecida |
| `%2147483648d` | — | estourou | −1 | `'\0'` → retorno −1, nada impresso |

A diretiva incompleta vira o `-1` do contrato
([../01-contrato/api.md](../01-contrato/api.md)) e nada dela é impresso; a
desconhecida é reimpressa a partir da struct
([conversoes.md](conversoes.md)).
