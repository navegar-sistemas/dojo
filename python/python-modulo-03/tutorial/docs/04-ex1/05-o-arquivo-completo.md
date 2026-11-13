---
sidebar_position: 5
title: O arquivo completo
---

# O arquivo completo

O `main` imprime o título, separa as pontuações e escolhe entre a mensagem de uso e as
estatísticas:

```python
def main() -> None:
    """Read the scores from the command line and analyse them."""
    print("=== Player Score Analytics ===")
    scores = parse_scores(sys.argv[1:])
    if len(scores) == 0:
        print(f"No scores provided. Usage: python3 {printable(sys.argv[0])}"
              " <score1> <score2> ...")
    else:
        show_stats(scores)
```

- `sys.argv[1:]` passa só os argumentos, sem o nome do programa;
- uma lista vazia cobre os dois casos de erro do enunciado: nenhum argumento e nenhum argumento
  válido. Nos dois, sai a mensagem de uso;
- numa linha só, o `print` da mensagem de uso passaria dos 79 caracteres que o flake8 aceita. A
  mensagem é quebrada em dois textos lado a lado, que o Python junta num só. Os parênteses do
  `print` deixam a quebra de linha acontecer no meio da chamada;
- o nome do programa na mensagem vem de `sys.argv[0]`, e não está escrito à mão: assim a mensagem
  mostra o caminho do programa do jeito que a pessoa digitou. De dentro de `ex1`, sai
  `ft_score_analytics.py`, igual ao enunciado. Ele passa por `printable`, como os argumentos
  inválidos (veja abaixo).

O arquivo inteiro:

```python title="ex1/ft_score_analytics.py"
import sys

MAX_SCORE = 2 ** 53


def printable(text: str) -> str:
    """Return the text, or a marker if it is not valid UTF-8."""
    try:
        text.encode()
    except UnicodeEncodeError:
        return "<not valid UTF-8>"
    return text


def parse_scores(arguments: list[str]) -> list[int]:
    """Convert the arguments to scores, reporting and skipping bad ones."""
    scores: list[int] = []
    for argument in arguments:
        try:
            score = int(argument)
        except ValueError:
            print(f"Invalid parameter: '{printable(argument)}'")
            continue
        if not -MAX_SCORE <= score <= MAX_SCORE:
            print(f"Invalid parameter: '{printable(argument)}'")
            continue
        scores.append(score)
    return scores


def show_stats(scores: list[int]) -> None:
    """Print the statistics of a non-empty list of scores."""
    total = sum(scores)
    high = max(scores)
    low = min(scores)
    print(f"Scores processed: {scores}")
    print(f"Total players: {len(scores)}")
    print(f"Total score: {total}")
    print(f"Average score: {total / len(scores)}")
    print(f"High score: {high}")
    print(f"Low score: {low}")
    print(f"Score range: {high - low}")


def main() -> None:
    """Read the scores from the command line and analyse them."""
    print("=== Player Score Analytics ===")
    scores = parse_scores(sys.argv[1:])
    if len(scores) == 0:
        print(f"No scores provided. Usage: python3 {printable(sys.argv[0])}"
              " <score1> <score2> ...")
    else:
        show_stats(scores)


if __name__ == "__main__":
    main()
```

Como no [exercício 0](../03-ex0/05-o-arquivo-completo.md), o arquivo termina com uma única quebra
de linha depois da última linha, `    main()`, que o botão de copiar não leva.

O arquivo traz a mesma função `printable` do
[exercício 0](../03-ex0/05-o-arquivo-completo.md#um-argumento-que-não-é-texto-válido). O
argumento inválido é impresso na mensagem `Invalid parameter` e o nome do programa na mensagem de
uso, e os dois passam por ela: um argumento com bytes que não são UTF-8 sai como
`Invalid parameter: '<not valid UTF-8>'`, e o programa segue com as pontuações válidas.

Além das funções autorizadas, o arquivo usa `int()` e o método `encode` (dentro de `printable`),
liberados pela regra dos tipos, e o método `append` da lista, liberado desde que a lista foi
apresentada no exercício 0.
