---
sidebar_position: 8
title: Rodar e conferir
---

# Rodar e conferir

```bash
python3 ex4/ft_garden_security.py
```

```text
=== Garden Security System ===
Plant created: Rose: 15.0cm, 10 days old

Height updated: 25cm
Age updated: 30 days

Rose: Error, height can't be negative
Height update rejected
Rose: Error, age can't be negative
Age update rejected

Current state: Rose: 25.0cm, 30 days old
```

## Comparar com o enunciado

```bash
diff <(python3 ex4/ft_garden_security.py) - <<'FIM'
=== Garden Security System ===
Plant created: Rose: 15.0cm, 10 days old

Height updated: 25cm
Age updated: 30 days

Rose: Error, height can't be negative
Height update rejected
Rose: Error, age can't be negative
Age update rejected

Current state: Rose: 25.0cm, 30 days old
FIM
```

O `diff` não imprime nada.

## Os casos que a saída não mostra

Dois casos da classe não aparecem na saída do enunciado: a criação com um valor inválido e o
crescimento negativo. O comando `python3 -c` roda o código escrito entre aspas. O trecho
**importa** a classe do arquivo, e por isso o bloco main dele não roda
([O ponto de partida](../02-ex0/03-o-ponto-de-partida.md)). Com `-c` não existe arquivo de
script, e o Python procura os módulos a importar na **pasta atual**; por isso o `cd ex4` vem
antes.

```bash
cd ex4
python3 -c 'from ft_garden_security import Plant; Plant("Fern", -3.0, 10).show()'
cd ..
```

```text
Fern: Error, height can't be negative
Fern: 0.0cm, 10 days old
```

`from ft_garden_security import Plant` é a outra forma do `import`: carrega o arquivo
`ft_garden_security.py` e traz dele só o nome `Plant`, que então é usado direto, sem o nome do
módulo na frente. A altura negativa foi recusada na criação, e a samambaia nasceu com o valor
padrão, `0.0` cm.

```bash
cd ex4
python3 -c 'from ft_garden_security import Plant; fern = Plant("Fern", 15.0, 10); fern.grow(-20.0); fern.show()'
cd ..
```

```text
Fern: Error, height can't be negative
Fern: 15.0cm, 10 days old
```

O `grow(-20.0)` levaria a altura a `-5.0`; o setter recusou, e a samambaia continua com 15 cm.

O import deixou uma pasta `ex4/__pycache__`, que não faz parte da entrega e pode ser apagada.

## Conferir estilo e tipos

```bash
.venv/bin/flake8 ex4
.venv/bin/mypy --strict ex4
```

```text
Success: no issues found in 1 source file
```

O exercício 4 está pronto.
