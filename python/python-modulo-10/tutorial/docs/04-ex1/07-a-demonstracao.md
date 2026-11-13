---
sidebar_position: 7
title: A demonstração
---

# A demonstração

O `main` entra no fim do arquivo, depois de `spell_sequence`. As duas primeiras seções reproduzem
o exemplo do enunciado; as duas últimas demonstram as outras duas funções, como o enunciado exige.

```python
def main() -> None:
    print("\nTesting spell combiner...")
    combined = spell_combiner(fireball, heal)
    print(f"Combined spell result: {', '.join(combined('Dragon', 10))}")

    print("\nTesting power amplifier...")
    mega_echo = power_amplifier(power_echo, 3)
    print(f"Original: {power_echo('Dragon', 10)}, "
          f"Amplified: {mega_echo('Dragon', 10)}")

    print("\nTesting conditional caster...")
    careful_fireball = conditional_caster(is_strong, fireball)
    print(f"Power 20: {careful_fireball('Goblin', 20)}")
    print(f"Power 5: {careful_fireball('Goblin', 5)}")

    print("\nTesting spell sequence...")
    combo = spell_sequence([fireball, heal, mega_echo])
    print(f"Sequence result: {combo('Wizard', 12)}")


if __name__ == "__main__":
    main()
```

- **combiner:** `combined('Dragon', 10)` devolve a tupla
  `('Fireball hits Dragon', 'Heals Dragon')`, e `', '.join(...)` junta os dois textos com vírgula
  e espaço, como na saída do enunciado;
- **amplifier:** a mesma chamada, `('Dragon', 10)`, vai para o feitiço original e para o
  amplificado; o original devolve `10`, o amplificado `30`;
- **conditional caster:** o mesmo feitiço condicional, com poder 20 (passa na condição) e 5 (não
  passa). Os rótulos `Power 20:` e `Power 5:` são do tutorial;
- **sequence:** o `print` mostra a lista devolvida como o Python a escreve, com colchetes e aspas,
  o que deixa claro que o resultado é uma lista.

O `\n` no começo de cada `Testing` imprime a linha vazia antes do título, inclusive a primeira
linha vazia da saída. O `if __name__ == "__main__":` roda o `main` só quando o arquivo é executado
com `python3` ([A demonstração do exercício 0](../03-ex0/05-a-demonstracao.md)).

Todas as variáveis (`combined`, `mega_echo`, `careful_fireball`, `combo`) ficam dentro do `main`:
nenhuma é global.
