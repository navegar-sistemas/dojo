---
sidebar_position: 10
title: O repositório completo
---

# O repositório completo

As mensagens do `MazeConfig` dizem o que está errado, mas não em qual arquivo: ele recebe só um
dicionário. Quem roda o programa com vários arquivos de configuração precisa saber qual deles
tem o erro. Esta página acrescenta o nome do arquivo às mensagens e mostra o
`FileConfigRepository` completo.

## O nome do arquivo na frente

```python
try:
    return MazeConfig.create(raw)
except ConfigError as error:
    raise ConfigError(f"{path}: {error}") from None
```

O `MazeConfig` não sabe de arquivo nenhum. O repositório sabe, e acrescenta o caminho na frente:
captura o `ConfigError`, monta um novo com `path: ` antes do texto do original e o levanta no
lugar dele.

```text
WIDTH must be an integer, got 'abc'               ← mensagem do MazeConfig
config.txt: WIDTH must be an integer, got 'abc'   ← o que sai do load
```

Assim, toda mensagem sobre a configuração cita o arquivo: as de leitura
([página 8](./10-as-falhas-da-leitura.md)), as de sintaxe, com o número da linha
([página 9](./06-linha-a-linha.md)), e as de regra.

### Por que a mensagem de sintaxe não sai com o caminho duas vezes

O erro de sintaxe (`config.txt, line 2: expected KEY=VALUE, ...`) já é montado com o caminho,
dentro do laço que lê as linhas. Esse laço fica **fora** deste último `try`, que só envolve a
chamada `MazeConfig.create(raw)`. Por isso o `except ConfigError` daqui só pega os erros de
regra, que ainda não têm o caminho, e nunca vê o de sintaxe.

## O arquivo completo

```python title="amazeing/repositories/config_repository.py"
"""Reading of the configuration file."""

from amazeing.domain.value_objects.maze_config import MazeConfig
from amazeing.errors import ConfigError


class FileConfigRepository:
    """Load a MazeConfig from a KEY=VALUE text file."""

    def load(self, path: str) -> MazeConfig:
        """Read the file, split it into keys and values and validate them.

        Args:
            path: Path of the configuration file, as typed by the user.

        Returns:
            The validated configuration.

        Raises:
            ConfigError: The file is missing, unreadable, not UTF-8, has a
                line outside KEY=VALUE or breaks a rule; the message names
                the file.
        """
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
        raw: dict[str, str] = {}
        for number, text in enumerate(lines, 1):
            line = text.strip()
            if not line or line.startswith("#"):
                continue
            key, sep, value = line.partition("=")
            if not sep or not key.strip():
                raise ConfigError(f"{path}, line {number}: expected "
                                  f"KEY=VALUE, got '{line}'")
            raw[key.strip().upper()] = value.strip()
        try:
            return MazeConfig.create(raw)
        except ConfigError as error:
            raise ConfigError(f"{path}: {error}") from None
```

O `load` não escreve o `Error: ` da frente: isso é trabalho do `main`
([parte 14](../14-menu-e-main/05-a-barreira-de-erros.md)), o lugar que imprime todo erro que
encerra o programa.

## Experimente

Os comandos, na raiz do projeto, criam alguns arquivos de configuração, passam cada um pelo
`load` e apagam os arquivos no fim:

```bash
printf '# top\n\n  width = 20  \nHeight=15\r\nENTRY=0,0\nEXIT=19,14\nOUTPUT_FILE=a=b.txt\nperfect=false\nCOLOR=red\nWIDTH=30' > solto_config.txt
printf 'WIDTH=20\nHEIGHT 15\n' > sintaxe_config.txt
printf 'WIDTH=20\nHEIGHT=15\nENTRY=0,0\nEXIT=19,14\nOUTPUT_FILE=maze.txt\nPERFECT=yes\n' > valor_config.txt
printf '# caf\xe9\n' > latin1_config.txt
mkdir pasta_config
.venv/bin/python -c '
from amazeing.errors import ConfigError
from amazeing.repositories.config_repository import FileConfigRepository

for path in ["solto_config.txt", "sintaxe_config.txt", "valor_config.txt",
             "nao_existe.txt", "latin1_config.txt", "pasta_config"]:
    try:
        print(FileConfigRepository().load(path))
    except ConfigError as error:
        print(error)
'
rm solto_config.txt sintaxe_config.txt valor_config.txt latin1_config.txt
rmdir pasta_config
```

```text
MazeConfig(width=30, height=15, entry=(0, 0), exit=(19, 14), output_file='a=b.txt', perfect=False, seed=None)
sintaxe_config.txt, line 2: expected KEY=VALUE, got 'HEIGHT 15'
valor_config.txt: PERFECT must be True or False, got 'yes'
configuration file not found: nao_existe.txt
configuration file is not valid UTF-8: latin1_config.txt
cannot read configuration file pasta_config: Is a directory
```

O `solto_config.txt` tem comentário, linha vazia, espaços em volta do `=`, chaves em minúsculas,
um fim de linha do Windows (`\r\n`), um `=` dentro do valor, uma chave desconhecida, `WIDTH`
repetida e nenhuma quebra de linha no fim. Tudo é aceito, e a largura é a da última linha: 30.
O `latin1_config.txt` tem o byte `e9`, o `é` do Latin-1, que não forma UTF-8. O `rmdir` apaga a
pasta vazia `pasta_config`.
