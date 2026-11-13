---
sidebar_position: 6
title: A demonstração
---

# A demonstração

O `main` entra no fim do arquivo, depois de `memory_vault`, e imprime a saída do enunciado:

```python
def main() -> None:
    print("Testing mage counter...")
    counter_a = mage_counter()
    counter_b = mage_counter()
    print(f"counter_a call 1: {counter_a()}")
    print(f"counter_a call 2: {counter_a()}")
    print(f"counter_b call 1: {counter_b()}")

    print("\nTesting spell accumulator...")
    base = 100
    accumulate = spell_accumulator(base)
    for amount in [20, 30]:
        print(f"Base {base}, add {amount}: {accumulate(amount)}")

    print("\nTesting enchantment factory...")
    flaming = enchantment_factory("Flaming")
    frozen = enchantment_factory("Frozen")
    print(flaming("Sword"))
    print(frozen("Shield"))

    print("\nTesting memory vault...")
    vault = memory_vault()
    store, recall = vault["store"], vault["recall"]
    key, value = "secret", 42
    store(key, value)
    print(f"Store '{key}' = {value}")
    print(f"Recall '{key}': {recall(key)}")
    print(f"Recall 'unknown': {recall('unknown')}")


if __name__ == "__main__":
    main()
```

- **contador:** os dois contadores são criados antes do primeiro uso. Os números depois dos
  dois-pontos são os valores devolvidos por cada chamada; o `call 1` e o `call 2` são só rótulos
  da mensagem;
- **acumulador:** o `for` chama o acumulador com 20 e depois com 30; `base` guarda o 100 para a
  mensagem;
- **fábrica:** duas funções de encantamento, uma de cada tipo;
- **cofre:** `store, recall = vault["store"], vault["recall"]` tira as duas funções do dicionário
  e as guarda em duas variáveis, de uma vez. `store(key, value)` não devolve nada; a linha
  `Store 'secret' = 42` só descreve o que foi guardado. As aspas simples em volta da chave fazem
  parte do texto da mensagem.

O primeiro `print` não tem `\n`: a saída começa direto no `Testing mage counter...`. Os outros
títulos têm, e cada um imprime a linha vazia que o separa do bloco anterior.
