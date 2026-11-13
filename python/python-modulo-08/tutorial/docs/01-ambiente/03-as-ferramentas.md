---
sidebar_position: 3
title: As ferramentas
---

# As ferramentas

O projeto usa três ferramentas que não vêm com o Python:

- o **flake8** e o **mypy**, que conferem o código ([próxima página](./04-type-hints-flake8-e-mypy.md));
- o **Poetry**, o gerenciador de projetos do exercício 1
  ([pip e Poetry](../04-ex1/02-pip-e-poetry.md)).

As três são instaladas com o **pip**, o instalador de bibliotecas que vem com o Python. Instalar
direto no Python do sistema mistura essas ferramentas com tudo o que o sistema usa, e muitos
sistemas recusam, com o erro `externally-managed-environment` ("ambiente gerenciado pelo
sistema"; [Pacotes e o pip](../02-conceitos/01-pacotes-e-o-pip.md#o-python-do-sistema-recusa)).
O jeito certo é um **ambiente virtual**: uma pasta com um Python próprio e as bibliotecas dele,
separada do Python do sistema. O exercício 0 é todo sobre ambientes virtuais, e a página
[O ambiente virtual por dentro](../02-conceitos/02-o-ambiente-virtual-por-dentro.md) mostra como
eles funcionam; aqui basta criar um.

## O ambiente das ferramentas

Na pasta `the-matrix`:

```bash
python3 -m venv .venv
```

- `python3 -m venv` pede ao Python que rode o `venv`, a ferramenta que vem com ele e cria
  ambientes virtuais. O `-m` quer dizer "rode esta ferramenta do Python";
- `.venv` é o nome da pasta criada. O ponto no começo é o costume para pastas de ferramentas.

O comando não imprime nada quando dá certo.

No Debian e no Ubuntu, a parte do Python que cria ambientes virtuais vem num pacote separado, o
`python3-venv` ([O Python](./01-o-python.md)). Sem ele, o comando acima falha com uma mensagem
que fala em `ensurepip` e manda instalar esse pacote. Nesse caso, instale-o (a mensagem pode pedir
o nome com a versão, como `python3.12-venv`; use o nome que ela mostrar), apague a pasta criada
pela metade e crie o venv de novo:

```bash
sudo apt install python3-venv
rm -rf .venv
python3 -m venv .venv
```

`rm -rf .venv` apaga a pasta `.venv` e tudo o que está dentro dela.

Este venv guarda só as ferramentas. Os programas dos exercícios rodam em outros ambientes, um por
exercício, criados nas páginas de cada um: assim, o que está instalado aqui nunca interfere no
que cada programa encontra.

## Instalar as três

```bash
.venv/bin/python -m pip install --upgrade pip flake8 mypy "poetry>=2"
```

- `.venv/bin/python` é o Python **de dentro** do venv. O `-m pip` roda o `pip` com ele, e o
  `pip` instala as bibliotecas dentro da pasta `.venv`;
- `--upgrade pip` atualiza o próprio `pip` antes, o que evita o aviso de "nova versão
  disponível";
- `"poetry>=2"` pede o Poetry na versão 2 ou mais nova: o arquivo do exercício 1 usa um formato
  que o Poetry só lê a partir da versão 2. As aspas são necessárias porque, no terminal, `>` sozinho
  manda a saída de um comando para um arquivo.

A saída é longa: uma linha para cada pacote baixado, porque cada ferramenta traz as bibliotecas de
que ela depende. A última linha lista tudo o que foi instalado:

```text
Successfully installed anyio-4.16.0 ast-serialize-0.13.1 build-1.6.1 cachecontrol-0.14.4 certifi-2026.10.23 cffi-2.1.1 charset_normalizer-3.5.2 cleo-2.1.0 crashtest-0.4.1 distlib-0.4.4 dulwich-1.2.21 fastjsonschema-2.22.3 filelock-4.2.10 findpython-0.8.0 flake8-7.5.0 h11-0.16.0 httpcore2-2.16.0 httpx2-2.16.0 idna-3.20 installer-1.1.0 jaraco.classes-3.4.0 jaraco.context-6.1.2 jaraco.functools-4.6.0 keyring-25.7.0 librt-0.16.0 mccabe-0.7.0 more-itertools-11.2.1 msgpack-1.2.4 mypy-2.4.1 mypy_extensions-1.2.0 packaging-26.3 pathspec-1.1.1 pbs-installer-2026.10.25 pip-26.3 pkginfo-1.13.3 platformdirs-4.14.5 poetry-2.5.1 poetry-core-2.5.0 pycodestyle-2.15.0 pycparser-3.12 pyflakes-4.1.0 pyproject-hooks-1.3.3 python-discovery-1.9.5 rapidfuzz-3.14.6 requests-2.34.2 requests-toolbelt-1.0.0 shellingham-1.5.4 tomlkit-0.15.2 trove-classifiers-2026.9.21.13 truststore-0.10.5 typing_extensions-4.16.0 urllib3-2.8.0 virtualenv-21.15.6 xattr-1.3.1
```

A lista e os números das versões podem ser outros na sua máquina. As ferramentas ficam em
`.venv/bin/`:

```bash
.venv/bin/flake8 --version
.venv/bin/mypy --version
.venv/bin/poetry --version
```

```text
7.5.0 (mccabe: 0.7.0, pycodestyle: 2.15.0, pyflakes: 4.1.0) CPython 3.14.5 on
Darwin
mypy 2.4.1 (compiled: yes)
Poetry (version 2.5.1)
```

A última palavra da primeira saída é o nome do sistema (`Linux`, ou `Darwin` no macOS). O que
importa é que os três comandos respondem e que o Poetry é da versão 2 ou mais nova.

## Por que o Poetry fica aqui

O próprio Poetry recomenda ser instalado num ambiente só dele, separado dos projetos que ele
gerencia: no exercício 1, ele cria e preenche **outro** ambiente virtual, o do programa
`loading.py`. O `.venv` desta página não é o ambiente de nenhum exercício, então serve. O Poetry é
sempre chamado pelo caminho, `.venv/bin/poetry` (ou `../.venv/bin/poetry` de dentro de uma pasta de
exercício), e o `.venv` nunca é **ativado** (o que é ativar um venv:
[O ambiente virtual por dentro](../02-conceitos/02-o-ambiente-virtual-por-dentro.md#ativar-e-desativar)).
