---
sidebar_position: 3
title: O ambiente virtual
---

# O ambiente virtual

O projeto precisa de três coisas que não vêm com o Python: o **Pydantic**, que os programas
importam, e as duas ferramentas que conferem o código, o **flake8** e o **mypy**. As três são
instaladas com o **pip**, o instalador de bibliotecas do Python, como o enunciado pede.

Instalar com `pip` direto no Python do sistema mistura essas bibliotecas com tudo o que o sistema
usa, e muitos sistemas Linux recusam, com o erro `externally-managed-environment` ("ambiente
gerenciado pelo sistema"). O enunciado exige um **ambiente virtual** (*virtual environment*, ou
**venv**): uma pasta com um Python próprio e as bibliotecas dele, só para este projeto.

## Criar o venv

Na pasta `cosmic-data`:

```bash
python3 -m venv .venv
```

- `python3 -m venv` pede ao Python que rode o `venv`, uma ferramenta que já vem instalada com
  ele e cria ambientes virtuais. O `-m` quer dizer "rode esta ferramenta do Python";
- `.venv` é o nome da pasta criada. O ponto no começo é o costume para pastas de ferramentas, e
  faz o `ls` comum escondê-la.

O comando não imprime nada quando dá certo.

No Debian e no Ubuntu, o `python3` vem instalado, mas a parte dele que cria ambientes virtuais
vem num pacote separado, o `python3-venv`. Sem ele, o comando acima falha com uma mensagem que
fala em `ensurepip` e manda instalar esse pacote. Nesse caso, instale-o (a mensagem pode pedir o
nome com a versão, como `python3.12-venv`; use o nome que ela mostrar), apague a pasta criada pela
metade e crie o venv de novo:

```bash
sudo apt install python3-venv
rm -rf .venv
python3 -m venv .venv
```

`rm -rf .venv` apaga a pasta `.venv` e tudo o que está dentro dela.

## Instalar o Pydantic, o flake8 e o mypy

```bash
.venv/bin/python -m pip install --upgrade pip "pydantic>=2,<3" flake8 mypy
```

- `.venv/bin/python` é o Python **de dentro** do venv. O `-m pip` roda o `pip` com ele, e o
  `pip` instala as bibliotecas dentro da pasta `.venv`;
- `--upgrade pip` atualiza o próprio `pip` antes, o que evita o aviso de "nova versão
  disponível";
- `"pydantic>=2,<3"` pede o Pydantic numa versão **maior ou igual a 2 e menor que 3**: qualquer
  2.x, a versão que o enunciado exige. As aspas são obrigatórias: sem elas, o terminal entende o
  `>` e o `<` como redirecionamento de arquivos;
- `flake8 mypy` são as duas ferramentas.

O `pip` também instala sozinho as bibliotecas de que o Pydantic depende, como o `pydantic-core`,
a parte do Pydantic que faz a validação de fato. A última linha da saída lista tudo o que foi
instalado, começando por `Successfully installed`.

Confira as versões:

```bash
.venv/bin/python -c "import pydantic; print(pydantic.VERSION)"
.venv/bin/flake8 --version
.venv/bin/mypy --version
```

```text
2.14.3
7.5.0 (mccabe: 0.7.0, pycodestyle: 2.15.0, pyflakes: 4.1.0) CPython 3.14.5 on
Darwin
mypy 2.4.1 (compiled: yes)
```

- `python -c "..."` roda o código escrito entre as aspas. Aqui ele importa o Pydantic e imprime
  a versão, guardada em `pydantic.VERSION`;
- a última palavra da saída do flake8 é o nome do sistema (`Linux`, `Darwin` no macOS).

Os números podem ser outros na sua máquina. O que importa é que a versão do Pydantic comece com
`2.`. As mensagens de erro do Pydantic mostradas no tutorial são as da versão 2.14.3; outra
versão 2.x pode escrever algumas delas com outras palavras.

## Sempre o Python do venv

O Pydantic está instalado **só** dentro da pasta `.venv`. Por isso, todo programa do projeto é
rodado com `.venv/bin/python`, e não com `python3`:

```bash
python3 -c "import pydantic"
```

Com o `python3` do sistema, que normalmente não tem o Pydantic, a última linha da saída é:

```text
ModuleNotFoundError: No module named 'pydantic'
```

("nenhum módulo chamado `pydantic`"). Com `.venv/bin/python` no lugar de `python3`, o mesmo
comando não imprime nada: o `import` funcionou.
