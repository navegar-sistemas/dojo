# Estilo

Regras que o código deste projeto segue. Elas moldam a granularidade dos
módulos, então vêm antes da arquitetura.

| Regra |
|---|
| Máximo 5 funções por arquivo `.c`, contando as `static` |
| Máximo 25 linhas no corpo de uma função (chaves de fora não contam) |
| Máximo 80 colunas por linha, com tabulação valendo 4 |
| Máximo 4 parâmetros e 5 variáveis locais por função |
| `for`, `do...while`, `switch`, `case`, `goto` e o ternário `?:` proibidos |
| Declarações no topo da função, uma por linha, sem inicialização na declaração |
| Uma linha vazia entre as declarações e o resto do corpo; nenhuma outra dentro da função |
| Indentação com tabulações reais; chaves sozinhas na própria linha |
| Identificadores em `snake_case` minúsculo |
| Valor de retorno entre parênteses: `return (x);` |
| Headers protegidos contra dupla inclusão; só protótipos, `#include` e `#define` de constantes |
| Variáveis globais proibidas; `static` local é o único estado persistente |
| VLAs proibidos; `#define` só para constantes |

## O que isso impõe ao desenho

**Corpo de 25 linhas.** Uma chamada tem três fases — ler, extrair, podar — e
elas não cabem juntas. Cada fase é uma função `static` de
`get_next_line.c`, e a pública só orquestra: 4 funções no arquivo, maior
corpo com 22 linhas ([../03-arquitetura/modulos.md](../03-arquitetura/modulos.md)).

**Cota de 5 funções.** Os utilitários de string ocupam exatamente a cota do
`get_next_line_utils.c`: `gnl_strlen`, `gnl_strchr`, `gnl_cpy`, `gnl_substr`,
`gnl_strjoin_free`. `gnl_cpy` existe **por causa do limite de 25 linhas**: sem
ela, `gnl_strjoin_free` precisaria de dois laços de cópia e fecharia em 25
linhas exatas, sem folga; com ela, fecha em 14.

**Sem `for`.** Todo laço é `while` com o contador declarado no topo e
inicializado depois da linha em branco. O pseudocódigo desta spec já está
escrito assim.

**Sem ternário.** Escolhas como "o `\n` entra na contagem?" viram `if`
explícito (`gnl_extract_line`).

**Sem inicialização na declaração.** `i = 0` é sempre a primeira instrução
após o bloco de declarações — exceto a estática (`static char *stash;`), que
a linguagem zera sozinha e é justamente a exceção permitida.

**Sem variável global.** O estado entre chamadas mora numa `static` local à
própria `get_next_line` — nenhum outro arquivo enxerga o stash, o que reduz o
contrato interno a "as três fases recebem e devolvem o ponteiro".

## Verificação

Não há verificador automático embutido nesta spec: as regras são conferidas
por inspeção, e a tabela de contagens por função em
[../03-arquitetura/modulos.md](../03-arquitetura/modulos.md) é o gabarito —
qualquer corpo acima de 25 linhas ou arquivo acima de 5 funções é divergência
da referência. A largura máxima medida no projeto é 61 colunas.
