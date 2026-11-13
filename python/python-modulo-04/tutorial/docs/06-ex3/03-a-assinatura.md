---
sidebar_position: 3
title: A assinatura
---

# A assinatura

A **assinatura** de uma função é a linha do `def`: o nome, os parâmetros com seus tipos e o tipo do
retorno. O enunciado descreve a de `secure_archive` em detalhe, e a avaliação a confere.

```python
def secure_archive(file_name: str, action: str = "read",
                   content: str = "") -> tuple[bool, str]:
```

Numa linha só, ela passaria dos 79 caracteres que o flake8 aceita (o aviso seria
`E501 line too long`). Dentro dos parênteses, a linha pode ser quebrada; a continuação fica alinhada
ao primeiro parâmetro.

## Os parâmetros

| Parâmetro | Tipo | Obrigatório? | Para quê |
|---|---|---|---|
| `file_name` | `str` | sim | o caminho do arquivo |
| `action` | `str` | não; vale `"read"` se ninguém informar | `"read"` para ler, `"write"` para escrever |
| `content` | `str` | não; vale `""` se ninguém informar | o texto a escrever |

O `= "read"` e o `= ""` são **valores padrão**: o valor que o parâmetro recebe quando quem chama não
o passa. Assim, `secure_archive("ancient_fragment.txt")` lê o arquivo, e
`secure_archive("new_archive.txt", "write", text)` grava `text` em `new_archive.txt`.

O enunciado deixa escolher entre `int` e `str` para a ação. A escolha aqui é `str`: a chamada
`secure_archive(name, "write", text)` diz o que faz, e `secure_archive(name, 1, text)` exigiria
saber o que o `1` significa.

## O retorno

`tuple[bool, str]` é o type hint de uma tupla de dois elementos: um `bool` e um `str`, nessa ordem.
Os quatro retornos possíveis:

| Situação | Retorno |
|---|---|
| leitura deu certo | `(True, <conteúdo do arquivo>)` |
| escrita deu certo | `(True, "Content successfully written to file")` |
| `open`, `read` ou `write` falhou | `(False, <mensagem da exceção>)` |
| ação desconhecida | `(False, "Unknown action '<ação>'")` |

A função não imprime nada: devolve o resultado, e quem chama decide o que fazer com ele.
