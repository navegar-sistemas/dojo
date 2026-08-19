# Formato do `--bench`

Cinco linhas em stderr, escritas depois do programa final ser impresso, só quando a flag está
presente.

```
[bench] disorder:  40.00%
[bench] strategy:  Adaptive / O(n√n)
[bench] total_ops: 9
[bench] sa: 1  sb: 0  ss: 0  pa: 2  pb: 2
[bench] ra: 1  rb: 0  rr: 0  rra: 2  rrb: 0  rrr: 1
```

## Regras de formatação

- Toda linha começa com `[bench] ` — colchetes, a palavra, colchete, um espaço.
- `disorder:` e `strategy:` são seguidos de **dois** espaços; `total_ops:` de **um**. Os dois
  primeiros rótulos têm 9 caracteres e `total_ops:` tem 10; o espaçamento compensa a diferença
  e os três valores começam na mesma coluna.
- Nas duas últimas linhas, cada par é `nome: valor` e os pares são separados por **dois**
  espaços. Não há espaço no fim da linha.
- Primeira linha de contagens: `sa sb ss pa pb`. Segunda: `ra rb rr rra rrb rrr`. A ordem é a
  mesma do enum `t_op`.

## Campos

**`disorder`** — a desordem medida antes de qualquer movimento, em porcentagem com exatamente
duas casas decimais, seguida de `%`. Ver [../04-algoritmos/desordem.md](../04-algoritmos/desordem.md).

**`strategy`** — `<Nome> / <classe>`:

| Flag | Nome | Classe |
|---|---|---|
| `--simple` | `Simple` | `O(n²)` |
| `--medium` | `Medium` | `O(n√n)` |
| `--complex` | `Complex` | `O(n log n)` |
| `--adaptive` | `Adaptive` | a classe do regime certificado |

Em `--adaptive`, a classe reflete o **regime** da desordem medida, não o candidato que venceu
o portfólio: desordem 0.40 imprime `Adaptive / O(n√n)`, desordem 0.60 imprime
`Adaptive / O(n log n)` — mesmo quando o programa emitido veio do guloso. Ver
[../04-algoritmos/adaptive.md](../04-algoritmos/adaptive.md).

Os símbolos `²` e `√` são UTF-8 dentro de literais de string; saem por `write` como qualquer
outro byte.

**`total_ops`** — quantidade de linhas escritas em stdout.

**Contagens** — quantas vezes cada uma das 11 operações apareceu.

## Invariantes

- A soma das 11 contagens é igual a `total_ops`.
- `total_ops` é igual ao número de linhas em stdout, ou seja
  `./push_swap --bench ARGS 2>&1 >/dev/null` e `./push_swap ARGS | wc -l` concordam.
- Com a entrada já ordenada ou vazia de movimentos, todas as contagens são 0 e `total_ops` é 0.

## Percentual sem formatador de ponto flutuante

Não há `printf` disponível, e a libft não formata `double`. O caminho é converter para inteiro
antes de imprimir:

```
centesimos = (int)(disorder * 10000.0 + 0.5)
imprime centesimos / 100
imprime '.'
imprime centesimos % 100 com dois dígitos (zero à esquerda quando < 10)
imprime '%'
```

O `+ 0.5` arredonda em vez de truncar. Casos de borda: `0.4` vira `4000` e imprime `40.00`;
`0.4993` vira `4993` e imprime `49.93`; `0.0` imprime `0.00`; `1.0` imprime `100.00`.

A parte decimal precisa do zero à esquerda: 5 centésimos imprime `.05`, não `.5`.

## Momento da coleta

As contagens são preenchidas pelo `prog_flush`, na mesma passada que imprime o programa final —
stdout e métricas não têm como divergir por construção. O `bench_print` roda depois do flush;
antes dele, reportaria tudo zerado. Ver
[../03-arquitetura/tipos.md](../03-arquitetura/tipos.md) para o mecanismo do programa gravado.
