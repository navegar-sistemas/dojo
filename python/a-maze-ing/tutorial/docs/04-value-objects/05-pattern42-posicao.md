---
sidebar_position: 5
title: "Pattern42: o desenho e a posição"
---

# `Pattern42`: o desenho e a posição

O enunciado exige que todo labirinto mostre o número **42** desenhado por células com as quatro
paredes fechadas. O gerador precisa saber, para uma grade de um tamanho qualquer, **quais
células** formam esse desenho, para nunca abrir paredes nelas. Esta página cria a classe que
calcula essas células, o `Pattern42`, em `mazegen/value_objects/pattern42.py`.

Os trechos desta página ainda não são o arquivo pronto: faltam os imports do topo, as
docstrings e a pergunta "esta célula é do 42?", que entram na página
[Pattern42: consultar o padrão](./06-pattern42-consulta.md). Ela termina com o arquivo completo
de `mazegen/value_objects/pattern42.py`. Dá para criar o arquivo já com estes trechos e
completá-lo lá, ou esperar e copiar a versão completa.

## Relembrando o "42"

A [parte 1](../01-o-problema/06-o-padrao-42.md) define o desenho: um bloco de 7 colunas por 5
linhas, centralizado na grade, com 18 células "do 42". Essas células ficam fechadas e **fora do
labirinto**: nenhum corredor passa por elas.

![O desenho do 42 num bloco de 7 por 5](/img/problema/glifo-42.svg)

O enunciado não diz onde o "42" fica nem o tamanho mínimo da grade; diz só que, se o labirinto
for pequeno demais, o "42" pode ficar de fora, com uma mensagem de erro. O centro e o mínimo de
9x7 são escolhas do projeto, explicadas abaixo.

## As constantes

```python
GLYPHS = ("X...XXX", "X.....X", "XXX.XXX", "..X.X..", "..X.XXX")
PATTERN_WIDTH = 7
PATTERN_HEIGHT = 5
MIN_WIDTH = 9
MIN_HEIGHT = 7
```

| Constante | Significado |
|---|---|
| `GLYPHS` | o desenho, uma string por linha: `X` é célula do "42", `.` é célula comum |
| `PATTERN_WIDTH`, `PATTERN_HEIGHT` | o tamanho do bloco: 7 colunas por 5 linhas |
| `MIN_WIDTH`, `MIN_HEIGHT` | o bloco mais uma célula de corredor de cada lado: 7 + 2 e 5 + 2 |

Lidas uma embaixo da outra, as cinco strings formam o desenho da figura acima: a primeira,
`"X...XXX"`, é a linha de cima do bloco, com o topo do "4" à esquerda e o topo do "2" à
direita.

O desenho fica em texto justamente por isso: quem abre o arquivo **enxerga** o número. Uma lista
de 18 coordenadas faria o mesmo trabalho, mas ninguém veria o desenho nela, nem perceberia um
erro de digitação.

## `@dataclass(frozen=True)` com `frozenset`

```python
@dataclass(frozen=True)
class Pattern42:
    cells: frozenset[Cell]
```

O padrão é um **value object**, como a `Cell` da [página anterior](./04-cell.md): o mesmo tamanho
de grade dá sempre as mesmas células, e nada as altera depois. Por isso o `@dataclass(frozen=True)`
(a classe gerada a partir dos campos, congelada).

Ao contrário da `Cell`, aqui não há `slots=True`. É uma escolha do projeto: o `slots` economiza
memória **por objeto**, e isso conta na `Cell`, criada aos milhares (uma grade 100x100 tem 10 000
posições). Padrão há um só por labirinto, e a economia não faria diferença.

O único campo, `cells`, é um **`frozenset`**: o `set` (conjunto) imutável do Python, que não
aceita `add` nem `remove`. Ele é necessário por dois motivos:

- `frozen=True` impede **trocar** o campo (`pattern.cells = ...`), mas não impede **mexer dentro**
  dele. Com um `set` comum, `pattern.cells.add(Cell(0, 0))` funcionaria, e o padrão mudaria.
