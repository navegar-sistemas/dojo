---
sidebar_position: 3
title: Escrever no stderr
---

# Escrever no stderr

Os três `print` de erro do exercício 1 (abrir, ler e gravar) passam a ir para a saída de erro, todos
com o mesmo prefixo. Em vez de repetir o prefixo e o `file=sys.stderr` em cada um, uma função cuida
disso:

```python
def report_error(message: str) -> None:
    sys.stdout.flush()
    print(f"[STDERR] {message}", file=sys.stderr)
```

E cada mensagem de erro passa por ela. Em `recover_archive`:

```python
    except OSError as error:
        report_error(f"Error opening file '{file_name}': {error}")
        return None
```

```python
    except (OSError, UnicodeDecodeError) as error:
        report_error(f"Error reading file '{file_name}': {error}")
```

E em `save_archive`, as duas mensagens, `Error opening file` e `Error writing file`, do mesmo jeito.

## O flush antes do erro

A primeira linha, `sys.stdout.flush()`, garante a ordem das mensagens. A saída padrão tem um buffer,
como os arquivos ([close e o recurso](../02-arquivos/04-close-e-o-recurso.md)):

- quando ela vai para o terminal, o Python despeja o buffer a cada quebra de linha, e as mensagens
  aparecem na hora;
- quando ela vai para um arquivo ou um pipe, o Python junta tudo num buffer grande e só despeja
  quando ele enche ou o programa termina.

A saída de erro não espera: cada mensagem sai na hora. Então, com a saída padrão redirecionada, um
erro pode sair **antes** das linhas que o programa imprimiu primeiro. Crie `experimentos/ordem.py`:

```python
import sys

print("first, on stdout")
print("second, on stderr", file=sys.stderr)
```

```bash
python3 experimentos/ordem.py 2>&1 | cat
```

```text
second, on stderr
first, on stdout
```

O `2>&1` junta a saída de erro à saída padrão, e o `| cat` faz a saída padrão ir para um pipe em vez
do terminal (o `cat` só repassa o que recebe). A linha impressa primeiro saiu por último: ficou no
buffer até o fim do programa.

`flush()` despeja o buffer na hora. Com ele antes da mensagem de erro, `experimentos/ordem.py` fica:

```python
import sys

print("first, on stdout")
sys.stdout.flush()
print("second, on stderr", file=sys.stderr)
```

```bash
python3 experimentos/ordem.py 2>&1 | cat
```

```text
first, on stdout
second, on stderr
```

É por isso que `report_error` começa com `sys.stdout.flush()`: o erro sai sempre depois do que o
programa já tinha impresso, vá a saída para onde for.
