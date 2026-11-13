---
sidebar_position: 1
title: O problema
---

# O problema

Um grimório (livro de feitiços) cresce rápido se cada variação de feitiço for escrita à mão: bola
de fogo, bola de fogo tripla, bola de fogo só contra alvos fortes, bola de fogo seguida de cura...
O exercício 1 escreve, uma vez só, funções que **fabricam** essas variações a partir de qualquer
feitiço: recebem feitiços e devolvem feitiços novos. São funções de ordem superior
([Funções são valores](../02-conceitos/01-funcoes-sao-valores.md)).

## O que o enunciado pede

Um arquivo `ex1/higher_magic.py`. Autorizados: a função embutida `callable()` e o type hint
`Callable` (importado de `collections.abc`).

Todo feitiço segue o mesmo contrato, a mesma assinatura:

```python
def spell(target: str, power: int) -> str
```

Um feitiço recebe um alvo (`target`) e um nível de poder (`power`), e devolve um texto que
descreve o que aconteceu. O exemplo do enunciado:

```python
def heal(target: str, power: int) -> str:
    return f"Heal restores {target} for {power} HP"
```

As quatro funções, com as assinaturas do enunciado:

```python
def spell_combiner(spell1: Callable, spell2: Callable) -> Callable
def power_amplifier(base_spell: Callable, multiplier: int) -> Callable
def conditional_caster(condition: Callable, spell: Callable) -> Callable
def spell_sequence(spells: list[Callable]) -> Callable
```

| Função | Devolve |
|---|---|
| `spell_combiner(spell1, spell2)` | um feitiço que lança os dois com os mesmos argumentos e devolve uma tupla com os dois resultados. Exemplo: `combined = spell_combiner(fireball, heal)` |
| `power_amplifier(base_spell, multiplier)` | um feitiço com a mesma assinatura do original, que multiplica o poder antes de lançar. Exemplo: `mega_fireball = power_amplifier(fireball, 3)` |
| `conditional_caster(condition, spell)` | um feitiço que só é lançado se a condição for verdadeira; se não for, devolve `"Spell fizzled"` ("o feitiço falhou"). A condição e o feitiço recebem os mesmos argumentos |
| `spell_sequence(spells)` | um feitiço que lança todos os feitiços da lista, em ordem, com os mesmos argumentos, e devolve a lista dos resultados |

O programa precisa demonstrar o uso de **todas** essas funções.

## A saída esperada

O enunciado mostra um exemplo curto:

```text

Testing spell combiner...
Combined spell result: Fireball hits Dragon, Heals Dragon

Testing power amplifier...
Original: 10, Amplified: 30
```

Como no exercício 0, a saída começa com uma linha vazia. O programa do tutorial imprime essas seis
linhas e depois mais duas seções, uma para `conditional_caster` e outra para `spell_sequence`
([A demonstração](./07-a-demonstracao.md)).

O enunciado sugere o gerador de dados para inspirar valores de poder e alvos
([O gerador de dados](../01-ambiente/05-o-gerador-de-dados.md)); a página
[Rodar e conferir](./09-rodar-e-conferir.md) usa os dados dele.
