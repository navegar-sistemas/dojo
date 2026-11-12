---
sidebar_position: 5
title: Abrindo o arquivo de configuração
---

# Abrindo o arquivo de configuração

O `FileConfigRepository` (`amazeing/repositories/config_repository.py`) tem um único método,
`load(path)`, que recebe o caminho digitado na linha de comando e devolve um `MazeConfig`. Ele
trabalha em três passos:

1. abrir o arquivo e ler as linhas;
2. separar cada linha em chave e valor;
3. entregar o dicionário ao `MazeConfig.create`.

O primeiro é o que pode falhar por motivos do sistema: arquivo que não existe, pasta no lugar de
arquivo, falta de permissão, bytes que não são texto.

## Abrir e ler

```python
with open(path, encoding="utf-8-sig") as file:
    lines = file.readlines()
```

- `with` fecha o arquivo ao sair do bloco, mesmo se der erro no meio.
- `encoding` sempre explícito: sem ele, o Python usa a codificação padrão da máquina, que muda de
  um sistema para outro.
- `readlines()` devolve a lista das linhas, cada uma ainda com o seu `\n` no fim.
- O modo texto do Python reconhece `\n`, `\r\n` (Windows) e `\r` como fim de linha, e entrega
  todas como `\n`. Um config salvo no Windows funciona sem tratamento nenhum.

### `utf-8-sig` e o BOM

Alguns editores, como o Bloco de Notas do Windows, gravam no início do arquivo um caractere
invisível, o **BOM** (*byte order mark*, `U+FEFF`). Lido com `utf-8` puro, ele vira parte da
primeira linha:

```bash
printf '\xef\xbb\xbf# Width\nWIDTH=20\n' > bom.txt
.venv/bin/python -c '
with open("bom.txt", encoding="utf-8") as f:
    print(f.readlines())
with open("bom.txt", encoding="utf-8-sig") as f:
    print(f.readlines())
'
```

```text
['\ufeff# Width\n', 'WIDTH=20\n']
['# Width\n', 'WIDTH=20\n']
```

Com `utf-8`, a primeira linha começa com `\ufeff` e não com `#`: deixa de ser comentário e vira
erro de sintaxe. Se a primeira linha fosse `WIDTH=20`, a chave seria `\ufeffWIDTH`, desconhecida,
e o programa reclamaria que falta `WIDTH`, com a linha `WIDTH=20` bem à vista. O `strip()` não
ajuda: para o Python, o BOM não é espaço.

`utf-8-sig` é o UTF-8 que descarta um BOM no início, se houver. Sem BOM, lê igual ao `utf-8`.

## Os erros do sistema viram `ConfigError`

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
| `UnicodeDecodeError` | bytes que não formam UTF-8 (um arquivo em Latin-1, por exemplo) | `configuration file is not valid UTF-8: latin1.txt` |
| `OSError` | qualquer outra falha do sistema: é uma pasta, falta permissão... | `cannot read configuration file pasta: Is a directory` |

### O `try` em volta do `with` inteiro

O `UnicodeDecodeError` não acontece no `open`, e sim no `readlines()`, quando o Python tenta
decodificar os bytes. Por isso o `try` cobre a leitura também, não só a abertura.

### A ordem dos `except`

O Python testa os `except` de cima para baixo e usa o primeiro que serve. `FileNotFoundError` é
uma subclasse de `OSError`: se `OSError` viesse antes, ele capturaria o arquivo inexistente e a
mensagem específica nunca apareceria. Do mais específico para o mais geral.

`UnicodeDecodeError` não é `OSError` (é um `ValueError`); a posição dele não muda nada, e fica
antes do `OSError` só para a leitura seguir do caso mais específico para o mais geral.

### `strerror` em vez de `str(error)`

```text
str(error)      → [Errno 21] Is a directory: 'pasta'
error.strerror  → Is a directory
```

`str(error)` traz o número do erro e repete o caminho, que a mensagem já cita. `strerror` é só a
frase do sistema operacional.

### Por que converter

O `main` captura `AppError` e `MazeError` e imprime `Error: <mensagem>`. Um `OSError` que
escapasse cairia no `except Exception` de último recurso, como "erro inesperado". Converter aqui,
na única camada que mexe em arquivo, mantém a promessa: todo problema do usuário sai como uma
linha clara. O `from None` descarta a exceção original, cujo conteúdo a nova mensagem já
resume.

O `path` vai na mensagem exatamente como o usuário digitou (`config.txt`, `../outro.cfg`), para
ele reconhecer o arquivo de que se fala.
