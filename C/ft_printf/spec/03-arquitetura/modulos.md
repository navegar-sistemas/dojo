# Módulos

Uma responsabilidade por arquivo, dentro do teto de 5 funções — `static`
contam — e 25 linhas por corpo
([../02-restricoes/estilo.md](../02-restricoes/estilo.md)). As colunas
"Funções" e "Maior corpo" são os valores reais do código.

## Parte obrigatória — 7 funções

| Arquivo | Funções | Maior corpo | Responsabilidade |
|---|---|---|---|
| `ft_printf.c` | 3 | 23 | laço, despacho por conversão, inteiro com sinal |
| `pf_put.c` | 4 | 16 | byte, string, dígitos por base (recursivo), ponteiro |

## Bônus — 21 funções

| Arquivo | Funções | Maior corpo | Responsabilidade |
|---|---|---|---|
| `ft_printf_bonus.c` | 3 | 20 | laço, consumo da diretiva, despacho |
| `parse_bonus.c` | 3 | 19 | gramática da diretiva → `t_fmt` |
| `put_bonus.c` | 4 | 12 | byte, n bytes, padding, comprimento |
| `conv_text_bonus.c` | 5 | 18 | `%c`, `%s`, `%%`, desconhecida canônica |
| `conv_num_bonus.c` | 2 | 19 | `%d`/`%i`, `%u` |
| `conv_hex_bonus.c` | 2 | 15 | `%x`/`%X`, `%p` |
| `num_render_bonus.c` | 2 | 23 | dígitos em buffer, montador de campo |

`conv_text_bonus.c` chega ao teto de 5 porque `conv_unknown` precisa do
ajudante `unk_head` para caber em 25 linhas. `ft_printf_bonus.c` fica em 3
para não disputar espaço.

## Onde está cada função

### Obrigatória

| Função | Arquivo | Visibilidade | Algoritmo em |
|---|---|---|---|
| `ft_printf` | `ft_printf.c` | pública | [fluxo.md](fluxo.md) |
| `pf_conv` | `ft_printf.c` | `static` | [fluxo.md](fluxo.md) |
| `pf_putnbr` | `ft_printf.c` | `static` | [../04-emissao/numeros.md](../04-emissao/numeros.md) |
| `pf_putchar` | `pf_put.c` | pública | [../04-emissao/escritores.md](../04-emissao/escritores.md) |
| `pf_putstr` | `pf_put.c` | pública | [../04-emissao/escritores.md](../04-emissao/escritores.md) |
| `pf_putnbr_base` | `pf_put.c` | pública | [../04-emissao/numeros.md](../04-emissao/numeros.md) |
| `pf_putptr` | `pf_put.c` | pública | [../04-emissao/numeros.md](../04-emissao/numeros.md) |

### Bônus

| Função | Arquivo | Visibilidade | Algoritmo em |
|---|---|---|---|
| `ft_printf` | `ft_printf_bonus.c` | pública | [fluxo.md](fluxo.md) |
| `pf_directive` | `ft_printf_bonus.c` | `static` | [fluxo.md](fluxo.md) |
| `pf_dispatch` | `ft_printf_bonus.c` | `static` | [fluxo.md](fluxo.md) |
| `fmt_init` | `parse_bonus.c` | `static` | [../05-bonus/formato.md](../05-bonus/formato.md) |
| `parse_flags` | `parse_bonus.c` | `static` | [../05-bonus/formato.md](../05-bonus/formato.md) |
| `parse_fmt` | `parse_bonus.c` | pública | [../05-bonus/formato.md](../05-bonus/formato.md) |
| `pf_putchar` | `put_bonus.c` | pública | [../04-emissao/escritores.md](../04-emissao/escritores.md) |
| `pf_putn` | `put_bonus.c` | pública | [../04-emissao/escritores.md](../04-emissao/escritores.md) |
| `pf_pad` | `put_bonus.c` | pública | [../04-emissao/escritores.md](../04-emissao/escritores.md) |
| `pf_strlen` | `put_bonus.c` | pública | [../04-emissao/escritores.md](../04-emissao/escritores.md) |
| `render_base` | `num_render_bonus.c` | pública | [../04-emissao/numeros.md](../04-emissao/numeros.md) |
| `put_num` | `num_render_bonus.c` | pública | [../05-bonus/montagem.md](../05-bonus/montagem.md) |
| `unk_head` | `conv_text_bonus.c` | `static` | [../05-bonus/conversoes.md](../05-bonus/conversoes.md) |
| `conv_unknown` | `conv_text_bonus.c` | pública | [../05-bonus/conversoes.md](../05-bonus/conversoes.md) |
| `conv_c` | `conv_text_bonus.c` | pública | [../05-bonus/conversoes.md](../05-bonus/conversoes.md) |
| `conv_s` | `conv_text_bonus.c` | pública | [../05-bonus/conversoes.md](../05-bonus/conversoes.md) |
| `conv_percent` | `conv_text_bonus.c` | pública | [../05-bonus/conversoes.md](../05-bonus/conversoes.md) |
| `conv_int` | `conv_num_bonus.c` | pública | [../05-bonus/conversoes.md](../05-bonus/conversoes.md) |
| `conv_uint` | `conv_num_bonus.c` | pública | [../05-bonus/conversoes.md](../05-bonus/conversoes.md) |
| `conv_hex` | `conv_hex_bonus.c` | pública | [../05-bonus/conversoes.md](../05-bonus/conversoes.md) |
| `conv_ptr` | `conv_hex_bonus.c` | pública | [../05-bonus/conversoes.md](../05-bonus/conversoes.md) |

## Headers

`ft_printf.h`:

```c
int	ft_printf(const char *format, ...);
int	pf_putchar(char c);
int	pf_putstr(char *s);
int	pf_putnbr_base(unsigned long n, const char *base);
int	pf_putptr(void *ptr);
```

`ft_printf_bonus.h` — a `t_fmt` está em [tipos.md](tipos.md):

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

Cada header só inclui `<stdarg.h>`; `<unistd.h>` fica nos dois `.c` que
chamam `write`.

## Contrato de retorno comum

Toda função que escreve devolve o número de bytes que escreveu, ou `-1` se
qualquer `write` falhou. É um contrato só, do `pf_putchar` até a
`ft_printf`: a soma no laço e a propagação de erro caem dele
([fluxo.md](fluxo.md)). `render_base` é a única exceção — não escreve, não
devolve nada.

## Quem chama quem

```
ft_printf ──► pf_directive ──► parse_fmt ──► fmt_init, parse_flags
                    │
                    ▼
               pf_dispatch ──► conv_c / conv_s / conv_percent
                    │          conv_unknown ──► unk_head
                    │          conv_int / conv_uint / conv_hex / conv_ptr
                    │                  │
                    │                  ▼
                    │            render_base ──► put_num
                    ▼
              (todos) ──► pf_putchar / pf_putn / pf_pad / pf_strlen
```

Na obrigatória a cadeia é mais curta — `ft_printf → pf_conv → pf_put*`, sem
struct e sem montador: os escritores emitem direto.
