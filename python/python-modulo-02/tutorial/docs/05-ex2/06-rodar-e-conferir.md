---
sidebar_position: 6
title: Rodar e conferir
---

# Rodar e conferir

## Comparar com o enunciado

```bash
diff <(python3 ex2/ft_different_errors.py) - <<'FIM'
=== Garden Error Types Demo ===
Testing operation 0...
Caught ValueError: invalid literal for int() with base 10: 'abc'
Testing operation 1...
Caught ZeroDivisionError: division by zero
Testing operation 2...
Caught FileNotFoundError: [Errno 2] No such file or directory: '/non/existent/file'
Testing operation 3...
Caught TypeError: can only concatenate str (not "int") to str
Testing operation 4...
Operation completed successfully

All error types tested successfully!
FIM
```

Sem nenhuma linha impressa, a saída é idêntica à do enunciado.

## Conferir estilo e tipos

```bash
.venv/bin/flake8 ex2
.venv/bin/mypy --disallow-untyped-defs ex2
```

```text
ex2/ft_different_errors.py:10: error: Unsupported operand types for + ("str" and "int")  [operator]
Found 1 error in 1 file (checked 1 source file)
```

O flake8 não imprime nada. O mypy mostra só o erro proposital da linha 10, explicado em
[O erro proposital do mypy](./03-o-erro-proposital-do-mypy.md). Qualquer outra linha nessa saída
seria um defeito a corrigir.
