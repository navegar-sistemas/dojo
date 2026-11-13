---
sidebar_position: 6
title: Rodar e conferir
---

# Rodar e conferir

## Rodar

```bash
python3 ex0/ft_first_exception.py
```

```text
=== Garden Temperature ===

Input data is '25'
Temperature is now 25°C

Input data is 'abc'
Caught input_temperature error: invalid literal for int() with base 10: 'abc'

All tests completed - program didn't crash!
```

## Comparar com o enunciado, letra por letra

Olhando, é fácil deixar passar um espaço ou uma linha vazia a mais. O comando `diff` compara dois
textos e imprime só as diferenças:

```bash
diff <(python3 ex0/ft_first_exception.py) - <<'FIM'
=== Garden Temperature ===

Input data is '25'
Temperature is now 25°C

Input data is 'abc'
Caught input_temperature error: invalid literal for int() with base 10: 'abc'

All tests completed - program didn't crash!
FIM
```

- `<(python3 ex0/ft_first_exception.py)` entrega ao `diff` a saída do programa como se fosse um
  arquivo;
- o `-` diz ao `diff` que o segundo texto não é um arquivo: é o texto escrito logo em seguida;
- `<<'FIM'` … `FIM` fornece esse texto ali mesmo, até a linha `FIM`: é a saída que o enunciado
  mostra. As aspas em `'FIM'` fazem o terminal copiar o texto como está, sem interpretar nenhum
  símbolo.

Ao digitar (ou colar) o comando, o terminal mostra um aviso no começo de cada linha (`>` no
bash, `heredoc>` no zsh) até receber a linha `FIM`: ele está esperando o resto do texto, não
travou.

Se os dois textos forem iguais, o `diff` **não imprime nada**. Se imprimir alguma linha, ela
mostra onde a saída do programa (marcada com `<`) difere do esperado (marcada com `>`).

## Conferir estilo e tipos

```bash
.venv/bin/flake8 ex0
.venv/bin/mypy --disallow-untyped-defs ex0
```

```text
Success: no issues found in 1 source file
```

O flake8 não imprime nada, e o mypy não acha problema: o exercício 0 está pronto.

## O fim do arquivo

Se o flake8 acusar algo na última linha do arquivo, o problema está no que vem depois de
`    test_temperature()`. Um exemplo, com o arquivo salvo sem a quebra final:

```text
ex0/ft_first_exception.py:18:23: W292 no newline at end of file
```

| Código | O que diz | Como fica o fim do arquivo | Correção |
|---|---|---|---|
| `W292` | `no newline at end of file` ("sem quebra de linha no fim do arquivo") | o arquivo acaba na própria linha do `test_temperature()` | pôr o cursor no fim dessa linha e apertar Enter |
| `W391` | `blank line at end of file` ("linha em branco no fim do arquivo") | há linhas vazias a mais depois dela | apagar as linhas vazias do fim, deixando só a quebra |
| `W293` | `blank line contains whitespace` ("linha em branco com espaços") | o Enter criou uma linha nova com espaços de recuo | apagar os espaços dessa linha, deixando-a vazia |

O `W293` costuma vir junto com o `W292`: a linha de espaços também fica sem quebra no fim. Depois
de corrigir, rode o flake8 de novo até ele não imprimir nada. O mesmo vale para os arquivos dos
outros exercícios.
