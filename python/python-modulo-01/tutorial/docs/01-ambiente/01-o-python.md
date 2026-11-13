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
maior serve (`3.10`, `3.11`, `3.12`, `3.13`, `3.14`). O código dos exercícios não usa nada que
só exista nas versões mais novas.

## Se o comando não existir

No Linux (Debian e Ubuntu), instale o Python do sistema e o pacote `python3-venv`, que permite
criar o [ambiente virtual](./03-o-ambiente-virtual.md):

```bash
sudo apt install python3 python3-venv
```

No macOS, instale o Python pelo instalador oficial, em
[python.org](https://www.python.org/downloads/). Depois, abra um terminal novo e rode
`python3 --version` de novo.

## Se a versão for menor que 3.10

Instalar de novo o `python3` do sistema não adianta: ele continua na mesma versão. É preciso
instalar um Python novo, separado do que veio com o sistema:

- **macOS:** o instalador oficial de [python.org](https://www.python.org/downloads/) instala a
  versão mais nova, que passa a responder pelo comando `python3`;
- **Linux:** muitas distribuições oferecem versões mais novas como pacotes com o número no nome.
  Confira se a sua tem, por exemplo, o `python3.11`:

  ```bash
  apt-cache policy python3.11
  ```

  Se a linha `Candidate:` mostrar uma versão (e não `(none)`), instale-o junto com o venv dele:

  ```bash
  sudo apt install python3.11 python3.11-venv
  ```

  Esse Python é chamado pelo nome com o número, `python3.11`. Se a distribuição não oferece
  nenhuma versão 3.10 ou mais nova, o caminho é atualizar a distribuição.

Quando o Python novo tem outro nome (como `python3.11`), use esse nome em todo lugar onde
aparece `python3`.

## O git

A entrega é feita num repositório **git**, o programa que guarda e envia versões de arquivos
([Entregar](../09-fechamento/02-entregar.md)). Confira se ele existe:

```bash
git --version
```

O comando responde `git version` seguido de um número; qualquer versão serve. Se o comando não
existir: no Linux, `sudo apt install git`; no macOS, o primeiro `git` abre uma janela oferecendo
instalar as ferramentas de linha de comando da Apple, que trazem o git; aceite e espere terminar.

Daqui em diante, `python3` quer dizer esse Python 3.10 ou mais novo.
