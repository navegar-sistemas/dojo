---
sidebar_position: 1
title: O Python
---

# O Python

Os programas precisam rodar com **Python 3.10 ou mais novo**, chamado pelo comando `python3`.
Confira a versão no terminal:

```bash
python3 --version
```

```text
Python 3.15.2
```

O número depois de `Python` é a versão, e na sua máquina pode ser outro. O enunciado exige `3.10`
ou maior (`3.10`, `3.11`, `3.12` e assim por diante). Abaixo do 3.9, cinco dos sete exercícios nem
rodam: eles anotam coleções com `list[int]` e `tuple[float, float, float]`, uma escrita que o
Python só aceita a partir do 3.9 ([Uma lista nova](../04-ex1/02-uma-lista-nova.md)).

## Se a versão for menor que 3.10, ou o comando não existir

O Python vem do gerenciador de pacotes do sistema:

| Sistema | Comando |
|---|---|
| Debian e Ubuntu | `sudo apt install python3` |
| Fedora | `sudo dnf install python3` |
| Arch | `sudo pacman -S python` |
| macOS | o instalador oficial, em [python.org](https://www.python.org/downloads/) |

Uma distribuição Linux antiga pode não oferecer nenhum Python 3.10 ou mais novo no gerenciador de
pacotes. Nesse caso, o [pyenv](https://github.com/pyenv/pyenv) instala uma versão própria, na pasta
do usuário, sem depender do sistema: depois de instalado e configurado no shell (o programa do
terminal que lê e executa os comandos, como o `bash` ou o `zsh`), como a página dele explica,
`pyenv install 3.12` baixa e compila o Python 3.12, e `pyenv global 3.12` faz o comando `python3`
passar a ser essa versão. `python3 --version` confirma a troca.

Daqui em diante, `python3` quer dizer esse Python 3.10 ou mais novo.
