---
sidebar_position: 3
title: str.capitalize
---

# str.capitalize

`water_plant` precisa saber se um nome está **capitalizado**. O método `capitalize()` de um texto
devolve uma cópia com a primeira letra maiúscula e todas as outras minúsculas:

| Nome | `nome.capitalize()` | Já estava capitalizado? |
|---|---|---|
| `"Tomato"` | `"Tomato"` | sim |
| `"lettuce"` | `"Lettuce"` | não |
| `"LETTUCE"` | `"Lettuce"` | não |
| `"carrots"` | `"Carrots"` | não |
| `"Carrot Cake"` | `"Carrot cake"` | não |

Um nome está capitalizado quando ele é **igual** à sua versão capitalizada:

```python
plant_name == plant_name.capitalize()
```

O método não muda o texto original (textos em Python não mudam nunca); ele devolve um texto novo,
que só serve para a comparação. Por isso `"Carrot Cake"` não passa: o `capitalize()` deixa
minúscula toda letra depois da primeira, inclusive o `C` de `Cake`.

`str.capitalize()` é o nome completo do método: `str` é a classe dos textos. Ele é a segunda
função autorizada do exercício 4, ao lado do `print()`.
