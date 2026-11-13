---
sidebar_position: 4
title: Variáveis de ambiente
---

# Variáveis de ambiente

Um programa precisa de informações que mudam de uma máquina para outra: o endereço do banco de
dados, a senha de um serviço, o modo em que ele roda. Escrever esses valores no código obriga a
mudar o código a cada máquina e põe as senhas dentro do repositório, à vista de quem tiver acesso
a ele. As **variáveis de ambiente** resolvem isso.

## O ambiente de um programa

Todo programa, ao começar, recebe de quem o iniciou (aqui, o terminal) um conjunto de pares
`NOME=valor`: o seu **ambiente**. Alguns já existem em todo terminal, como `HOME` (a pasta pessoal
do usuário) e `PATH` (a lista de pastas onde o terminal procura os comandos, que o `activate` de
um venv modifica; [O ambiente virtual por dentro](./02-o-ambiente-virtual-por-dentro.md#ativar-e-desativar)).
O programa lê esses valores enquanto roda, e o código não muda.

Em Python, o ambiente fica no módulo `os`:

- `os.environ` funciona como um dicionário: `os.environ["HOME"]` dá o valor, e lança `KeyError`
  se a variável não existe;
- `os.getenv("HOME")` dá o valor, ou `None` se a variável não existe.

Crie `experimentos/ambiente.py`:

```python title="experimentos/ambiente.py"
import os

user = os.getenv("MATRIX_USER")
if user is None:
    print("MATRIX_USER is not set")
else:
    print(f"Hello, {user}")
```

```bash
python3 experimentos/ambiente.py
```

```text
MATRIX_USER is not set
```

## Uma variável para um comando

Escrever `NOME=valor` antes de um comando cria a variável **só para aquele comando**:

```bash
MATRIX_USER=neo python3 experimentos/ambiente.py
```

```text
Hello, neo
```

O comando seguinte já não a vê:

```bash
python3 experimentos/ambiente.py
```

```text
MATRIX_USER is not set
```

## Uma variável para o terminal

`export` cria a variável no próprio terminal, e todos os comandos seguintes a recebem, até o
terminal ser fechado. `echo "$MATRIX_USER"` mostra o valor no terminal (o `$` antes do nome lê a
variável):

```bash
export MATRIX_USER=trinity
echo "$MATRIX_USER"
python3 experimentos/ambiente.py
```

```text
trinity
Hello, trinity
```

`unset` apaga a variável:

```bash
unset MATRIX_USER
python3 experimentos/ambiente.py
```

```text
MATRIX_USER is not set
```

## Quando a variável falta

`os.getenv` também aceita um segundo argumento, um valor padrão para quando a variável não
existe: `os.getenv("MATRIX_USER", "anonymous")`. O tutorial não usa essa forma para configuração:
com um valor padrão escrito no código, uma variável esquecida passa despercebida, e o programa roda
com um valor que ninguém escolheu (num servidor de produção, por exemplo, com o banco de dados de
teste). O experimento acima trata a falta às claras, com uma mensagem; o exercício 2 vai além e
se recusa a rodar sem a configuração completa.

## Por que configurar assim

- **o mesmo código em todo lugar**: a máquina de desenvolvimento e o servidor de produção rodam
  o mesmo arquivo `.py`, cada um com as suas variáveis;
- **segredos fora do código**: a senha fica no ambiente da máquina, e não no repositório;
- **troca sem editar nada**: `NOME=valor comando` muda um valor só para uma execução, como no
  exemplo do enunciado `MATRIX_MODE=production API_KEY=secret123 python3 oracle.py`.

Definir várias variáveis com `export` a cada terminal novo seria trabalhoso. O arquivo `.env` guarda
essas definições num arquivo, lido pelo programa ao iniciar
([O arquivo .env](../05-ex2/02-o-arquivo-env.md)).
