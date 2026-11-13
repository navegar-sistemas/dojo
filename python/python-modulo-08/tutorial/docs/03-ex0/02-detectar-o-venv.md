---
sidebar_position: 2
title: Detectar o venv
---

# Detectar o venv

A pergunta do programa é "estou dentro de um ambiente virtual?". A resposta está em `sys`: dentro
de um venv, `sys.prefix` (a pasta do ambiente em uso) é diferente de `sys.base_prefix` (a pasta do
Python global de onde o ambiente veio); fora, os dois são iguais
([O Python sabe onde está](../02-conceitos/02-o-ambiente-virtual-por-dentro.md#o-python-sabe-onde-está)).

Crie o arquivo `ex0/construct.py` e escreva nele o começo do programa:

```python
import os
import site
import sys


def inside_virtual_env() -> bool:
    return sys.prefix != sys.base_prefix
```

- os três `import` são os três módulos autorizados: `sys` para a detecção e o caminho do Python,
  `os` para tirar o nome do ambiente do caminho dele ([Dentro do venv](./04-dentro-do-venv.md)),
  `site` para o lugar dos pacotes ([Onde ficam os pacotes](./05-onde-ficam-os-pacotes.md));
- `inside_virtual_env` devolve `True` dentro de um venv e `False` fora. O nome diz o que ela
  responde, e o resto do programa só faz `if inside_virtual_env():`.

As próximas páginas acrescentam, nesta ordem, as funções `show_outside`, `show_inside`,
`show_package_path` e `main`, sempre no fim do arquivo.

## Por que não a variável VIRTUAL_ENV

O `activate` cria a variável de ambiente `VIRTUAL_ENV`
([Ativar e desativar](../02-conceitos/02-o-ambiente-virtual-por-dentro.md#ativar-e-desativar)),
e seria possível perguntar por ela com `os.getenv`. Mas ela diz se **o terminal** ativou um
ambiente, e não se **o Python que está rodando** é de um ambiente:

- `matrix_env/bin/python construct.py`, sem ativar nada, roda dentro do venv, e a variável não
  existe;
- com um venv ativado, um Python global chamado pelo caminho completo roda fora do venv, e a
  variável existe.

`sys.prefix` e `sys.base_prefix` vêm do próprio Python em execução e acertam nos dois casos. A
página [Rodar e conferir](./07-rodar-e-conferir.md) roda o primeiro.
