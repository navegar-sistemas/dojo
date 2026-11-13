---
sidebar_position: 5
title: Rodar e conferir
---

# Rodar e conferir

## Rodar

```bash
python3 ex0/ft_garden_intro.py
```

```text
=== Welcome to My Garden ===
Plant: Rose
Height: 25cm
Age: 30 days

=== End of Program ===
```

## Comparar com o enunciado, letra por letra

Olhando, é fácil deixar passar um espaço ou uma linha vazia a mais. O comando `diff` compara dois
textos e imprime só as diferenças. O comando abaixo usa recursos do `bash` e do `zsh`, os shells
(os programas que leem os comandos digitados no terminal) que o Linux e o macOS usam por
padrão:

```bash
diff <(python3 ex0/ft_garden_intro.py) - <<'FIM'
=== Welcome to My Garden ===
Plant: Rose
Height: 25cm
Age: 30 days

=== End of Program ===
FIM
```

- `<(python3 ex0/ft_garden_intro.py)` entrega ao `diff` a saída do programa como se fosse um
  arquivo;
- o `-` diz ao `diff` que o outro texto vem da entrada do comando;
- `<<'FIM'` … `FIM` escreve esse texto ali mesmo, no terminal, até a linha `FIM`: é a saída que o
  enunciado mostra. As aspas em `'FIM'` fazem o shell copiar o texto como está, sem
  interpretar nenhum símbolo.

Se os dois textos forem iguais, o `diff` **não imprime nada**. Se imprimir alguma linha, ela
mostra onde a saída do programa (marcada com `<`) difere do esperado (marcada com `>`).

Neste exercício, o enunciado não exige que a saída seja idêntica letra por letra. Usar o `diff`
mesmo assim é escolha do projeto: é o mesmo comando que confere a saída de cada exercício
seguinte.

## Conferir estilo e tipos

```bash
.venv/bin/flake8 ex0
.venv/bin/mypy --strict ex0
```

```text
Success: no issues found in 1 source file
```

O flake8 não imprime nada, e o mypy não acha problema: o programa do exercício 0 está pronto.
