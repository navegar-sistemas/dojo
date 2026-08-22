# Tipos

A parte obrigatória não define tipo nenhum: os escritores recebem valores
primitivos e escrevem na hora. Todo o estado de formatação do bônus vive numa
única struct, em `ft_printf_bonus.h`.

## `t_fmt`

```c
typedef struct s_fmt
{
	int		minus;
	int		zero;
	int		hash;
	int		plus;
	int		space;
	int		width;
	int		prec;
	char	conv;
}	t_fmt;
```

| Campo | Conteúdo | Invariante |
|---|---|---|
| `minus` `zero` `hash` `plus` `space` | flags, 0 ou 1 | repetição no formato não acumula |
| `width` | largura mínima | ≥ 0; 0 = ausente (largura 0 explícita é indistinguível de ausente, como na referência) |
| `prec` | precisão | **−1 = ausente**; 0 é valor legal e distinto (`"%.d"` ≡ `"%.0d"`) |
| `conv` | byte de conversão | `'\0'` = formato acabou no meio da diretiva |

A struct nasce sempre por `fmt_init` (zera tudo e põe `prec = -1`), porque as
regras de estilo proíbem inicialização na declaração
([../02-restricoes/estilo.md](../02-restricoes/estilo.md)).

## Quem consome o quê

| Campo | Consumidores |
|---|---|
| `minus`, `width` | todas as conversões com campo (`conv_c`, `conv_s`, `put_num`) |
| `zero` | só `put_num` — e só quando `prec == -1` e `minus == 0` |
| `prec` | `conv_s` (truncamento), `put_num` (mínimo de dígitos), `conv_ptr` (neutralizada para `NULL`) |
| `hash` | `conv_hex` |
| `plus`, `space` | `conv_int`, `conv_ptr` |
| `conv` | `pf_dispatch`, `conv_hex` (decide `x`/`X`), `conv_unknown` |

`%%` ignora a struct inteira — medido em
[../06-aceitacao/casos.md](../06-aceitacao/casos.md).

## Por que `prec` não pode ser 0 quando ausente

`"%.0d"` com `0` imprime vazio; `"%d"` com `0` imprime `[0]`. Se ausência
fosse 0, as duas seriam indistinguíveis. O sentinela −1 também é o que permite
a `conv_ptr` "desligar" a precisão para `(nil)` com uma atribuição.
