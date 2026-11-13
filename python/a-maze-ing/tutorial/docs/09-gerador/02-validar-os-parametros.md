---
sidebar_position: 3
title: Validar os parâmetros
---

# Validar os parâmetros

Quem chama `MazeGenerator(width=0, height=15)` pediu um labirinto impossível. Se o construtor
aceitasse, o erro só apareceria mais tarde, no meio da geração, com uma mensagem confusa ou um
labirinto errado. Esta página mostra o começo do construtor, que confere cada parâmetro e recusa
os impossíveis com uma mensagem que diz o que corrigir.

## Por que o construtor confere

A aplicação `amazeing` já confere o arquivo de configuração antes de criar o gerador
([parte 11](../11-configuracao/03-a-ordem-das-validacoes.md)). Mesmo assim, o `MazeGenerator`
confere de novo, porque ele é uma biblioteca: um projeto futuro pode chamá-lo direto, sem arquivo
de configuração nenhum, e o gerador não pode confiar que alguém conferiu antes.

Os erros aparecem **no construtor**, antes de qualquer trabalho. Assim, um `MazeGenerator` que
existe sempre tem parâmetros possíveis, e o método `generate()` não precisa conferir nada.

O erro é sempre um `MazeError`, a exceção do `mazegen`
([parte 4](../04-value-objects/01-maze-error.md)), e a mensagem **cita o nome do parâmetro**: quem
recebe o erro sabe o que corrigir sem ler o código.

## Tamanho

```python
        for name, value in (("width", width), ("height", height)):
            if not MIN_SIZE <= value <= MAX_SIZE:
                raise MazeError(f"{name} must be between {MIN_SIZE} and "
                                f"{MAX_SIZE}, got {value}")
```

- O laço percorre dois pares `(nome, valor)`: assim o mesmo `if` serve para a largura e para a
  altura, sem ser escrito duas vezes. `width` vem antes de `height`: com os dois errados, o erro
  fala de `width`.
- `MIN_SIZE <= value <= MAX_SIZE` é uma comparação encadeada do Python: vale o mesmo que
  `MIN_SIZE <= value and value <= MAX_SIZE`. O `not` inverte: o erro sai quando o valor está fora
  do intervalo.
- `raise MazeError(...)` interrompe o construtor e **levanta** (lança) a exceção: ela sobe para
  quem chamou `MazeGenerator(...)`, e o objeto nunca chega a existir.
- O `f` antes das aspas faz uma **f-string**: cada `{nome}` dentro dela é trocado pelo valor da
  variável. Com `width=0`, a mensagem fica `width must be between 1 and 100, got 0`. As duas
  f-strings seguidas, uma em cada linha, são coladas numa só pelo Python.

## Entrada e saída na grade

```python
        if exit is None:
            exit = (width - 1, height - 1)
        for name, (x, y) in (("entry", entry), ("exit", exit)):
            if not (0 <= x < width and 0 <= y < height):
                raise MazeError(f"{name} ({x}, {y}) is outside the maze")
        if entry == exit:
            raise MazeError("entry and exit must differ")
```

- O `None` vira o canto de baixo à direita **antes** das conferências, para a saída padrão passar
  pelas mesmas regras que uma saída informada.
- `for name, (x, y) in ...` desmonta cada item em três variáveis de uma vez: o nome e as duas
  coordenadas.
- Uma coordenada está dentro da grade quando `x` vai de 0 a `width − 1` e `y` de 0 a
  `height − 1`.
- O enunciado exige entrada e saída dentro da grade e diferentes uma da outra.

## Tamanho possível para o Pac-Man

```python
        if not perfect and (width - 1) * (height - 1) < 2:
            raise MazeError(
                "perfect=False needs (width - 1) x (height - 1) >= 2 for a "
                f"Pac-Man board, got {width}x{height}")
```

O tabuleiro Pac-Man precisa de pelo menos 2 ciclos (duas rotas independentes). Uma grade
`width x height` com **todas** as paredes de dentro abertas tem `(width − 1) × (height − 1)`
ciclos independentes: um para cada quadradinho 2x2 de células
([parte 1](../01-o-problema/09-sem-saloes-e-o-braiding.md#tamanhos-impossíveis)). Se essa conta dá menos que 2, nem abrindo
tudo o tabuleiro chega lá: grades de 1 linha, de 1 coluna e 2x2 são impossíveis no modo Pac-Man.

Recusar já no construtor é escolha do projeto: evita gastar as tentativas de `generate()` numa
grade que nunca vai dar certo, e a mensagem explica o motivo.

## Entrada e saída fora do "42"

```python
        pattern42 = Pattern42.for_size(width, height)
        for name, (x, y) in (("entry", entry), ("exit", exit)):
            if Cell(x, y) in pattern42:
                raise MazeError(f'{name} ({x}, {y}) lies on the "42" pattern')
```

- `Pattern42.for_size` calcula as células do "42" para o tamanho pedido
  ([parte 4](../04-value-objects/05-pattern42-posicao.md)). O "42" depende só do tamanho, então é
  calculado uma vez, aqui.
- Uma entrada ou saída dentro do "42" seria uma célula fechada nos quatro lados, impossível de
  alcançar. Recusar (em vez de, por exemplo, mudar o "42" de lugar) é escolha do projeto.
- `in pattern42` pergunta se a célula faz parte do desenho. O `Pattern42` responde a `in` só para
  `Cell` ([parte 4](../04-value-objects/06-pattern42-consulta.md)), por isso a tupla vira
  `Cell(x, y)` antes.
- A mensagem usa aspas simples por fora (`f'...'`) porque o texto tem aspas duplas dentro (`"42"`).

## Guardar o estado

```python
        self._width = width
        self._height = height
        self._entry = Cell(*entry)
        self._exit = Cell(*exit)
        self._perfect = perfect
        self._pattern42 = pattern42
        self._rng = random.Random(seed)
        self.grid: list[list[int]] = []
        self.solution = ""
        self.pattern: set[tuple[int, int]] = {
            cell.as_tuple() for cell in pattern42.cells
        }
```

- Os atributos com sublinhado no começo (`_width`, `_rng`...) são internos: quem usa o pacote não
  deve mexer neles.
- `Cell(*entry)`: o `*` desmonta a tupla `(x, y)` em dois argumentos, como se estivesse escrito
  `Cell(entry[0], entry[1])`. Dentro do pacote, entrada e saída passam a ser `Cell`.
- `random.Random(seed)` cria o **único** sorteador do pacote
  ([parte 6](../06-carver/04-a-seed.md)). Com `seed=None`, o Python pega um valor imprevisível do
  sistema operacional, e cada execução sai diferente.
- `grid` e `solution` começam vazios: só `generate()` os preenche.
- `pattern` é montado com uma **compreensão de conjunto** (em inglês, *set comprehension*): o
  mesmo jeito curto da compreensão de lista
  ([pré-requisitos](../00-introducao/03-pre-requisitos.md)), mas
  entre chaves `{...}`, o que cria um `set` em vez de uma lista. Para cada `Cell` do "42", guarda
  a tupla `(x, y)` que `as_tuple()` devolve. Tuplas são o formato de fora do pacote.

Cada uma dessas recusas aparece rodando no fim da [página 5](./04-o-arquivo-do-gerador.md),
depois que o arquivo `mazegen/generator.py` estiver completo.
