# Regras de estilo

Regras fixadas para este projeto. Não são preferências soltas: várias delas
determinam a forma dos módulos, e o desenho de
[../03-arquitetura/modulos.md](../03-arquitetura/modulos.md) só faz sentido com
elas na mesa.

| Regra |
|---|
| Máximo 5 funções por arquivo `.c`, contando as `static` |
| Máximo 25 linhas no corpo de uma função (entre as chaves, tudo contado) |
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

## O que isso impõe ao desenho

**Sem `for`.** Todo laço é `while` com o contador declarado no topo e
inicializado depois da linha em branco. O pseudocódigo desta spec já vem
assim.

**Sem ternário.** Escolhas como "qual prefixo" viram cadeias de `if` com
atribuição (`pre = "";` … `if (v < 0) pre = "-";`).

**Declaração sem inicialização.** É o motivo de `fmt_init` existir: uma struct
não pode nascer com lista de inicialização, então há uma função que zera campo
a campo ([../05-bonus/formato.md](../05-bonus/formato.md)). Pelo mesmo motivo,
`pre` e contadores são atribuídos na primeira linha após as declarações.

**Sem variável global.** Tabelas de despacho como
`int (*conv[256])(t_fmt *, va_list *)` estão fora duas vezes: em escopo de
arquivo seriam globais; locais, a inicialização `= {…}` viola a regra
anterior. O despacho é uma cadeia de `if` ([../03-arquitetura/fluxo.md](../03-arquitetura/fluxo.md)),
e os alfabetos de dígitos são literais passados na chamada
(`"0123456789abcdef"`).

**Corpo de 25 linhas.** Os dois montadores centrais fecham perto do teto:
`put_num` em 23 linhas — as três emissões de erro comum fundidas num único
`if` com `||` — e o laço obrigatório da `ft_printf` em 23. Função que passasse
disso teria que ceder um pedaço, consumindo a cota de funções do arquivo.

**5 funções por arquivo.** `conv_unknown` precisa de um ajudante
(`unk_head`) para caber em 25 linhas; o par mora em `conv_text_bonus.c`, que
fecha em exatamente 5 funções. O arquivo do laço bônus fica com 3 para não
disputar espaço.

**4 parâmetros.** O pior caso real é 3 (`put_num`, `render_base`). A struct
`t_fmt` existe também para isso: sem ela, largura, precisão e cinco flags não
passariam por nenhuma assinatura legal.

## Auditoria mecânica

De `../project/`:

```bash
grep -nE '\bfor\b|\bswitch\b|\bgoto\b|\bdo\b' *.c *.h     # nada
grep -n '?' *.c                                           # nada (sem ternário)
expand -t4 *.c *.h | awk 'length > 80'                    # nada
grep -n '	 \|  ' *.c | grep -v ' \* '                     # nada (espaço duplo/tab+espaço)
```

Os limites por função (25 linhas, 5 variáveis, 4 parâmetros) e por arquivo
(5 funções) estão tabelados com os valores reais em
[../03-arquitetura/modulos.md](../03-arquitetura/modulos.md); a auditoria é a
leitura.
