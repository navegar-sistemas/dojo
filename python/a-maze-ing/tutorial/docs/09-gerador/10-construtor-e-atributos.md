---
sidebar_position: 2
title: Construtor e atributos
---

# Construtor e atributos

Quem usa a fachada `MazeGenerator` ([página anterior](./01-a-fachada.md)) precisa saber o que
passar ao criá-la e onde ler o resultado depois. Esta página mostra as constantes do arquivo
`mazegen/generator.py`, a assinatura do construtor, com os parâmetros e os valores que valem
quando um parâmetro é omitido, e os três atributos que o gerador preenche.

## As constantes

```python
MIN_SIZE = 1
MAX_SIZE = 100
MAX_ATTEMPTS = 20
```

Ficam no topo do arquivo, fora da classe. Escritas em maiúsculas, seguem a convenção do Python
para **constante**: um valor que o programa nunca muda.

- `MIN_SIZE` e `MAX_SIZE`: os limites da largura e da altura, os mesmos do arquivo de
  configuração. O mínimo 1 vem da lógica (não há labirinto com 0 colunas); o máximo 100 é escolha
  do projeto, para um valor enorme virar uma mensagem de erro em vez de travar o computador
  ([parte 1](../01-o-problema/03-o-arquivo-de-configuracao.md)).
- `MAX_ATTEMPTS`: quantas vezes o modo Pac-Man tenta gerar um tabuleiro bom antes de desistir
  ([página 4](./03-generate.md)).

## A assinatura

```python
    def __init__(self, width: int, height: int,
                 entry: tuple[int, int] = (0, 0),
                 exit: tuple[int, int] | None = None, perfect: bool = False,
                 seed: int | None = None) -> None:
```

`__init__` é o **construtor**: o método que o Python roda ao criar o objeto, em
`MazeGenerator(...)`. Um parâmetro com `=` tem **valor padrão**: se quem chama não o passa, vale o
valor depois do `=`. A anotação `tuple[int, int]` quer dizer "uma tupla de dois inteiros", e
`| None` quer dizer "ou `None`". O `-> None` no fim diz que o construtor não devolve nada.

| Parâmetro | Valor quando omitido | Significado |
|---|---|---|
| `width`, `height` | nenhum: são obrigatórios | largura (colunas) e altura (linhas), de 1 a 100 |
| `entry` | `(0, 0)` | célula de entrada, `(x, y)` |
| `exit` | `None` | célula de saída; `None` quer dizer o canto de baixo à direita |
| `perfect` | `False` | `True` para labirinto perfeito, `False` para tabuleiro Pac-Man |
| `seed` | `None` | a semente do sorteio (mesmo número, mesmo labirinto); `None` gera um labirinto diferente a cada execução ([parte 6](../06-carver/04-a-seed.md)) |

### `perfect=False` quando omitido

O enunciado chama o tabuleiro Pac-Man (`PERFECT=False`) de modo **padrão**: é o que vale quando
o labirinto perfeito não é pedido. Esta classe leva isso ao pé da letra: `MazeGenerator(20, 15)`,
sem `perfect`, gera um tabuleiro Pac-Man.

No arquivo de configuração é diferente: lá a chave `PERFECT` é obrigatória, e o programa recusa
um arquivo sem ela ([parte 11](../11-configuracao/03-a-ordem-das-validacoes.md)). O valor padrão
só existe aqui, para quem usa o gerador direto pelo Python.

### O `exit` padrão é calculado

O padrão de `exit` não pode ser uma tupla fixa: o canto de baixo à direita depende da largura e
da altura, que ainda não se conhecem quando o Python lê a assinatura. `None` quer dizer "calcule a
partir do tamanho", e o construtor faz essa conta ([página 3](./02-validar-os-parametros.md)).

`exit` também é o nome de uma função que já vem no Python. Como nome de parâmetro, ele só esconde
essa função dentro do construtor, que não a usa. O nome acompanha as opções do arquivo de
configuração (`ENTRY`, `EXIT`).

## Os atributos públicos

Um **atributo** é uma variável guardada dentro do objeto, lida com `gen.nome`. Os três atributos
sem sublinhado no começo são os que quem usa o pacote pode ler:

| Atributo | Antes de `generate()` | Depois de `generate()` |
|---|---|---|
| `grid` | `[]` (lista vazia) | `height` listas de `width` inteiros; `grid[y][x]` são as paredes da célula `x,y` |
| `solution` | `""` (texto vazio) | o caminho mais curto em letras `N`, `E`, `S`, `W` |
| `pattern` | as células `(x, y)` do "42" | as mesmas |

`generate()` é o método que gera o labirinto ([página 4](./03-generate.md)).

`pattern` já existe desde o construtor porque só depende do tamanho. A aplicação o usa para pintar
o "42" de cinza e para avisar quando ele não coube (conjunto vazio, em grades menores que 9x7).

`grid` usa os mesmos números do arquivo de saída: cada número, de 0 a 15, soma os bits das paredes
fechadas da célula (Norte = 1, Leste = 2, Sul = 4, Oeste = 8,
[parte 1](../01-o-problema/02-paredes-em-bits.md)). O enunciado permite outro formato: ele diz
que o gerador dá acesso à estrutura do labirinto, "não necessariamente no mesmo formato do
arquivo de saída". Mas com os mesmos números a aplicação grava o arquivo sem conversão nenhuma;
usar o mesmo formato é escolha do projeto.
