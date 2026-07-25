# `--complex` — O(n log n)

Radix sort binário LSD sobre [ranks](ranks.md), que o `main` já converteu antes de chamar a
estratégia.

```
sort_complex(c, conf):
    conf.name = "Complex"
    conf.cclass = "O(n log n)"
    se a.size <= 3:
        sort_tiny(c); devolve
    se stack_is_sorted(a):
        devolve

    n = a.size
    bits = 0
    enquanto (n - 1) >> bits:
        bits += 1

    bit = 0
    enquanto bit < bits:
        i = 0
        size = a.size
        enquanto i < size:
            se ((a.data[0] >> bit) & 1) == 0:
                op_pb(c)
            senão:
                op_ra(c)
            i += 1
        enquanto b.size > 0:
            op_pa(c)
        bit += 1
```

## Detalhes que quebram se forem trocados

**`size` é capturado antes do laço interno.** `a->size` diminui a cada `pb`; usar
`a->size` na condição faria a varredura parar cedo e deixaria elementos sem examinar.

**A passada percorre exatamente `size` posições**, uma por elemento, independentemente de
quantos foram para `b`. Cada elemento é examinado uma única vez por bit.

**A contagem de bits usa `n - 1`**, o maior rank. Para n = 500, `499` precisa de 9 bits porque
`2⁹ = 512 > 499`. Usar `n` daria 9 também nesse caso, mas erraria em potências de 2: com
n = 256 o maior rank é 255, que cabe em 8 bits, enquanto `256` exigiria 9 e gastaria uma
passada inteira à toa.

Para n = 1 o laço nem começa (`0 >> 0` é falso) e nenhuma operação é emitida.

## Por que ordena

Cada passada é uma partição estável. Os elementos com bit 0 vão para `b` na ordem inversa em
que apareciam; ao voltarem com `pa`, a inversão se desfaz e eles ficam **por cima** dos
elementos com bit 1, que permaneceram em `a` na ordem relativa original.

Processando do bit menos significativo para o mais significativo, cada passada preserva a
ordenação estabelecida pelas anteriores dentro de cada grupo. Depois de `⌈log₂ n⌉` passadas, a
pilha está ordenada.

## Contagem fechada

Cada passada custa `size` movimentos na varredura mais um `pa` por elemento que foi para `b`,
isto é, por elemento com aquele bit zerado. O total não depende de como a entrada estava
embaralhada:

```
total = bits × n + Σ (quantidade de ranks em 0..n-1 com o bit b zerado)
                   b
```

| n | bits | varreduras | `pa` | total |
|---|---|---|---|---|
| 100 | 7 | 700 | 384 | **1084** |
| 500 | 9 | 4500 | 2284 | **6784** |

Os dois valores foram confirmados por simulação: em amostras aleatórias distintas do mesmo
tamanho, a contagem observada foi sempre a mesma. **Qualquer variação entre execuções indica
bug** — tipicamente na contagem de bits ou no `size` capturado.

6784 é também o número que o enunciado publica no exemplo de entrada grande.

## Custo

`log₂(n)` passadas de O(n) movimentos: **O(n log n)**.

## Parada antecipada (opcional)

```
se stack_is_sorted(a) e b.size == 0:
    interrompe o laço de bits
```

Reduz movimentos quando os bits altos não separam nada, ao custo de romper a igualdade exata
com 1084 e 6784. Só vale implementar **depois** que esses números baterem, e implica atualizar
os casos de aceitação.

Para n = 500 com entrada aleatória não há ganho: os ranks `256..499` só se separam de
`0..255` no nono bit, então todas as passadas são necessárias.
