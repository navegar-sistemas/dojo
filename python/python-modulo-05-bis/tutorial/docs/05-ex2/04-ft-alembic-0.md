---
sidebar_position: 4
title: ft_alembic_0.py
---

# ft_alembic_0.py

O primeiro programa alcança o ingrediente que está à mão: o `elements.py` da raiz, com a estrutura
`import ...`, a que traz o módulo inteiro. Crie `ft_alembic_0.py`, na raiz:

```python title="ft_alembic_0.py"
import elements

if __name__ == "__main__":
    print("=== Alembic 0 ===")
    print("Using: 'import ...' structure to access elements.py")
    print(f"Testing create_fire: {elements.create_fire()}")
```

- `import elements` acha o `elements.py` na primeira pasta do `sys.path`, a raiz, onde o programa
  está ([Onde o Python procura](../04-conceitos/02-onde-o-python-procura.md)). O nome `elements`
  passa a ser o módulo, e a função é chamada pelo caminho `elements.create_fire()`;
- o código fica dentro de `if __name__ == "__main__":`, como em todos os programas do projeto:
  roda quando o arquivo é o programa, e não roda se algum dia o arquivo for importado;
- as aspas simples em `'import ...'` fazem parte do texto; o `print` usa aspas duplas por fora.

```bash
python3 ft_alembic_0.py
```

```text
=== Alembic 0 ===
Using: 'import ...' structure to access elements.py
Testing create_fire: Fire element created
```

`import elements` não confunde o `elements.py` da raiz com o `alchemy/elements.py`: o segundo só
seria encontrado como `alchemy.elements`, pelo caminho do pacote.
