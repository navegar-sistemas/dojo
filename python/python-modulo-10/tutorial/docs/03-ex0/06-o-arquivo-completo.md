---
sidebar_position: 6
title: O arquivo completo
---

# O arquivo completo

```python title="ex0/lambda_spells.py"
def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    return sorted(artifacts, key=lambda artifact: artifact["power"],
                  reverse=True)


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    return list(filter(lambda mage: mage["power"] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda spell: f"* {spell} *", spells))


def mage_stats(mages: list[dict]) -> dict:
    if not mages:
        return {"max_power": 0, "min_power": 0, "avg_power": 0.0}
    strongest = max(mages, key=lambda mage: mage["power"])
    weakest = min(mages, key=lambda mage: mage["power"])
    total = sum(map(lambda mage: mage["power"], mages))
    return {
        "max_power": strongest["power"],
        "min_power": weakest["power"],
        "avg_power": round(total / len(mages), 2),
    }


def main() -> None:
    artifacts = [
        {"name": "Crystal Orb", "power": 85, "type": "focus"},
        {"name": "Fire Staff", "power": 92, "type": "weapon"},
        {"name": "Ice Wand", "power": 70, "type": "accessory"},
    ]
    print("\nTesting artifact sorter...")
    first, second = artifact_sorter(artifacts)[:2]
    print(f"{first['name']} ({first['power']} power) comes before "
          f"{second['name']} ({second['power']} power)")

    print("\nTesting spell transformer...")
    print(" ".join(spell_transformer(["fireball", "heal", "shield"])))


if __name__ == "__main__":
    main()
```

O que o arquivo usa, todos autorizados: as funções embutidas `sorted`, `filter`, `map`, `max`,
`min`, `sum`, `len` e `round` (as oito da lista do enunciado), mais `list` (o tipo padrão de
lista) e `print`, e o método `join` de `str`. Não há nenhum `import`. São seis lambdas, uma em
cada ordenação, filtro, transformação ou comparação, e cinco `def`: as quatro funções do enunciado
e o `main`.
