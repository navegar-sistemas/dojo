# Tipos

Tudo em `push_swap.h`.

## Constantes

```c
# define STRAT_NONE     0
# define STRAT_SIMPLE   1
# define STRAT_MEDIUM   2
# define STRAT_COMPLEX  3
# define STRAT_ADAPTIVE 4
# define FLAG_BENCH     5
# define GREEDY_MAX_N   1500
```

`STRAT_NONE` é o valor inicial durante o parsing e serve para detectar dois seletores: gravar
por cima de qualquer coisa diferente de `STRAT_NONE` é erro.

`FLAG_BENCH` é o retorno de `flag_id` para `--bench` — fora da faixa dos seletores para nunca
colidir com um valor gravável em `conf->strategy`.

`GREEDY_MAX_N` limita o tamanho de entrada em que o guloso participa do portfólio: acima de
1500 elementos a varredura de candidatos fica pesada em CPU e só o certificador roda — ver
[../04-algoritmos/adaptive.md](../04-algoritmos/adaptive.md).

## Pilha

```c
typedef struct s_stack
{
	int	*data;
	int	size;
	int	cap;
}	t_stack;
```

| Invariante | |
|---|---|
| `data[0]` | topo |
| `data[size - 1]` | fundo |
| `size` | 0 ≤ `size` ≤ `cap` |
| `cap` | fixado na criação; nunca muda |

As duas pilhas juntas nunca contêm mais que `n` elementos, então alocar `cap = n` para cada uma
elimina qualquer realocação durante a ordenação. O ponteiro `data` é estável do início ao fim.

## Operações

```c
typedef enum e_op
{
	OP_SA,
	OP_SB,
	OP_SS,
	OP_PA,
	OP_PB,
	OP_RA,
	OP_RB,
	OP_RR,
	OP_RRA,
	OP_RRB,
	OP_RRR
}	t_op;
```

A ordem dos membros é a ordem das colunas do `--bench`, o que permite indexar o vetor de
contagens direto pelo enum e imprimir as duas linhas de métricas percorrendo `OP_SA..OP_PB` e
`OP_RA..OP_RRR`.

## Programa gravado

```c
typedef struct s_prog
{
	t_op	*ops;
	int		len;
	int		cap;
}	t_prog;
```

Um fluxo de operações **gravado**, não impresso. Nada sai em stdout durante a ordenação: cada
operação entra aqui via `emit` → `prog_push`, e `prog_flush` imprime o programa final de uma
vez no fim do `main`. É o que permite ao `--adaptive` gerar vários programas-candidatos e
imprimir só o mais curto ([../04-algoritmos/adaptive.md](../04-algoritmos/adaptive.md)).

O buffer nasce com capacidade 64 e dobra quando enche (`prog_grow`), mantendo `prog_push`
amortizado O(1). Falha de alocação no crescimento cai em `ps_die`.

## Par de rotações

```c
typedef struct s_move
{
	int	a;
	int	b;
}	t_move;
```

Rotações a executar antes de um push, uma por pilha: contagem positiva significa rotação para
cima (`ra`/`rb`), negativa para baixo (`rra`/`rrb`). `exec_move` funde as partes de mesmo
sinal em `rr`/`rrr` — exatamente o que `move_cost` precificou com um máximo em vez de uma
soma. Ver [../04-algoritmos/greedy.md](../04-algoritmos/greedy.md).

## Contexto de execução

```c
typedef struct s_ctx
{
	t_stack			*a;
	t_stack			*b;
	int				*counts;
	int				bias;
	t_prog			*prog;
	struct s_ctx	*up;
}	t_ctx;
```

| Campo | Papel |
|---|---|
| `a`, `b` | as duas pilhas |
| `counts` | `int[11]` indexado por `t_op`, preenchido por `prog_flush` para o `--bench`; só o `main` do `push_swap` o liga — simulações e checker deixam `NULL` |
| `bias` | política de desempate do guloso (0 ou 1) — ver [../04-algoritmos/greedy.md](../04-algoritmos/greedy.md) |
| `prog` | define o modo de operação (tabela abaixo) |
| `up` | encadeia uma simulação ao contexto que a criou |

| `prog` | Modo | Quem usa |
|---|---|---|
| não-`NULL` | gerador: aplica o efeito e **grava** a operação | `push_swap` (contexto real e simulações) |
| `NULL` | executor: aplica só o efeito, em silêncio | `checker` |

É o ponteiro `prog` que permite ao `checker` reaproveitar as mesmas 11 funções de operação sem
produzir saída nenhuma. E é o `up` que torna o caminho de erro seguro em qualquer
profundidade: `ps_die` percorre a cadeia liberando as pilhas e o programa de cada contexto —
uma falha de alocação dentro de uma simulação do portfólio libera também o contexto real antes
do `exit`.

Um único parâmetro `t_ctx *` também resolve o problema do `-Wunused-parameter`: se as
operações recebessem `(t_stack *a, t_stack *b)`, `op_sa` não usaria `b` e a compilação
falharia com `-Werror`.

## Ponteiro de estratégia

```c
typedef void	(*t_sortfn)(t_ctx *c, t_conf *conf);
```

A assinatura comum das estratégias. É o tipo do certificador que `run_portfolio` recebe, e o
que permite ao portfólio simular qualquer estratégia sem conhecê-la.

## Configuração

```c
typedef struct s_conf
{
	int		strategy;
	int		bench;
	char	*name;
	char	*cclass;
}	t_conf;
```

`name` e `cclass` são `char *`, **não** `const char *`: receber literais de string num
`char *` é legal e não gera aviso, enquanto `const char *` faria `ft_putstr_fd(conf->name, 2)`
falhar na compilação — o parâmetro da libft é `char *`, e o descarte do qualificador é erro
sob `-Werror`.

| Campo | Origem | Uso |
|---|---|---|
| `strategy` | flags | despacho |
| `bench` | flag `--bench` | decide se as métricas saem |
| `name` | gravado pela estratégia que roda | `--bench` |
| `cclass` | gravado pela estratégia; em `--adaptive`, sobrescrito com a classe do regime | `--bench` |

## Ciclo de vida da memória

| Bloco | Alocado em | Liberado em |
|---|---|---|
| `a` e `a->data` | parsing | `cleanup` no fim do `main`, e em todo caminho de erro (`ps_die`) |
| `b` e `b->data` | `setup`, após o parsing | idem |
| `prog` do contexto real | `setup` (`prog_new`) | `cleanup` — ou antes, pelo `run_portfolio`, que o descarta e o substitui pelo candidato vencedor |
| programas candidatos | `simulate` (`prog_new`) | `take_if_shorter` fica com o mais curto e libera o outro; o vencedor vira `c->prog` |
| pilhas de simulação | `simulate` (`stack_dup`) | fim da própria `simulate` |
| array do `ft_split` | por argumento, durante o parsing | logo após consumir os tokens, inclusive no caminho de erro |
| cópia ordenada dos ranks | `build_ranks` | antes de `build_ranks` retornar |

O vetor `counts` é uma variável local do `main`, sem alocação.
