---
sidebar_position: 1
title: O programa que trava
---

# O programa que trava

O enunciado exige que os programas **nunca travem**. Antes de evitar o travamento, é preciso
vê-lo acontecer. Crie `experimentos/trava.py`:

```python
print("Before the error")
temperature = int("abc")
print("After the error")
```

`int()` converte um texto num número inteiro: `int("25")` dá `25`. Mas `"abc"` não é um número.
Rode:

```bash
python3 experimentos/trava.py
```

```text
Before the error
Traceback (most recent call last):
  File "/…/garden-guardian/experimentos/trava.py", line 2, in <module>
    temperature = int("abc")
ValueError: invalid literal for int() with base 10: 'abc'
```

(No lugar de `/…`, aparece o caminho da pasta na sua máquina. Dependendo da versão do Python,
pode aparecer também uma linha de marcas `^` sob o código; a página
[A exceção sobe](./05-a-excecao-sobe.md) explica essas marcas.)

A primeira linha foi impressa. Na segunda, o `int("abc")` não conseguiu fazer o seu trabalho, e o
Python **parou o programa ali**: a terceira linha, `After the error`, nunca foi impressa. Em vez
dela, apareceu um relatório de erro.

Isso é **travar**: o programa termina no meio, por causa de um erro que ninguém tratou. O
terminal também fica sabendo que algo deu errado. Logo depois de rodar, o comando `echo $?`
mostra o **código de saída** do último programa, um número que ele devolve ao terminal ao
terminar:

```bash
echo $?
```

```text
1
```

`0` quer dizer "terminou bem"; qualquer outro número quer dizer "terminou com erro". O programa
que trava termina com `1`.

A [próxima página](./02-lendo-o-traceback.md) lê esse relatório linha por linha.
