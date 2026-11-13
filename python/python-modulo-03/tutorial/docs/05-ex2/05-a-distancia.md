---
sidebar_position: 5
title: A distância
---

# A distância

A distância entre dois pontos é o comprimento da linha reta que os liga. No plano, com dois
eixos, ela vem do **teorema de Pitágoras**: num triângulo com um ângulo reto, o lado maior ao
quadrado é a soma dos quadrados dos outros dois. Em 3D, o teorema é aplicado duas vezes.

![Uma caixa entre os pontos (1.0, 2.5, 3.0) e (4.0, 5.0, 6.0). Os lados da caixa medem 3 no eixo x, 2.5 no eixo y e 3 no eixo z. A diagonal do chão da caixa mede a raiz de 3 ao quadrado mais 2.5 ao quadrado; a diagonal da caixa inteira, que liga os dois pontos, mede a raiz de 9 mais 6.25 mais 9, cerca de 4.9244](/img/ex2/distancia.svg)

Entre `(1.0, 2.5, 3.0)` e `(4.0, 5.0, 6.0)`, as diferenças em cada eixo são `4 − 1 = 3`,
`5 − 2.5 = 2.5` e `6 − 3 = 3`:

1. no chão da caixa, os lados 3 e 2.5 formam um triângulo reto, e a diagonal do chão mede
   √(3² + 2.5²);
2. essa diagonal e o lado vertical 3 formam outro triângulo reto, e a distância entre os pontos
   mede √(3² + 2.5² + 3²) = √24.25 ≈ 4.9244.

A fórmula, para os pontos `(x1, y1, z1)` e `(x2, y2, z2)`:

```text
distância = √((x2 − x1)² + (y2 − y1)² + (z2 − z1)²)
```

## Em Python

```python
import math


def distance(first: tuple[float, float, float],
             second: tuple[float, float, float]) -> float:
    """Return the Euclidean distance between two 3D points."""
    x1, y1, z1 = first
    x2, y2, z2 = second
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
```

- `math.sqrt` é a raiz quadrada (*square root*), do módulo `math` ("matemática"), que o
  `import math` no topo do arquivo carrega;
- `**` é a potência: `3 ** 2` é 9. As coordenadas chegam a esta função dentro da faixa de
  `get_player_pos`, e o `** 2` nunca estoura
  ([A faixa de valores](./04-get-player-pos.md#a-faixa-de-valores));
- as duas tuplas são desempacotadas em seis variáveis, o que deixa a fórmula legível;
- a linha do `def` passaria de 79 caracteres, então os parâmetros são quebrados em duas linhas,
  alinhados dentro dos parênteses.

O nome técnico desta distância é **distância euclidiana**. A distância até o centro é a mesma
função com o primeiro ponto em `(0.0, 0.0, 0.0)`: para `(1.0, 2.5, 3.0)`, √(1 + 6.25 + 9) =
√16.25 ≈ 4.0311.

## Quatro casas com round

`math.sqrt(16.25)` dá `4.031128874149275`. O enunciado mostra `4.0311`: o valor **arredondado**
em quatro casas depois do ponto. `round(número, casas)` faz isso:

```python title="experimentos/arredondar.py"
print(round(4.031128874149275, 4))
print(round(4.924428900898052, 4))
print(round(5.0, 4))
```

```bash
python3 experimentos/arredondar.py
```

```text
4.0311
4.9244
5.0
```

`round` devolve um número, não um texto com quatro casas fixas: quando as casas finais são zero,
elas não aparecem, e `5.0` continua `5.0`.
