---
sidebar_position: 2
title: Os feitiços de teste
---

# Os feitiços de teste

As funções do exercício precisam de feitiços para modificar. Crie o arquivo `ex1/higher_magic.py`
com o `import` e os quatro feitiços de teste desta página. As páginas seguintes acrescentam as
quatro funções do enunciado, sempre no fim do arquivo, e depois a demonstração.

```python
from collections.abc import Callable


def fireball(target: str, power: int) -> str:
    return f"Fireball hits {target}"


def heal(target: str, power: int) -> str:
    return f"Heals {target}"


def power_echo(target: str, power: int) -> str:
    return str(power)


def is_strong(target: str, power: int) -> bool:
    return power >= 15
```

## fireball e heal

Os dois seguem o contrato `(target: str, power: int) -> str`. Os textos saem da saída do
enunciado: `Combined spell result: Fireball hits Dragon, Heals Dragon` é a junção dos resultados
de `fireball` e `heal` com o alvo `Dragon`.

O enunciado mostra outro `heal` como exemplo do contrato, que devolve
`"Heal restores {target} for {power} HP"`, mas a saída de exemplo mostra `Heals Dragon`. O
tutorial segue a saída, que é o que pode ser comparado; com o `heal` do exemplo, a linha seria
`Fireball hits Dragon, Heal restores Dragon for 10 HP`.

Os dois feitiços não usam `power`, mas recebem o parâmetro mesmo assim: o contrato é o mesmo para
todos os feitiços, e as funções do exercício chamam qualquer feitiço com os dois argumentos.

## power_echo

A saída do enunciado mostra `Original: 10, Amplified: 30`: os números são o poder com que o
feitiço original e o amplificado foram lançados. Um feitiço que devolve um texto sem o poder,
como `fireball`, não mostraria a diferença. `power_echo` é um feitiço de teste, escolha do
tutorial, que devolve o próprio poder recebido, como texto (`str(power)`): lançado com 10, devolve
`"10"`; amplificado por 3, devolve `"30"`.

## is_strong

`is_strong` é a condição de teste de `conditional_caster`. O enunciado diz que a condição recebe
os mesmos argumentos do feitiço; por isso ela também recebe `(target, power)`, e devolve um `bool`:
`True` quando o poder é pelo menos 15. O valor 15 é escolha do tutorial.

Os quatro ficam no nível de cima do arquivo, como funções. O enunciado só diz "variáveis globais
(adote a pureza funcional sempre que possível)"; a leitura do tutorial é que uma função definida
com `def` no nível de cima não é uma variável global no sentido da proibição, porque não guarda um
estado que muda.
