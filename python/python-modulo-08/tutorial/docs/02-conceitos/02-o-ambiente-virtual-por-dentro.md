---
sidebar_position: 2
title: O ambiente virtual por dentro
---

# O ambiente virtual por dentro

Um **ambiente virtual** resolve os dois problemas da [página anterior](./01-pacotes-e-o-pip.md):
cada projeto ganha o seu próprio `site-packages`, onde o pip pode instalar à vontade, sem tocar no
Python do sistema (o Python **global**) nem nos outros projetos. O `.venv` criado em
[As ferramentas](../01-ambiente/03-as-ferramentas.md) é um ambiente virtual; esta página abre ele.

## O que tem na pasta

```bash
ls .venv
```

```text
bin
include
lib
pyvenv.cfg
```

- `bin/`: os programas do ambiente: `python` e `python3`, `pip`, as ferramentas instaladas
  (`flake8`, `mypy`, `poetry`) e os scripts `activate`, explicados abaixo;
- `lib/`: dentro dela, `python3.14/site-packages/`, a pasta das bibliotecas deste ambiente;
- `include/`: uma pasta para bibliotecas que compilam código em C; fica vazia aqui;
- `pyvenv.cfg`: o arquivo que transforma a pasta num ambiente virtual.

Em alguns Linux aparece também `lib64`, um atalho para `lib`.

```bash
cat .venv/pyvenv.cfg
```

```text
home = /…/bin
include-system-site-packages = false
version = 3.14.5
executable = /…/bin/python3.14
command = /…/bin/python3.14 -m venv /…/the-matrix/.venv
```

- `home` é a pasta do Python que criou o ambiente, o Python global;
- `include-system-site-packages = false` diz que este ambiente **não** enxerga as bibliotecas do
  `site-packages` global: só as próprias;
- `version` é a versão do Python;
- `executable` e `command` registram o Python e o comando usados para criar o ambiente. O Python
  3.10 não escreve essas duas linhas.

O `.venv/bin/python` não é uma cópia do Python: é um **atalho** (*link simbólico*) para o Python
global. O interpretador é o mesmo; a diferença é que, ao iniciar, ele encontra o `pyvenv.cfg` na
pasta acima da sua e passa a usar o `site-packages` do ambiente.

## O Python sabe onde está

O módulo `sys` guarda o que o Python sabe sobre si mesmo, e o módulo `site` sabe onde ficam as
pastas de pacotes. Crie `experimentos/onde_estou.py`:

```python title="experimentos/onde_estou.py"
import site
import sys

print(f"executable:  {sys.executable}")
print(f"prefix:      {sys.prefix}")
print(f"base_prefix: {sys.base_prefix}")
print(f"packages:    {site.getsitepackages()[0]}")
```

- `sys.executable`: o caminho do Python que está rodando o programa;
- `sys.prefix`: a pasta-base do ambiente em uso;
- `sys.base_prefix`: a pasta-base do Python global, de onde o ambiente veio;
- `site.getsitepackages()`: a lista das pastas `site-packages` do ambiente em uso. A primeira
  (`[0]`) é onde o pip instala.

Rode com o Python global e com o Python do `.venv`:

```bash
python3 experimentos/onde_estou.py
```

```text
executable:  /…/bin/python3.14
prefix:      /…
base_prefix: /…
packages:    /…/lib/python3.14/site-packages
```

```bash
.venv/bin/python experimentos/onde_estou.py
```

```text
executable:  /…/the-matrix/.venv/bin/python
prefix:      /…/the-matrix/.venv
base_prefix: /…
packages:    /…/the-matrix/.venv/lib/python3.14/site-packages
```

O `/…` marca a parte que muda de máquina para máquina: na primeira saída, a pasta onde o Python
está instalado (num Linux com o Python do sistema, `prefix` é `/usr` e o executável é algo como
`/usr/bin/python3`); na segunda, a pasta do projeto.

A comparação é a regra que o exercício 0 usa:

| | `sys.prefix` | `sys.base_prefix` |
|---|---|---|
| Python global | a pasta do Python global | a mesma pasta |
| Python de um venv | a pasta do venv | a pasta do Python global |

**Dentro de um ambiente virtual, `sys.prefix` é diferente de `sys.base_prefix`.** Fora, os dois
são iguais.

## Ativar e desativar

Escrever `.venv/bin/python` toda vez é longo. **Ativar** um ambiente faz o terminal usar os
programas dele quando se digita só `python3`, `python` ou `pip`. O comando `command -v` mostra
qual programa o terminal vai usar para um nome:

```bash
command -v python3
```

```text
/…/bin/python3
```

É o Python global (num Linux, `/usr/bin/python3`). Agora ative o `.venv`:

```bash
source .venv/bin/activate
command -v python3
echo "$VIRTUAL_ENV"
```

```text
/…/the-matrix/.venv/bin/python3
/…/the-matrix/.venv
```

- `source .venv/bin/activate` roda o script `activate` **dentro** do terminal atual (por isso o
  `source`, e não só o nome do script). O script muda a variável `PATH`, a lista de pastas em que
  o terminal procura os comandos, pondo `.venv/bin` na frente
  ([Variáveis de ambiente](./04-variaveis-de-ambiente.md));
- o script também cria a variável `VIRTUAL_ENV`, com a pasta do ambiente, e põe o nome do
  ambiente no começo da linha onde se digita, o *prompt*: `(.venv) $`.

Com o ambiente ativado, `python3` já é o do venv:

```bash
python3 experimentos/onde_estou.py
```

```text
executable:  /…/the-matrix/.venv/bin/python3
prefix:      /…/the-matrix/.venv
base_prefix: /…
packages:    /…/the-matrix/.venv/lib/python3.14/site-packages
```

O comando `deactivate`, criado pelo `activate`, desfaz tudo:

```bash
deactivate
command -v python3
```

```text
/…/bin/python3
```

Ativar é só uma comodidade do terminal: o que torna um Python "de dentro do venv" é o caminho do
executável, e não a ativação. `.venv/bin/python` funciona dentro do venv mesmo com nada ativado,
como na seção anterior. A ativação vale só para o terminal onde foi feita; um terminal novo começa
sem nada ativado.

No resto do projeto, o `.venv` das ferramentas não é ativado: as ferramentas são chamadas pelo
caminho. Cada exercício cria e ativa o seu próprio ambiente.
