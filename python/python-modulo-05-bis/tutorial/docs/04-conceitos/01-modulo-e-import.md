---
sidebar_position: 1
title: Módulo e import
---

# Módulo e import

Os exercícios 2 a 4 espalham o código por vários arquivos, e um arquivo usa as funções de outro.
O `import` é o que liga os arquivos. Esta parte explica, com experimentos pequenos na pasta
`experimentos`, como ele encontra e carrega o código; os exercícios aplicam cada ideia.

## O módulo

Todo arquivo `.py` é um **módulo**, e o nome do módulo é o nome do arquivo sem o `.py`. Crie
`experimentos/sigil.py`:

```python title="experimentos/sigil.py"
print(f"loading {__name__}")

WORD = "lumen"


def shout(text: str) -> str:
    return text.upper() + "!"
```

O `print` da primeira linha mostra quando o código do módulo roda, e com qual `__name__`.

## import e from ... import

Crie `experimentos/use_import.py`, que usa o módulo `sigil` dos dois jeitos:

```python title="experimentos/use_import.py"
import sigil
from sigil import shout

print(sigil.WORD)
print(shout(sigil.WORD))
print(shout is sigil.shout)
print(__name__)
```

```bash
python3 experimentos/use_import.py
```

```text
loading sigil
lumen
LUMEN!
True
__main__
```

Linha por linha:

1. `import sigil` procura o arquivo `sigil.py`, roda o código dele de cima a baixo e guarda o
   resultado num **objeto módulo**. O `print` do `sigil.py` roda nessa hora, com `__name__` valendo
   `"sigil"`. O nome `sigil` passa a apontar para o objeto módulo, e tudo o que o arquivo definiu
   (variáveis, funções) vira um **atributo** dele, lido com ponto: `sigil.WORD`, `sigil.shout`;
2. `from sigil import shout` não roda o `sigil.py` de novo: **um módulo roda uma vez só** por
   programa, e o segundo import reaproveita o objeto já carregado. Por isso `loading sigil`
   aparece uma única vez. Essa forma traz só o nome `shout` para o arquivo atual, sem o prefixo;
3. `shout is sigil.shout` é `True`: os dois nomes apontam para a mesma função (`is` pergunta se
   dois nomes são o mesmo objeto);
4. no arquivo rodado com `python3`, `__name__` vale `"__main__"`.

| Forma | O que entra no arquivo | Uso |
|---|---|---|
| `import sigil` | o nome `sigil`, o módulo inteiro | `sigil.shout("x")` |
| `from sigil import shout` | só o nome `shout` | `shout("x")` |

O enunciado chama a primeira de "estrutura `import ...`" e a segunda de "estrutura
`from ... import ...`", e cada exercício pede uma delas.

## O módulo rodado como programa

O mesmo arquivo pode ser rodado direto:

```bash
python3 experimentos/sigil.py
```

```text
loading __main__
```

Agora `__name__` vale `"__main__"`, e é isso que o `if __name__ == "__main__":` dos programas
testa ([Pré-requisitos](../00-introducao/03-pre-requisitos.md#o-programa-que-roda-e-o-programa-que-é-importado)):
o código dentro dele só roda quando o arquivo é o programa, e não quando é importado.

## A pasta \_\_pycache\_\_

Depois do primeiro import, aparece uma pasta `__pycache__` em `experimentos`. Nela o Python guarda
o módulo já traduzido para o formato que ele executa (arquivos `.pyc`), para carregar mais rápido
da próxima vez. Ela é refeita sozinha quando o `.py` muda, pode ser apagada à vontade e não faz
parte da entrega.
