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
| largura e precisão cabem em `int` | fora disso é fora do domínio ([../01-contrato/api.md](../01-contrato/api.md)) |

Em `%007r` os dois `0` são flags e a largura é 7. Em `%00500d` o primeiro `0`
é flag e a largura é 500 — o laço de flags para no `5`, e daí em diante todo
dígito é largura, zeros incluídos.

## As três funções

`parse_bonus.c` inteiro: uma para zerar, uma para as flags, uma para o resto.

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
    enquanto *s é dígito:
        f->width = f->width * 10 + (*s - '0')
        s += 1
    se *s == '.':
        s += 1
        f->prec = 0
        enquanto *s é dígito:
            f->prec = f->prec * 10 + (*s - '0')
            s += 1
    f->conv = *s
    devolve s
```

O `.` põe `prec = 0` **antes** do laço de dígitos: é isso que faz a precisão
vazia valer 0 sem nenhum caso especial. Quando o formato acaba no meio,
`*s` é `'\0'` e `f->conv` recebe `'\0'` — o sinal de diretiva incompleta,
tratado por quem chamou.

## Casos de análise que enganam

| Formato | flags | `width` | `prec` | `conv` |
|---|---|---|---|---|
| `%-05d` | `minus`, `zero` | 5 | −1 | `d` |
| `%00500d` | `zero` | 500 | −1 | `d` |
| `%5.d` | — | 5 | 0 | `d` |
| `%.5` | — | 0 | 5 | `'\0'` → incompleta, retorno −1 |
| `% ` | `space` | 0 | −1 | `'\0'` → incompleta, retorno −1 |
| `%5.2r` | — | 5 | 2 | `r` → desconhecida |

A diretiva incompleta vira o `-1` do contrato
([../01-contrato/api.md](../01-contrato/api.md)) e nada dela é impresso; a
desconhecida é reimpressa a partir da struct
([conversoes.md](conversoes.md)).
