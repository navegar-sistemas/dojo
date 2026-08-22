# Módulos

Uma responsabilidade por arquivo, respeitando o teto de 5 funções (contando
`static`) e 25 linhas por corpo. As contagens são as da implementação de
referência, que compila com `-Wall -Wextra -Werror` e cabe nos dois limites.

## Parte obrigatória

| Arquivo | Funções | Maior corpo | Responsabilidade |
|---|---|---|---|
| `ft_printf.c` | 3 | 23 | laço, despacho por conversão, inteiro com sinal |
| `pf_put.c` | 4 | 16 | byte, string, dígitos por base (recursivo), ponteiro |

## Bônus

| Arquivo | Funções | Maior corpo | Responsabilidade |
|---|---|---|---|
| `ft_printf_bonus.c` | 3 | 20 | laço, consumo da diretiva, despacho |
| `parse_bonus.c` | 3 | 19 | gramática da diretiva → `t_fmt` |
| `put_bonus.c` | 4 | 12 | byte, n bytes, padding, comprimento |
| `conv_text_bonus.c` | 5 | 18 | `%c`, `%s`, `%%`, desconhecida canônica |
| `conv_num_bonus.c` | 2 | 19 | `%d`/`%i`, `%u` |
| `conv_hex_bonus.c` | 2 | 15 | `%x`/`%X`, `%p` |
| `num_render_bonus.c` | 2 | 23 | dígitos em buffer, montador de campo |

`conv_text_bonus.c` fecha em 5 funções — o teto — porque `conv_unknown`
precisa do ajudante `unk_head` para caber em 25 linhas
([../02-restricoes/estilo.md](../02-restricoes/estilo.md)).

## Assinaturas públicas — obrigatória (`ft_printf.h`)

```c
int	ft_printf(const char *format, ...);
int	pf_putchar(char c);
int	pf_putstr(char *s);
int	pf_putnbr_base(unsigned long n, const char *base);
int	pf_putptr(void *ptr);
```

`static` em `ft_printf.c`: `pf_putnbr(int n)` (sinal + dígitos) e
`pf_conv(char conv, va_list *ap)` (despacho).

## Assinaturas públicas — bônus (`ft_printf_bonus.h`)

```c
int			ft_printf(const char *format, ...);
const char	*parse_fmt(const char *s, t_fmt *f);
int			pf_putchar(char c);
int			pf_putn(const char *s, int n);
int			pf_pad(char c, int n);
int			pf_strlen(const char *s);
void		render_base(unsigned long n, const char *base, char *buf);
int			put_num(t_fmt *f, char *pre, char *digits);
int			conv_c(t_fmt *f, char c);
int			conv_s(t_fmt *f, char *s);
int			conv_percent(void);
int			conv_unknown(t_fmt *f);
int			conv_int(t_fmt *f, int n);
int			conv_uint(t_fmt *f, unsigned int n);
int			conv_hex(t_fmt *f, unsigned int n);
int			conv_ptr(t_fmt *f, void *p);
```

`static`: `fmt_init` e `parse_flags` em `parse_bonus.c`; `pf_dispatch` e
`pf_directive` em `ft_printf_bonus.c`; `unk_head` em `conv_text_bonus.c`.

## Contrato de retorno comum

Toda função que escreve devolve o número de bytes que escreveu, ou `-1` se
qualquer `write` falhou. É um contrato só, do `pf_putchar` até a `ft_printf` —
a soma no laço e a propagação de erro caem da mesma convenção
([fluxo.md](fluxo.md)).

## Quem chama quem

```
ft_printf ──► pf_directive ──► parse_fmt
                    │
                    ▼
               pf_dispatch ──► conv_c / conv_s / conv_percent / conv_unknown
                    │                conv_int / conv_uint / conv_hex / conv_ptr
                    │                        │
                    │                        ▼
                    │                  render_base + put_num
                    ▼
              (todos) ──► pf_putchar / pf_putn / pf_pad
```

Na obrigatória a cadeia é mais curta: `ft_printf → pf_conv → pf_put*`, sem
struct e sem montador — os escritores emitem direto.
