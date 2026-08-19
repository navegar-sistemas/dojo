# Tarefas

## Quadro

| # | Tarefa | Depende de | Entrega |
|---|---|---|---|
| [T01](T01-esqueleto-build.md) | Esqueleto de build | — | `Makefile`, `push_swap.h`, `libft/` |
| [T02](T02-pilha.md) | Pilha | T01 | `stack.c` |
| [T03](T03-prog-emissao.md) | Programa gravado e emissão | T02 | `prog.c`, `emit.c`, `utils.c` (`ps_die`, `zero_counts`) |
| [T04](T04-operacoes.md) | Operações | T03 | `ops_*.c` |
| [T05](T05-parsing.md) | Parsing e validação | T02 | `parse.c`, `parse_utils.c` |
| [T06](T06-orquestracao.md) | Orquestração do `main` | T04, T05 | `main.c` |
| [T07](T07-sort-tiny-simple.md) | Caso base e `--simple` | T06 | `sort_tiny.c`, `sort_simple.c`, `utils.c` (rotações, `isqrt`) |
| [T08](T08-desordem.md) | Desordem | T06 | `disorder.c` |
| [T09](T09-ranks.md) | Ranks | T02 | `rank.c` |
| [T10](T10-sort-complex.md) | `--complex` | T07, T09 | `sort_complex.c` |
| [T11](T11-sort-medium.md) | `--medium` | T07, T09 | `sort_medium.c` |
| [T12](T12-guloso.md) | Guloso por custo | T07, T09 | `greedy_cost.c`, `greedy_pick.c`, `greedy_exec.c`, `sort_greedy.c` |
| [T13](T13-portfolio-adaptive.md) | Portfólio e `--adaptive` | T08, T10, T11, T12 | `portfolio.c`, `sort_adaptive.c` |
| [T14](T14-bench.md) | `--bench` | T13 | `bench.c` |
| [T15](T15-checker-bonus.md) | `checker` | T04, T05 | `*_bonus.c`, regra `bonus` |
| [T16](T16-fechamento.md) | Fechamento | T15 | validação final |

## Ordem

Depois de T01 vem T02; a partir dela, T03 e T05 andam em paralelo, e T09 também só depende de
T02. T04 segue T03. De T06 em diante a coluna de dependências manda; T15 usa só os módulos
compartilhados, mas roda por último antes do fechamento — bônus só interessa com a parte
obrigatória inteira verde.

T03 vem antes das operações de propósito: os `op_*` chamam `emit`, então o gravador de
programa nasce primeiro e nada é reescrito depois. O preço é T03 ser pura infraestrutura — o
primeiro comportamento visível chega em T04, e o primeiro ponto verificável de ponta a ponta é
**T07**: antes disso não existe receita para conferir contra o checker de referência.

## Formato de uma tarefa

Cada arquivo tem:

- **Objetivo** — uma frase.
- **Depende de** — tarefas que precisam estar prontas.
- **Arquivos** — o que é criado ou alterado.
- **Especificação** — links para os documentos que definem o comportamento.
- **Implementação** — o que fazer, na granularidade de função.
- **Pronto quando** — comandos com a saída esperada. Todos verdes, sem exceção.

## Header incremental

`push_swap.h` nasce mínimo em T01 (apenas a guarda de inclusão) e cresce junto com as tarefas: a
tarefa que cria um tipo ou função pública é a que acrescenta a declaração ao header, guiada
por [tipos.md](../03-arquitetura/tipos.md) e [modulos.md](../03-arquitetura/modulos.md).
Nenhuma tarefa transcreve declarações de código que ainda não existe.

## Regra de conclusão

Uma tarefa só está pronta com **todos** os comandos de "Pronto quando" executados e verdes, no
estado atual do código. Isso inclui, em toda tarefa que toca `.c` ou `.h`:

```bash
make re            # zero warning
norminette *.c *.h # nenhuma linha "Error:"
```

Tarefa anterior vermelha bloqueia a seguinte.
