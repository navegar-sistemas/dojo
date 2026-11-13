---
sidebar_position: 3
title: O float e o round
---

# O float e o round

Um `float` guarda a maioria dos números decimais de forma **aproximada**. O computador guarda
números em base 2, e 0,8, como 1/3 em base 10, não tem representação exata nessa base: o que fica
guardado é o número mais próximo possível. A diferença é minúscula, mas aparece quando o número é
impresso depois de algumas contas.

## Um experimento

```python title="experimentos/decimais.py"
height = 25.0
height += 0.8
print(height)
height += 0.8
print(height)
height += 0.8
print(height)
print(round(height, 1))
print(0.1 + 0.2)
print(round(25.0, 1))
print(round(25, 1))
print(round(25.0))
```

```bash
python3 experimentos/decimais.py
```

```text
25.8
26.6
27.400000000000002
27.4
0.30000000000000004
25.0
25
25
```

- no terceiro dia, a soma acumulou o erro, e o `print` mostra `27.400000000000002` em vez de
  `27.4`. A soma clássica `0.1 + 0.2` mostra o mesmo efeito;
- **`round(número, 1)`** arredonda para **uma** casa decimal: `round(height, 1)` dá `27.4`. O
  `round` é uma das funções autorizadas deste exercício;
- `round(25.0, 1)` dá `25.0`, que imprime com a casa decimal que a saída pede;
- `round(25, 1)` dá `25`, **sem** casa decimal: arredondar um inteiro devolve um inteiro;
- `round(25.0)`, sem o número de casas, arredonda para o inteiro mais próximo e devolve um `int`.
  O exercício 4 usa isso.

## As duas consequências

1. **O `show()` arredonda na hora de imprimir.** O valor guardado continua exato até onde o
   `float` permite; só o texto impresso é arredondado:

   ```python
       def show(self) -> None:
           print(
               f"{self.name}: {round(self.height, 1)}cm, "
               f"{self.age_days} days old"
           )
   ```

   Numa linha só,
   `print(f"{self.name}: {round(self.height, 1)}cm, {self.age_days} days old")` teria 82
   caracteres, contando os oito espaços de recuo, e o flake8 acusaria
   `E501 line too long (82 > 79 characters)` ("linha comprida demais"): o estilo padrão limita
   cada linha a 79 caracteres. Por isso a linha foi dividida em duas f-strings. Duas strings
   seguidas, sem nada entre elas, viram uma só: o Python as junta numa só ao ler o código. Os
   parênteses do `print` são o que permite quebrar a linha entre as duas.

   Arredondar só no `show()` é escolha do projeto: a altura guardada não perde nada, e todo lugar
   que imprime uma altura arredonda do mesmo jeito. Outra opção seria arredondar ao guardar, em
   `grow()`; aí cada método que muda a altura precisaria lembrar de arredondar.

2. **A altura começa como `25.0`, não `25`.** Com `25`, a altura seria um `int`, e `round(25, 1)`
   imprimiria `25cm` em vez de `25.0cm`. Escrevendo `25.0`, ela já nasce `float`.

O enunciado não autoriza `float()`, a função que converte um valor em `float`; escrever o número
com `.0` resolve sem ela.
