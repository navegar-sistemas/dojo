---
sidebar_position: 5
title: O arquivo completo
---

# O arquivo completo

A classe, e no bloco main as três plantas: cada uma instanciada e depois preenchida, atributo por
atributo. No fim, o título e um `show()` por planta:

```python title="ex1/ft_garden_data.py"
class Plant:
    name: str
    height: int
    age_days: int

    def show(self) -> None:
        print(f"{self.name}: {self.height}cm, {self.age_days} days old")


if __name__ == "__main__":
    rose = Plant()
    rose.name = "Rose"
    rose.height = 25
    rose.age_days = 30

    sunflower = Plant()
    sunflower.name = "Sunflower"
    sunflower.height = 80
    sunflower.age_days = 45

    cactus = Plant()
    cactus.name = "Cactus"
    cactus.height = 15
    cactus.age_days = 120

    print("=== Garden Plant Registry ===")
    rose.show()
    sunflower.show()
    cactus.show()
```

O arquivo só chama `print()`, a função autorizada; `Plant()` é a própria classe, e `show()` é um
método do próprio arquivo. As linhas em branco dentro do bloco main só separam uma planta da
outra.

O preenchimento repete quatro linhas por planta. O exercício 3 resolve essa repetição.
