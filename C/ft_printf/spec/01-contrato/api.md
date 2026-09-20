# API e entrega

## Assinatura

```c
int	ft_printf(const char *format, ...);
```

Único símbolo público. Percorre `format`, copia os bytes literais para a
saída, substitui cada diretiva `%…` pelo próximo argumento variádico e
devolve o total de bytes escritos.

## Entrega

| | |
|---|---|
| Artefato | `libftprintf.a`, biblioteca estática criada com `ar rcs`, na raiz de `../project/` |
| Header | `ft_printf.h`, com o protótipo acima |
| Uso | `cc main.c -L. -lftprintf` |

A biblioteca tem duas variantes que ocupam o mesmo `.a`: `make` a constrói
com a parte obrigatória, `make bonus` a reconstrói com a implementação
completa de flags ([../02-restricoes/build.md](../02-restricoes/build.md)).

## Valor de retorno

| Situação | Retorno |
|---|---|
| Sucesso | número de bytes escritos em `stdout` |
| `write` devolve erro em qualquer ponto | `-1` |
| Formato termina no meio de uma diretiva (`"abc%"`, `"%5"`, `"%-"`, `"%."`) | `-1` |

Nos dois casos de `-1`, os bytes já escritos **permanecem escritos**:
`"abc%"` imprime `[abc]` e devolve `-1`. Não existe rollback.

## Canal

Toda a saída vai para o descritor 1, byte a byte, via `write`. Nada é escrito
em qualquer outro descritor e não há buffer próprio: quando `ft_printf`
retorna, tudo já foi entregue ao kernel.

A referência buferiza internamente, mas o conteúdo final do fluxo é idêntico
— o harness diferencial compara arquivos depois que os processos terminam,
onde a diferença desaparece
([../06-aceitacao/validacao.md](../06-aceitacao/validacao.md)).

## O contrato de espelho

Dentro do domínio suportado, `ft_printf` é indistinguível da `printf` da
glibc: mesmos bytes, mesmo retorno, para qualquer formato e argumentos —
inclusive nos cantos que a linguagem não define
([../06-aceitacao/casos.md](../06-aceitacao/casos.md)).

### Domínio suportado

| Elemento | Parte |
|---|---|
| Conversões `c s p d i u x X %` | obrigatória |
| Conversão desconhecida (byte que não é conversão nem prefixo válido) | obrigatória |
| Formato terminando no meio de uma diretiva | obrigatória |
| Flags `-` `0` `#` `+` espaço, em qualquer ordem, com repetição | bônus |
| Largura mínima de campo em dígitos (`%20d`) | bônus |
| Precisão em dígitos, inclusive vazia (`%.7x`, `%.s`) | bônus |

### Fora do domínio

Comportamento não especificado — nenhum teste os exercita e a implementação
não promete nada sobre eles:

| Entrada | Observação |
|---|---|
| `format == NULL` | — |
| largura ou precisão que não cabem em `int` | — |
| `*`, modificadores `l` `h` `ll` `hh`, flags `'` e `I`, conversões `o n e f g a` | o byte cai na regra de conversão desconhecida ([diretivas.md](diretivas.md)), o que **diverge** da referência, que os interpreta |
| total de bytes acima de `INT_MAX` | — |

## Estado

Nenhuma variável global ou `static` com estado: chamadas consecutivas ou
intercaladas não interferem entre si. A função não aloca heap
([../03-arquitetura/decisoes.md](../03-arquitetura/decisoes.md)).
