# Gramática da diretiva (bônus)

## Forma

```
diretiva  := '%' flag* largura? precisao? conversao
flag      := '-' | '0' | '#' | '+' | ' '
largura   := digito+
precisao  := '.' digito*
conversao := qualquer byte (inclusive nenhum, se o formato acabar)
```

- Flags em **qualquer ordem**, com **repetição** — repetir não acumula:
  `%--5d` ≡ `%-5d`.
- `0` à esquerda da largura é flag, não dígito de largura: o laço de flags
  consome **todos** os bytes do conjunto antes de a largura começar. Em
  `%007r` os dois `0` são flags e a largura é 7; em `%00500d`, flag `0` e
  largura 500.
- Precisão vazia vale **0**: `%.d` ≡ `%.0d`, `%.s` ≡ `%.0s` — medido.
- Largura e precisão cabem em `int`; fora disso é fora do domínio
  ([../01-contrato/api.md](../01-contrato/api.md)).

## `parse_fmt`

```c
const char	*parse_fmt(const char *s, t_fmt *f);
```

Recebe `s` no primeiro byte **depois** do `%`; preenche `f` e devolve o
ponteiro parado no byte de conversão — sem consumi-lo (quem avança é
`pf_directive`, [../03-arquitetura/fluxo.md](../03-arquitetura/fluxo.md)).

```
parse_fmt(s, f):
    fmt_init(f)                       # zera tudo, prec = -1
    s = parse_flags(s, f)             # laço no conjunto "-0# +"
    enquanto '0' <= *s <= '9':
        f.largura = f.largura * 10 + (*s - '0'); s += 1
    se *s == '.':
        s += 1; f.prec = 0
        enquanto '0' <= *s <= '9':
            f.prec = f.prec * 10 + (*s - '0'); s += 1
    f.conv = *s
    devolve s
```

`fmt_init` existe porque declaração com inicialização é proibida
([../02-restricoes/estilo.md](../02-restricoes/estilo.md)).

## Casos de análise que enganam

| Formato | flags | largura | prec | conv |
|---|---|---|---|---|
| `%-05d` | `-`, `0` | 5 | ausente | `d` |
| `%00500d` | `0` | 500 | ausente | `d` |
| `%5.d` | — | 5 | 0 | `d` |
| `%.5` | — | 0 | 5 | `'\0'` → incompleta, retorno −1 |
| `% ` | espaço | 0 | ausente | `'\0'` → incompleta, retorno −1 |
| `%5.2r` | — | 5 | 2 | `r` → desconhecida |

A diretiva incompleta (`conv == '\0'`) é detectada por `pf_directive` e vira o
`-1` do contrato ([../01-contrato/api.md](../01-contrato/api.md)) — nada da
diretiva parcial é impresso, medido em
[../06-aceitacao/casos.md](../06-aceitacao/casos.md).
