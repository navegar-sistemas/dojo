---
sidebar_position: 4
title: Absoluto e relativo
---

# Absoluto e relativo

Um módulo de dentro de um pacote pode importar outro módulo do mesmo pacote de dois jeitos, e o
exercício 3 pede os dois no mesmo arquivo.

- **Import absoluto:** o caminho completo, a partir de uma pasta do `sys.path`, com os nomes
  separados por ponto. `from cabinet.shelf import take_salt` quer dizer "o módulo `shelf` do
  pacote `cabinet`", e funciona igual em qualquer arquivo.
- **Import relativo:** o caminho a partir do pacote onde está o arquivo que importa, começando com
  pontos. Um ponto é o próprio pacote; dois pontos, o pacote de cima; três, o de cima deste.
  `from .shelf import take_mercury`, escrito dentro do pacote `cabinet`, quer dizer "o módulo
  `shelf` do meu pacote".

## Os dois no mesmo arquivo

Crie `experimentos/cabinet/potion.py`:

```python title="experimentos/cabinet/potion.py"
from cabinet.shelf import take_salt

from .shelf import take_mercury


def mix() -> str:
    return f"{take_salt()} + {take_mercury()}"
```

E um programa que o usa, `experimentos/use_potion.py`:

```python title="experimentos/use_potion.py"
from cabinet.potion import mix

print(mix())
```

```bash
python3 experimentos/use_potion.py
```

```text
salt + mercury
```

Os dois imports chegaram ao mesmo `shelf.py`. A linha em branco entre eles separa os grupos de
`import`, como na [página do python-dotenv](../03-ex1/03-o-arquivo-env-e-o-python-dotenv.md#load_dotenv):
os absolutos primeiro, os relativos depois.

## O relativo só existe dentro de um pacote

O ponto do import relativo é contado a partir do pacote do arquivo, que o Python guarda quando
importa o arquivo como parte de um pacote. Um arquivo rodado direto com `python3` não é parte de
pacote nenhum, e um import relativo nele não tem de onde partir:

```bash
python3 -c 'from .shelf import take_salt'
```

```text
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    from .shelf import take_salt
ImportError: attempted relative import with no known parent package
```

("tentativa de import relativo sem pacote pai conhecido"; do Python 3.10 ao 3.12, sem a linha do
código.)
Os pontos também não sobem além do pacote mais alto: dentro de `cabinet`, que não está dentro de
outro pacote, `from ..sigil import WORD` falha com `ImportError: attempted relative import beyond
top-level package`.

E um módulo de pacote rodado direto também perde os imports absolutos, porque a primeira pasta do
`sys.path` vira a pasta dele, e não a de cima:

```bash
python3 experimentos/cabinet/potion.py
```

```text
Traceback (most recent call last):
  File "/path/to/the-codex/experimentos/cabinet/potion.py", line 1, in <module>
    from cabinet.shelf import take_salt
ModuleNotFoundError: No module named 'cabinet'
```

A pasta `experimentos/cabinet` não tem nenhum `cabinet` dentro. Módulos de pacote são feitos para
serem importados; quem roda são os programas de fora do pacote, como `use_potion.py` aqui e os
`ft_*.py` no projeto.

## Qual usar

| | Absoluto | Relativo |
|---|---|---|
| exemplo | `from cabinet.shelf import take_salt` | `from .shelf import take_mercury` |
| lido como | "o `shelf` do pacote `cabinet`" | "o `shelf` do meu pacote" |
| funciona em | qualquer arquivo: programas, módulos, outros pacotes | só em módulos de dentro de um pacote |
| alcança | qualquer módulo encontrável pelo `sys.path`, dentro ou fora do pacote | só módulos do mesmo pacote, ou dos pacotes de cima até o mais alto |
| se o pacote mudar de nome | precisa ser reescrito | continua igual |

O relativo deixa claro que o módulo é vizinho, e sobrevive a uma troca de nome do pacote. O
absoluto é o único que alcança módulos de fora do pacote, e diz o caminho inteiro a quem lê. A
[página das perguntas](../08-fechamento/03-perguntas-de-revisao.md) volta a essa escolha.
