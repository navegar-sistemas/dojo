---
sidebar_position: 5
title: Gravar o arquivo
---

# Gravar o arquivo

A gravação abre o arquivo para escrita, escreve o texto e fecha. Cada um desses passos pode falhar,
e o `main` precisa saber se o texto foi gravado ou não.

```python
def save_archive(file_name: str, content: str) -> bool:
    try:
        file: typing.IO[str] = open(file_name, "w")
    except (OSError, ValueError) as error:
        print(f"Error opening file '{file_name}': {error}")
        return False
    try:
        try:
            file.write(content)
        finally:
            file.close()
    except OSError as error:
        print(f"Error writing file '{file_name}': {error}")
        return False
    return True
```

A função devolve um `bool`: `True` quando gravou, `False` quando não gravou. Quem avisa o resultado
é o `main`.

## O modo "w"

O segundo argumento do `open()` é o modo de abertura. `"w"` (*write*) abre para escrita:

- se o arquivo não existe, ele é **criado**;
- se já existe, o conteúdo antigo é **apagado** na hora em que o arquivo é aberto, e o arquivo passa
  a ter só o que for escrito agora.

É exatamente o que o enunciado pede: "crie o arquivo ou substitua-o se ele já existir". Para
escrever, também é preciso permissão: abrir para escrita um arquivo protegido, ou criar um arquivo
numa pasta protegida, falha com `PermissionError`, um `OSError` que o primeiro `except` captura.

O nome vem do que a pessoa digitou, e pode trazer o caractere nulo, o de código 0, que nenhum nome
de arquivo admite. Esse nome nem chega ao sistema: o `open()` o recusa com
`ValueError: embedded null byte` ("byte nulo no meio do nome"), e `ValueError` não é um `OSError`.
Por isso o primeiro `except` captura a tupla `(OSError, ValueError)`. [Rodar e
conferir](./08-rodar-e-conferir.md#as-falhas) mostra esse caso.

## write

`file.write(content)` escreve o texto no arquivo, sem acrescentar nada: diferente do `print`, não
põe quebra de linha no fim. Os `\n` gravados são os que já estão no texto.

## Um try dentro do outro

O texto escrito vai primeiro para o buffer ([close e o
recurso](../02-arquivos/04-close-e-o-recurso.md)). Um texto pequeno como o do fragmento só chega ao
disco no `close()`, e é nesse momento que uma falha de disco cheio aparece. (Um texto maior que o
buffer começa a ir para o disco já no `write()`, que também pode falhar. O tamanho do buffer muda
com a versão do Python: cerca de 8 mil caracteres até o 3.13 e, a partir do 3.14, entre 130 mil e
140 mil, conforme o sistema.)
Por isso, o `close()` também precisa de proteção:

- o `try` de dentro, com `finally`, garante que o arquivo é fechado mesmo que o `write()` falhe;
- o `try` de fora captura um `OSError` lançado pelo `write()` **ou** pelo `close()`. Uma exceção
  lançada dentro de um `finally` sobe como qualquer outra, e o `except` de fora a recebe.

A mensagem `Error writing file` é escolha do projeto, no molde do `Error opening file`.

Com um único `try`, o `close()` ficaria no `finally` do mesmo `try` que tem o `except`:

```python
try:
    file.write(content)
except OSError as error:
    print(f"Error writing file '{file_name}': {error}")
finally:
    file.close()
```

O `except` de um `try` só captura o que acontece no bloco do `try`. Uma exceção lançada pelo
`close()`, dentro do `finally`, escaparia dele e travaria o programa. No Linux, o arquivo especial
`/dev/full` simula um disco cheio: abre normalmente e recusa toda escrita. Ele aparece em [Rodar e
conferir](./08-rodar-e-conferir.md).
