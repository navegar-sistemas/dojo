---
sidebar_position: 1
title: O Python
---

# O Python

O enunciado exige **Python 3.10 ou mais novo**: os programas são rodados com o comando `python3`,
e esse comando precisa ser de uma dessas versões. Confira no terminal:

```bash
python3 --version
```

```text
Python 3.15.2
```

O número depois de `Python` é a versão. Qualquer `3.10` ou maior serve (`3.10`, `3.11`, …,
`3.14`, `3.15`); o número da sua máquina pode ser outro.

## Se o comando não existir

No Linux (Debian e Ubuntu), instale o Python do sistema e o pacote `python3-venv`, que permite
criar o ambiente virtual da página [O ambiente virtual](./03-o-ambiente-virtual.md). `apt` é o
instalador de programas do Debian e do Ubuntu, e `sudo` roda o comando como administrador (ele
pede a sua senha):

```bash
sudo apt install python3 python3-venv
```

No Fedora, o instalador é o `dnf`, e o comando é `sudo dnf install python3`; no Arch, o
instalador é o `pacman`, e o comando é `sudo pacman -S python`. Nessas duas distribuições, o
pacote do Python já traz o que cria ambientes virtuais, sem pacote separado.

No macOS, o comando `python3` pode abrir uma janela oferecendo instalar as ferramentas de linha
de comando da Apple. Pode aceitar: elas trazem o `git`, usado na entrega (fim desta página). Mas
o Python que vem com elas é o 3.9, antigo demais para o projeto; instale também o Python pelo
instalador oficial, em [python.org](https://www.python.org/downloads/), que passa a responder
pelo `python3`. Depois, abra um terminal novo e rode `python3 --version` de novo.

## Se a versão for menor que 3.10

Instalar de novo o `python3` do sistema não adianta: ele continua na mesma versão. É preciso
instalar um Python novo, separado do que veio com o sistema:

- **macOS:** o instalador oficial de [python.org](https://www.python.org/downloads/) instala a
  versão mais nova, que passa a responder pelo comando `python3`;
- **Linux (Debian e Ubuntu):** muitas versões dessas distribuições oferecem Pythons mais novos
  como pacotes com o número no nome. Confira se a sua tem, por exemplo, o `python3.11`:

  ```bash
  apt-cache policy python3.11
  ```

  Se a saída tiver uma linha `Candidate:` com uma versão (e não `(none)`), instale-o junto com o
  venv dele (quando o pacote não existe na distribuição, o comando não imprime nada):

  ```bash
  sudo apt install python3.11 python3.11-venv
  ```

  Esse Python é chamado pelo nome com o número, `python3.11`. Se a distribuição não oferece
  nenhuma versão 3.10 ou mais nova, o caminho é atualizar a distribuição;
- **outras distribuições Linux:** o Python novo vem do gerenciador de pacotes delas (`dnf` no
  Fedora, `pacman` no Arch).

Quando o Python novo tem outro nome (como `python3.11`), use esse nome em todo lugar onde o
tutorial escreve `python3`.

## O git

A entrega é feita num **repositório**: uma pasta cujo histórico de versões é guardado pelo
**git**, o programa que registra e envia versões de arquivos, com uma cópia num servidor
([Entregar](../08-fechamento/02-entregar.md)). Confira se ele existe:

```bash
git --version
```

```text
git version 2.54.0 (Apple Git-157)
```

Qualquer versão serve; o número e o texto entre parênteses (que só aparece no macOS) podem ser
outros. Se o comando não existir: no Debian e no Ubuntu, `sudo apt install git`; no Fedora,
`sudo dnf install git`; no Arch, `sudo pacman -S git`; no macOS, o primeiro `git` abre a mesma
janela das ferramentas de linha de comando da Apple; aceite e espere terminar.

No resto do tutorial, `python3` quer dizer o Python 3.10 ou mais novo desta página.
