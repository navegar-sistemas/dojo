---
sidebar_position: 5
title: O arquivo completo
---

# O arquivo completo

O cabeçalho, a contagem e o laço ficam dentro de uma função `main`, e o fim do arquivo a chama.
Uma função nova, `printable`, impede que um argumento com bytes inválidos trave o `print`
([Um argumento que não é texto válido](#um-argumento-que-não-é-texto-válido)):

```python title="ex0/ft_command_quest.py"
import sys


def printable(text: str) -> str:
    """Return the text, or a marker if it is not valid UTF-8."""
    try:
        text.encode()
    except UnicodeEncodeError:
        return "<not valid UTF-8>"
    return text


def main() -> None:
    """Show the program name and every command-line argument."""
    print("=== Command Quest ===")
    print(f"Program name: {printable(sys.argv[0])}")
    arguments = sys.argv[1:]
    if len(arguments) == 0:
        print("No arguments provided!")
    else:
        print(f"Arguments received: {len(arguments)}")
        number = 1
        for argument in arguments:
            print(f"Argument {number}: {printable(argument)}")
            number += 1
    print(f"Total arguments: {len(sys.argv)}")


if __name__ == "__main__":
    main()
```

O arquivo termina com **uma** quebra de linha logo depois da última linha, `    main()`, e nada
depois dela: nem outra linha vazia, nem espaços. O botão de copiar, no canto do bloco, não leva
essa quebra final. Depois de colar, se o cursor ficar no fim de `    main()`, aperte Enter uma vez
antes de salvar, e apague os espaços de recuo se o editor os puser na linha nova; alguns editores
já acrescentam a quebra sozinhos ao salvar. Sem a quebra, o flake8 acusa
`W292 no newline at end of file` ("falta a quebra de linha no fim do arquivo"); com mais de uma,
`W391 blank line at end of file` ("linha em branco no fim do arquivo").

## O main

`main` ("principal") é o nome costumeiro da função que faz o trabalho do programa. Definir a
função não a executa; quem a chama é o bloco do fim:

```python
if __name__ == "__main__":
    main()
```

`__name__` é uma variável que o Python cria em todo arquivo:

- quando o arquivo é **rodado** (`python3 ft_command_quest.py`), ela vale `"__main__"`;
- quando o arquivo é **importado** por outro (`import ft_command_quest`), ela vale o nome do
  arquivo, `"ft_command_quest"`.

Com o `if`, o programa roda quando o arquivo é executado e fica quieto quando outro código só
quer usar as suas funções. Todos os exercícios terminam com esse bloco.

## Um argumento que não é texto válido

O shell entrega os argumentos ao programa como **bytes**, e o Python os transforma em texto pela
codificação do sistema, que nos sistemas atuais é a **UTF-8**: a forma padrão de escrever letras,
acentos e símbolos em bytes. Um argumento pode trazer bytes que não formam texto UTF-8 válido,
como o byte de valor 255, escrito `\xff`: `\x` seguido do valor em base 16, onde `ff` é 255.
Nenhum texto UTF-8 válido contém esse byte. O Python ainda guarda o argumento em `sys.argv`, com
uma marca no lugar do byte estranho.

Na hora de imprimir essa marca, o comportamento depende da configuração de idioma do sistema (o
**locale**) e da versão do Python. Com locales como `en_US.UTF-8` ou `pt_BR.UTF-8` e o Python
3.14 ou anterior, o `print` não consegue escrevê-la e lança `UnicodeEncodeError`, o erro de
conversão de texto para bytes, e o programa trava com um **traceback**: o relatório de erro que o
Python imprime quando um erro não é capturado. Com os locales `C` e `C.UTF-8`, e a partir do
Python 3.15, o `print` escreve o byte de volta como veio.

A função `printable` tira essa dependência:

```python
def printable(text: str) -> str:
    """Return the text, or a marker if it is not valid UTF-8."""
    try:
        text.encode()
    except UnicodeEncodeError:
        return "<not valid UTF-8>"
    return text
```

- `text.encode()` é o método de `str` que converte o texto em bytes UTF-8, sempre no modo
  estrito: com a marca de um byte inválido, ele lança `UnicodeEncodeError`;
- a função devolve o próprio texto quando a conversão dá certo, e o aviso `<not valid UTF-8>`
  quando não dá;
- o programa imprime o nome e cada argumento passando por `printable`, e a saída é a mesma em
  qualquer versão, nos locales UTF-8 e no `C`
  ([Rodar e conferir](./06-rodar-e-conferir.md#um-argumento-que-não-é-utf-8)).

O laço de [Percorrer os argumentos](./04-percorrer-os-argumentos.md) é o mesmo, com
`printable(argument)` no lugar de `argument` dentro do `print`.

O arquivo usa só `import sys`, `sys.argv`, `len()` e `print()`, além da fatia, do `for` e do
método `encode` de `str`, liberado pela **regra dos tipos**: `str`, `int` e `float` podem ser
usados com todos os seus métodos e construtores em qualquer exercício
([O que pode ser usado](../00-introducao/02-o-enunciado-em-linguagem-simples.md#o-que-pode-ser-usado)).
