---
sidebar_position: 3
title: O erro proposital do mypy
---

# O erro proposital do mypy

O mypy confere os tipos **sem rodar** o programa. Ao ler `"abc" + 5`, ele já sabe que um texto
mais um número sempre falha. Com o arquivo completo, o comando
`.venv/bin/mypy --disallow-untyped-defs ex2` da página
[Rodar e conferir](./06-rodar-e-conferir.md) acusa:

```text
ex2/ft_different_errors.py:10: error: Unsupported operand types for + ("str" and "int")  [operator]
Found 1 error in 1 file (checked 1 source file)
```

"Tipos de operando não suportados para `+` (`str` e `int`)": o mesmo problema que o Python
encontra ao rodar, achado antes.

O enunciado avisa que isso vai acontecer e que **é o trabalho do mypy**: achar esse tipo de erro
antes de o programa rodar. Como o exercício precisa mostrar o `TypeError` acontecendo, o erro
fica no código de propósito. Esta é a **única** reclamação aceita do mypy em todo o projeto:
qualquer outra precisa ser corrigida.

O comentário em cima da linha registra a intenção para quem ler o código depois. O número da
linha, `10`, é o da linha `"abc" + 5` no arquivo completo.

O flake8 não confere tipos, então para ele o arquivo está limpo.
