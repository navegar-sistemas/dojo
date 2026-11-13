---
sidebar_position: 8
title: Rodar e conferir
---

# Rodar e conferir

## Rodar como no enunciado

```bash
python3 ex1/ft_archive_creation.py ancient_fragment.txt
```

O programa mostra o texto, o texto transformado e para em `Enter new file name (or empty):`. Digite
`new_fragment.txt` e aperte Enter. As últimas linhas são:

```text
Enter new file name (or empty): new_fragment.txt
Saving data to 'new_fragment.txt'
Data saved in file 'new_fragment.txt'.
```

```bash
cat new_fragment.txt
```

```text
[FRAGMENT 001] Digital preservation protocols established 2087#
[FRAGMENT 002] Knowledge must survive the entropy wars#
[FRAGMENT 003] Every byte saved is a victory against oblivion#
```

Rode de novo e aperte Enter sem digitar nada: a última linha é `Not saving data.`

## Comparar sem digitar

Para conferir com `diff`, a resposta precisa vir pronta, sem ninguém digitar. O comando
`printf 'texto'` imprime o texto, e a barra `|` (o *pipe*) entrega o que um comando imprime como se
fosse digitado no programa seguinte. `\n` no `printf` é o Enter:

```bash
diff <(printf '\n' | python3 ex1/ft_archive_creation.py ancient_fragment.txt) - <<'FIM'
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
Enter new file name (or empty): Not saving data.
FIM
```

Sem nenhuma linha impressa, a saída é a esperada. Uma diferença em relação ao terminal: a resposta
não aparece depois da pergunta, e `Not saving data.` sai na mesma linha. O que se digita no terminal
aparece na tela porque o **terminal** o mostra enquanto se digita; o programa nunca imprime a
resposta. Com o `printf`, ninguém digitou, e nada aparece.

Gravando, e conferindo o arquivo gravado:

```bash
printf 'new_fragment.txt\n' | python3 ex1/ft_archive_creation.py ancient_fragment.txt | tail -n 2
diff new_fragment.txt - <<'FIM'
[FRAGMENT 001] Digital preservation protocols established 2087#
[FRAGMENT 002] Knowledge must survive the entropy wars#
[FRAGMENT 003] Every byte saved is a victory against oblivion#
FIM
```

```text
Enter new file name (or empty): Saving data to 'new_fragment.txt'
Data saved in file 'new_fragment.txt'.
```

`tail -n 2` mostra só as duas últimas linhas da saída. O `diff` não imprime nada. Como o arquivo já
existia da rodada anterior, isso também mostra que ele foi **substituído**: se o texto novo tivesse
sido acrescentado ao antigo, o arquivo teria seis linhas e o `diff` acusaria.

## As falhas

Um arquivo de leitura que não existe para tudo logo no começo, sem pergunta:

```bash
python3 ex1/ft_archive_creation.py foo
```

```text
=== Cyber Archives Recovery & Preservation ===
Accessing file 'foo'
Error opening file 'foo': [Errno 2] No such file or directory: 'foo'
```

Para a gravação falhar por falta de permissão, crie um arquivo que ninguém pode alterar:

```bash
echo sealed > vault.txt
chmod 444 vault.txt
```

`444` é `r--r--r--`: todos só leem, e nem o dono escreve
([Permissões](../02-arquivos/05-quando-o-open-falha.md#permissões)). O enunciado usa como exemplo o
`/etc/passwd`, o arquivo de contas do sistema. No macOS, tentar gravar nele abre uma janela do
sistema pedindo para "administrar o computador"; o `vault.txt` dá a mesma falha, `[Errno 13]`, no
Linux e no macOS, sem tocar em arquivo do sistema.

Gravar no `vault.txt`, gravar no "disco cheio" `/dev/full` (só existe no Linux) e uma entrada que
acaba sem Enter (`< /dev/null` faz o programa ler de um arquivo vazio):

```bash
printf 'vault.txt\n' | python3 ex1/ft_archive_creation.py ancient_fragment.txt | tail -n 3
printf '/dev/full\n' | python3 ex1/ft_archive_creation.py ancient_fragment.txt | tail -n 3
python3 ex1/ft_archive_creation.py ancient_fragment.txt < /dev/null | tail -n 2
```

```text
Enter new file name (or empty): Saving data to 'vault.txt'
Error opening file 'vault.txt': [Errno 13] Permission denied: 'vault.txt'
Data not saved.
Enter new file name (or empty): Saving data to '/dev/full'
Error writing file '/dev/full': [Errno 28] No space left on device
Data not saved.
Enter new file name (or empty): 
Not saving data.
```

No caso do `/dev/full`, o `open()` deu certo e a falha veio ao gravar, capturada pelo `try` de fora
([Gravar o arquivo](./05-gravar-o-arquivo.md)). No macOS, onde `/dev/full` não existe, o sistema não
deixa criar o arquivo na pasta `/dev`, e a falha vem já no `open()`:
`Error opening file '/dev/full': [Errno 1] Operation not permitted: '/dev/full'`. No último, o
`EOFError` virou resposta vazia ([Pedir o nome](./04-pedir-o-nome.md)).

## Conferir estilo e tipos

```bash
.venv/bin/flake8 ex1
.venv/bin/mypy --disallow-untyped-defs ex1
```

```text
Success: no issues found in 1 source file
```
