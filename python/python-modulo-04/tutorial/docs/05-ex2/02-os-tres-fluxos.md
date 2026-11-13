---
sidebar_position: 2
title: Os três fluxos
---

# Os três fluxos

Todo programa começa com três canais de comunicação já abertos, chamados **fluxos** (*streams*).
Cada um tem um número, o **descritor**, e um nome:

| Descritor | Nome | Em Python | Para quê |
|---|---|---|---|
| 0 | entrada padrão (*standard input*) | `sys.stdin` | o que o programa lê; normalmente, o teclado |
| 1 | saída padrão (*standard output*) | `sys.stdout` | os resultados do programa; normalmente, o terminal |
| 2 | saída de erro (*standard error*) | `sys.stderr` | os avisos de erro; normalmente, também o terminal |

`input()` lê de `sys.stdin`; `print()` escreve em `sys.stdout`. Os três são objetos arquivo, com os
mesmos métodos de um arquivo aberto com `open()`: `read()`, `readline()`, `write()`, `flush()`.

![À esquerda, python3 programa.py: o teclado entra no programa pelo fluxo 0, stdin; o fluxo 1, stdout, e o fluxo 2, stderr, vão os dois para o terminal. À direita, python3 programa.py 2> erros.txt: o stdin e o stdout continuam iguais, e o stderr vai para o arquivo erros.txt](/img/ex2/os-tres-fluxos.svg)

## Por que duas saídas

Quando as duas saídas vão para o terminal, elas se misturam na tela e parecem uma só. A separação
aparece quando o terminal **redireciona** uma delas: manda para outro lugar o que o programa escreve
num fluxo, sem o programa saber.

Crie `experimentos/fluxos.py`:

```python
import sys

print("to stdout")
print("to stderr", file=sys.stderr)
```

O parâmetro `file` do `print` escolhe onde escrever; sem ele, o `print` escreve em `sys.stdout`.

```bash
python3 experimentos/fluxos.py
```

```text
to stdout
to stderr
```

As duas linhas aparecem. Agora com `>`, que redireciona a saída padrão para um arquivo:

```bash
python3 experimentos/fluxos.py > saida.txt
```

```text
to stderr
```

Só a linha de erro ficou na tela. A outra foi para o arquivo:

```bash
cat saida.txt
```

```text
to stdout
```

`2>` redireciona o fluxo 2, a saída de erro:

```bash
python3 experimentos/fluxos.py 2> erros.txt
cat erros.txt
rm saida.txt erros.txt
```

```text
to stdout
to stderr
```

A primeira linha é a tela; a segunda, o conteúdo de `erros.txt`. O `rm` apaga os dois arquivos do
experimento.

É para isso que a saída de erro existe: quem roda `python3 programa.py > resultado.txt` guarda só o
resultado no arquivo e continua vendo os erros na tela. Um aviso de erro misturado ao resultado iria
parar dentro do arquivo, sem ninguém ver.

## Os redirecionamentos do tutorial

| Escrito no comando | Efeito |
|---|---|
| `> arquivo` | a saída padrão vai para o arquivo, que é criado ou substituído |
| `2> arquivo` | a saída de erro vai para o arquivo |
| `2>&1` | a saída de erro vai para onde a saída padrão estiver indo |
| `> /dev/null` | a saída padrão é descartada; `/dev/null` é um arquivo especial que joga fora tudo o que recebe |
| `< arquivo` | a entrada padrão lê do arquivo, em vez do teclado |
| `comando1 \| comando2` | a saída padrão do primeiro vira a entrada padrão do segundo (o *pipe*) |
