# Fluxo do `main`

```
 1. conf = { STRAT_NONE, 0, NULL, NULL }
 2. se parse_flags(argc, argv, &conf) falhar  -> erro
 3. se conf.strategy == STRAT_NONE            -> conf.strategy = STRAT_ADAPTIVE
 4. a = parse_numbers(argc, argv)
    se a == NULL                              -> erro
 5. se a->size == 0                           -> libera a, retorna 0 sem imprimir
 6. b = stack_new(a->size)
    se b == NULL                              -> erro
 7. counts[0..10] = 0
    ctx = { a, b, counts }
 8. d = compute_disorder(a)
 9. despacha por conf.strategy:
       STRAT_SIMPLE   -> sort_simple(&ctx, &conf)
       STRAT_MEDIUM   -> sort_medium(&ctx, &conf)
       STRAT_COMPLEX  -> sort_complex(&ctx, &conf)
       STRAT_ADAPTIVE -> sort_adaptive(&ctx, &conf, d)
    (o despacho é pulado se stack_is_sorted(a), mas conf.name/cclass
     ainda precisam ser preenchidos — ver abaixo)
10. se conf.bench                             -> bench_print(&ctx, &conf, d)
11. libera a e b, retorna 0
```

## Ordens que não podem ser trocadas

**A desordem é medida no passo 8, antes do 9.** O enunciado exige a medida antes de qualquer
movimento, e a conversão em ranks do passo 9 substituiria os valores. Matematicamente a
desordem dos ranks é igual à dos valores, mas medir antes elimina a dúvida.

**As flags são lidas antes dos números.** Um token `--foo` precisa ser rejeitado como flag
desconhecida, não tentado como número.

**A validação inteira acontece antes do primeiro movimento.** É o que garante que nunca sai
metade da receita seguida de `Error`.

**`b` é alocada depois do parsing.** A capacidade é `a->size`, que só se conhece ao final da
leitura.

## Entrada já ordenada

O despacho é pulado, mas `conf.name` e `conf.cclass` precisam existir para o `--bench`. Duas
formas equivalentes:

- Cada `sort_*` começa com `conf->name = ...; conf->cclass = ...;` e só depois testa
  `stack_is_sorted`, retornando sem emitir nada. O despacho roda sempre, e a checagem de
  ordenação fica dentro da estratégia.
- O `main` resolve nome e classe e pula a chamada.

A primeira é preferível: mantém o `main` menor e deixa cada estratégia dona do próprio rótulo.
Em `--adaptive`, `sort_adaptive` continua escolhendo a rota pela desordem mesmo com a pilha
ordenada — desordem 0 cai em `< 0.2`, então o rótulo reportado é `Adaptive / O(n²)`.

## Caminho de erro

Um único ponto de falha:

```
erro:
    escreve "Error\n" em stderr (descritor 2)
    libera o que já foi alocado
    exit(1)
```

Como o `main` está limitado a 25 linhas, esse tratamento cabe numa função `static` auxiliar
chamada de cada ponto de verificação. A liberação precisa lidar com ponteiros `NULL` — em
`stack_free(NULL)` a função retorna sem fazer nada.

## Distribuição das funções em `main.c`

| Função | Papel |
|---|---|
| `main` | passos 1 a 11 |
| `run_strategy` (static) | passo 9, a cadeia de `if` sobre `conf.strategy` |
| `fail` (static) | caminho de erro: mensagem, liberação, `exit(1)` |

Três funções, dentro da cota do arquivo.
