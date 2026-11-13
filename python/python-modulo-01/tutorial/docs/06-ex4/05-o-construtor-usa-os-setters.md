---
sidebar_position: 5
title: O construtor usa os setters
---

# O construtor usa os setters

O construtor também recebe uma altura e uma idade, e elas também podem ser negativas. O enunciado
dá duas saídas para um valor inválido: manter o dado como estava ou, na criação, usar um **valor
padrão**. Na criação não existe valor anterior, então o projeto usa o valor padrão: altura `0.0`
e idade `0`.

```python
    def __init__(self, name: str, height: float, age_days: int) -> None:
        self._name = name
        self._height = 0.0
        self._age_days = 0
        self.set_height(height)
        self.set_age(age_days)
```

1. o nome é guardado primeiro, porque as mensagens de erro dos setters o usam;
2. altura e idade começam com o valor padrão;
3. os setters tentam trocar o padrão pelos valores recebidos. Um valor válido entra; um negativo
   é recusado com a mensagem de erro, e o padrão fica.

A validação continua escrita num lugar só: o construtor não repete o `if height < 0`, ele chama o
setter. `Plant("Fern", -3.0, 10)` imprime `Fern: Error, height can't be negative` e cria uma
samambaia com `0.0` cm e 10 dias ([Rodar e conferir](./08-rodar-e-conferir.md) roda esse
caso).

Os setters não imprimem nada quando aceitam o valor, e por isso a criação de uma planta válida é
silenciosa, como a saída do enunciado mostra (`Plant created:` vem logo depois do título, sem
nenhuma linha entre os dois).
