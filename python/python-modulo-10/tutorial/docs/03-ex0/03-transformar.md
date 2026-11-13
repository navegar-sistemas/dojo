---
sidebar_position: 3
title: Transformar nomes
---

# Transformar nomes

`spell_transformer` recebe uma lista de nomes de feitiço e devolve outra lista, com cada nome
enfeitado: `"fireball"` vira `"* fireball *"`. Uma transformação item a item é o trabalho do
`map`. A função entra depois de `power_filter`:

```python
def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda spell: f"* {spell} *", spells))
```

- a lambda recebe um nome e devolve a f-string com `"* "` antes e `" *"` depois;
- `map` aplica a lambda a cada nome, na ordem da lista;
- `list(...)` transforma o iterador do `map` na lista que o enunciado pede.

A lista recebida não muda: `map` cria valores novos, e a lista de entrada continua com os nomes
sem enfeite.

Na demonstração, a lista transformada é impressa com os nomes separados por espaço, e por isso a
saída fica `* fireball * * heal * * shield *`: são três itens, `* fireball *`, `* heal *` e
`* shield *`, um depois do outro ([A demonstração](./05-a-demonstracao.md)).
