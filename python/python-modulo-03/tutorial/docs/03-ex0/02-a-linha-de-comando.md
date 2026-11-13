---
sidebar_position: 2
title: A linha de comando
---

# A linha de comando

O texto digitado no terminal para rodar um programa se chama **linha de comando**. Quem lê esse
texto é o **shell**, o programa que roda dentro do terminal, interpreta cada comando e inicia os
outros programas (no Linux, normalmente o `bash`). O shell corta a linha nos espaços: cada pedaço
depois do nome do programa vira um **argumento**. Para que um
texto com espaço chegue como um argumento só, ele vai entre aspas: `"Data Quest"` é um argumento,
e `Data Quest` sem aspas seriam dois.

## O módulo sys e a lista sys.argv

O Python entrega a linha de comando ao programa numa **lista** chamada `sys.argv`. Ela fica no
módulo `sys` (de *system*, "sistema"), um dos módulos que vêm com o Python. Para usá-lo, o
arquivo começa com:

```python
import sys
```

`import sys` carrega o módulo, e daí em diante `sys.argv` está disponível. O nome `argv` vem da
linguagem C, onde os argumentos chegam ao programa numa sequência de textos com esse nome (de
*argument vector*, "vetor de argumentos").

```python title="experimentos/argumentos.py"
import sys

print(sys.argv)
print(len(sys.argv))
```

```bash
python3 experimentos/argumentos.py hello world 42
python3 experimentos/argumentos.py "Data Quest"
python3 experimentos/argumentos.py
```

```text
['experimentos/argumentos.py', 'hello', 'world', '42']
4
['experimentos/argumentos.py', 'Data Quest']
2
['experimentos/argumentos.py']
1
```

Uma lista impressa aparece entre colchetes, com os elementos separados por vírgula. Três coisas
nessa saída:

- a primeira posição é sempre o **nome do programa**; os argumentos vêm depois. Por isso uma lista
  sem argumentos ainda tem um elemento;
- todo elemento é **texto**: o `42` chegou como `'42'`, entre aspas, e não como o número 42. As
  aspas simples são o jeito do Python mostrar um texto dentro de uma lista;
- as aspas de `"Data Quest"` não chegaram ao programa: o shell as usou para juntar as duas
  palavras e as tirou.

## O nome do programa

A primeira posição guarda o nome do programa **do jeito que foi digitado**. Rodado de fora da
pasta, como acima, o nome inclui a pasta: `experimentos/argumentos.py`. Rodado de dentro da pasta,
fica só o nome do arquivo:

```bash
cd experimentos
python3 argumentos.py hello
cd ..
```

```text
['argumentos.py', 'hello']
2
```

O enunciado roda o programa de dentro da pasta `ex0`, e é por isso que a saída dele mostra
`Program name: ft_command_quest.py`, sem a pasta. Rodado de dentro de `ex0`, o exercício imprime
o nome igual ao do enunciado.
