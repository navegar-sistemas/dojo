*This project has been created as part of the 42 curriculum by macoelho, <login2>.*

<!-- TODO: trocar <login2> pelo login do segundo integrante antes de submeter. -->

# push_swap

## Description

`push_swap` recebe uma lista de inteiros e imprime, na saída padrão, o menor
programa que encontrar — escrito na linguagem de 11 operações do Push_swap
(`sa`, `sb`, `ss`, `pa`, `pb`, `ra`, `rb`, `rr`, `rra`, `rrb`, `rrr`) — capaz
de ordenar esses inteiros usando duas pilhas (`a` e `b`).

O binário embute **quatro estratégias**, selecionáveis em tempo de execução:

| Flag         | Estratégia                            | Classe (em nº de operações) |
|--------------|---------------------------------------|-----------------------------|
| `--simple`   | selection sort adaptado às pilhas     | O(n²)                       |
| `--medium`   | ordenação por blocos (√n *chunks*)    | O(n√n)                      |
| `--complex`  | radix sort binário LSD                | O(n log n)                  |
| `--adaptive` | portfólio guiado pela desordem (padrão) | limite do regime (ver abaixo) |

A **desordem** (fração de pares invertidos, 0 a 1) é medida antes de qualquer
movimento, como o enunciado exige, e o modo `--bench` a reporta junto com a
estratégia usada, sua classe e a contagem de cada operação — tudo em `stderr`,
sem poluir o fluxo de operações.

## Instructions

```sh
make            # compila a libft e o binário push_swap (cc -Wall -Wextra -Werror)
make bonus      # compila o checker
./push_swap 2 1 3 6 5 8
./push_swap --medium "4 67 3 87 23" | wc -l
ARG="4 67 3 87 23"; ./push_swap $ARG | ./checker $ARG        # OK
ARG=$(shuf -i 0-9999 -n 500 | tr '\n' ' ')
./push_swap --bench $ARG 2>bench.txt | ./checker $ARG; cat bench.txt
```

Erros (token não numérico, fora do intervalo de `int`, duplicata, flag
desconhecida, argumento vazio) imprimem `Error` em `stderr` e retornam 1.
Sem argumentos, o programa devolve o prompt em silêncio.

## Algoritmos e justificativa

### As três estratégias nomeadas

* **`--simple` — selection sort (O(n²)).** Repetidamente traz o mínimo de A ao
  topo pela rotação mais curta e o empurra para B; ao final, devolve tudo a A.
  Cada um dos n elementos custa no máximo ⌈n/2⌉ rotações + 2 pushes, logo o
  total é ≤ n·(⌈n/2⌉ + 2) = **O(n²)** operações.
* **`--medium` — ordenação por blocos (O(n√n)).** Os ranks são divididos em
  k = √(n/2) blocos contíguos. A fase de coleta varre A uma vez por bloco
  (≤ k·n rotações + n pushes); na drenagem, o máximo restante de B está sempre
  entre os ≤ ⌈n/k⌉ elementos do bloco do topo, então cada `pa` custa no máximo
  ⌈n/k⌉ + 1 operações. Total ≤ k·n + n·(⌈n/k⌉ + 2) = **O(n√n)** operações.
* **`--complex` — radix binário LSD (O(n log n)).** Os valores são reduzidos a
  ranks 0..n-1 e ordenados bit a bit: ⌈log₂ n⌉ passadas de no máximo 2n
  operações cada (`pb`/`ra` na ida, `pa` na volta) = **O(n log n)** operações.

### `--adaptive` — portfólio com certificador (projeto do aluno)

O regime é escolhido pela desordem `d`, com os limiares que o enunciado fixa:

| Regime            | Método interno                                   | Limite garantido |
|-------------------|--------------------------------------------------|------------------|
| `d < 0.2`         | portfólio: guloso ×2 + **selection certificador** | O(n²)            |
| `0.2 ≤ d < 0.5`   | portfólio: guloso ×2 + **blocos certificador**    | O(n√n)           |
| `d ≥ 0.5`         | portfólio: guloso ×2 + **radix certificador**     | O(n log n)       |

**Como funciona.** Cada regime gera até três programas-candidatos em cópias
privadas das pilhas: duas variantes do *guloso por custo* (abaixo) e o
algoritmo *certificador* do regime. Só o programa **mais curto** é impresso.

