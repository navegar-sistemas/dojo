---
sidebar_position: 6
title: O erro proposital do mypy
---

# O erro proposital do mypy

O teste pedido pelo enunciado chama `ingest` com um dado inválido, sem validar antes, para mostrar
que a exceção acontece. No teste do Numeric Processor, a chamada é:

```python
processor.ingest("foo")
```

A assinatura de `NumericProcessor.ingest` diz que ele recebe `int | float | list[int | float]`, e
`"foo"` é um `str`. O mypy confere os tipos **sem rodar** o programa e acusa a chamada. Com o
arquivo completo, o comando `.venv/bin/mypy --disallow-untyped-defs ex0` da página
[Rodar e conferir](./09-rodar-e-conferir.md) mostra:

```text
ex0/data_processor.py:111: error: Argument 1 to "ingest" of "NumericProcessor" has incompatible type "str"; expected "int | float | list[int | float]"  [arg-type]
Found 1 error in 1 file (checked 1 source file)
```

"O argumento 1 de `ingest` tem o tipo incompatível `str`; o esperado era
`int | float | list[int | float]`". É a assinatura específica de `ingest` fazendo o seu trabalho:
o erro foi achado antes de o programa rodar.

O enunciado avisa que esse teste deixa um aviso do mypy **de propósito**. Como o teste precisa
mostrar a exceção acontecendo de verdade, a chamada fica no código. Esta é a **única**
reclamação aceita do mypy em todo o projeto: qualquer outra precisa ser corrigida. O número da
linha, `111`, é o da chamada `processor.ingest("foo")` no
[arquivo completo](./08-o-arquivo-completo.md).

O flake8 não confere tipos, então para ele o arquivo está limpo.

Os exercícios 1 e 2 não repetem esse teste, e o mypy não acusa nada neles.