- O `__hash__` que o `@dataclass` escreve calcula o hash a partir dos campos, e um `set` comum
  não tem hash (porque pode mudar). Um `frozenset` tem.

Um conjunto (`set` ou `frozenset`) também responde rápido à pergunta "esta célula está aqui?",
sem percorrer as 18 células uma a uma.

## `for_size`: criar o padrão a partir do tamanho da grade

```python
    @classmethod
    def for_size(cls, width: int, height: int) -> "Pattern42":
        if width < MIN_WIDTH or height < MIN_HEIGHT:
            return cls(frozenset())
```

O `__init__` escrito pelo `@dataclass` recebe as células prontas: `Pattern42(cells)`. Mas quem
precisa de um padrão só sabe o tamanho da grade. `for_size` resolve isso: é um **método de
fábrica**, que recebe o tamanho, calcula as células e cria o objeto.

- `@classmethod` faz o método ser chamado pela **classe**, não por um objeto:
  `Pattern42.for_size(20, 15)`. Faz sentido, porque ainda não existe objeto nenhum; ele é
  justamente o que o método vai criar.
- O primeiro parâmetro, `cls`, recebe a própria classe `Pattern42` (assim como um método comum
  recebe o objeto em `self`). `cls(...)` cria o objeto, igual a `Pattern42(...)`.

A primeira decisão é se o "42" cabe. Abaixo de 9x7, o resultado é um padrão **vazio**
(`frozenset()` sem nada dentro). Não é um erro: o labirinto é gerado sem o desenho, e o programa
só avisa.

```python
        x0 = (width - PATTERN_WIDTH) // 2
        y0 = (height - PATTERN_HEIGHT) // 2
```

`x0,y0` é a célula do canto de cima à esquerda do bloco 7x5. Para centralizar, as colunas que
sobram (`width - 7`) são divididas entre a esquerda e a direita do bloco. O `//` é a divisão
inteira, que joga fora a parte quebrada: com sobra ímpar, a coluna extra fica à direita. O mesmo
vale para as linhas.

```python
        return cls(frozenset(
            Cell(x0 + dx, y0 + dy)
            for dy, row in enumerate(GLYPHS)
            for dx, char in enumerate(row)
            if char == "X"
        ))
```

Percorre o desenho linha a linha e caractere a caractere, e cria uma `Cell` para cada `X`:

- `enumerate(GLYPHS)` dá cada linha do desenho junto com o seu número: `dy` vai de 0 a 4;
- `enumerate(row)` faz o mesmo com os caracteres da linha: `dx` vai de 0 a 6;
- `if char == "X"` pula as células comuns;
- `Cell(x0 + dx, y0 + dy)` desloca a posição do desenho para a posição na grade.

As linhas entre os parênteses de `frozenset(...)` são uma **expressão geradora**: um jeito curto
de escrever um laço que produz valores. Ela faz o mesmo que este laço comum, que monta um `set`
e o congela no fim:

```python
cells = set()
for dy, row in enumerate(GLYPHS):
    for dx, char in enumerate(row):
        if char == "X":
            cells.add(Cell(x0 + dx, y0 + dy))
return cls(frozenset(cells))
```

Lida na ordem em que está escrita, a expressão geradora diz: "uma `Cell(x0 + dx, y0 + dy)` para
cada linha `dy`, para cada caractere `dx` dessa linha, quando o caractere é `X`". Os dois `for`
ficam na mesma ordem dos dois laços acima: o de fora primeiro.

A mesma ideia escrita entre colchetes, `[... for ... in ...]`, monta uma lista e se chama
**compreensão de lista** (*list comprehension*). Entre os parênteses de uma chamada, como aqui,
os valores vão direto para o `frozenset`, sem montar uma lista no meio. O resultado são 18
células.

## Onde o bloco cai

A [próxima página](./07-pattern42-tamanhos.md) aplica o `for_size` a três tamanhos de grade, um
deles pequeno demais para o "42", e mostra por que a margem em volta do bloco vale em todo
tamanho permitido.
