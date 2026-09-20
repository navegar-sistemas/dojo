# Regras de estilo

A fonte é **A Norma, versão 4.1** (`../private/pt_br.norm.pdf`), conferida
pela `norminette` oficial. Regras marcadas com (\*) a norminette não verifica
— quem verifica é o avaliador, e elas reprovam do mesmo jeito.

| Regra | Norma |
|---|---|
| Máximo 25 linhas por função, sem contar as chaves dela | III.2 |
| Máximo 80 colunas por linha, com tabulação valendo 4 | III.2 |
| Indentação com tabulações reais | III.2 |
| Declarações no topo da função, uma por linha, sem inicialização na declaração | III.2 |
| Uma linha vazia entre as declarações e o resto do corpo; nenhuma outra | III.2 |
| Uma instrução por linha; chaves sozinhas na própria linha | III.2 |
| Linha quebrada: o operador vai no **início** da linha de continuação | III.2 |
| Máximo 4 parâmetros por função, todos nomeados nos protótipos | III.3 |
| Máximo 5 variáveis declaradas por função | III.3 |
| `return` com parênteses no valor; uma tabulação entre tipo de retorno e nome | III.3 |
| Headers com guarda de inclusão (`FT_PRINTF_H`, `FT_PRINTF_BONUS_H`) | III.5 |
| (\*) Inclusão de header não utilizado é proibida | III.5 |
| (\*) `#define` só para valores literais e constantes; nome em maiúsculas | III.7 |
| (\*) Macro de biblioteca padrão só se o projeto a permitir | III.7 |
| `for`, `do…while`, `switch`, `case`, `goto`, ternário e VLA proibidos | III.8 |
| Comentários só fora do corpo de funções; (\*) em inglês e úteis | III.9 |
| Máximo 5 definições de função por arquivo `.c` | III.10 |
| Global só se `const` ou `static`, com prefixo `g_` | III.1 |
| Identificadores em `snake_case`; structs `s_`, typedefs `t_` | III.1 |
| Todo `.c` e `.h` começa com o header padrão da 42 | III.6 |
| Arquivos da variante bônus com sufixo `_bonus.{c,h}` | subject, cap. II |

## O que cada uma impõe ao desenho

| Regra | Consequência no código |
|---|---|
| sem `for` | todo laço é `while`, com o contador declarado no topo e inicializado depois da linha em branco |
| sem ternário | "qual prefixo" vira cadeia de `if` com atribuição: `pre = ""` … `se v < 0: pre = "-"` |
| sem inicialização na declaração | é o motivo de `fmt_init` existir: a struct não pode nascer com lista de inicialização, então uma função zera campo a campo ([../05-bonus/formato.md](../05-bonus/formato.md)) |
| macro de biblioteca só se permitida | o subject autoriza `malloc`, `free`, `write` e as `va_*` — `INT_MAX` de `<limits.h>` não está na lista. Os dois headers definem a própria constante, `PF_INT_MAX`, como valor literal |
| 25 linhas de corpo | `put_num` fecha em 24, com as três emissões centrais fundidas num `if` com `\|\|`; o laço obrigatório da `ft_printf`, em 22 |
| 5 funções por arquivo | `conv_text_bonus.c` e `put_bonus.c` estão no teto; `conv_unknown` precisa do ajudante `unk_head` para caber em 25 linhas |
| 4 parâmetros | o pior caso real é 3 (`put_num`, `render_base`); a `t_fmt` existe também por isso — sem ela, largura, precisão e cinco flags não passariam por nenhuma assinatura legal |

O despacho por cadeia de `if` **não** é imposição da Norma: uma tabela
`static const` de ponteiros para função seria legal, porque a III.1 só proíbe
globais que não sejam `const` nem `static`, e a III.2 abre exceção de
inicialização na declaração justamente para elas. A cadeia é escolha do
projeto — nove ramos não pagam uma tabela de 256 entradas
([../03-arquitetura/fluxo.md](../03-arquitetura/fluxo.md)).

## Verificação

De `../project/`:

```bash
norminette *.c *.h
grep -nE '\bfor\b|\bswitch\b|\bgoto\b|\bdo\b' *.c *.h     # nada
grep -n '?' *.c                                           # nada (sem ternário)
expand -t4 *.c *.h | awk 'length > 80'                    # nada
```

A `norminette` é a autoridade nos itens que controla (Norma, cap. I). Sem o
header da 42 ela acusa `INVALID_HEADER` em cada arquivo — e só isso.

Os limites por função e por arquivo estão tabelados com os valores reais em
[../03-arquitetura/modulos.md](../03-arquitetura/modulos.md).
