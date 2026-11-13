---
sidebar_position: 6
title: O arquivo completo
---

# O arquivo completo

## O main

```python
def main() -> None:
    """Read two positions and show the distances between them."""
    print("=== Game Coordinate System ===")
    print("\nGet a first set of coordinates")
    first = get_player_pos()
    print(f"Got a first tuple: {first}")
    x, y, z = first
    print(f"It includes: X={x}, Y={y}, Z={z}")
    to_center = distance((0.0, 0.0, 0.0), first)
    print(f"Distance to center: {round(to_center, 4)}")
    print("\nGet a second set of coordinates")
    second = get_player_pos()
    between = distance(first, second)
    print(f"Distance between the 2 sets of coordinates: {round(between, 4)}")
```

- o `\n` antes de `Get a first set` e de `Get a second set` imprime as linhas vazias da saída do
  enunciado;
- `{first}` imprime a tupla com os parênteses: `(1.0, 2.5, 3.0)`;
- a tupla é desempacotada para mostrar cada coordenada separada;
- `to_center` e `between` guardam as distâncias antes de imprimir, para as linhas do `print`
  caberem em 79 caracteres.

## Quando o usuário desiste

`get_player_pos` pergunta até receber uma posição válida. Mas o usuário pode desistir de
responder de dois jeitos:

- **Ctrl-D** (segurar Ctrl e apertar D) numa linha vazia avisa que a entrada acabou: não vem
  mais nenhum texto. O
  `input()` lança `EOFError` (*end of file*, "fim do arquivo"). O mesmo acontece quando as
  respostas vêm de um texto preparado
  ([Rodar e conferir](./07-rodar-e-conferir.md#a-entrada-que-acaba-antes-da-hora)) e ele acaba
  antes da hora;
- **Ctrl-C** interrompe o programa, e o Python lança `KeyboardInterrupt` ("interrupção pelo
  teclado") onde quer que o programa esteja.

Sem tratamento, os dois terminam o programa com um traceback, o relatório de erro do Python, e
isso é travar. Nenhum dos dois pode ser resolvido dentro de `get_player_pos`: ela promete devolver
uma posição, e não há posição para devolver. O programa inteiro termina, com uma mensagem, e a
captura fica no bloco do fim:

```python
if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nInput interrupted - leaving the coordinate system")
```

Um `except` com uma tupla de tipos captura qualquer um deles. O `\n` do começo da mensagem
passa para uma linha nova, porque o cursor está parado no fim da pergunta quando o usuário
desiste.

## O arquivo inteiro

```python title="ex2/ft_coordinate_system.py"
import math

PROMPT = "Enter new coordinates as floats in format 'x,y,z': "
LIMIT = 1e150


def get_player_pos() -> tuple[float, float, float]:
    """Ask for coordinates until the user types three valid floats."""
    while True:
        try:
            x_text, y_text, z_text = input(PROMPT).split(",")
        except ValueError:
            print("Invalid syntax")
            continue
        values: list[float] = []
        for text in (x_text, y_text, z_text):
            parameter = text.strip()
            try:
                value = float(parameter)
            except ValueError as error:
                print(f"Error on parameter '{parameter}': {error}")
                break
            if not -LIMIT <= value <= LIMIT:
                print(f"Error on parameter '{parameter}': out of range")
                break
            values.append(value)
        else:
            return (values[0], values[1], values[2])


def distance(first: tuple[float, float, float],
             second: tuple[float, float, float]) -> float:
    """Return the Euclidean distance between two 3D points."""
    x1, y1, z1 = first
    x2, y2, z2 = second
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)


def main() -> None:
    """Read two positions and show the distances between them."""
    print("=== Game Coordinate System ===")
    print("\nGet a first set of coordinates")
    first = get_player_pos()
    print(f"Got a first tuple: {first}")
    x, y, z = first
    print(f"It includes: X={x}, Y={y}, Z={z}")
    to_center = distance((0.0, 0.0, 0.0), first)
    print(f"Distance to center: {round(to_center, 4)}")
    print("\nGet a second set of coordinates")
    second = get_player_pos()
    between = distance(first, second)
    print(f"Distance between the 2 sets of coordinates: {round(between, 4)}")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nInput interrupted - leaving the coordinate system")
```

Além das funções autorizadas, o arquivo usa `float()` e os métodos `split` e `strip`, liberados
pela regra dos tipos, e `append` da lista, liberado desde o exercício 0. Não chama `len()`, que
este exercício não autoriza.
