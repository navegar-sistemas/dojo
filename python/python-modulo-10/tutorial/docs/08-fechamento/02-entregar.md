---
sidebar_position: 2
title: Entregar
---

# Entregar

O enunciado pede a entrega num **repositório Git**, e só o que estiver no repositório conta; ele
também recomenda conferir duas vezes os nomes dos arquivos. Só os cinco arquivos pedidos
precisam ir; ficam de fora a pasta `.venv`, a pasta `experimentos`, o anexo `generator.tar.gz`, a
pasta `gerador`, as pastas `__pycache__`, que o Python cria ao importar um arquivo, e a pasta
`.mypy_cache`, que o mypy cria.

## Copiar os arquivos para o repositório

O repositório fica num serviço de hospedagem de Git (como GitHub ou GitLab), e o endereço dele
(a URL) aparece na página do repositório nesse serviço. O `git clone` e o `git push` podem pedir
login ou uma **chave SSH**, conforme o serviço. Uma chave SSH é um par de arquivos que identifica o
seu computador para o serviço, no lugar de uma senha; a documentação do serviço explica como
criar a chave e cadastrá-la. A partir da pasta `funcmage`, suba um nível, baixe o repositório
numa pasta `entrega` e copie só os arquivos `.py` de cada exercício. Se a pasta do projeto tem
outro nome ([A pasta do projeto](../01-ambiente/02-a-pasta-do-projeto.md)), troque `funcmage`
pelo nome da sua pasta no `cp`:

```bash
cd ..
git clone <endereço-do-repositório> entrega
for ex in ex0 ex1 ex2 ex3 ex4; do
    mkdir -p "entrega/$ex"
    cp "funcmage/$ex/"*.py "entrega/$ex/"
done
cd entrega
```

Troque `<endereço-do-repositório>` pelo endereço do seu repositório. O `git clone` baixa o
repositório; o `for` cria cada pasta de exercício dentro de `entrega` (o `-p` do `mkdir` não
reclama se ela já existir) e copia para ela os arquivos `.py` com `cp`.

## Registrar e enviar

```bash
git add ex0 ex1 ex2 ex3 ex4
git status
```

```text
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
	new file:   ex0/lambda_spells.py
	new file:   ex1/higher_magic.py
	new file:   ex2/scope_mysteries.py
	new file:   ex3/functools_artifacts.py
	new file:   ex4/decorator_mastery.py

```

`git add` marca os arquivos para o próximo registro; `git status` mostra o que está marcado. A
lista `Changes to be committed` ("mudanças a registrar") tem exatamente os cinco arquivos. O resto
pode variar: esta é a saída de um repositório vazio (`No commits yet`, "nenhum registro
ainda"); num repositório que já tem registros, essa linha não aparece. A primeira linha
mostra o **ramo** (*branch*), a linha de histórico em que os registros entram; o nome padrão pode
ser `main` ou `master`.

Cada registro guarda o nome e o e-mail do autor. Antes do primeiro `git commit`, informe os seus,
dentro da pasta `entrega` (sem `--global`, a configuração vale só para este repositório):

```bash
git config user.name "Seu Nome"
git config user.email "voce@exemplo.com"
```

O `git config` não imprime nada. Depois, registre e envie:

```bash
git commit -m "Add exercises 0 to 4"
```

```text
[main (root-commit) ba57fc1] Add exercises 0 to 4
 5 files changed, 379 insertions(+)
 create mode 100644 ex0/lambda_spells.py
 create mode 100644 ex1/higher_magic.py
 create mode 100644 ex2/scope_mysteries.py
 create mode 100644 ex3/functools_artifacts.py
 create mode 100644 ex4/decorator_mastery.py
```

`git commit` registra os arquivos com uma mensagem. A primeira linha mostra o ramo, `root-commit`
(o primeiro registro do repositório; num repositório com registros, essa palavra não aparece) e o
código do registro, `ba57fc1`, que muda a cada registro. As outras linhas dizem quantos arquivos e
linhas entraram.

Sem o `git config`, o git reage de um de dois jeitos, conforme o sistema. Em muitos sistemas
Linux, ele recusa o registro, com `Author identity unknown` e `*** Please tell me who you are.`
na saída; nesse caso, rode os dois `git config` acima e repita o `git commit`. Em outros, como o
macOS, ele não pede nada: aceita o registro com um nome e um e-mail montados a partir do usuário
e do nome do computador, e mostra no meio da saída uma linha `Committer:` com essa identidade e o
aviso:

```text
Your name and email address were configured automatically based
on your username and hostname. Please check that they are accurate.
```

Esse aviso é o sinal de que o registro saiu com a identidade errada. Nesse caso, rode os dois
`git config` acima e corrija o registro com `git commit --amend --reset-author --no-edit`, que
refaz o último registro com a identidade nova, mantendo a mensagem.

Por fim, envie o registro para o repositório no serviço de hospedagem:

```bash
git push
```

## Conferir o que foi enviado

O que conta é o que está **no repositório**, não na sua pasta. Baixe uma cópia nova numa pasta à
parte e rode um programa nela:

```bash
cd ..
git clone <endereço-do-repositório> conferencia
cd conferencia
ls ex0 ex1 ex2 ex3 ex4
python3 ex2/scope_mysteries.py
```

Os cinco arquivos aparecem, e o programa imprime a mesma saída que na pasta do projeto. Depois, a
pasta `conferencia` pode ser apagada (`cd .. && rm -rf conferencia`).
