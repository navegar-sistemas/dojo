---
sidebar_position: 6
title: Os argumentos do terminal
---

# Os argumentos do terminal

Os exercícios 0, 1 e 2 recebem o nome do arquivo no próprio comando que roda o programa:
`python3 ex0/ft_ancient_text.py ancient_fragment.txt`. O programa recebe esse nome pelo módulo
`sys`.

## import sys

`sys` é um **módulo** que vem com o Python: um conjunto de valores e funções ligados ao programa em
execução. Um módulo entra no programa com `import`, no topo do arquivo, e os nomes dele são usados
com ponto: `sys.argv`, `sys.stdout`.

## sys.argv

`sys.argv` é uma lista de `str` com as palavras do comando, a partir do nome do programa. Cada
palavra é um **argumento**. Crie `experimentos/argumentos.py`:

```python
import sys

print(sys.argv)
print(len(sys.argv))
```

Rode sem argumento, com um, e com um nome que tem espaço, sem e com aspas:

```bash
python3 experimentos/argumentos.py
python3 experimentos/argumentos.py ancient_fragment.txt
python3 experimentos/argumentos.py my file.txt
python3 experimentos/argumentos.py "my file.txt"
```

```text
['experimentos/argumentos.py']
1
['experimentos/argumentos.py', 'ancient_fragment.txt']
2
['experimentos/argumentos.py', 'my', 'file.txt']
3
['experimentos/argumentos.py', 'my file.txt']
2
```

- `sys.argv[0]` é sempre o caminho do programa, escrito do jeito que foi digitado no comando;
- os argumentos de verdade começam em `sys.argv[1]`;
- `len(sys.argv)` conta todos, incluindo o `[0]`: um programa que espera exatamente um nome de
  arquivo espera `len(sys.argv) == 2`;
- o terminal separa os argumentos nos espaços. Um nome com espaço vai entre aspas para chegar como
  um argumento só.
