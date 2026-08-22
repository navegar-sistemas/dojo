# Decisões de desenho

Cada uma com a alternativa rejeitada e a evidência.

## Stash único realocado, não lista de buffers

O resto entre chamadas é **uma** string na heap, recopiada a cada junção. A
alternativa clássica — lista encadeada de buffers, juntando só na extração —
lê a mesma quantidade e copia menos, mas espalha o estado por nós que todos os
caminhos de erro precisam percorrer, e cada função extra briga com as cotas de
[../02-restricoes/estilo.md](../02-restricoes/estilo.md).

Com a string única: os invariantes cabem numa linha ("`NULL` ou não vazia"),
o erro converge sempre para `free(stash)`, e os utilitários são os cinco de
qualquer biblioteca pessoal. O preço, medido: ≈ L²/2B cópias para uma linha
de tamanho L — ≈ 8 s no pior caso da suíte (L = 65 536, B = 1) e
imperceptível já com B = 42 no mesmo arquivo. Para linhas reais (até alguns
KB) a diferença não aparece. Corretude não depende de B; velocidade sim, e o
contrato só promete a primeira.

## Checar `\n` antes de qualquer `read`

`gnl_read_loop` testa `gnl_strchr(stash, '\n')` **na condição do laço**, antes
da primeira leitura. Três consequências observáveis, todas na aceitação:

- linha já bufferizada custa **zero** chamadas a `read` (medido: 1 único
  `read` entrega as três primeiras linhas de um arquivo pequeno);
- consumo total de um arquivo custa `⌈tamanho/B⌉` `read`s de dados — cada
  byte é lido uma vez — mais um ou dois `read`s vazios no fim
  (contagem exata em [../04-algoritmo/leitura.md](../04-algoritmo/leitura.md));
- fd fechado ainda entrega as linhas completas que já estão no stash
  ([../01-contrato/api.md](../01-contrato/api.md)).

Ler primeiro e checar depois leria além da conta e quebraria o caso do fd
intercalado do bônus.

## `read == 0` interrompe antes da junção

No fim do fluxo o laço para **sem** juntar o buffer vazio. Juntar `""` seria
inofensivo para o resultado, mas (a) faria um `malloc`+cópia inúteis por
chamada de fim de arquivo e (b) no arquivo vazio criaria um stash `""` — e o
invariante "nunca string vazia" de [fluxo.md](fluxo.md) teria uma exceção a
tratar.

## Buffer de leitura na heap, um por chamada

`malloc(BUFFER_SIZE + 1)` no começo de `gnl_read_loop`, `free` na saída. Um
array local (`char buf[BUFFER_SIZE + 1]`) estouraria a pilha com os B grandes
do contrato (10 000 000 na matriz de aceitação) — e B vem da linha de
compilação, fora do controle do código. O custo de um `malloc` por chamada é
irrelevante perto do próprio `read`.

A alocação acontece antes de checar se há `\n` bufferizado — simplicidade em
troca de um `malloc` dispensável quando a linha já está no stash; continua
O(1) alocações por chamada.

## `(size_t)BUFFER_SIZE + 1`, cast antes da soma

`BUFFER_SIZE` é um `int` de linha de comando. Com o maior `int` possível,
`BUFFER_SIZE + 1` estoura antes de virar argumento de `malloc`; o cast
primeiro faz a soma em `size_t`. (Nesse extremo o `malloc` provavelmente
falha — e aí vale o caminho de erro normal: `NULL`, sem efeito colateral.)

## `gnl_strjoin_free` consome o argumento

A junção libera o stash antigo **também quando o `malloc` falha**. Se não
liberasse, o único chamador teria que distinguir "falhou e preciso liberar" de
"deu certo e o ponteiro antigo já morreu" — exatamente o tipo de contrato
duplo que produz double free. Aqui: quem passa o stash para a junção nunca
mais o toca.

## Utilitários tolerantes a `NULL`

`gnl_strlen(NULL) == 0`, `gnl_strchr(NULL, c) == NULL`, `gnl_cpy(dst, NULL)`
copia 0. A primeira chamada de todas (stash `NULL`) passa pelos mesmos
caminhos que as demais — sem um `if` de inicialização em `gnl_read_loop`, que
já é a maior função do projeto (22 linhas).

## Prefixo `gnl_` nos símbolos exportados

Cinco utilitários precisam ser visíveis entre os dois `.c`, logo têm linkage
externo. `ft_strlen` colidiria com a biblioteca pessoal típica do programa
hospedeiro; `gnl_` não colide ([../02-restricoes/build.md](../02-restricoes/build.md)).

## Bônus: array indexado por fd, não lista

`static char *stash[FD_MAX];` — acesso O(1), zero código novo (as três fases
recebem `stash[fd]` como recebiam `stash`), custo fixo de `FD_MAX` ponteiros
zerados no BSS (8 KiB com o default 1024). A alternativa — lista de pares
(fd, stash) — aceitaria fd ilimitado ao custo de busca linear e mais duas
funções de gerência de nós, que não cabem na cota do arquivo. O limite é
honesto e configurável (`-D FD_MAX=n`); fd fora dele devolve `NULL` sem tocar
em nada ([../05-bonus/multi-fd.md](../05-bonus/multi-fd.md)).
