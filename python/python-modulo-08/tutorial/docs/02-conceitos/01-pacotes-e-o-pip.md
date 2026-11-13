---
sidebar_position: 1
title: Pacotes e o pip
---

# Pacotes e o pip

O Python vem com uma biblioteca padrão grande (`os`, `sys`, `json`...), mas muito do que se usa
em análise de dados vem de fora: o numpy, o pandas e o matplotlib do exercício 1, o python-dotenv
do exercício 2. Cada uma dessas bibliotecas é distribuída como um **pacote**: um conjunto de
módulos com nome e número de versão, pronto para ser instalado.

## PyPI e pip

Os pacotes ficam no **PyPI** (*Python Package Index*, "índice de pacotes do Python",
[pypi.org](https://pypi.org)), um repositório público na internet. O **pip** é o programa que baixa
um pacote do PyPI e o instala num Python. Ele vem junto com o Python e é chamado como um módulo:
`python3 -m pip install nome`.

O pip instala os pacotes numa pasta chamada **`site-packages`**, que pertence a um Python
específico: o Python que rodou o pip. É nessa pasta que o `import` procura as bibliotecas de
fora. Instalar com um Python e rodar o programa com outro é o erro mais comum de quem começa: a
biblioteca está instalada, mas no `site-packages` do outro Python.

## Dependências

Uma **dependência** é uma biblioteca de que um programa precisa para rodar. Os pacotes também
têm dependências, e o pip instala tudo junto. O comando `pip show` mostra as informações de um
pacote instalado. Para o flake8, instalado no ambiente das ferramentas
([As ferramentas](../01-ambiente/03-as-ferramentas.md)):

```bash
.venv/bin/python -m pip show flake8
```

```text
Name: flake8
Version: 7.5.0
Summary: the modular source code checker: pep8 pyflakes and co
Home-page: https://github.com/pycqa/flake8
Author: Tarek Ziade
Author-email: tarek@ziade.org
License: MIT
Location: /…/the-matrix/.venv/lib/python3.14/site-packages
Requires: mccabe, pycodestyle, pyflakes
Required-by: 
```

- `Location` é o `site-packages` onde ele está: o do `.venv`. Em `/…/the-matrix`, o `/…` é o
  caminho da pasta do projeto na sua máquina; o `python3.14` muda com a versão do Python;
- `Requires` lista as dependências do flake8: três outros pacotes, instalados junto com ele;
- `Required-by` (vazio aqui) lista os pacotes instalados que dependem dele.

## Versões

Cada pacote tem versões numeradas, como `7.5.0`. Sem indicação, o pip instala a mais nova que
funciona com aquele Python. Uma **restrição de versão** limita a escolha:

| Escrito | Aceita |
|---|---|
| `numpy` | qualquer versão |
| `numpy>=1.25.0` | a 1.25.0 ou qualquer mais nova |
| `numpy==2.5.4` | só a 2.5.4 |

Uma biblioteca nova pode deixar de funcionar com um Python antigo: o numpy 2.5, por exemplo, não
funciona no Python 3.10. Com `numpy>=1.25.0`, o pip escolhe a mais nova que serve para o Python
que está rodando, e o mesmo arquivo de dependências funciona do 3.10 ao 3.14.

## O Python do sistema recusa

Um ensaio de instalação no Python do sistema, fora de qualquer ambiente virtual. A opção
`--dry-run` ("ensaio") faz o pip mostrar o que faria, sem instalar nada:

```bash
python3 -m pip install --dry-run numpy
```

As primeiras linhas da saída são:

```text
error: externally-managed-environment

× This environment is externally managed
```

O resto da mensagem depende do sistema e sugere usar um ambiente virtual. Muitos sistemas (Debian,
Ubuntu, macOS com Python de gerenciadores de pacotes) marcam o seu Python como "gerenciado pelo
sistema": os pacotes dele são instalados pelo instalador do sistema, e um pip mexendo na mesma
pasta poderia quebrar programas do próprio sistema que dependem de versões específicas. O pip
recusa antes mesmo do ensaio. Se no seu sistema a saída for `Would install numpy-…` ("instalaria o
numpy"), o seu Python não tem essa marca; a regra continua valendo: bibliotecas de projeto vão
num ambiente virtual.

A opção `--break-system-packages`, citada na mensagem, força a instalação. Não use: é exatamente o
problema que o ambiente virtual resolve ([próxima página](./02-o-ambiente-virtual-por-dentro.md)).