**Argumento de complexidade (modelo do enunciado: nº de operações geradas).**
O programa emitido nunca excede o do certificador, portanto o custo de cada
regime é limitado por construção: ≤ O(n²) com desordem baixa, ≤ O(n√n) com
média e ≤ O(n log n) com alta — exatamente os alvos do enunciado, valendo no
pior caso, e não apenas na média. O guloso serve para *encurtar* o programa
(na prática ele vence em praticamente toda entrada aleatória); o certificador
serve para *provar o limite*.

**O guloso por custo.** Duas fases: (1) enquanto restam > 3 elementos e o
resto de A não está circularmente ordenado, empurra para B o elemento mais
barato — custo = rotações de A + rotações de B para posicionar o elemento
acima do sucessor em um B mantido circularmente decrescente, com rotações de
mesmo sentido fundidas em `rr`/`rrr` e as quatro combinações de sentido
avaliadas; (2) reinsere cada elemento de B, sempre o mais barato primeiro, num
A circularmente crescente, e alinha o mínimo ao topo. A varredura de
candidatos é podada: um candidato a k passos do topo custa ≥ k, então a busca
para assim que k alcança o melhor custo já visto — a poda acelera sem alterar
a resposta. As duas variantes diferem apenas na política de desempate
(`bias`), o que descorrelaciona as trajetórias e corta a cauda da
distribuição de operações. Isolado, o guloso não tem limite melhor que O(n²)
operações no pior caso — é por isso que ele nunca roda sem um certificador.

**Racional dos limiares.** 0.2 e 0.5 são os pontos exigidos pelo enunciado; a
implementação os explora bem: abaixo de 0.2 a entrada é quase ordenada e a
saída antecipada do guloso (resto circularmente ordenado fica em A) gera
programas mínimos, com o selection como teto quadrático barato em n pequeno;
uma permutação uniforme concentra a desordem em ~0.5 ± 0.01, então os regimes
médio/alto são os que respondem pelos benchmarks — ambos entregam o mesmo
guloso na prática, mas com tetos O(n√n) e O(n log n) respectivamente.

**Espaço.** Pilhas e ranks: O(n). Programas gravados: O(custo do
certificador) inteiros por candidato — O(n log n) no regime alto, O(n√n) no
médio, O(n²) no baixo (n²/2 + 2n inteiros no teto). **Tempo de CPU** (que o
enunciado distingue do custo em operações): a varredura podada do guloso é
O(n²) no pior caso; acima de `GREEDY_MAX_N` (1500) elementos só o
certificador roda, mantendo o tempo de parede baixo — os benchmarks do
enunciado param em 500.

### Resultados medidos (invocação padrão, entradas aleatórias)

| n   | média | máximo observado | requisito excelente |
|-----|-------|------------------|---------------------|
| 100 | ~549  | 631 (800 seeds)  | < 700 ✓             |
| 500 | ~5030 | 5401 (600 seeds) | < 5500 ✓            |

## Bonus — checker

`./checker <numeros>` lê operações de `stdin` (uma por linha), aplica-as e
imprime `OK` se A terminou ordenada com B vazia, `KO` caso contrário e
`Error` em `stderr` para argumentos ou instruções inválidos. Ele reutiliza o
parser e as operações do binário principal — no checker o contexto roda com
`prog == NULL`, o modo silencioso que aplica o efeito sem gravar nada.

## Contributions

<!-- TODO: descrever a divisão real de trabalho entre os dois integrantes. -->
- **macoelho** — parsing e validação, operações e pilhas, estratégias
  `--simple`/`--medium`/`--complex`, checker.
- **<login2>** — métrica de desordem, estratégia adaptativa (portfólio e
  guloso), `--bench`, testes e benchmark.

## Resources

- D. E. Knuth, *The Art of Computer Programming, vol. 3: Sorting and
  Searching* — seleção, radix e análise de custo.
- CLRS, *Introduction to Algorithms* — noção de limites assintóticos e
  contagem de inversões (a métrica de desordem é inversões normalizadas).
- Artigos da comunidade 42 sobre o push_swap (radix nas duas pilhas e
  inserção gulosa por custo, o "Turk algorithm").
- **Uso de IA:** assistência de IA (Claude) foi usada para explorar variantes
  do algoritmo guloso e seus parâmetros, gerar a suíte de testes/benchmark
  (permutações exaustivas, fuzzing com verificador independente, valgrind) e
  rascunhar comentários e documentação. 
  <!-- TODO: ajustar esta seção para refletir fielmente o processo da dupla. -->
