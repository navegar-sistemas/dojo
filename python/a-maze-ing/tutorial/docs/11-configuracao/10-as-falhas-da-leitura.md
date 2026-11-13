---
sidebar_position: 8
title: As falhas da leitura
---

# As falhas da leitura

Abrir e ler o arquivo de configuração ([página anterior](./05-abrindo-o-arquivo.md)) pode dar
errado: o arquivo pode não existir, ser uma pasta, estar sem permissão de leitura ou não estar
em UTF-8. O enunciado cita "arquivo não encontrado" entre os erros que precisam virar uma
mensagem clara. Esta página transforma cada uma dessas falhas numa linha que o usuário entende.

## As falhas do sistema viram `ConfigError`

O `open` e o `readlines` levantam exceções do próprio Python quando algo dá errado. O `load` as
captura e levanta um `ConfigError`, a exceção de configuração da
[parte 10](../10-utilitarios/05-a-hierarquia-app-error.md):

```python
try:
    # utf-8-sig drops a leading BOM; text mode turns \r\n and \r
    # into line ends.
    with open(path, encoding="utf-8-sig") as file:
        lines = file.readlines()
except FileNotFoundError:
    raise ConfigError(
        f"configuration file not found: {path}") from None
except UnicodeDecodeError:
    raise ConfigError(
        f"configuration file is not valid UTF-8: {path}") from None
except OSError as error:
    raise ConfigError(f"cannot read configuration file {path}: "
                      f"{error.strerror}") from None
```

| Exceção | Quando | Mensagem |
|---|---|---|
| `FileNotFoundError` | o arquivo não existe | `configuration file not found: nao_existe.txt` |
| `UnicodeDecodeError` | os bytes não formam UTF-8 (um arquivo salvo em Latin-1, por exemplo) | `configuration file is not valid UTF-8: latin1_config.txt` |
| `OSError` | qualquer outra falha do sistema: é uma pasta, falta permissão... | `cannot read configuration file pasta_config: Is a directory` |

O `from None` no fim de cada `raise` descarta a exceção original, que a nova mensagem já resume
([página 2](./02-convertendo-um-valor.md)).

### Por que converter

O `main`, a função principal do `a_maze_ing.py`
([parte 14](../14-menu-e-main/05-a-barreira-de-erros.md)), captura `ConfigError` e imprime
`Error: <mensagem>` numa linha. Ele também tem um `except` genérico, o último, que existe para
bugs e imprime `Error: unexpected: ...`. Um `OSError` que escapasse daqui cairia nesse `except`
genérico, como se fosse um defeito do programa. Converter aqui, onde o arquivo é aberto,
garante que todo problema causado pelo usuário saia como uma linha clara.

O `path` vai na mensagem exatamente como o usuário digitou (`config.txt`, `../outro.cfg`), para
ele reconhecer de que arquivo se fala.

### O `try` em volta do `with` inteiro

O `UnicodeDecodeError` não acontece no `open`, e sim no `readlines()`, quando o Python tenta
transformar os bytes em texto. Por isso o `try` cobre a leitura também, e não só a abertura.

### A ordem dos `except`

O Python testa os `except` de cima para baixo e usa o primeiro que combina. `FileNotFoundError`
é uma subclasse ("filha") de `OSError` (todo arquivo não encontrado é uma falha do sistema). Se o
`except OSError` viesse antes, ele capturaria o arquivo inexistente, e a mensagem específica
nunca apareceria. Por isso a ordem vai do mais específico para o mais geral.

`UnicodeDecodeError` não é filha de `OSError` (é um tipo de `ValueError`), então a posição dela
não muda o resultado; fica antes do `OSError` só para manter a leitura do específico para o
geral.

### `strerror` em vez de `str(error)`

```text
str(error)      → [Errno 21] Is a directory: 'pasta_config'
error.strerror  → Is a directory
```

`str(error)` traz o número interno do erro e repete o caminho, que a mensagem já cita.
`strerror` é só a frase do sistema operacional.

O resto do `load`, que separa as linhas em chave e valor, está na
[próxima página](./06-linha-a-linha.md), e o Experimente da
[página 10](./09-o-repositorio-completo.md#experimente) provoca cada uma destas mensagens.
