---
sidebar_position: 6
title: Rodar e conferir
---

# Rodar e conferir

## Rodar

O programa roda de dentro da pasta `ex0`, como no enunciado
([O nome do programa](./02-a-linha-de-comando.md#o-nome-do-programa)):

```bash
(cd ex0 && python3 ft_command_quest.py hello world 42)
```

```text
=== Command Quest ===
Program name: ft_command_quest.py
Arguments received: 3
Argument 1: hello
Argument 2: world
Argument 3: 42
Total arguments: 4
```

- `cd ex0 && python3 …` entra na pasta e, se a entrada deu certo (`&&` quer dizer "e então, se o
  anterior deu certo"), roda o programa;
- os parênteses rodam os dois comandos numa cópia do shell, e o `cd` vale só dentro dessa
  cópia. Por isso, depois do comando, você continua na
  pasta `data-quest`, sem precisar de `cd ..`.

## Comparar com o enunciado, letra por letra

O comando `diff` compara dois textos e imprime só as diferenças, inclusive um espaço ou uma linha
vazia a mais:

```bash
diff <(cd ex0 && python3 ft_command_quest.py) - <<'FIM'
=== Command Quest ===
Program name: ft_command_quest.py
No arguments provided!
Total arguments: 1
FIM
```

- `<(cd ex0 && python3 ft_command_quest.py)` entrega ao `diff` a saída do programa como se fosse
  um arquivo;
- o `-` diz ao `diff` que o outro texto vem da **entrada** do comando: o texto que chega a ele,
  aqui o que está entre `<<'FIM'` e `FIM`;
- `<<'FIM'` … `FIM` escreve esse texto ali mesmo, no comando, até a linha `FIM`: é a saída que o
  enunciado mostra. As aspas em `'FIM'` fazem o shell copiar o texto como está, sem interpretar
  nenhum símbolo.

Se os dois textos forem iguais, o `diff` **não imprime nada**. Se imprimir alguma linha, ela
mostra onde a saída do programa (marcada com `<`) difere do esperado (marcada com `>`).

Os outros dois exemplos do enunciado:

```bash
diff <(cd ex0 && python3 ft_command_quest.py hello world 42) - <<'FIM'
=== Command Quest ===
Program name: ft_command_quest.py
Arguments received: 3
Argument 1: hello
Argument 2: world
Argument 3: 42
Total arguments: 4
FIM
diff <(cd ex0 && python3 ft_command_quest.py "Data Quest") - <<'FIM'
=== Command Quest ===
Program name: ft_command_quest.py
Arguments received: 1
Argument 1: Data Quest
Total arguments: 2
FIM
```

Nenhum dos dois imprime nada.

## Um argumento que não é UTF-8

`$'\xff'` faz o shell passar ao programa o byte `\xff`, que não forma texto UTF-8
([Um argumento que não é texto válido](./05-o-arquivo-completo.md#um-argumento-que-não-é-texto-válido)):

```bash
(cd ex0 && python3 ft_command_quest.py ok $'\xff' fim)
echo $?
```

```text
=== Command Quest ===
Program name: ft_command_quest.py
Arguments received: 3
Argument 1: ok
Argument 2: <not valid UTF-8>
Argument 3: fim
Total arguments: 4
0
```

O argumento inválido aparece como `<not valid UTF-8>`, e o programa segue até o fim. `echo $?`
mostra o **código de saída** do último comando, o número que o programa devolve ao shell ao
terminar: `0` quer dizer "terminou bem".

## Conferir estilo e tipos

```bash
.venv/bin/flake8 ex0
.venv/bin/mypy --disallow-untyped-defs ex0
```

```text
Success: no issues found in 1 source file
```

O flake8 não imprime nada, e o mypy não acha problema: o exercício 0 está pronto.
