# push_swap — funcionamento

## O que o programa faz

O `push_swap` recebe uma lista de inteiros e descobre como ordená-la usando **duas pilhas** e
um conjunto de **11 movimentos permitidos**, gastando o menor número possível de movimentos.

O que ele imprime **não é a lista ordenada** — é a **receita**: a sequência de movimentos que,
aplicada à pilha inicial, a deixaria ordenada. Um movimento por linha, em stdout, e nada mais.
Os números não reaparecem na saída em momento nenhum.

```
$ ./push_swap 3 2 1
sa
rra
```

Essas duas linhas significam "troque os dois elementos do topo, depois traga o do fundo para o
topo". Quem seguir as instruções partindo de `3 2 1` chega em `1 2 3` — mas o `push_swap` não
mostra esse resultado, ele entrega só o roteiro.

A ordenação em si acontece **dentro** do programa: ele mantém as duas pilhas em memória, simula
os movimentos sobre elas para descobrir quais funcionam e vai anotando os que usou. No fim as
pilhas simuladas são descartadas e o que sai é apenas a anotação.

Quem executa a receita de verdade é um segundo programa, o `checker`: ele recebe a mesma lista,
lê os movimentos de stdin, aplica um a um e responde se a pilha terminou ordenada. Uma versão
pronta dele acompanha o projeto em `assets/`, então dá para verificar a saída do `push_swap`
desde o primeiro dia — os detalhes estão na [seção do checker](#o-checker).

O custo de uma solução não é medido em tempo de CPU — é medido em **quantas linhas foram
impressas**. Ordenar 500 números com um algoritmo ruim gera dezenas de milhares de linhas; com
um bom, alguns milhares.

## As duas pilhas

- **Pilha `a`** — começa com os números passados por argumento. O primeiro argumento é o
  **topo** da pilha. Os números são inteiros, positivos ou negativos, sem repetições.
- **Pilha `b`** — começa vazia. É a área de trabalho.
- **Objetivo** — terminar com `a` em ordem crescente (menor valor no topo) e `b` vazia.

Notação usada neste documento: `a = [1 2 3]` significa topo à esquerda. Ou seja, `1` é o topo
e `3` é o fundo — e essa pilha está ordenada.

Pilha é acesso restrito: **só o topo é alcançável**. Não existe "pegue o 7º elemento". Para
mexer num elemento do meio, é preciso girar a pilha até ele chegar ao topo, e cada giro custa
uma linha da receita. Essa restrição é a origem de toda a dificuldade do projeto.

## Os 11 movimentos

Usando `a = [1 2 3 4]` e `b = [9 8 7]` como estado de partida em cada linha:

| Op | Nome | O que faz | Exemplo |
|---|---|---|---|
| `sa` | swap a | troca os 2 elementos do topo de `a` | a `1 2 3 4` → `2 1 3 4` |
| `sb` | swap b | troca os 2 elementos do topo de `b` | b `9 8 7` → `8 9 7` |
| `ss` | — | `sa` e `sb` de uma vez | — |
| `pa` | push a | tira o topo de `b` e põe no topo de `a` | → a `9 1 2 3 4`, b `8 7` |
| `pb` | push b | tira o topo de `a` e põe no topo de `b` | → a `2 3 4`, b `1 9 8 7` |
| `ra` | rotate a | gira para cima: o topo vai para o fundo | a `1 2 3 4` → `2 3 4 1` |
| `rb` | rotate b | idem em `b` | b `9 8 7` → `8 7 9` |
| `rr` | — | `ra` e `rb` de uma vez | — |
| `rra` | reverse rotate a | gira para baixo: o fundo vai para o topo | a `1 2 3 4` → `4 1 2 3` |
| `rrb` | reverse rotate b | idem em `b` | b `9 8 7` → `7 9 8` |
| `rrr` | — | `rra` e `rrb` de uma vez | — |

Movimento sem efeito possível não faz nada e não é erro: `sa` numa pilha de 1 elemento, `pa`
com `b` vazia.

Três propriedades desses movimentos governam todos os algoritmos:

1. **Girar é circular e custa 1 por posição.** Nada se perde num giro: `ra` aplicado n vezes
   numa pilha de n elementos devolve a pilha original. Para trazer ao topo o elemento que está
   na posição `i` de uma pilha de tamanho `n`, há dois caminhos — `ra` × `i`, ou `rra` ×
   `(n - i)`. O caminho mais curto custa **min(i, n − i)**, e escolher o mais curto é a
   economia mais básica que qualquer estratégia precisa fazer.

2. **Push inverte a ordem.** Empurrar `1`, depois `2`, depois `3` de `a` para `b` deixa
   `b = [3 2 1]` — cada elemento novo cobre o anterior. Consequência prática: se `b` está em
   ordem **decrescente** vista do topo, trazer tudo de volta com `pa` deposita os valores em
   `a` em ordem **crescente**. É por isso que todas as estratégias que usam `b` como depósito
   reinserem do **maior para o menor**.

3. **Os movimentos duplos são desconto.** `rr` faz o trabalho de `ra` + `rb` por uma linha só.
   Quando as duas pilhas precisam girar na mesma direção, usar o movimento duplo corta o custo
   pela metade.

### Exemplo completo

Ordenando `2 1 3 6 5 8` (topo = 2) em 12 movimentos:

| Movimento | Estado depois |
|---|---|
| início | a `2 1 3 6 5 8`, b vazia |
| `sa` | a `1 2 3 6 5 8` — os dois do topo trocaram |
| `pb pb pb` | a `6 5 8`, b `3 2 1` — os três primeiros foram para `b`, invertidos |
| `ra rb` | a `5 8 6`, b `2 1 3` — as duas pilhas giraram para cima |
| `rra rrb` | a `6 5 8`, b `3 2 1` — o giro anterior foi desfeito |
| `sa` | a `5 6 8`, b `3 2 1` — `a` está ordenada |
| `pa pa pa` | a `1 2 3 5 6 8`, b vazia — `b` estava decrescente, então voltou crescente |

Os dois pares de giros simultâneos poderiam ser `rr` e `rrr`: a mesma receita cairia de 12
para 10 linhas.

## Ranks: trabalhar com posições, não com valores

Os valores da entrada podem ser qualquer coisa — `-2147483648`, `7`, `1000000`. Antes de gerar
movimentos, duas das estratégias substituem cada valor pelo seu **rank**: a posição que ele
ocuparia na lista ordenada, de `0` a `n-1`.

```
entrada:  -5   1000000   3
ranks:     0      2      1
```

Ordenar os ranks é o mesmo problema que ordenar os valores, porque a ordem relativa é
idêntica. A vantagem é que os ranks são densos e conhecidos: valem exatamente `0..n-1`, o que
permite dividir em faixas uniformes (chunk sort) e limitar a quantidade de bits a
`log₂(n)` em vez de 32 (radix sort).

O cálculo dos ranks acontece em memória, em C, com uma ordenação auxiliar comum. Ele **não
gera movimentos** — não aparece na receita e não entra na contagem de complexidade, que conta
apenas movimentos push_swap.

## A métrica de desordem

A desordem quantifica, **antes de qualquer movimento**, o quão bagunçada a entrada está: um
número entre 0 e 1 igual à fração de pares fora de ordem. Percorrendo todos os pares de
posições `(i, j)` com `i < j`, cada par em que `a[i] > a[j]` conta como um erro:

```
desordem = pares errados / total de pares
```

- `1 2 3` → 0 — nenhum par errado, já está ordenado
- `3 2 1` → 1 — todos os pares errados, ordem exatamente inversa
- `4 67 3 87 23` → 0.40 — 4 dos 10 pares errados

Isso é a densidade de inversões, e ela mede algo que "quantos elementos estão fora do lugar"
não mede: uma lista quase ordenada com um único elemento deslocado tem desordem baixa mesmo
que muitos elementos tenham mudado de índice. Uma lista embaralhada ao acaso fica em torno de
0.5, porque cada par tem 50% de chance de estar invertido.

É essa medida que a estratégia adaptativa usa para escolher qual algoritmo rodar.

## As quatro estratégias

O binário embute quatro algoritmos diferentes para o mesmo problema, escolhidos por flag em
tempo de execução. Todos funcionam para qualquer entrada válida e todos produzem uma receita
que ordena a pilha — o que muda entre eles é **qual** receita sai e, principalmente, **quantas
linhas** ela tem.

```
./push_swap [--simple|--medium|--complex|--adaptive] [--bench] <inteiros...>
```

### `--simple` — O(n²), extração de mínimo

O algoritmo mais direto possível. Repete n vezes:

1. Procura o menor valor ainda em `a` e vê em que posição ele está.
2. Gira `a` até ele chegar ao topo, pelo caminho mais curto (`ra` × `i` ou `rra` × `n − i`).
3. `pb` — manda esse mínimo para `b`.

Como o que sai de `a` é sempre o menor restante, `b` vai sendo empilhada em ordem crescente
de baixo para cima, ou seja, **decrescente vista do topo**. Ao final, `pa` × n devolve tudo
para `a` já em ordem crescente (propriedade 2 da seção anterior).

É o selection sort traduzido para pilhas. Cada uma das n rodadas gasta até `n/2` giros, então
o total é **O(n²) movimentos**. Para n = 500 isso significa dezenas de milhares de linhas —
inviável. O algoritmo só compensa em entradas pequenas ou quase ordenadas, onde o mínimo já
está perto do topo e os giros são poucos.

### `--medium` — O(n√n), ordenação por blocos

O desperdício do `--simple` é procurar **um** elemento por vez: uma varredura inteira de `a`
para mover um único número. O chunk sort corrige isso movendo um grupo por varredura.

1. **Espalhar.** Divide os ranks em blocos por faixa (para n = 500: 15 blocos de 34 ranks cada
   — 0–33, 34–67, ...). Percorrendo os blocos do menor para o maior, varre `a` e dá `pb` em
   todo elemento que pertence ao bloco atual; quando o topo não pertence, `ra` para descartá-lo
   e seguir. Cada varredura leva um bloco inteiro de uma vez, não um elemento só.

2. **Recolher.** Com `a` vazia, repete n vezes: traz ao topo de `b` o maior rank restante,
   girando pelo caminho mais curto, e faz `pa`. Do maior para o menor, `a` cresce ordenada.

O que faz a fase 2 ser barata é a fase 1 já entregar `b` **aproximadamente** decrescente do
topo, e isso sai de graça da ordem dos blocos: o primeiro bloco empurrado (o de valores
menores) fica no fundo e o último (o de valores maiores) fica no topo. Dentro de um mesmo
bloco a ordem é arbitrária — os elementos chegam na ordem em que apareceram em `a` — mas o
bloco é pequeno, então o giro para achar o maior deles é curto. É essa diferença que faz a
fase 2 valer a pena: procurar o extremo entre 34 elementos, em vez de numa pilha embaralhada
de 500.

A quantidade de blocos é o que decide o custo, e os dois lados se opõem: mais blocos encarecem
a fase 1 (mais varreduras de `a`) e barateiam a fase 2 (busca em blocos menores). O mínimo fica
em torno de `√n / 2` — 15 blocos para n = 500, contra os 22 que a leitura ingênua de "√n
blocos" sugeriria, o que custaria cerca de 800 movimentos a mais.

Custo: um número de varreduras proporcional a √n, cada uma O(n) → **O(n√n) movimentos**, de
7000 a 7600 para 500 números.

### `--complex` — O(n log n), radix sort binário

Radix LSD: ordena os ranks olhando **um bit por vez**, do menos significativo para o mais
significativo. Para cada bit, uma passada:

- Percorre `a` uma vez (exatamente `size(a)` iterações): se o bit atual do rank no topo é `0`,
  `pb`; se é `1`, `ra`.
- Terminada a varredura, os ranks com bit `1` estão em `a` e os com bit `0` em `b`. `pa` até
  esvaziar `b`, o que recoloca os "bit 0" por cima dos "bit 1".

Cada passada é uma partição estável: separa zeros de uns preservando a ordem relativa que a
passada anterior estabeleceu. Ordenando do bit menos significativo ao mais significativo,
depois de `⌈log₂ n⌉` passadas (9 para n = 500, pois 2⁹ = 512 ≥ 500) a pilha está ordenada.

Rodando com 4 ranks (2 bits bastam para `0..3`):

```
a = 2 0 3 1                       (topo à esquerda)

bit 0:  pb pb ra ra   →  a = 3 1     b = 0 2
        pa pa         →  a = 2 0 3 1     (pares em cima, ímpares embaixo)
bit 1:  ra pb ra pb   →  a = 2 3     b = 1 0
        pa pa         →  a = 0 1 2 3     ordenada
```

Custo: `log₂(n)` passadas × O(n) movimentos por passada → **O(n log n)**. A contagem é
praticamente determinística: cada passada gasta o tamanho da pilha mais os `pa` de retorno,
quase independente de como a entrada estava embaralhada. Dá 1084 movimentos para n = 100 e
6784 para n = 500.

Descer bem abaixo disso exige outra família de algoritmo — tipicamente uma estratégia gulosa
de custo mínimo: empurrar tudo para `b` e, a cada reinserção, escolher o elemento cujo custo
total de giros em `a` e `b` somados é o menor, aproveitando `rr`/`rrr` sempre que as duas
pilhas precisarem girar para o mesmo lado.

### `--adaptive` — o padrão

Quando nenhuma flag de estratégia é passada, o programa mede a desordem da entrada e despacha
para uma das três rotas acima:

| Desordem | Rota escolhida |
|---|---|
| < 0.2 | O(n²) |
| 0.2 ≤ d < 0.5 | O(n√n) |
| ≥ 0.5 | O(n log n) |

O raciocínio é que nenhum algoritmo é o melhor em todo regime. Numa entrada quase ordenada
(poucas inversões), o quadrático mal precisa girar — encontra cada mínimo já perto do topo e
resolve em pouquíssimos movimentos, enquanto o radix gastaria suas ~6800 linhas fixas
igualmente. Numa entrada caótica o quadrático explode para dezenas de milhares de linhas e o
O(n log n) passa a ser a única opção viável. A desordem é o sinal barato — calculado antes de
qualquer movimento — que diz em qual dos dois regimes a entrada está.

Vale notar que entrada aleatória fica colada em 0.5, ora um pouco abaixo, ora um pouco acima:
o `--adaptive` cai ora no ramo O(n√n), ora no O(n log n), dependendo do sorteio.

## Linha de comando e saídas

Flags podem vir em qualquer ordem, antes ou depois dos números. `--bench` combina com qualquer
seletor de estratégia; duas flags de estratégia ao mesmo tempo, ou uma flag desconhecida, são
erro.

- **Saída normal** — um movimento por linha em stdout, `\n` como único separador, mais nada.
  Entrada já ordenada não produz nenhuma linha.
- **Sem argumento nenhum** — não imprime nada e devolve o prompt.
- **Erro** — imprime `Error` seguido de `\n` em **stderr** (nunca em stdout), e nada mais:

```bash
./push_swap 0 one 2 3      # Error — argumento não é inteiro
./push_swap --simple 3 2 3 # Error — valor duplicado
./push_swap 2147483648     # Error — estoura o range de int
./push_swap                # não imprime nada
```

### `--bench`

Modo de instrumentação. Depois de calcular a ordenação, escreve as métricas em **stderr**: a
desordem medida em % com duas casas, a estratégia usada com sua classe de complexidade, o
total de movimentos e a contagem de cada um dos 11 tipos. A soma das 11 contagens é igual ao
total.

Como as métricas vão para stderr e a receita continua em stdout, dá para medir e verificar na
mesma execução:

```
$ ./push_swap --bench $(cat args.txt) 2> bench.txt | ./checker $(cat args.txt)
OK
$ cat bench.txt
[bench] disorder:  49.93%
[bench] strategy:  Adaptive / O(n√n)
[bench] total_ops: 7997
[bench] sa: 0  sb: 0  ss: 0  pa: 500  pb: 500
[bench] ra: 4840  rb: 1098  rr: 0  rra: 0  rrb: 1059  rrr: 0
```

## O `checker`

O programa que **executa** a receita, em vez de calculá-la. Recebe a mesma lista de inteiros
por argumento (primeiro argumento no topo), lê movimentos de stdin — um por linha, até EOF —
aplica cada um às suas próprias pilhas e no final responde:

- `OK` em stdout, se `a` ficou ordenada **e** `b` vazia;
- `KO` em stdout, em qualquer outro estado final;
- `Error` em stderr, se um argumento for inválido (mesmas regras do push_swap) ou se aparecer
  uma instrução inexistente ou mal formatada.

`OK` e `KO` saem com código de retorno 0; `Error` sai com 255. Sem nenhum argumento, o programa
não imprime nada e encerra. Lista de movimentos vazia é aceita: se a entrada já estava
ordenada, a resposta é `OK`.

```
$ printf 'sa\nrra\n' | ./checker 3 2 1
OK
$ printf 'sa\n' | ./checker 3 2 1
KO
$ ./checker 3 2 one
Error
```

O `checker` é o que fecha o ciclo: sem ele, a saída do `push_swap` é uma lista de siglas que
ninguém confere. Ligando os dois, a receita é gerada e verificada numa tacada — é assim que se
testa se o `push_swap` está certo:

```bash
ARG="4 67 3 87 23"; ./push_swap $ARG | ./checker $ARG
```

### O checker de referência em `assets/`

Não é preciso esperar ter um `checker` escrito para testar o `push_swap`: `assets/` traz o
binário de referência já compilado, em três builds — `checker_linux`, `fedora_checker` e
`checker_Mac`. Todos são x86-64. Os arquivos chegam sem permissão de execução:

```bash
chmod +x assets/checker_linux
printf 'sa\nrra\n' | ./assets/checker_linux 3 2 1   # OK
```

Escrever a própria versão desse programa é a parte opcional do projeto — o comportamento
esperado é o mesmo descrito acima, que é justamente o que o binário de referência exibe.
