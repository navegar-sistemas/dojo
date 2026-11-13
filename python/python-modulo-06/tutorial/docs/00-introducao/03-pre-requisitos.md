---
sidebar_position: 3
title: Pré-requisitos
---

# Pré-requisitos

O projeto não tem classes nem algoritmos: as funções só montam textos. O que ele usa de Python é
o básico:

| Assunto | Exemplo |
|---|---|
| funções com `def` e `return`, com type hints | `def create_fire() -> str: return "Fire element created"` |
| f-strings: texto com valores dentro de `{}` | `f"Testing: {create_fire()}"` vira `Testing: Fire element created` |
| listas e o laço `for` | `for item in ["earth", "air"]:` |
| `if` e `return` antecipado | `if allowed in text: return "VALID"` |
| `in` entre dois textos: o primeiro aparece dentro do segundo? | `"fire" in "Earth, wind and fire"` dá `True` |
| `lower()`: o texto em letras minúsculas | `"EARTH".lower()` dá `"earth"` |
| `endswith()`: o texto termina com outro? | `"water - VALID".endswith("VALID")` dá `True` |

Um arquivo com esses itens, para conferir:

```python
def greet(name: str) -> str:
    return f"Hello, {name}"


print(greet("Ana"))
print("fire" in "Earth, wind and fire")
print("EARTH".lower())
print("water - VALID".endswith("VALID"))
print("Testing: ", end="")
print("done")
```

```text
Hello, Ana
True
earth
True
Testing: done
```

As duas últimas linhas mostram o parâmetro `end` do `print`. Normalmente o `print` termina a
linha depois do texto; com `end=""`, ele não termina, e o próximo texto impresso continua na
mesma linha. A Parte I usa isso para pôr uma mensagem de erro logo depois de um texto.

## Exceções e o traceback

Quando algo dá errado, o Python cria uma **exceção**: um objeto que descreve o erro, com um
**tipo** (como `ValueError`) e uma **mensagem**. Se nada a captura, o programa para e imprime um
relatório chamado **traceback**. O comando abaixo roda uma linha de Python direto do terminal: o
`-c` faz o `python3` executar o texto entre aspas em vez de um arquivo.

```bash
python3 -c 'print(int("fire"))'
```

```text
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    print(int("fire"))
          ~~~^^^^^^^^
ValueError: invalid literal for int() with base 10: 'fire'
```

Como se lê:

- `Traceback (most recent call last)`: "rastro, com a chamada mais recente por último";
- cada par de linhas seguinte é um ponto do caminho até o erro: o arquivo (aqui `<string>`, o
  texto do `-c`), o número da linha, o lugar (`<module>` quer dizer "no corpo do arquivo, fora de
  qualquer função") e a linha de código;
- os sinais `~` e `^` embaixo do código marcam o trecho exato que falhou; o `^` aponta a parte
  principal;
- a última linha é o tipo da exceção e a mensagem: "literal inválido para `int()` na base 10:
  `'fire'`".

O Python 3.10 imprime menos: sem as linhas de marcação, e, para código vindo do `-c`, sem a linha
de código. O tipo e a mensagem são os mesmos. Este projeto tem dois tracebacks esperados, e cada
um tem uma página que o lê linha a linha.

O comando terminou com **código de saída** `1`. Todo programa devolve um número ao terminar: `0`
quer dizer que deu tudo certo, e outro número, que deu erro. Uma exceção que ninguém captura,
como esta, termina o programa com o código `1`.

## O terminal

O **terminal** é a janela onde se digitam comandos. É preciso saber andar entre pastas com `cd`,
listar arquivos com `ls` e criar pastas com `mkdir`; os outros comandos são explicados onde
aparecem. Os comandos funcionam no terminal do Linux e do macOS.
