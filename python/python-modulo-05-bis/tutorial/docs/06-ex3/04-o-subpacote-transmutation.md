---
sidebar_position: 4
title: O subpacote transmutation
---

# O subpacote transmutation

A receita de transformar chumbo em ouro fica um nível abaixo, no subpacote `transmutation`, e usa
três ingredientes de três lugares: o ar (no pacote de cima, `alchemy`), a poção de força (também
no pacote de cima) e o fogo (fora de qualquer pacote). O enunciado pede, nesse arquivo, pelo menos
um import absoluto e um relativo.

## O subpacote

Um subpacote é uma pasta com `__init__.py` dentro de um pacote. Crie a pasta e um `__init__.py`
vazio:

```bash
mkdir alchemy/transmutation
touch alchemy/transmutation/__init__.py
```

O `__init__.py` fica vazio: o subpacote não expõe nada na interface dele, e o programa da
transmutação chega à receita pelo caminho completo. Um `__init__.py` vazio é comum e não gera
aviso nenhum do flake8 nem do mypy. Deixá-lo vazio é escolha do tutorial; o enunciado só pede que
a pasta seja um pacote.

## recipes.py

Crie `alchemy/transmutation/recipes.py`:

```python title="alchemy/transmutation/recipes.py"
from alchemy.potions import strength_potion
from elements import create_fire

from ..elements import create_air


def lead_to_gold() -> str:
    return ("Recipe transmuting Lead to Gold: "
            f"brew '{create_air()}' and '{strength_potion()}'"
            f" mixed with '{create_fire()}'")
```

Os três imports, um de cada tipo:

| Import | Tipo | Chega a |
|---|---|---|
| `from alchemy.potions import strength_potion` | absoluto, para dentro do pacote | `alchemy/potions.py`, pelo caminho completo a partir da raiz |
| `from elements import create_fire` | absoluto, para fora do pacote | `elements.py`, da raiz; o único jeito de sair do pacote |
| `from ..elements import create_air` | relativo | `alchemy/elements.py`: um ponto seria o pacote `alchemy.transmutation`; dois pontos sobem um nível, para o `alchemy` |

O enunciado pede "pelo menos um" de cada. O tutorial usa os dois tipos para chegar a módulos de
dentro do mesmo pacote `alchemy` (a poção, em `alchemy.potions`, pelo absoluto; o ar, em
`alchemy.elements`, pelo relativo): o mesmo arquivo mostra os dois jeitos de alcançar um vizinho
do pacote, lado a lado. Pelo costume da [página das perguntas](../08-fechamento/03-perguntas-de-revisao.md#exercício-3-quando-usar-um-caminho-absoluto-e-quando-um-relativo),
os dois seriam relativos; o absoluto para a poção é uma exceção, escolha do tutorial, para o
arquivo mostrar as duas formas. O fogo só tem o caminho absoluto, e esse import sozinho já
cumpriria o "pelo menos um absoluto" do enunciado.

A frase segue o modelo do enunciado: o ar, depois a poção de força inteira, depois o fogo, cada um
entre aspas simples. Três pedaços de texto seguidos dentro dos parênteses formam uma frase só; o
primeiro não tem nada a substituir, e por isso não precisa do `f`.

## Rodar recipes.py direto não funciona

Um módulo de pacote é feito para ser importado. Rodado direto, a primeira pasta do `sys.path` vira
`alchemy/transmutation`, e o primeiro import já falha:

```bash
python3 alchemy/transmutation/recipes.py
```

```text
Traceback (most recent call last):
  File "/path/to/the-codex/alchemy/transmutation/recipes.py", line 1, in <module>
    from alchemy.potions import strength_potion
ModuleNotFoundError: No module named 'alchemy'
```

(`/path/to/the-codex` está no lugar do caminho da pasta do projeto.) Quem roda a receita é o
programa da [próxima página](./05-ft-transmutation-0.md), da raiz.
