# Guloso por custo

Inserção gulosa sobre as duas pilhas, guiada pelo custo real em movimentos de cada candidato.
Não é selecionável por flag: roda apenas dentro do portfólio do
[`--adaptive`](adaptive.md), sempre ao lado de um certificador — sozinho, seu pior caso não
tem teto melhor que O(n²) operações.

## As duas fases

**Fase de empurrar.** Enquanto restam mais de 3 elementos em `a` e o resto de `a` não está
circularmente ordenado, o elemento mais barato vai para `b`:

```
push_phase(c):
    enquanto a.size > 3 e não is_circular_sorted(a):
        m = best_push(c)
        exec_move(c, m)
        op_pb(c)
```

`b` é mantida **circularmente decrescente**: cada rank entra logo acima do seu sucessor (o
maior rank menor que ele), então a fase de inserção devolve tudo já no lugar.

**Fase de inserir.** Devolve cada elemento de `b`, sempre o mais barato primeiro, mantendo `a`
**circularmente crescente**; um único alinhamento final leva o mínimo ao topo:

```
insert_phase(c):
    enquanto b.size > 0:
        m = best_insert(c)
        exec_move(c, m)
        op_pa(c)

sort_greedy_run(c, conf):
    grava rótulos; devolve se ordenada; sort_tiny se n <= 3
    push_phase(c)
    se a.size <= 3: sort_tiny(c)
    insert_phase(c)
    rotate_a_to_top(c, stack_min_index(a))
```

## Saída antecipada

`is_circular_sorted` responde se uma rotação final basta: lidos ciclicamente, os ranks descem
no máximo uma vez. É o que faz entrada quase ordenada manter a maior parte dos elementos fora
de `b` — o regime em que o guloso mais brilha.

```
is_circular_sorted(s):
    descidas = 0
    i = 0
    enquanto i < s.size:
        se s.data[i] > s.data[(i + 1) % s.size]:
            descidas += 1
        i += 1
    devolve (descidas <= 1)
```

## Custo de um movimento

Um candidato é um `t_move`: quantas rotações em `a` e em `b` antes do push, com sinal —
positivo gira para cima (`ra`/`rb`), negativo para baixo (`rra`/`rrb`).

```
move_cost(m):
    se m.a e m.b têm o mesmo sinal: devolve max(|m.a|, |m.b|)
    senão:                          devolve |m.a| + |m.b|
```

O máximo em vez da soma é a fusão: `exec_move` roda as partes de mesmo sinal como `rr`/`rrr` e
só então as sobras. O custo cobrado é exatamente o custo executado.

`pair_best(c, ia, ib)` avalia as quatro combinações de sentido — cada índice pode viajar para
frente (o próprio índice) ou para trás (índice menos o tamanho, negativo) — e devolve a mais
barata segundo `move_better`.

## Alvos

**`target_in_b(b, valor)`** — onde um rank entra numa `b` circularmente decrescente: logo
acima do sucessor (o maior rank abaixo dele); sem sucessor — o valor é menor que tudo, ou é o
novo máximo — entra acima do máximo atual. Os dois casos preservam a ordem circular.

**`target_in_a(a, valor)`** — espelho para a `a` circularmente crescente: logo acima do teto
(o menor rank acima dele); sem teto, acima do mínimo.

## Varredura podada

`best_push` percorre os candidatos do topo para fora — índices 0, depois 1 e n−1, depois 2 e
n−2... Um candidato a `k` passos do topo custa pelo menos `k` rotações, então:

```
best_push(c):
    best = candidato do índice 0
    k = 1
    enquanto k <= size - k e k < move_cost(best):
        best = move_better(best, candidato(k))
        se size - k != k:
            best = move_better(best, candidato(size - k))
        k += 1
    devolve best
```

Quando `k` alcança o custo do melhor já visto, nada mais distante pode vencer: a poda acelera
sem nunca mudar a resposta. `best_insert` é a mesma varredura sobre os índices de `b`.

## Desempate e variantes

`move_better` prefere o menor custo; no empate, `bias` decide o lado. `sort_greedy` roda com
`bias = 0` e `sort_greedy_alt` com `bias = 1` — as duas trajetórias divergem no primeiro
empate, e o portfólio fica com o menor programa. As variantes moram em `greedy_exec.c` porque
`sort_greedy.c` fechou a cota de 5 funções com as fases.

## Limites

- **Em operações:** sem teto melhor que O(n²) no pior caso — por isso o guloso nunca roda sem
  um certificador ao lado ([adaptive.md](adaptive.md)).
- **Em CPU:** a varredura é O(n²) no total mesmo com a poda; acima de `GREEDY_MAX_N` (1500)
  elementos o portfólio roda só o certificador.
- **Em espaço:** grava O(comprimento do programa) inteiros no candidato, como qualquer
  estratégia neste desenho.

Contagens medidas na invocação padrão — em que um dos gulosos vence em praticamente toda
entrada aleatória — em [../06-aceitacao/desempenho.md](../06-aceitacao/desempenho.md).
