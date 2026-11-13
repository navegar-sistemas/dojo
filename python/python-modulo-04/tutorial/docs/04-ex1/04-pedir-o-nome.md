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
    except (EOFError, KeyboardInterrupt, UnicodeDecodeError):
        print()
        return ""
```

Apertar Enter sem digitar nada faz o `input()` devolver `""`, e o `main` entende isso como "não
gravar".

## Os três jeitos de o input() falhar

O `input()` pode lançar três exceções, e qualquer uma delas, sem um `except`, travaria o programa:

- **`EOFError`** (*end of file*, "fim do arquivo"): a entrada acabou sem nenhum caractere para ler.
  No terminal, acontece quando a pessoa aperta `Ctrl+D` numa linha vazia; também acontece quando a
  entrada do programa vem de um arquivo vazio em vez do teclado, caso que [Rodar e
  conferir](./08-rodar-e-conferir.md#as-falhas) mostra com `< /dev/null`. Uma entrada vinda de um
  arquivo que termina com texto e sem Enter não lança nada: o `input()` devolve o texto;
- **`KeyboardInterrupt`**: a pessoa apertou `Ctrl+C`, o atalho de "interromper";
- **`UnicodeDecodeError`**: a entrada trouxe bytes que não formam texto, como os de um programa (o
  `/bin/ls`, por exemplo) entregue ao `python3` no lugar do teclado. É o mesmo erro do `read()` com
  um arquivo que não é texto ([Quando o open
  falha](../02-arquivos/05-quando-o-open-falha.md#quando-a-falha-vem-depois-do-open)). Na entrada,
  ele só aparece até o Python 3.14, com a configuração de idioma mais comum ([open e o objeto
  arquivo](../02-arquivos/02-open-e-o-objeto-arquivo.md#abrir)). A partir do 3.15, o `input()`
  guarda cada byte inválido como um caractere especial, o mesmo que os argumentos ganham em [O
  uso](../03-ex0/02-o-uso.md#um-nome-que-não-pode-ser-mostrado), e devolve o texto sem lançar nada.
  Esse nome segue para a gravação, e uma recusa do `open()` (os bytes do `/bin/ls` trazem o
  caractere nulo, por exemplo) é tratada em [Gravar o arquivo](./05-gravar-o-arquivo.md#o-modo-w).
  O `except` continua necessário para as versões de 3.10 a 3.14.

As três querem dizer que a pessoa não deu um nome. O `except` trata as três como resposta vazia: o
`print()` sozinho imprime uma quebra de linha, para que a mensagem seguinte não saia grudada na
pergunta, e a função devolve `""`.
