# Decisões de desenho

Escolhas que não são óbvias a partir do contrato, com a evidência que as sustenta.

## Pilha em array, não em lista encadeada

`data[0]` é o topo; rotação é um `ft_memmove` de `size - 1` inteiros mais a reposição de um
elemento.

A lista encadeada dá rotação O(1) contra O(n) do array, mas o custo em CPU é irrelevante aqui:
o pior caso do projeto é `--simple` com 500 elementos, ~34000 rotações de no máximo 2 KB, o que
é ordem de dezenas de milissegundos. Em troca, o array elimina toda a manipulação de ponteiros,
`stack_min_index` vira um `while` sobre índices, e cada função fica bem abaixo do limite de 25
linhas.

## Programa gravado, impressão única no fim

Nenhuma operação é impressa quando acontece: tudo entra num `t_prog` e `prog_flush` imprime o
programa final de uma vez.

O motivo de existir é o portfólio do `--adaptive`: para imprimir só o mais curto entre três
candidatos, os candidatos precisam existir inteiros antes de qualquer byte sair em stdout. O
desenho traz mais dois efeitos:

- as contagens do `--bench` são preenchidas pelo próprio flush, na mesma passada que imprime —
  stdout e métricas não têm como divergir;
- a saída é atômica em relação a falhas: uma alocação que falha no meio da gravação morre em
  `ps_die` com stdout ainda vazio, nunca com meia receita impressa.

O custo é o buffer: O(comprimento do programa) inteiros por candidato vivo, com pico no regime
baixo (teto quadrático do selection). Não há passe de otimização sobre o programa gravado: o
guloso já emite `rr`/`rrr` nativamente pela fusão do `exec_move`, e os certificadores não
produzem pares de rotação canceláveis adjacentes.

## Modo executor por `prog == NULL`

O `checker` zera o contexto inteiro e roda com `prog == NULL`: `emit` retorna sem gravar, e as
mesmas 11 operações aplicam o efeito em silêncio. Um campo booleano `silent` daria no mesmo,
mas o ponteiro que já existe carrega as duas informações — onde gravar e se deve gravar — numa
coisa só.

## Portfólio com certificador, em vez de guloso puro

O guloso por custo é quem entrega os programas curtos, mas sozinho ele não tem teto melhor que
O(n²) operações no pior caso — declará-lo como a rota O(n√n) ou O(n log n) seria falso. A
saída é rodá-lo **junto** de um certificador: `run_portfolio` gera os candidatos em cópias
privadas das pilhas e fica com o mais curto, então o programa emitido nunca excede o do
certificador do regime. O limite de complexidade vale por construção, no pior caso — e não
apenas na média — enquanto o guloso responde pelos benchmarks (ele vence em praticamente toda
entrada aleatória). Ver [../04-algoritmos/adaptive.md](../04-algoritmos/adaptive.md).

## Duas variantes do guloso, por política de desempate

`bias` decide qual lado fica com o empate em `move_better`. Duas execuções com políticas
opostas divergem logo no primeiro empate e descorrelacionam as trajetórias; o mínimo entre as
duas corta a cauda da distribuição de operações por um custo marginal — uma simulação a mais,
sem nenhum movimento extra no programa final.

## `GREEDY_MAX_N = 1500`

A varredura de candidatos do guloso é O(n²) em CPU mesmo com a poda. Acima de 1500 elementos o
tempo de parede começa a pesar e os benchmarks param em 500, então o portfólio passa a rodar só
o certificador. O teto preserva o contrato — a seleção de estratégia funciona para qualquer
tamanho — sem deixar o binário lento em entradas gigantes.

## Caso base em n ≤ 3, não em n ≤ 5

As quatro estratégias delegam para `sort_tiny` quando restam 3 elementos ou menos. O limite é
3, e não os 5 usuais, para preservar a saída exata do caso A1: o selection sort completo
rodando em `--simple 5 4 3 2 1` é a única verificação exata do `--simple`. Números e ganho em
[../04-algoritmos/tiny.md](../04-algoritmos/tiny.md).

## Número de blocos do chunk sort: `max(2, isqrt(n / 2))`

`isqrt(n)` parece natural e é pior: leva o pior caso do certificador médio em 500 elementos
para além de 8000 movimentos, enquanto `isqrt(n / 2)` fica na região plana do ótimo medido. A
varredura de k que sustenta a escolha e o papel do piso de 2 estão em
[../04-algoritmos/medium.md](../04-algoritmos/medium.md).

## Fase 1 do chunk sort só com `ra`

Girar sempre para cima é mais simples **e** não perde para o caminho mais curto: o giro para
trás embaralha a ordem de chegada em `b` e encarece a fase 2, devolvendo em média o que
economizou na fase 1 — com cauda pior. Medições em
[../04-algoritmos/medium.md](../04-algoritmos/medium.md).

## Radix como estratégia O(n log n) declarada

O radix binário tem contagem fechada e demonstrável: `bits × n` mais um `pa` por elemento com
bit zero, o que dá exatamente 1084 movimentos para n = 100 e 6784 para n = 500, sem variação
entre entradas não ordenadas do mesmo tamanho. É essa previsibilidade que o qualifica como
certificador do regime alto e como a rota da flag `--complex` — o guloso, que gasta menos,
não tem classe declarável melhor que O(n²) e por isso só roda dentro do portfólio.

## Tabela de nomes por cadeia de `if`

Ver [../02-restricoes/norma.md](../02-restricoes/norma.md): array local com inicializador viola
`DECL_ASSIGN_LINE` e tabela em escopo de arquivo é variável global, proibida neste projeto. A
cadeia de 11 `if` cabe em 23 linhas.
