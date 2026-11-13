---
sidebar_position: 1
title: O Python
---

# O Python

Os programas rodam com o comando `python3`, que precisa ser o **Python 3.10 ou mais novo**.
Confira no terminal:

```bash
python3 --version
```

```text
Python 3.12.3
```

O número depois de `Python` é a versão; na sua máquina ele pode ser outro. Qualquer `3.10` ou
maior serve (`3.10`, `3.11`, `3.12`, `3.13`, `3.14`, `3.15`). O código dos exercícios não usa nada que
só exista nas versões mais novas.

## Se o comando não existir

No Linux (Debian e Ubuntu), instale o Python do sistema e o pacote `python3-venv`, que permite
criar o [ambiente virtual](./03-o-ambiente-virtual.md):

```bash
sudo apt install python3 python3-venv
```

O `apt` é o gerenciador de pacotes (o instalador de programas) do Debian e do Ubuntu, e o `sudo`
na frente roda o comando como administrador do sistema, o que pode pedir a sua senha.

Em outras distribuições Linux, o Python vem do gerenciador de pacotes delas (`dnf` no Fedora,
`pacman` no Arch).

No macOS, instale o Python pelo instalador oficial, em
[python.org](https://www.python.org/downloads/). Depois, abra um terminal novo e rode
`python3 --version` de novo.

## Se a versão for menor que 3.10

Instalar de novo o `python3` do sistema não adianta: ele continua na mesma versão. É preciso
instalar um Python novo, separado do que veio com o sistema:

- **macOS:** o instalador oficial de [python.org](https://www.python.org/downloads/) instala a
  versão mais nova, que passa a responder pelo comando `python3` nos terminais abertos depois da
  instalação. Abra um terminal novo e confira com `python3 --version`;
- **Linux (Debian e Ubuntu):** muitas versões dessas distribuições oferecem Pythons mais novos
  como pacotes com o número no nome. Confira se a sua tem, por exemplo, o `python3.11`:

  ```bash
  apt-cache policy python3.11
  ```

  Sem nenhuma linha impressa, ou com `Candidate: (none)`, a distribuição não tem esse pacote: troque
  o `3.11` por outra versão, como `3.12`, e confira de novo. Se a linha `Candidate:` mostrar uma
  versão, instale-o junto com o venv dele:

  ```bash
  sudo apt install python3.11 python3.11-venv
  ```

  Esse Python é chamado pelo nome com o número, `python3.11`. Se a distribuição não oferece
  nenhuma versão 3.10 ou mais nova, o caminho é atualizar a distribuição;
- **outras distribuições Linux:** o Python novo vem do gerenciador de pacotes delas (`dnf` no
  Fedora, `pacman` no Arch).

Quando o Python novo tem outro nome (como `python3.11`), use esse nome em todo comando digitado
no terminal onde aparece `python3`. A linha do [shebang](../02-ex0/06-o-shebang.md) é a exceção:
ela continua `#!/usr/bin/env python3`.

## O git

A entrega é feita num repositório **git**, o programa que guarda e envia versões de arquivos
([Entregar](../09-fechamento/02-entregar.md)). Confira se ele existe:

```bash
git --version
```

O comando responde `git version` seguido de um número; qualquer versão serve. Se o comando não
existir: no Linux (Debian e Ubuntu), `sudo apt install git`; em outras distribuições Linux, o
pacote `git` do gerenciador de pacotes delas; no macOS, o primeiro `git` abre uma janela
oferecendo instalar as ferramentas de linha de comando da Apple, que trazem o git; aceite e
espere terminar.

Daqui em diante, `python3` quer dizer esse Python 3.10 ou mais novo.
