---
sidebar_position: 2
title: Devolver o texto
---

# Devolver o texto

No exercício 0, o texto lido ia direto para a tela e era esquecido. Agora o `main` precisa dele para
transformá-lo, então `recover_archive` passa a devolvê-lo. E precisa haver um jeito de dizer "não
consegui ler", para o `main` não seguir em frente.

```python
def recover_archive(file_name: str) -> str | None:
    print(f"Accessing file '{file_name}'")
    try:
        file: typing.IO[str] = open(file_name)
    except OSError as error:
        print(f"Error opening file '{file_name}': {error}")
        return None
    content: str | None = None
    try:
        content = file.read()
        display(content)
    except (OSError, UnicodeDecodeError) as error:
        print(f"Error reading file '{file_name}': {error}")
    finally:
        file.close()
        print(f"File '{file_name}' closed.")
    return content
```

## None

`None` é o valor do Python para "nada", "nenhum valor". A função devolve o texto quando a leitura dá
certo e `None` quando dá errado.

O type hint `str | None` diz exatamente isso: "um `str` **ou** `None`". A barra `|` entre tipos foi
criada no Python 3.10, a versão mínima do enunciado.

## O que mudou

- o `return` da falha do `open()` agora devolve `None` explicitamente;
- `content` começa valendo `None`. Se o `read()` der certo, ganha o texto; se falhar, continua
  `None`;
- `content: str | None = None` anota a variável com o mesmo tipo do retorno, e quem lê sabe de saída
  que ela pode guardar as duas coisas;
- a leitura e o `display` ficam em duas linhas, porque o texto precisa ficar guardado em `content`;
- o `return content` vem depois do `try`. O `finally` roda antes, então o arquivo já está fechado
  quando a função devolve o texto.

A saída na tela é a mesma do exercício 0.
