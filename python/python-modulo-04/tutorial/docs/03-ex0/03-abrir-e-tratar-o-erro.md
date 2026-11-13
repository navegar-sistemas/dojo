---
sidebar_position: 3
title: Abrir e tratar o erro
---

# Abrir e tratar o erro

`recover_archive` começa avisando qual arquivo vai acessar e tentando abri-lo. Se o `open()` falhar,
não há o que ler: o programa avisa o motivo e para.

```python
def recover_archive(file_name: str) -> None:
    print(f"Accessing file '{file_name}'")
    try:
        file: typing.IO[str] = open(file_name)
    except OSError as error:
        print(f"Error opening file '{file_name}': {error}")
        return
```

- `file: typing.IO[str]` anota a variável com o tipo de um arquivo aberto em modo texto ([open e o
  objeto arquivo](../02-arquivos/02-open-e-o-objeto-arquivo.md));
- `open(file_name)` abre para leitura, o modo padrão;
- `except OSError` captura todas as falhas que o sistema operacional devolve ao abrir: arquivo
  inexistente, sem permissão, pasta no lugar de arquivo ([Quando o open
  falha](../02-arquivos/05-quando-o-open-falha.md));
- `{error}` imprime a mensagem da exceção, como `[Errno 2] No such file or directory: 'foo'`;
- o `return` encerra a função ali. Ela não devolve nada (`-> None`), então o `return` sozinho só
  serve para parar.

O resultado, para um arquivo que não existe, é a saída do enunciado:

```text
Accessing file 'foo'
Error opening file 'foo': [Errno 2] No such file or directory: 'foo'
```

Não há linha `File 'foo' closed.`: o arquivo nunca foi aberto, então não há o que fechar.

## Por que o try envolve só o open

O `try` tem uma linha só. Assim, o `except` só pode estar capturando uma falha do `open()`, e a
mensagem "Error opening file" é sempre verdadeira. As falhas da leitura, que acontecem com o arquivo
já aberto, têm o seu próprio `try`, na [próxima página](./04-ler-e-fechar.md).
