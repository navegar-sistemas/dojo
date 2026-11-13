---
sidebar_position: 3
title: O __init__.py de alchemy
---

# O \_\_init\_\_.py de alchemy

O enunciado quer o pacote `alchemy` mostrando `create_air` na sua interface, e nada que mostre
`create_earth`. A **interface** de um pacote são os nomes que existem direto nele, os que se
alcançam com `alchemy.nome` depois de um `import alchemy`. Quem cria esses nomes é o
`__init__.py` ([Pacote e \_\_init\_\_.py](../04-conceitos/03-pacote-e-init.md)).

Crie `alchemy/__init__.py`:

```python title="alchemy/__init__.py"
from .elements import create_air

__all__ = ["create_air"]
```

- `from .elements import create_air` carrega o módulo `alchemy/elements.py` e cria, no pacote, o
  nome `create_air`. O ponto é o import relativo: "o `elements` deste pacote", e não o
  `elements.py` da raiz ([Absoluto e relativo](../04-conceitos/04-absoluto-e-relativo.md));
- `__all__ = ["create_air"]` declara `create_air` como a interface pública. Sem essa linha, o
  flake8 acusa `F401 '.elements.create_air' imported but unused`, porque o próprio `__init__.py`
  não usa o nome que importa. A `__all__` é a convenção habitual que o enunciado pede para esse
  caso;
- `create_earth` não aparece em lugar nenhum do arquivo: o `__init__.py` não cria esse nome, e
  `alchemy.create_earth` não existe.

O import relativo é escolha do tutorial; o absoluto `from alchemy.elements import create_air`
funciona igual. O relativo é o costume dentro de um pacote, para o pacote não depender do próprio
nome.

## Nada foi escondido

Como na [experiência do armário](../04-conceitos/03-pacote-e-init.md#o-que-o-pacote-mostra-e-o-que-fica-acessível),
carregar `alchemy/elements.py` cria também o atributo `alchemy.elements`, e por ele a função
`create_earth` continua alcançável pelo caminho completo, `alchemy.elements.create_earth()`. O
enunciado pede que `create_earth` não seja alcançável **pela interface**, `alchemy.create_earth`,
e é isso que o `__init__.py` garante. Esconder o módulo inteiro não é pedido, nem possível: o
Python não tem módulos privados.
