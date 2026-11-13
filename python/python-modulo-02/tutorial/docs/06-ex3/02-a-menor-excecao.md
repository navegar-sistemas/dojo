---
sidebar_position: 2
title: A menor exceção
---

# A menor exceção

Um tipo de exceção novo é uma **classe que herda de `Exception`**. A menor possível não tem nada
dentro:

```python
class GardenError(Exception):
    pass
```

- `class GardenError(Exception):` cria a classe `GardenError` como filha de `Exception`. Ela
  ganha tudo o que uma exceção tem: pode ser lançada com `raise`, capturada com `except` e
  transformada em texto;
- `pass` é a instrução "não faça nada", necessária porque o corpo de uma classe não pode ficar
  vazio.

Um experimento, `experimentos/menor.py`:

```python
class GardenError(Exception):
    pass


try:
    raise GardenError("The garden is flooded!")
except GardenError as error:
    print(f"Caught GardenError: {error}")
```

```bash
python3 experimentos/menor.py
```

```text
Caught GardenError: The garden is flooded!
```

O tipo novo funciona como os embutidos. Na árvore de tipos da página
[Os tipos embutidos](../02-excecoes/06-os-tipos-embutidos.md), `GardenError` entra como mais um
filho de `Exception`.

Falta a mensagem padrão: criado sem mensagem, `GardenError()` não tem texto nenhum. A
[próxima página](./03-a-mensagem-padrao.md) resolve isso.
