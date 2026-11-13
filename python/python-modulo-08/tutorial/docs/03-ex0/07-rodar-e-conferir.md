---
sidebar_position: 7
title: Rodar e conferir
---

# Rodar e conferir

Os comandos desta página são rodados dentro da pasta `ex0`, como nos exemplos do enunciado:

```bash
cd ex0
```

Nenhum ambiente pode estar ativado: se o *prompt* começa com um nome entre parênteses, rode
`deactivate` antes.

## Fora do venv

```bash
python3 construct.py
```

```text

MATRIX STATUS: You're still plugged in

Current Python: /…/bin/python3.15
Virtual Environment: None detected

WARNING: You're in the global environment!
The machines can see everything you install.

To enter the construct, run:
python -m venv matrix_env
source matrix_env/bin/activate # On Unix
matrix_env\Scripts\activate  # On Windows

Then run this program again.

Package installation path:
/…/lib/python3.15/site-packages
```

O `/…` marca a pasta onde o Python global está instalado. Num Linux com o Python do sistema, as
duas linhas com caminho ficam parecidas com `Current Python: /usr/bin/python3` e
`/usr/local/lib/python3.12/dist-packages` (o Debian e o Ubuntu chamam a pasta de `dist-packages`).

### Comparar com o enunciado

O `diff` compara duas listas de linhas e mostra só as diferenças. Aqui, a saída do programa contra
a saída do enunciado:

```bash
diff <(python3 construct.py) - <<'FIM'

MATRIX STATUS: You're still plugged in

Current Python: /usr/bin/python3.11
Virtual Environment: None detected

WARNING: You're in the global environment!
The machines can see everything you install.

To enter the construct, run:
python -m venv matrix_env
source matrix_env/bin/activate # On Unix
matrix_env\Scripts\activate  # On Windows

Then run this program again.
FIM
```

- `<(python3 construct.py)` entrega ao `diff` a saída do programa como se fosse um arquivo;
- o `-` diz ao `diff` para ler o segundo texto da entrada do comando, em vez de um arquivo;
- `<<'FIM'` escreve nessa entrada as linhas seguintes, até a linha `FIM`: a saída copiada do
  enunciado. Cole o bloco inteiro, até a linha `FIM`; sem ela, o terminal fica esperando mais
  linhas.

```text
4c4
< Current Python: /…/bin/python3.15
---
> Current Python: /usr/bin/python3.11
16,18d15
< 
< Package installation path:
< /…/lib/python3.15/site-packages
```

O `diff` descreve como transformar o primeiro texto no segundo. As linhas com `<` são do
programa, e as com `>`, do enunciado:

- `4c4`: a linha 4 muda (*change*). É o caminho do Python, diferente em cada máquina;
- `16,18d15`: as linhas 16 a 18 do programa não existem no enunciado (*delete*). São as três
  linhas da escolha do tutorial ([Onde ficam os pacotes](./05-onde-ficam-os-pacotes.md)).

Todas as outras linhas, inclusive as vazias e os dois espaços da linha do Windows, são iguais.

## Dentro do venv

Crie o ambiente com os comandos que o programa sugere e ative-o:

```bash
python3 -m venv matrix_env
source matrix_env/bin/activate
```

Os dois comandos não imprimem nada; o *prompt* passa a começar com `(matrix_env)`.

```bash
python3 construct.py
```

```text

MATRIX STATUS: Welcome to the construct

Current Python: /…/the-matrix/ex0/matrix_env/bin/python3
Virtual Environment: matrix_env
Environment Path: /…/the-matrix/ex0/matrix_env

SUCCESS: You're in an isolated environment!
Safe to install packages without affecting
the global system.

Package installation path:
/…/the-matrix/ex0/matrix_env/lib/python3.15/site-packages
```

Aqui o `/…` é a pasta onde fica a `the-matrix`.

### Comparar com o enunciado

O enunciado roda `python`, que existe dentro do venv, e escreve `/path/to` no lugar da pasta. O
`sed` faz a mesma troca na saída do programa antes do `diff`:

```bash
diff <(python construct.py | sed "s|$PWD|/path/to|") - <<'FIM'

MATRIX STATUS: Welcome to the construct

Current Python: /path/to/matrix_env/bin/python
Virtual Environment: matrix_env
Environment Path: /path/to/matrix_env

SUCCESS: You're in an isolated environment!
Safe to install packages without affecting
the global system.

Package installation path:
/path/to/matrix_env/lib/python3.11/site-packages
FIM
```

- `$PWD` é uma variável do terminal com o caminho da pasta atual, a `ex0`;
- `sed "s|antes|depois|"` troca, em cada linha, o texto `antes` por `depois`. Aqui troca o
  caminho da `ex0` por `/path/to`;
- o `|` entre `python construct.py` e `sed` (*pipe*, "cano") liga a saída do primeiro comando à
  entrada do segundo.

```text
13c13
< /path/to/matrix_env/lib/python3.15/site-packages
---
> /path/to/matrix_env/lib/python3.11/site-packages
```

A única diferença é a versão do Python no caminho dos pacotes: `python3.15` aqui, `python3.11`
na máquina de quem escreveu o enunciado.

## Dentro do venv, sem ativar

```bash
deactivate
matrix_env/bin/python construct.py
```

```text

MATRIX STATUS: Welcome to the construct

Current Python: /…/the-matrix/ex0/matrix_env/bin/python
Virtual Environment: matrix_env
Environment Path: /…/the-matrix/ex0/matrix_env

SUCCESS: You're in an isolated environment!
Safe to install packages without affecting
the global system.

Package installation path:
/…/the-matrix/ex0/matrix_env/lib/python3.15/site-packages
```

O terminal não tem nada ativado, mas o Python que roda é o do venv, e o programa acerta: a
detecção olha para o Python em execução, e não para a ativação
([Por que não a variável VIRTUAL_ENV](./02-detectar-o-venv.md#por-que-não-a-variável-virtual_env)).

## Em outras versões do Python

Com o Python 3.10 ou o 3.14, as saídas são as mesmas, com `python3.10` ou `python3.14` no lugar
de `python3.15` nos caminhos.

## Conferir estilo e tipos

As ferramentas estão no `.venv` da pasta de cima, a `the-matrix`, e são chamadas com `../`:

```bash
../.venv/bin/flake8 construct.py
../.venv/bin/mypy --disallow-untyped-defs construct.py
```

```text
Success: no issues found in 1 source file
```

O flake8 não imprime nada, e o mypy não acha problema. Volte para a pasta do projeto:

```bash
cd ..
```

A pasta `matrix_env` pode ficar na `ex0`: ela não é entregue
([Entregar](../06-fechamento/02-entregar.md)). Para apagá-la, `rm -rf ex0/matrix_env`; o comando
`python3 -m venv matrix_env` cria outra igual quando for preciso.
