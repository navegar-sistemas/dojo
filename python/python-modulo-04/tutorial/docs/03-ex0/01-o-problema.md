---
sidebar_position: 1
title: O problema
---

# O problema

O primeiro programa faz o trabalho do comando `cat`: recebe o nome de um arquivo no terminal e
mostra o conteúdo dele. A diferença é o tratamento das falhas: em vez da mensagem de erro do Python,
o programa explica o que aconteceu e termina normalmente.

## O que o enunciado pede

Um arquivo `ex0/ft_ancient_text.py` que:

- pega o nome de um arquivo da linha de comando ([Os argumentos do
  terminal](../02-arquivos/06-os-argumentos-do-terminal.md));
- lê o conteúdo do arquivo e o mostra como o `cat` mostraria, com um cabeçalho e um rodapé;
- trata os casos de falha: arquivo inexistente, arquivo inacessível e outros.

O programa só pode usar `import sys`, `sys.argv`, `len()`, `open()`, `import typing`, `typing.IO`,
`read()`, `close()` e `print()`. O enunciado também pergunta qual é o tipo do dado devolvido por
`open()`; a resposta está em [open e o objeto
arquivo](../02-arquivos/02-open-e-o-objeto-arquivo.md).

## A saída esperada

Sem o nome do arquivo, o programa mostra como deve ser usado:

```text
Usage: ex0/ft_ancient_text.py <file>
```

Com um arquivo que não existe:

```text
=== Cyber Archives Recovery ===
Accessing file 'foo'
Error opening file 'foo': [Errno 2] No such file or directory: 'foo'
```

Com um arquivo sem permissão de leitura:

```text
=== Cyber Archives Recovery ===
Accessing file '/etc/sudoers'
Error opening file '/etc/sudoers': [Errno 13] Permission denied: '/etc/sudoers'
```

Com um arquivo que pode ser lido:

```text
=== Cyber Archives Recovery ===
Accessing file 'ancient_fragment.txt'
---

[FRAGMENT 001] Digital preservation protocols established 2087
[FRAGMENT 002] Knowledge must survive the entropy wars
[FRAGMENT 003] Every byte saved is a victory against oblivion

---
File 'ancient_fragment.txt' closed.
```

O conteúdo fica entre duas linhas `---`, com uma linha vazia de cada lado ([read e o
texto](../02-arquivos/03-read-e-o-texto.md)). A última linha confirma que o arquivo foi fechado.

## A estrutura do programa

O enunciado não fixa funções. A divisão abaixo é escolha do projeto, e o arquivo terá três:

| Função | O que faz |
|---|---|
| `main()` | confere os argumentos, imprime o cabeçalho e chama `recover_archive` |
| `recover_archive(file_name)` | abre, lê, mostra e fecha o arquivo, avisando cada falha |
| `display(content)` | imprime um texto entre as duas linhas `---` |
