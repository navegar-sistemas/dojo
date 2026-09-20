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
| Largura ou precisão acima de `INT_MAX` (`"%2147483648d"`) | `-1` |
| A saída inteira passaria de `INT_MAX` bytes | `-1` |

Em todos os casos de `-1`, os bytes já escritos **permanecem escritos**:
`"abc%"` imprime `[abc]` e devolve `-1`. Não existe rollback.

As duas últimas linhas são o `EOVERFLOW` da referência: o retorno é `int`, e
um valor que não cabe nele não pode ser devolvido. Sem essas guardas, as
somas estourariam `int` com sinal — comportamento indefinido em C, em vez de
um `-1` previsível
([../03-arquitetura/decisoes.md](../03-arquitetura/decisoes.md)).

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
| Saída e strings de mais de `INT_MAX` bytes → `-1` | obrigatória |
| Flags `-` `0` `#` `+` espaço, em qualquer ordem, com repetição | bônus |
| Largura mínima de campo em dígitos, até `INT_MAX` (`%20d`) | bônus |
| Precisão em dígitos, inclusive vazia, até `INT_MAX` (`%.7x`, `%.s`) | bônus |
| Largura ou precisão acima de `INT_MAX` → `-1`, nada da diretiva impresso | bônus |
| `%.Ns` sobre array de N bytes sem terminador | bônus |

### Fora do domínio

Comportamento não especificado — nenhum teste os exercita e a implementação
não promete nada sobre eles:

| Entrada | Observação |
|---|---|
| `format == NULL` | — |
| `*`, modificadores `l` `h` `ll` `hh`, flags `'` e `I`, conversões `o n e f g a` | o byte cai na regra de conversão desconhecida ([diretivas.md](diretivas.md)), o que **diverge** da referência, que os interpreta |
| **quais** bytes saem antes do `-1`, quando o total estoura no meio de uma diretiva | o retorno é o da referência; a quantidade emitida pode diferir — ver abaixo |

### O resíduo acima de 2 GB

Quando o total passa de `INT_MAX`, a referência confere o contador depois de
cada **pedaço** que escreve (preenchimento, prefixo, dígitos); `ft_printf`
confere depois de cada **diretiva**. Se o estouro cai no último pedaço da
diretiva, as duas emitem exatamente os mesmos bytes — 11 dos 12 casos medidos
em [../06-aceitacao/casos.md](../06-aceitacao/casos.md). Se cai num pedaço
anterior, `ft_printf` termina a diretiva antes de devolver `-1`, e a
referência para no pedaço: em `%1500000000d%1500000000d` são 3000000000 bytes
contra 2999999999, um de diferença, com o mesmo retorno.

Igualar isso exigiria carregar o contador para dentro de cada função de
emissão. O subject pede para **não** reimplementar o gerenciamento de buffer
da original, e a granularidade desses pedaços é detalhe interno dele.

## Estado

Nenhuma variável global ou `static` com estado: chamadas consecutivas ou
intercaladas não interferem entre si. A função não aloca heap
([../03-arquitetura/decisoes.md](../03-arquitetura/decisoes.md)).
