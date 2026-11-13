---
sidebar_position: 4
title: Ler sem input
---

# Ler sem input

`input()` faz três coisas: escreve a pergunta na saída padrão, lê uma linha da entrada padrão e tira
o `\n` do fim. Sem `input()`, o programa faz as três com os fluxos:

```python
def ask_file_name() -> str:
    sys.stdout.write("Enter new file name (or empty): ")
    sys.stdout.flush()
    try:
        line = sys.stdin.readline()
    except (KeyboardInterrupt, UnicodeDecodeError):
        line = ""
    if line == "":
        print()
    return line.rstrip("\n")
```

## Escrever a pergunta

`sys.stdout.write(...)` escreve o texto na saída padrão sem acrescentar quebra de linha, para a
resposta ser digitada na mesma linha da pergunta.

Sem quebra de linha, porém, o texto fica no buffer: no terminal, o Python só despeja a saída a cada
`\n` ([Escrever no stderr](./03-escrever-no-stderr.md)). O programa ficaria esperando a resposta a
uma pergunta que ainda não apareceu na tela. O `sys.stdout.flush()` despeja a pergunta antes de
esperar. O `input()` faz esse `flush` sozinho; aqui ele é explícito.

## Ler a linha

`sys.stdin.readline()` lê da entrada padrão até o `\n` do Enter, inclusive, e devolve a linha. Crie
`experimentos/readline.py`:

```python
import sys

line = sys.stdin.readline()
print(repr(line))
```

```bash
printf 'abc\n' | python3 experimentos/readline.py
printf 'abc' | python3 experimentos/readline.py
python3 experimentos/readline.py < /dev/null
```

```text
'abc\n'
'abc'
''
```

- uma linha com Enter vem com o `\n` no fim;
- se a entrada acaba sem Enter, vem o que havia, sem `\n`;
- se a entrada já acabou (`Ctrl+D` numa linha vazia do terminal, ou um arquivo vazio como o
  `/dev/null`), `readline()` devolve `""`. Diferente do `input()`, ele **não** lança `EOFError`.

## Tratar o resultado

- `line.rstrip("\n")` tira o `\n` do fim, se houver. Assim, Enter sem texto (`"\n"`) vira `""`, a
  resposta vazia que o `main` entende como "não gravar";
- `Ctrl+C` lança `KeyboardInterrupt` dentro do `readline()`, e bytes que não formam texto lançam
  `UnicodeDecodeError`, como no `input()` ([Pedir o nome](../04-ex1/04-pedir-o-nome.md)). O
  `except` troca as duas pela resposta vazia;
- `line == ""` quer dizer que nenhum caractere chegou depois da pergunta: a entrada acabou, ou o
  `except` tratou uma falha. Nesse caso, o `print()` sozinho termina a linha da pergunta, para
  `Not saving data.` não sair grudado.
