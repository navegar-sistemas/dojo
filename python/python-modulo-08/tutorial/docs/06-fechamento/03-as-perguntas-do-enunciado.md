---
sidebar_position: 3
title: As perguntas do enunciado
---

# As perguntas do enunciado

O capítulo de entrega do enunciado diz que, na avaliação entre pares, você vai demonstrar quatro
coisas: o entendimento dos ambientes virtuais e da importância deles, as diferenças entre o pip e
o Poetry, como as variáveis de ambiente deixam uma aplicação segura e configurável, e a
capacidade de explicar tudo isso a outros aprendizes. O exercício 2 acrescenta uma quinta: saber
explicar por que o `.env` fica no `.gitignore`. E o exercício 0 avisa que você precisa saber
criar um ambiente virtual novo durante a avaliação, se for preciso.

## O que é um ambiente virtual, e por que importa?

Um ambiente virtual é uma pasta com um Python próprio (um atalho para o Python global) e um
`site-packages` só dele ([O ambiente virtual por dentro](../02-conceitos/02-o-ambiente-virtual-por-dentro.md)).
Ele importa porque:

- **isola os projetos**: cada projeto instala as versões de que precisa sem afetar os outros nem
  o Python do sistema, que muitos sistemas nem deixam alterar
  ([O Python do sistema recusa](../02-conceitos/01-pacotes-e-o-pip.md#o-python-do-sistema-recusa));
- **é descartável e reproduzível**: apagar a pasta apaga tudo o que foi instalado nela, e
  `python3 -m venv` mais o arquivo de dependências recriam o mesmo ambiente em qualquer máquina;
- **não vai para o repositório**: tem milhares de arquivos e caminhos da máquina onde foi criado.
  Vai a receita (o `requirements.txt` ou o `pyproject.toml`), e cada um recria o seu.

Para mostrar ao vivo: o `construct.py` fora e dentro do `matrix_env`, e dentro sem ativar
([Rodar e conferir do exercício 0](../03-ex0/07-rodar-e-conferir.md)). O ponto central é que
`sys.prefix` muda e `sys.base_prefix` não.

## Quais são as diferenças entre o pip e o Poetry?

O pip é um instalador; o Poetry, um gerenciador de projetos
([pip e Poetry](../04-ex1/02-pip-e-poetry.md)):

| | pip | Poetry |
|---|---|---|
| arquivo | `requirements.txt` | `pyproject.toml` |
| versões exatas | não guarda (só com `pip freeze`, à mão) | guarda no `poetry.lock`, para cada versão de Python |
| ambiente virtual | você cria e ativa | o Poetry cria e usa |
| comandos | `pip install -r requirements.txt` e `python3 loading.py` | `poetry install` e `poetry run python loading.py` |

Para mostrar ao vivo: o `loading.py` num venv vazio, depois com o `pip install -r` e depois com o
`poetry run` ([Rodar com o pip](../04-ex1/10-rodar-com-pip.md),
[Rodar com o Poetry](../04-ex1/11-rodar-com-poetry.md)); o `grep` das três versões do numpy no
`poetry.lock` mostra o que o pip não guarda. A saída do caso sem bibliotecas resume a diferença
nas próprias instruções ([As instruções de instalação](../04-ex1/06-as-instrucoes-de-instalacao.md)).

## Como as variáveis de ambiente deixam a aplicação segura e configurável?

- **configurável**: o mesmo `oracle.py` roda em desenvolvimento e em produção; muda só o ambiente
  ([Variáveis de ambiente](../02-conceitos/04-variaveis-de-ambiente.md)). Uma variável na linha de
  comando sobrepõe o `.env` sem editar nada
  ([Quem vale mais](../05-ex2/02-o-arquivo-env.md#quem-vale-mais));
- **segura**: senhas e chaves ficam fora do código e, portanto, fora do repositório. Quem lê o
  código não conhece a chave, e trocar uma chave vazada não exige mudar o programa;
- **à prova de esquecimento**: sem valores padrão no código, uma variável que falta é acusada
  pelo nome, e o programa não roda com um valor que ninguém escolheu
  ([Sem valores padrão](../05-ex2/04-ler-a-configuracao.md#sem-valores-padrão)).

Para mostrar ao vivo: o `oracle.py` sem configuração, com o `.env`, com
`MATRIX_MODE=production API_KEY=secret123` e com a produção completa
([Rodar e conferir do exercício 2](../05-ex2/10-rodar-e-conferir.md)).

## Por que o .env fica no .gitignore?

Porque ele guarda segredos, como a `API_KEY`. Tudo o que entra num repositório Git fica no
histórico para sempre: apagar o arquivo num registro seguinte não o tira dos registros antigos, e
qualquer pessoa que tenha uma cópia do repositório consegue lê-lo. Um segredo que vazou assim
precisa ser trocado. Com o `.env` no `.gitignore`, o Git o ignora mesmo num `git add` da pasta
inteira ([O .env nunca entra](./02-entregar.md#o-env-nunca-entra)). O que vai para o repositório
é o `.env.example`, com os nomes das variáveis e sem os segredos.

## Explicar a outros aprendizes

Os programas foram feitos para isso: cada um demonstra a sua ferramenta na própria saída. Uma
ordem que funciona: rodar o `construct.py` fora e dentro do venv; rodar o `loading.py` num venv
vazio e depois instalar; rodar o `oracle.py` sem `.env`, com `.env` e em produção. A cada passo,
a pergunta é a mesma: **de onde** o programa tirou o que mostrou (qual Python, qual
`site-packages`, qual variável).

## Recriar tudo a partir da entrega

O repositório tem só os oito arquivos; para rodar os programas a partir dele, os ambientes são
recriados em cada pasta de exercício, com os comandos já rodados no tutorial:

| Exercício | Comandos | Onde foram rodados |
|---|---|---|
| 0 | `python3 -m venv matrix_env`, `source matrix_env/bin/activate`, `python3 construct.py` | [Rodar e conferir](../03-ex0/07-rodar-e-conferir.md#dentro-do-venv) |
| 1 (pip) | `python3 -m venv matrix_env`, `source matrix_env/bin/activate`, `pip install -r requirements.txt`, `python3 loading.py` | [Rodar com o pip](../04-ex1/10-rodar-com-pip.md#todas-as-bibliotecas) |
| 1 (Poetry) | `../.venv/bin/poetry install`, `../.venv/bin/poetry run python loading.py` (o Poetry do `.venv` das ferramentas), sem nenhum ambiente ativado | [Rodar com o Poetry](../04-ex1/11-rodar-com-poetry.md) |
| 2 | `python3 -m venv matrix_env`, `source matrix_env/bin/activate`, `pip install -r requirements.txt`, `cp .env.example .env`, preencher a `API_KEY`, `python3 oracle.py` | [Rodar e conferir](../05-ex2/10-rodar-e-conferir.md#o-env-preenchido) |
