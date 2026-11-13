---
sidebar_position: 6
title: Rodar e conferir
---

# Rodar e conferir

## Comparar com o enunciado

O mesmo `diff` do [exercício 0](../03-ex0/06-rodar-e-conferir.md), com a saída do exercício 1:

```bash
diff <(python3 ex1/ft_raise_exception.py) - <<'FIM'
=== Garden Temperature Checker ===

Input data is '25'
Temperature is now 25°C

Input data is 'abc'
Caught input_temperature error: invalid literal for int() with base 10: 'abc'

Input data is '100'
Caught input_temperature error: 100°C is too hot for plants (max 40°C)

Input data is '-50'
Caught input_temperature error: -50°C is too cold for plants (min 0°C)

All tests completed - program didn't crash!
FIM
```

Sem nenhuma linha impressa, a saída é idêntica à do enunciado.

## Conferir os limites

O teste do enunciado não passa pelos limites exatos. Para ver que 0 e 40 são aceitos, rode a
função direto, com `python3 -c`, que executa o código escrito entre aspas:

```bash
cd ex1
python3 -B -c 'from ft_raise_exception import input_temperature; print(input_temperature("0"), input_temperature("40"))'
cd ..
```

```text
0 40
```

- `cd ex1` entra na pasta do exercício, para o Python achar o arquivo;
- `from ft_raise_exception import input_temperature` traz a função `input_temperature` do
  arquivo `ft_raise_exception.py` (o nome do arquivo sem o `.py`) para ser usada ali;
- o `;` separa duas instruções escritas na mesma linha;
- `-B` impede o Python de criar a pasta `__pycache__`, que ele gera ao importar um arquivo e que
  não faz parte da entrega;
- o `if __name__ == "__main__":` da página [O main](../03-ex0/04-o-main.md) faz o teste do arquivo
  **não** rodar na importação: só aparece o `0 40`.

## Conferir estilo e tipos

```bash
.venv/bin/flake8 ex1
.venv/bin/mypy --disallow-untyped-defs ex1
```

```text
Success: no issues found in 1 source file
```
