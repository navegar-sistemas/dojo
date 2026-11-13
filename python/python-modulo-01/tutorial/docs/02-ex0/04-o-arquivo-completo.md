---
sidebar_position: 4
title: O arquivo completo
---

# O arquivo completo

As variáveis e os `print` vão dentro do bloco `if __name__ == "__main__":`, com quatro espaços
de recuo:

```python title="ex0/ft_garden_intro.py"
if __name__ == "__main__":
    name: str = "Rose"
    height: int = 25
    age: int = 30
    print("=== Welcome to My Garden ===")
    print(f"Plant: {name}")
    print(f"Height: {height}cm")
    print(f"Age: {age} days")
    print()
    print("=== End of Program ===")
```

O arquivo só chama `print()`, a única função autorizada.
