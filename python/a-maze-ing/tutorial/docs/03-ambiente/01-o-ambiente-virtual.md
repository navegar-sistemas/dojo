---
sidebar_position: 1
title: O ambiente virtual
---

# O ambiente virtual

Antes do primeiro arquivo de código, o projeto precisa de três ferramentas instaladas: o
**flake8** e o **mypy**, que verificam o código, e o **build**, que monta o pacote do gerador.
Esta página mostra onde instalá-las sem mexer no resto do computador.

## O problema de instalar no Python do sistema

O computador já tem um Python instalado, o **Python do sistema**, usado por todos os projetos e,
às vezes, pelo próprio sistema operacional. O `pip` (o programa que baixa e instala bibliotecas
Python) instalaria as ferramentas ali, e isso causa três problemas:

- outro projeto pode precisar de uma versão diferente do flake8, e instalar uma apaga a outra;
- em várias distribuições Linux, instalar no Python do sistema é até bloqueado, e o `pip`
  recusa com o erro `externally-managed-environment`;
- a máquina do avaliador pode ter outra versão do mypy, ou nenhuma, e o resultado do lint mudaria
  de uma máquina para a outra.

## O que é um ambiente virtual

Um **ambiente virtual** (*virtual environment*, ou **venv**) é uma pasta com um Python próprio e
um `pip` próprio. O que se instala com esse `pip` fica só dentro da pasta: não mexe no Python do
sistema nem nos outros projetos. Apagar a pasta desfaz tudo.

O projeto usa uma pasta chamada `.venv`, na raiz:

```bash
python3 -m venv .venv
```

- `python3` é o Python do sistema, usado só para criar o ambiente;
- `-m venv` executa o módulo `venv`, que vem com o Python e cria ambientes virtuais;
- `.venv` é o nome da pasta. O ponto no começo do nome a esconde do `ls` comum, porque ninguém
  precisa abri-la à mão.

Depois desse comando, a pasta tem, entre outros arquivos, `.venv/bin/python` e `.venv/bin/pip`.
Instalar as ferramentas com esse Python as coloca dentro da pasta. O comando seria este, mas
**não o rode agora**: ele aparece só para mostrar a ideia. Quem instala de verdade é o
`make install`, escrito [duas páginas adiante](./02-makefile-instalar-e-rodar.md), que faz o
mesmo com as versões de cada ferramenta fixadas.

```bash
.venv/bin/python -m pip install flake8 mypy build
```

`.venv/bin/python -m pip` quer dizer "o `pip` deste Python". Assim não há dúvida sobre onde a
instalação vai parar.

O enunciado do projeto recomenda exatamente isso: usar um ambiente virtual (ele cita `venv` ou
`conda`) para isolar as dependências durante o desenvolvimento.

## Sem `activate`

O jeito comum de usar um ambiente virtual é "ativá-lo" com `source .venv/bin/activate`: a partir
daí, o comando `python` daquele terminal passa a ser o do `.venv`. O projeto não depende disso.
O `Makefile` (o arquivo de atalhos, na [próxima página](./10-o-que-e-um-makefile.md))
chama `.venv/bin/python` pelo caminho completo.

Assim, `make lint` usa sempre o Python do `.venv`, com o terminal ativado ou não. E se o `.venv`
ainda não existe, o comando falha na hora:

```text
make: .venv/bin/python: No such file or directory
```

Essa é uma escolha do projeto: não há plano B silencioso que use o Python do sistema quando o
`.venv` falta. Um plano B desses rodaria, sem avisar, outra versão das ferramentas, e um erro de
lint poderia aparecer numa máquina e sumir na outra.

## O que o programa precisa

O programa em si **não tem dependência**: o `mazegen` e o `amazeing` só usam a biblioteca padrão
do Python (os módulos que já vêm com ele). As três ferramentas do `.venv` servem para verificar e
empacotar o código, não para rodá-lo:

| Ferramenta | O que faz | Usada por |
|---|---|---|
| `flake8` | confere o estilo do código | `make lint` e `make lint-strict` |
| `mypy` | confere as anotações de tipo | `make lint` e `make lint-strict` |
| `build` | monta o arquivo do pacote `mazegen` | `make build` |

O flake8 e o mypy são explicados em detalhe na
[página de verificar o código](./03-makefile-limpar-verificar-empacotar.md), e o build na
[página de empacotar](./09-makefile-empacotar.md).

## Começando a pasta do projeto

A entrega é feita num **repositório Git**: uma pasta cujo histórico de versões o Git guarda e
envia para o servidor de entrega. Quem recebe o projeto fornece o endereço (a URL) do
repositório de entrega, que começa vazio. Copie esse endereço e crie a raiz do projeto como um
clone dele:

```bash
git clone <url-do-repositório> a-maze-ing
cd a-maze-ing
```

- `git clone` baixa o repositório e cria a pasta `a-maze-ing` já ligada a ele. É para lá que o
  `git push` do fim do tutorial envia o trabalho
  ([parte 15](../15-fechamento/09-enviar-e-conferir.md)).
- Para praticar sem um repositório de entrega, `mkdir a-maze-ing`, `cd a-maze-ing` e `git init`
  criam uma pasta com um repositório só local; o envio fica para quando houver o endereço.

O `.venv` não precisa ser criado à mão: a regra `install` do `Makefile`, escrita
[duas páginas adiante](./02-makefile-instalar-e-rodar.md#install), faz isso e instala as
ferramentas de uma vez.
