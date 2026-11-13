---
sidebar_position: 1
title: O problema
---

# O problema

O exercício 1 recupera o texto do mesmo jeito que o exercício 0, transforma o texto e grava o
resultado num arquivo novo, com o nome que a pessoa digitar.

## O que o enunciado pede

Um arquivo `ex1/ft_archive_creation.py` que parte do código do exercício 0 e, depois de mostrar o
arquivo:

- acrescenta um `#` no fim de cada linha;
- mostra o texto novo;
- pergunta o nome do arquivo onde gravar; uma resposta vazia quer dizer "não gravar";
- se um nome foi digitado, grava o texto novo nele e mostra uma mensagem final. O arquivo é
  **criado** se não existir e **substituído** se já existir.

À lista do exercício 0 somam-se dois autorizados: `write()`, para escrever no arquivo, e `input()`,
para ler o que a pessoa digita.

## A saída esperada

O cabeçalho muda para `=== Cyber Archives Recovery & Preservation ===`. Depois do
`File 'ancient_fragment.txt' closed.`, vêm uma linha vazia, o texto transformado e a pergunta:

```text
=== Cyber Archives Recovery & Preservation ===
Accessing file 'ancient_fragment.txt'
---

[FRAGMENT 001] Digital preservation protocols established 2087
[FRAGMENT 002] Knowledge must survive the entropy wars
[FRAGMENT 003] Every byte saved is a victory against oblivion

---
File 'ancient_fragment.txt' closed.

Transform data:
---

[FRAGMENT 001] Digital preservation protocols established 2087#
[FRAGMENT 002] Knowledge must survive the entropy wars#
[FRAGMENT 003] Every byte saved is a victory against oblivion#

---
Enter new file name (or empty):
```

O programa para nessa linha e espera. Com Enter sem nada digitado:

```text
Enter new file name (or empty):
Not saving data.
```

Com um nome:

```text
Enter new file name (or empty): new_fragment.txt
Saving data to 'new_fragment.txt'
Data saved in file 'new_fragment.txt'.
```

E o arquivo novo contém o texto transformado:

```text
[FRAGMENT 001] Digital preservation protocols established 2087#
[FRAGMENT 002] Knowledge must survive the entropy wars#
[FRAGMENT 003] Every byte saved is a victory against oblivion#
```

Quando a gravação falha, o enunciado mostra (no exercício 2) a mensagem `Data not saved.` depois do
erro.

## A estrutura do programa

O arquivo mantém `display` e `recover_archive` do exercício 0, com uma mudança, e ganha três
funções:

| Função | O que faz |
|---|---|
| `recover_archive(file_name)` | o mesmo do exercício 0, mas agora **devolve** o texto lido |
| `transform(content)` | devolve o texto com um `#` no fim de cada linha |
| `ask_file_name()` | pergunta o nome do arquivo e devolve a resposta |
| `save_archive(file_name, content)` | grava o texto no arquivo e diz se deu certo |
