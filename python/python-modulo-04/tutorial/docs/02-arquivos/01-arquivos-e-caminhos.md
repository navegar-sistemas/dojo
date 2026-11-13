---
sidebar_position: 1
title: Arquivos e caminhos
---

# Arquivos e caminhos

Para abrir um arquivo, o programa precisa dizer **qual** arquivo, pelo nome.

## Arquivo e pasta

Um **arquivo** é um conjunto de dados guardado no disco, com um nome. Os arquivos ficam dentro de
**pastas** (também chamadas de **diretórios**), e as pastas ficam dentro de outras pastas. A pasta
mais de fora de todas é a **raiz**, escrita `/`.

## O caminho

O **caminho** (*path*) de um arquivo é a sequência de pastas até ele, separadas por `/`. Há dois
tipos:

- **caminho absoluto**: começa com `/` e parte da raiz. `/etc/sudoers` é o arquivo `sudoers`, dentro
  da pasta `etc`, dentro da raiz. Ele aponta para o mesmo arquivo de qualquer lugar;
- **caminho relativo**: não começa com `/` e parte da **pasta atual**, a pasta em que o terminal
  está. `ancient_fragment.txt` é "o arquivo com esse nome na pasta atual"; `ex0/ft_ancient_text.py`
  é "o arquivo `ft_ancient_text.py` dentro da pasta `ex0` da pasta atual".

O comando `pwd` mostra a pasta atual. Na pasta do projeto:

```bash
pwd
```

```text
/…/data-archivist
```

(No lugar de `/…`, aparece o caminho da pasta na sua máquina.)

## O mesmo nome, outra pasta atual

Um caminho relativo muda de sentido quando a pasta atual muda. Entre na pasta `ex0` e peça o arquivo
pelo mesmo nome:

```bash
cd ex0
cat ancient_fragment.txt
```

```text
cat: ancient_fragment.txt: No such file or directory
```

"Arquivo ou pasta inexistente": dentro de `ex0` não há nenhum `ancient_fragment.txt`. O nome
especial `..` quer dizer "a pasta de cima", e com ele o arquivo é encontrado:

```bash
cat ../ancient_fragment.txt
cd ..
```

```text
[FRAGMENT 001] Digital preservation protocols established 2087
[FRAGMENT 002] Knowledge must survive the entropy wars
[FRAGMENT 003] Every byte saved is a victory against oblivion
```

O `cd ..` volta para a pasta `data-archivist`.

Um programa Python segue a mesma regra: um caminho relativo passado ao `open()` parte da pasta atual
do terminal que rodou o programa, e **não** da pasta onde o arquivo `.py` está. Por isso todos os
comandos do tutorial são rodados a partir da pasta `data-archivist`, onde fica o
`ancient_fragment.txt`.
