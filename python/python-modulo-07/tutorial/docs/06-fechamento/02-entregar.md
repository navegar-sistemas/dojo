---
sidebar_position: 2
title: Entregar
---

# Entregar

O enunciado pede a entrega num **repositório Git**, e o que conta é o que está no repositório,
não na sua pasta de trabalho. Vão os três programas de teste, na raiz do repositório, e as três
pastas de pacote, com os seus arquivos `.py`. A pasta `.venv`, a pasta `experimentos`, as pastas
`__pycache__` e a pasta `.mypy_cache` ficam de fora.

## Copiar os arquivos para o repositório

Você precisa do endereço (a URL) do repositório remoto, a cópia do repositório guardada no
serviço que o hospeda (GitHub, GitLab ou outro). O `git clone` e o `git push` podem pedir login
ou uma **chave SSH**: um par de arquivos que identifica o seu computador para o serviço, no lugar
de uma senha. A documentação do serviço explica como criar a chave e cadastrá-la. A partir da
pasta `datadeck`, suba um nível e baixe o repositório numa pasta `entrega`:

```bash
cd ..
git clone <endereço-do-repositório> entrega
```

Troque `<endereço-do-repositório>` pelo endereço do seu repositório **antes** de rodar: os sinais
`<` e `>` têm outro significado no terminal. Se o repositório ainda estiver vazio, o `git clone`
avisa `warning: You appear to have cloned an empty repository.` ("parece que você clonou um
repositório vazio"): é o esperado. Uma linha começando com `fatal:` quer dizer que o clone
falhou; confira o endereço e o acesso e rode o `git clone` de novo antes de seguir.

Depois, copie só os arquivos `.py` e entre na pasta `entrega`:

```bash
cp datadeck/battle.py datadeck/capacitor.py datadeck/tournament.py entrega/
for ex in ex0 ex1 ex2; do
    mkdir -p "entrega/$ex"
    cp "datadeck/$ex/"*.py "entrega/$ex/"
done
cd entrega
```

Se a pasta do projeto tem outro nome, troque `datadeck` pelo nome da sua pasta. O primeiro `cp`
copia os três programas para a raiz da `entrega`; o `for` cria cada pasta de exercício dentro
dela (o `-p` do `mkdir` não reclama se a pasta já existir) e copia os arquivos `.py` do pacote.
O `*.py` deixa a `__pycache__` para trás.

## Registrar e enviar

```bash
git add battle.py capacitor.py tournament.py ex0 ex1 ex2
git status
```

```text
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
	new file:   battle.py
	new file:   capacitor.py
	new file:   ex0/__init__.py
	new file:   ex0/creature.py
	new file:   ex0/factory.py
	new file:   ex1/__init__.py
	new file:   ex1/capability.py
	new file:   ex1/creature.py
	new file:   ex1/factory.py
	new file:   ex2/__init__.py
	new file:   ex2/strategy.py
	new file:   tournament.py

```

`git add` marca os arquivos para o próximo registro; `git status` mostra o que está marcado. A
lista `Changes to be committed` ("mudanças a registrar") tem os doze arquivos. O resto pode
variar: esta é a saída de um repositório vazio (`No commits yet`, "nenhum registro
ainda"); num repositório que já tem registros, essa linha não aparece. A primeira linha mostra o
**ramo** (*branch*), a linha de histórico em que os registros entram; o nome padrão pode ser
`main` ou `master`.

Cada registro leva o nome e o e-mail do autor. Antes do primeiro registro, informe os seus,
dentro da pasta `entrega` (troque pelos seus dados):

```bash
git config user.name "Seu Nome"
git config user.email "voce@exemplo.com"
```

Os dois comandos não imprimem nada e valem só para este repositório. Sem eles, o `git` pode
recusar o registro (`Please tell me who you are`) ou, como costuma acontecer no macOS, aceitá-lo com um nome e um
e-mail deduzidos do usuário e do nome do computador. Nesse caso, a saída do `git commit` traz um
aviso que começa com `Your name and email address were configured automatically` ("o seu nome e
e-mail foram configurados automaticamente"): sinal de que o registro saiu com a identidade
errada.

```bash
git commit -m "Add exercises 0 to 2"
git push
```

`git commit` registra os arquivos com uma mensagem; `git push` envia o registro para o
repositório remoto.

## Conferir o que foi enviado

O que conta é o que está **no repositório**, não na sua pasta. Baixe uma cópia nova numa pasta à
parte e rode um programa nela:

```bash
cd ..
git clone <endereço-do-repositório> conferencia
cd conferencia
LC_ALL=C ls -1 *.py ex0 ex1 ex2
python3 tournament.py
```

Os doze arquivos aparecem, sem nenhuma `__pycache__`, e o programa imprime a mesma saída que na pasta do projeto: os pacotes
foram junto, e os imports funcionam a partir da raiz. Depois, a pasta `conferencia` pode ser
apagada (`cd .. && rm -rf conferencia`).
