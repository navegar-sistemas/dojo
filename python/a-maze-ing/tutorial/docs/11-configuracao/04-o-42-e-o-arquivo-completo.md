---
sidebar_position: 4
title: As regras da grade e do "42"
---

# As regras da grade e do "42"

Com a largura e a altura já conferidas ([página anterior](./03-a-ordem-das-validacoes.md)),
faltam as regras que dependem delas: a entrada e a saída precisam ficar dentro da grade, ser
células diferentes e não cair em cima do "42", e o modo Pac-Man precisa de espaço para os seus
ciclos. Esta página escreve as regras 4 a 7 do `MazeConfig.create`.

## 4. Dentro da grade

```python
for key, (x, y) in (("ENTRY", entry), ("EXIT", exit)):
    if not (0 <= x < width and 0 <= y < height):
        raise ConfigError(
            f"{key}={x},{y} is outside the maze "
            f"(x in 0..{width - 1}, y in 0..{height - 1})")
```

- `for key, (x, y) in ...` separa cada par em três nomes de uma vez: `("ENTRY", (0, 0))` dá
  `key = "ENTRY"`, `x = 0` e `y = 0`.
- Numa grade de 20 colunas, as colunas vão de 0 a 19: por isso `x < width`, e não `x <= width`.
- A mensagem mostra a faixa válida, para o usuário não ter de lembrar que a contagem começa em
  0: `ENTRY=20,0 is outside the maze (x in 0..19, y in 0..14)`.

É aqui que o `-1,0`, aceito como formato pelo conversor, é recusado. O enunciado exige que a
entrada e a saída estejam dentro do labirinto.

## 5. Entrada diferente da saída

```python
if entry == exit:
    raise ConfigError("ENTRY and EXIT must differ")
```

Também é regra do enunciado. Vem depois da 4: com `ENTRY=30,30` e `EXIT=30,30` numa grade
20x15, o problema mais útil de apontar é "fora da grade".

## 6. O tabuleiro Pac-Man precisa de espaço

```python
if not perfect and (width - 1) * (height - 1) < 2:
    raise ConfigError(
        "PERFECT=False needs (WIDTH - 1) x (HEIGHT - 1) >= 2 for a "
        f"Pac-Man board, got {width}x{height}")
```

Com `PERFECT=False`, o enunciado pede um tabuleiro de Pac-Man com pelo menos dois **ciclos**
(dois jeitos de andar em círculo, para quem foge sempre ter outra rota).

De onde vem a conta: um bloco de 2x2 células sem nenhuma parede por dentro é um ciclo, porque dá
para dar a volta nele. Numa grade de `WIDTH` colunas e `HEIGHT` linhas cabem
`(WIDTH − 1) × (HEIGHT − 1)` blocos 2x2 diferentes (o canto de cima à esquerda do bloco pode
estar em qualquer coluna menos a última e em qualquer linha menos a última). Com todas as
paredes de dentro abertas, esse é o número de ciclos independentes da grade
([parte 1](../01-o-problema/09-sem-saloes-e-o-braiding.md#tamanhos-impossíveis)).

Grades 1xN e Nx1 não têm nenhum bloco 2x2, e a 2x2 tem um só: nem abrindo tudo chegam a 2
ciclos, e o gerador nunca conseguiria cumprir a regra. Recusar logo, com a conta na mensagem, é
escolha do projeto.

## 7. Entrada e saída fora do "42"

Lembrando ([parte 1](../01-o-problema/06-o-padrao-42.md)): o enunciado exige um número 42
desenhado no meio do labirinto por células com as quatro paredes fechadas. Essas células ficam
**fora** do labirinto: o gerador nunca abre passagem para elas. Uma entrada ou saída em cima de
uma delas não teria por onde sair.

![Grade 20 por 15 com as coordenadas, o 42 em cinza e a entrada 6,5, marcada com E, em cima da primeira célula do 4](/img/configuracao/entrada-no-42.svg)

Na figura, o cinza marca as células do "42" e o `E` marca a **entrada** (`ENTRY=6,5`), não o
lado Leste.

O enunciado não diz o que fazer nesse caso. O projeto escolheu recusar a configuração; a outra
opção seria mudar o "42" de lugar, o que tornaria a posição dele imprevisível.

```python
pattern = Pattern42.for_size(width, height)
for key, (x, y) in (("ENTRY", entry), ("EXIT", exit)):
    if Cell(x, y) in pattern:
        raise ConfigError(f'{key}={x},{y} lies on the "42" pattern')
```

- `Pattern42.for_size(width, height)` calcula as células do "42" para aquele tamanho de grade
  ([parte 4](../04-value-objects/05-pattern42-posicao.md)). É a mesma função que o gerador usa:
  o `MazeConfig` e o gerador acham exatamente as mesmas células. O `Pattern42` e a `Cell` são
  importados pelos caminhos internos do pacote (`mazegen.value_objects.pattern42` e
  `mazegen.value_objects.cell`), porque o `mazegen` só oferece diretamente `MazeGenerator` e
  `MazeError`.
- `Cell(x, y) in pattern` pergunta se a célula faz parte do "42". `Cell` é a classe do
  `mazegen` que representa o endereço de uma célula ([parte 4](../04-value-objects/04-cell.md)).
- Quando o "42" não cabe (grade menor que 9x7), o padrão vem vazio e a regra nunca acusa nada:
  o labirinto é gerado sem o desenho, e o menu imprime o aviso
  `Error: maze too small for the "42" pattern` antes de cada desenho
  ([parte 14](../14-menu-e-main/03-mostrar-o-labirinto.md)).
- É a última regra porque o `for_size` precisa de um tamanho válido, e "está no 42?" só faz
  sentido para uma célula que está dentro da grade.

A mensagem usa aspas simples por fora (`f'...'`) porque o texto tem aspas duplas em volta do
`"42"`.

### Por que `Cell(x, y)` e não `(x, y)`

`entry` é uma tupla, mas o `Pattern42` guarda objetos `Cell`, e o operador `in` dele só
reconhece `Cell` ([parte 4](../04-value-objects/06-pattern42-consulta.md)). Na raiz do projeto:

```bash
.venv/bin/python -c '
from mazegen.value_objects.cell import Cell
from mazegen.value_objects.pattern42 import Pattern42

pattern = Pattern42.for_size(20, 15)
print(Cell(6, 5) in pattern)
print((6, 5) in pattern)
'
```

```text
True
False
```

Escrever `(x, y) in pattern` não daria erro: daria sempre `False`, e a regra nunca dispararia.
É o tipo de bug que passa despercebido, porque o programa continua rodando. Por isso a conversão
para `Cell` é explícita.

A [próxima página](./07-validar-duas-vezes.md) explica por que o `MazeConfig` confere regras que
o gerador também confere.
