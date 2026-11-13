---
sidebar_position: 4
title: Pedir o nome
---

# Pedir o nome

O programa pergunta onde gravar. `input()` mostra um texto, espera a pessoa digitar e apertar Enter,
e devolve o que foi digitado, sem a quebra de linha do Enter.

```python
def ask_file_name() -> str:
    try:
        return input("Enter new file name (or empty): ")
    except (EOFError, KeyboardInterrupt):
        print()
        return ""
```

Apertar Enter sem digitar nada faz o `input()` devolver `""`, e o `main` entende isso como "não
gravar".

## Os dois jeitos de o input() falhar

O `input()` pode lançar duas exceções, e qualquer uma delas travaria o programa:

- **`EOFError`** (*end of file*, "fim do arquivo"): a entrada acabou antes de chegar um Enter. No
  terminal, acontece quando a pessoa aperta `Ctrl+D`; também acontece quando o programa recebe a
  entrada de um arquivo vazio;
- **`KeyboardInterrupt`**: a pessoa apertou `Ctrl+C`, o atalho de "interromper".

As duas querem dizer que a pessoa não deu um nome. O `except` trata as duas como resposta vazia: o
`print()` sozinho imprime uma quebra de linha, para que a mensagem seguinte não saia grudada na
pergunta, e a função devolve `""`.
