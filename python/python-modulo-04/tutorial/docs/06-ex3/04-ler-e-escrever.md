---
sidebar_position: 4
title: Ler e escrever
---

# Ler e escrever

O corpo de `secure_archive` escolhe a operação pela ação, faz o trabalho dentro de um `with` e
transforma qualquer falha numa tupla com `False`.

```python
def secure_archive(file_name: str, action: str = "read",
                   content: str = "") -> tuple[bool, str]:
    try:
        if action == "read":
            with open(file_name) as file:
                return (True, file.read())
        if action == "write":
            with open(file_name, "w") as file:
                file.write(content)
            return (True, "Content successfully written to file")
    except (OSError, UnicodeDecodeError) as error:
        return (False, str(error))
    return (False, f"Unknown action '{action}'")
```

## Ler

`return (True, file.read())` lê o arquivo e devolve a tupla de dentro do `with`. O `with` fecha o
arquivo antes de a função devolver o valor ([O with](./02-o-with.md)).

## Escrever

O modo `"w"` cria o arquivo ou substitui o conteúdo dele ([Gravar o
arquivo](../04-ex1/05-gravar-o-arquivo.md)). O `return` fica **depois** do bloco do `with`: a
mensagem de sucesso só é devolvida depois que o `close()` despejou o buffer no disco sem erro. Se o
`close()` falhar, por disco cheio por exemplo, o `OSError` sobe do `with` e cai no `except`, e a
função devolve `False`.

## As falhas

Um único `try` envolve as duas operações. O `except` captura:

- `OSError`: arquivo inexistente, sem permissão, pasta no lugar de arquivo, disco cheio, tanto ao
  abrir quanto ao ler, escrever ou fechar;
- `UnicodeDecodeError`: um arquivo que não é texto, na leitura.

`str(error)` transforma a exceção no texto da mensagem, o mesmo que o `{error}` das f-strings
mostrava: `[Errno 2] No such file or directory: '/not/existing/file'`. `str()` é o construtor do
tipo `str`, permitido pela regra geral dos tipos.

## A ação desconhecida

Se `action` não é `"read"` nem `"write"`, nenhum `if` roda, o `try` termina sem `return`, e a última
linha devolve `False` com a ação recebida: `secure_archive("ancient_fragment.txt", "delete")`
devolve `(False, "Unknown action 'delete'")`.
