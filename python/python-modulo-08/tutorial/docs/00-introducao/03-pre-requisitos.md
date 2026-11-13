---
sidebar_position: 3
title: Pré-requisitos
---

# Pré-requisitos

Os exercícios usam o básico de Python sem explicação longa:

| Assunto | Exemplo |
|---|---|
| variáveis, `int`, `float`, `str` e `bool` | `count = 3`, `name = "neo"`, `ready = True` |
| `if`, `elif`, `else`, `not`, `and`, `or` | `if not value:` |
| laço `for` sobre uma lista | `for name in names:` |
| funções com `def` e `return` | `def double(n: int) -> int: return n * 2` |
| f-strings: texto com valores dentro de `{}` | `f"total {count}"` vira `total 3` |
| listas, tuplas e dicionários | `["a", "b"]`, `("pandas", "Data")`, `{"MODE": "development"}` |
| desempacotar uma tupla no `for` | `for name, role in [("numpy", "math")]:` |
| `in` para perguntar se algo está numa lista ou num texto | `"localhost" in url` |

Um valor "vazio" conta como falso num `if`: `""` (texto vazio), `[]` (lista vazia), `0` e
`None` (o valor que quer dizer "nada"). Por isso `if not value:` é verdadeiro tanto para `None`
quanto para `""`.

## Módulos e import

Um **módulo** é um arquivo de código Python que outro programa usa com `import`. Os que vêm com o
Python (`os`, `sys`, `site`, `importlib`) formam a **biblioteca padrão**. Os outros, como numpy e
pandas, precisam ser instalados antes ([Pacotes e o pip](../02-conceitos/01-pacotes-e-o-pip.md)).

```python
import sys
from os import path
```

A primeira linha traz o módulo inteiro, usado como `sys.argv`; a segunda traz um nome de dentro do
módulo, usado direto como `path`.

## Exceções, em resumo

Quando algo dá errado, o Python cria uma **exceção**: um objeto que descreve o erro, com um tipo
(como `ValueError` ou `ImportError`) e uma mensagem. Se nenhum `except` a captura, o programa para
e imprime um relatório de erro chamado **traceback**. Um bloco `try` captura a exceção, e o bloco
`else` roda só quando o `try` terminou sem erro:

```python
try:
    number = int("42")
except ValueError:
    print("not a number")
else:
    print(f"got {number}")
```

```text
got 42
```

Com `int("abc")`, o `except` rodaria e imprimiria `not a number`. `except ValueError as error`
guarda a exceção na variável `error`, e `{error}` imprime a mensagem dela.

## O código de saída

Todo programa, ao terminar, devolve ao terminal um número, o **código de saída**: `0` quer dizer
que deu tudo certo, e qualquer outro número quer dizer erro. Em Python, `sys.exit(n)` termina o
programa na hora, com o código `n`. No terminal, `$?` guarda o código do último comando:

```bash
python3 -c 'import sys; sys.exit(3)'
echo $?
```

```text
3
```

`python3 -c '...'` roda o código entre aspas sem precisar de um arquivo, e `echo` imprime o valor.
Os programas do projeto terminam com `sys.exit(1)` quando não podem continuar (uma biblioteca que
falta, uma configuração ausente), e assim outro programa ou script consegue saber que algo falhou.

## O terminal

O **terminal** é a janela onde se digitam comandos. É preciso saber andar entre pastas com `cd`
(e `cd ..` para voltar à pasta de cima), listar arquivos com `ls`, criar pastas com `mkdir`,
copiar arquivos com `cp` e mostrar um arquivo com `cat`; os outros comandos são explicados onde
aparecem. Os comandos funcionam no terminal do Linux e do macOS, nos dois *shells* (o programa que
interpreta o que se digita) mais comuns, o bash e o zsh.
