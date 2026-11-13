---
sidebar_position: 5
title: Os papéis das classes
---

# Os papéis das classes

Um projeto com vinte classes fica difícil de ler se cada uma for um caso à parte. Aqui, toda
classe tem um **papel** dentre poucos possíveis, e o papel diz, antes de ler o código, o que
ela pode e o que não pode fazer: um value object nunca muda, um repository é o único que abre
arquivo. Esta página apresenta os papéis do miolo do programa, cada um com um exemplo do
próprio projeto; a [página seguinte](./06-os-outros-papeis.md) apresenta os outros.

Duas palavras ajudam a separar os papéis:

- **estado**: os dados que um objeto guarda nos seus atributos e que podem mudar entre uma
  chamada e outra. Uma lista que ganha elementos tem estado que muda; o número `3`, não.
- **I/O** (de *input/output*, entrada e saída): tudo o que fala com fora do programa. Abrir um
  arquivo, imprimir na tela e ler o teclado são I/O.

## Value object

Um objeto que é só um **valor**, como um número ou uma string: não muda depois de criado e é
comparado pelo **conteúdo**.

Exemplo: a `Cell`, a posição `x,y` de uma célula. Duas `Cell(3, 4)` criadas em lugares
diferentes são iguais, porque guardam os mesmos números:

```python
Cell(3, 4) == Cell(3, 4)   # True
```

Numa classe comum, o `==` compara a **identidade**: dois objetos criados separadamente são
diferentes, mesmo com os mesmos atributos. Num value object, o que importa é o valor.

- Feito com `@dataclass(frozen=True)`, um recurso do Python que escreve sozinho o `==` por
  conteúdo e impede mudar os campos ([parte 4, `Cell`](../04-value-objects/04-cell.md)), ou com
  `Enum`, quando os valores possíveis são uma lista fechada, como os quatro lados da célula
  ([parte 4, `Direction`](../04-value-objects/02-direction-bits.md)).
- Quando há uma regra para criar, a classe tem um **método de fábrica**: um método que recebe os
  dados brutos, faz as contas ou valida, e devolve o objeto pronto. O `Pattern42.for_size(20, 15)`
  recebe só o tamanho da grade e calcula quais células desenham o "42".
- Exemplos: `Cell`, `Direction` (um lado da célula), `Pattern42` (as células do "42"),
  `MazeConfig` (as opções lidas do config) e `GeneratedMaze`, um **retrato** do labirinto
  pronto: uma cópia tirada no fim da geração, que não muda mais, com a grade, a entrada, a
  saída, o caminho mais curto e as células do "42".

## Entidade

Um objeto com **estado que muda**, mas que protege as próprias regras: nenhum método deixa o
objeto num estado proibido.

Exemplo: o `Maze`, a grade de paredes. As paredes mudam o tempo todo enquanto o labirinto é
cavado. Mas o único jeito de abrir uma parede é o método `open_wall`, e ele sempre muda as duas
células que dividem aquela parede. Assim, duas vizinhas nunca discordam sobre a parede entre
elas (a regra de **coerência** do enunciado).

- Exemplos: `Maze` e `ViewState` (o estado da tela: se o caminho aparece e qual é a cor das
  paredes, que mudam quando o usuário escolhe uma opção do menu).

## Service

Uma **operação**, sem estado: recebe o que precisa por parâmetro, faz o trabalho e devolve. Não
guarda nada de uma chamada para a outra.

Exemplo: o `Carver` recebe um `Maze` todo fechado e cava os corredores. Chamá-lo duas vezes, com
duas grades, dá dois trabalhos independentes.

- Exemplos: `Carver` (cava), `Braider` (transforma em tabuleiro Pac-Man) e `Solver` (acha o
  caminho mais curto), os três na pasta `mazegen/services/`, que faz parte do gerador, no anel
  central das camadas; e `RenderService` (transforma o labirinto em texto colorido), na pasta
  `amazeing/services/`, a camada `services` do anel de fora.

## Use case

**Uma operação completa da aplicação**, do jeito que o usuário a enxerga, num único método
chamado `execute`.

- Não sabe quem grava o arquivo: depende de uma **porta** (abaixo), não de uma classe concreta.
- Exemplo: `GenerateMaze`, cujo `execute` gera o labirinto, monta o retrato `GeneratedMaze` (a
  cópia que não muda mais, descrita no value object acima) e o grava no arquivo de saída.

## Port

Uma **descrição** do que um use case precisa de outra classe: os nomes dos métodos e os tipos,
sem código dentro. É escrita como `typing.Protocol`, um recurso do Python explicado na
[parte 12](../12-geracao-e-saida/03-a-porta-maze-repository.md).

- Exemplo: `MazeRepository`, que diz "preciso de algo com um método `save(path, maze)`".

O [próximo grupo de papéis](./06-os-outros-papeis.md) é o que fica nas pontas: a classe que quem
reutiliza o gerador usa, os tipos de erro, quem abre arquivos, quem fala com o usuário e quem
liga tudo.
