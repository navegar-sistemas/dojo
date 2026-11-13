---
sidebar_position: 2
title: Entregar
---

# Entregar

O enunciado pede a entrega num **repositório Git**, com a árvore de arquivos esperada na raiz dele,
e só o que estiver no repositório é avaliado. Dois tipos de arquivo **não** podem ir: nenhum
ambiente virtual e nenhum arquivo `.env`. Também ficam de fora o `poetry.lock`, que não está na
lista do enunciado ([Poetry e pyproject.toml](../02-ex0/07-poetry-e-pyproject.md#o-poetrylock)), a
pasta `experimentos`, as pastas `__pycache__` e a `.mypy_cache`.

## Copiar os arquivos para o repositório

O endereço (a URL) do repositório de entrega vem junto com o projeto. O `git clone` e o
`git push` podem pedir login ou uma **chave SSH**, conforme o servidor do repositório. Uma chave
SSH é um par de arquivos que identifica o seu computador para o servidor, no lugar de uma senha;
quem fornece o repositório explica como criar a chave e cadastrá-la no servidor. A partir da
pasta `the-codex`, suba um nível, baixe o repositório numa pasta `entrega` e copie para ela só os
arquivos da entrega:

```bash
cd ..
git clone <endereço-do-repositório> entrega
mkdir -p entrega/ex0 entrega/ex1
cp the-codex/ex0/construct.py the-codex/ex0/loading.py the-codex/ex0/pyproject.toml the-codex/ex0/requirements.txt entrega/ex0/
cp the-codex/ex1/oracle.py the-codex/ex1/requirements.txt the-codex/ex1/.env.example the-codex/ex1/.gitignore entrega/ex1/
cp -R the-codex/alchemy entrega/
rm -rf entrega/alchemy/__pycache__ entrega/alchemy/*/__pycache__
cp the-codex/elements.py the-codex/ft_*.py entrega/
cd entrega
```

- troque `<endereço-do-repositório>` pelo endereço recebido. O `git clone` baixa o repositório
  para a pasta `entrega`. Se a pasta do projeto tem outro nome, troque `the-codex` pelo nome da
  sua pasta nos comandos `cp`;
- o `mkdir -p` cria as pastas `ex0` e `ex1` (o `-p` não reclama se elas já existirem);
- os arquivos de `ex0` e `ex1` são copiados um a um, pelo nome: assim o `poetry.lock` e o `.env`
  ficam para trás. Um `cp the-codex/ex1/*` não serviria, porque o `*` não pega os nomes que começam
  com ponto, como `.gitignore` e `.env.example`;
- `cp -R` copia a pasta `alchemy` inteira, e o `rm -rf` apaga dela as pastas `__pycache__` que o
  Python criou ao importar os módulos (a do `alchemy` e as dos dois subpacotes);
- o último `cp` copia o `elements.py` e os seis `ft_*.py` da raiz.

## Conferir antes de registrar

```bash
git status --short --untracked-files=all
```

```text
?? alchemy/__init__.py
?? alchemy/elements.py
?? alchemy/grimoire/__init__.py
?? alchemy/grimoire/dark_spellbook.py
?? alchemy/grimoire/dark_validator.py
?? alchemy/grimoire/light_spellbook.py
?? alchemy/grimoire/light_validator.py
?? alchemy/potions.py
?? alchemy/transmutation/__init__.py
?? alchemy/transmutation/recipes.py
?? elements.py
?? ex0/construct.py
?? ex0/loading.py
?? ex0/pyproject.toml
?? ex0/requirements.txt
?? ex1/.env.example
?? ex1/.gitignore
?? ex1/oracle.py
?? ex1/requirements.txt
?? ft_alembic_0.py
?? ft_alembic_1.py
?? ft_distillation_0.py
?? ft_kaboom_0.py
?? ft_kaboom_1.py
?? ft_transmutation_0.py
```

Os 25 arquivos da árvore do enunciado, todos novos (`??`), e nada mais: nenhum `.env`, nenhum
ambiente virtual, nenhum `__pycache__`. Num repositório de entrega que já tinha arquivos de antes,
eles também aparecem, com outras marcas.

## Registrar e enviar

Cada registro do git leva o nome e o e-mail de quem o fez. Diga ao git quem você é, dentro do
repositório de entrega, antes do primeiro registro:

```bash
git config user.name "Seu Nome"
git config user.email "voce@exemplo.com"
```

Troque pelo seu nome e pelo seu e-mail. Os dois comandos não imprimem nada; sem `--global`, a
configuração vale só para este repositório. Depois, registre e envie:

```bash
git add .
git commit -m "Add The Codex exercises 0 to 4"
git push
```

- `git add .` marca para o próximo registro tudo o que está na pasta (o ponto), menos o que algum
  `.gitignore` manda ignorar; não imprime nada;
- `git commit` registra os arquivos marcados, com a mensagem do `-m`, e mostra um resumo:

  ```text
  [main (root-commit) 1e44538] Add The Codex exercises 0 to 4
   25 files changed, 376 insertions(+)
  ```

  seguido de uma linha `create mode` por arquivo. `main` é o **ramo** (*branch*), a linha de
  histórico onde o registro entra (pode ser `master`, conforme o servidor); `root-commit` aparece
  só no primeiro registro do repositório; o código de sete caracteres identifica o registro e muda
  a cada vez;
- `git push` envia o registro para o repositório de entrega.

Sem os dois `git config`, conforme a máquina, o git recusa o registro com
`Please tell me who you are` ("diga quem você é"), ou registra assim mesmo, com um nome e um
e-mail montados a partir do seu usuário e do nome da máquina. No macOS, sem nenhuma configuração,
acontece o segundo: o resumo vem junto de uma mensagem que começa com

```text
Your name and email address were configured automatically based
on your username and hostname. Please check that they are accurate.
```

("o seu nome e o seu e-mail foram configurados automaticamente a partir do seu usuário e do nome
da máquina; confira se estão certos"). Essa mensagem é o sinal de que o registro saiu com a
identidade errada. Rode os dois `git config` e corrija o último registro, antes do `git push`:

```bash
git commit --amend --reset-author --no-edit
```

`--amend` refaz o último registro, `--reset-author` troca o autor pela identidade configurada
agora, e `--no-edit` mantém a mensagem. O comando mostra o resumo de novo, já sem o aviso.

## Conferir o que foi enviado

O que conta é o que está **no repositório**, não na sua pasta. Baixe uma cópia nova numa pasta à
parte e sele um laboratório novo nela, como a avaliação pode pedir:

```bash
cd ..
git clone <endereço-do-repositório> conferencia
cd conferencia
python3 -m venv lab_env
lab_env/bin/python -m pip install -r ex0/requirements.txt -r ex1/requirements.txt
lab_env/bin/python ex0/loading.py
python3 ft_kaboom_0.py
```

O `pip install` aceita vários `-r`, um por arquivo. O `loading.py` termina com
`All reagents present and accounted for.`, e o `ft_kaboom_0.py` registra o feitiço, como na pasta
do projeto. Depois, a pasta `conferencia` pode ser apagada (`cd .. && rm -rf conferencia`).
