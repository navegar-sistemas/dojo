# Tipos

A parte obrigatória não define tipo nenhum: os escritores recebem valores
primitivos e escrevem na hora. Todo o estado de formatação do bônus vive numa
única struct, declarada em `ft_printf_bonus.h`.

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
| `width` | largura mínima | ≥ 0; **0 = ausente** — largura 0 explícita é indistinguível de nenhuma largura |
| `prec` | precisão | **−1 = ausente**; 0 é valor legal e distinto (`%.d` ≡ `%.0d`) |
| `conv` | byte de conversão | **`'\0'` = o formato acabou no meio da diretiva** |

Uma instância nasce por diretiva, na pilha de `pf_directive`, e morre com
ela ([fluxo.md](fluxo.md)). Sempre por `fmt_init`, que zera tudo e põe
`prec = -1`, porque as regras de estilo proíbem inicialização na declaração
([../02-restricoes/estilo.md](../02-restricoes/estilo.md)).

## Quem lê cada campo

| Campo | Leitores |
|---|---|
| `width` | `conv_c`, `conv_s`, `put_num`, `conv_unknown` |
| `minus` | `conv_c`, `conv_s`, `put_num`, `unk_head` |
| `zero` | `put_num` — só quando `prec == -1` e `minus == 0` — e `unk_head` |
| `prec` | `conv_s` (truncamento), `put_num` (mínimo de dígitos), `conv_int`/`conv_uint`/`conv_hex` (esvaziamento), `conv_unknown`, e `conv_ptr`, que **escreve** −1 para `NULL` |
| `hash` | `conv_hex`, `unk_head` |
| `plus`, `space` | `conv_int`, `conv_ptr`, `unk_head` |
| `conv` | `pf_dispatch`, `conv_hex` (decide `x` ou `X`), `conv_unknown` |

`conv_percent` não lê nenhum: `%%` ignora a struct inteira.

`conv_ptr` é o único que escreve depois da análise — `f->prec = -1` desliga a
precisão antes de delegar `(nil)` a `conv_s`
([../05-bonus/conversoes.md](../05-bonus/conversoes.md)). Como a struct é
local à diretiva, a escrita não vaza para a próxima.

## Por que `prec` não pode ser 0 quando ausente

`%.0d` com 0 imprime vazio; `%d` com 0 imprime `[0]`. Se ausência fosse 0, as
duas seriam indistinguíveis. O sentinela −1 é também o que dá a `conv_ptr` um
jeito de uma linha de ignorar a precisão.

`width` não precisa de sentinela porque largura 0 e largura ausente produzem
a mesma saída em todos os casos.
