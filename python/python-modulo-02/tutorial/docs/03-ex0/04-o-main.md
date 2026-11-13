---
sidebar_position: 4
title: O main
---

# O main

Definir funções não as executa: o arquivo precisa chamar `test_temperature()` quando é rodado. O
jeito costumeiro em Python é este bloco, no fim do arquivo:

```python
if __name__ == "__main__":
    test_temperature()
```

`__name__` é uma variável que o Python cria em todo arquivo:

- quando o arquivo é **rodado** (`python3 ex0/ft_first_exception.py`), ela vale `"__main__"`;
- quando o arquivo é **importado** por outro, ela vale o nome do arquivo sem o `.py`,
  `"ft_first_exception"`.

**Importar** é carregar um arquivo `.py` de dentro de outro código, para usar as funções dele.
Num programa que está na mesma pasta, a linha `import ft_first_exception` (o nome do arquivo sem
o `.py`) executa o arquivo inteiro e deixa as funções dele disponíveis. A página de
conferência do [exercício 1](../04-ex1/06-rodar-e-conferir.md) usa uma variante,
`from ... import ...`, que traz só uma função.

Na importação, o arquivo inteiro roda, mas o `if __name__ == "__main__":` dá falso, porque ali
`__name__` vale `"ft_first_exception"`: as funções ficam definidas e o teste não roda.

Com o `if`, o teste roda quando o arquivo é executado e não roda quando outro código só quer
usar `input_temperature`. Esse trecho é chamado de **main** ("principal"), a parte que o arquivo
executa por conta própria; o enunciado usa esse nome nos exercícios seguintes.
