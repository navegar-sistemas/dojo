# Regras de estilo

Regras fixadas para este projeto. Várias determinam a forma dos módulos — o
desenho de [../03-arquitetura/modulos.md](../03-arquitetura/modulos.md) só
faz sentido com elas na mesa.

| Regra |
|---|
| Máximo 5 funções por arquivo `.c`, contando as `static` |
| Máximo 25 linhas no corpo de uma função, tudo entre as chaves |
| Máximo 4 parâmetros por função |
| Máximo 5 variáveis declaradas por função |
| Máximo 80 colunas por linha, com tabulação valendo 4 |
| Indentação com tabulações reais; uma tabulação entre tipo de retorno e nome |
| `for`, `do…while`, `switch`, `case`, `goto` proibidos |
| Operador ternário proibido |
| Variáveis globais proibidas |
| Declarações no topo da função, uma por linha, sem inicialização na declaração |
| Uma linha vazia entre as declarações e o resto do corpo; nenhuma outra |
| Uma instrução por linha; chaves sozinhas na própria linha |
| `return` sempre com parênteses no valor |
| Identificadores em `snake_case`; structs `s_`, typedefs `t_` |
| Headers com guarda de inclusão (`FT_PRINTF_H`, `FT_PRINTF_BONUS_H`) |
| Comentários só fora do corpo de funções, em inglês |
| Arquivos da variante bônus com sufixo `_bonus.{c,h}` |

## O que cada uma impõe ao desenho

| Regra | Consequência no código |
|---|---|
| sem `for` | todo laço é `while`, com o contador declarado no topo e inicializado depois da linha em branco — o pseudocódigo desta spec já vem assim |
| sem ternário | "qual prefixo" vira cadeia de `if` com atribuição: `pre = ""` … `se v < 0: pre = "-"` |
| sem inicialização na declaração | é o motivo de `fmt_init` existir: a struct não pode nascer com lista de inicialização, então uma função zera campo a campo ([../05-bonus/formato.md](../05-bonus/formato.md)) |
| sem variável global | tabela de despacho `int (*conv[256])(t_fmt *, va_list *)` está fora duas vezes: em escopo de arquivo seria global, local exigiria inicialização na declaração — o despacho é cadeia de `if` ([../03-arquitetura/fluxo.md](../03-arquitetura/fluxo.md)) e os alfabetos de dígitos são literais na chamada |
| 25 linhas de corpo | `put_num` fecha em 23 com as três emissões centrais fundidas num `if` com `\|\|`; o laço obrigatório da `ft_printf`, também em 23 |
| 5 funções por arquivo | `conv_unknown` precisa do ajudante `unk_head` para caber em 25 linhas, e o par lota `conv_text_bonus.c` |
| 4 parâmetros | o pior caso real é 3 (`put_num`, `render_base`); a `t_fmt` existe também por isso — sem ela, largura, precisão e cinco flags não passariam por nenhuma assinatura legal |

## Auditoria mecânica

De `../project/`:

```bash
grep -nE '\bfor\b|\bswitch\b|\bgoto\b|\bdo\b' *.c *.h     # nada
grep -n '?' *.c                                           # nada (sem ternário)
expand -t4 *.c *.h | awk 'length > 80'                    # nada
grep -n '	 \|  ' *.c | grep -v ' \* '        # nada (espaço duplo, tab+espaço)
```

Os limites por função e por arquivo estão tabelados com os valores reais em
[../03-arquitetura/modulos.md](../03-arquitetura/modulos.md).
