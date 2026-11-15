---
sidebar_position: 1
title: O estado da tela
---

# O estado da tela

O menu do programa tem duas opções que mudam o **desenho** sem mudar o labirinto: a `2` mostra
ou esconde o caminho mais curto, e a `3` troca a cor das paredes. O programa precisa lembrar
essas duas escolhas de um desenho para o seguinte, inclusive depois que o usuário pede um
labirinto novo. A classe `ViewState` ("estado da visualização") guarda as duas.

## Quem usa o `ViewState`

- O `Menu` ([parte 14](../14-menu-e-main/01-o-laco-do-menu.md)), a classe que mostra as opções e
  lê o que o usuário digita, **muda** o estado: na opção `2` ele liga ou desliga o caminho, na
  opção `3` passa para a próxima cor.
- O `RenderService`, a classe que transforma o labirinto em linhas coloridas de texto (as
  próximas páginas desta parte), só **lê** o estado, para decidir as cores.

## Por que não guardar junto com o labirinto

O labirinto pronto fica num `GeneratedMaze`: o **retrato** de uma geração, com as paredes, a
entrada, a saída, o caminho e as células do "42", que nunca muda depois de criado
([parte 12](../12-geracao-e-saida/01-o-retrato-generated-maze.md)). A opção `1` do menu gera
outro labirinto e cria um retrato **novo**. Se o estado da tela morasse no retrato, ele voltaria
ao início a cada labirinto novo.

As opções do arquivo de configuração ficam num `MazeConfig`
([parte 11](../11-configuracao/01-o-value-object-maze-config.md)), que também nunca muda durante
a execução.

O estado da tela precisa do contrário dos dois: **mudar** durante a sessão e **sobreviver** aos
labirintos novos. Quem mostrou o caminho e trocou a cor para verde, e depois pediu um labirinto
novo, continua vendo o caminho, em paredes verdes. Por isso ele mora num objeto próprio, criado
uma vez no começo do programa.

## Uma entidade

O projeto separa as classes por papel ([parte 2](../02-arquitetura/04-papeis-das-classes.md)).
Dois papéis importam aqui:

- um **value object** é um valor que nunca muda depois de criado, como uma coordenada;
- uma **entidade** é um objeto cujo estado muda com o tempo, mas que protege as próprias
  regras: os métodos dele nunca o deixam num estado inválido.

O `ViewState` muda (o caminho liga e desliga, a cor gira), então é uma entidade. As regras que
ele protege são pequenas, mas existem:

- `colour_index`, a posição da cor atual na lista de cores, fica sempre entre 0 e 3;
- `show_path` ("mostrar o caminho") só vale `True` ou `False`.

Os métodos `toggle_path()` e `next_colour()` ([próxima página](./07-os-metodos-do-view-state.md))
só levam o estado de um valor válido para outro. Nada no Python, porém, impede um código de fora
de escrever `state.colour_index = 7`: o atributo é público, sem `_` na frente. A proteção é uma
convenção do projeto: o `Menu` só muda o estado pelos métodos, e o `RenderService` só lê. Com
`colour_index = 7`, a paleta, que tem quatro cores (índices 0 a 3), não teria a cor pedida, e o
Python levantaria (lançaria) a exceção `IndexError` na hora de desenhar.

O arquivo fica em `amazeing/domain/entities/`. O projeto tem dois pacotes
([parte 2](../02-arquitetura/02-dois-pacotes.md)): o `mazegen`, o gerador reutilizável que outro
projeto pode instalar, e o `amazeing`, a aplicação (configuração, arquivo de saída, tela e
menu). Caminho visível e cor de parede são assuntos da tela, então o `ViewState` fica no
`amazeing`; o `mazegen` nem sabe que existe uma tela. A pasta `domain` reúne as classes da
aplicação que não abrem arquivos nem imprimem nada.

## A paleta

```python
from amazeing.utils.ansi import Ansi, Rgb

PALETTE = (Ansi.CHARCOAL, Ansi.ORANGE, Ansi.GREEN, Ansi.BLUE)
```

`PALETTE` ("paleta") é a lista das cores que as paredes podem ter, na ordem do rodízio. Cada cor
é uma tupla de três números, a quantidade de vermelho, de verde e de azul (uma **cor RGB**, de 0
a 255 cada), e entra no desenho como a cor do traço das paredes. A classe `Ansi`
([parte 10](../10-utilitarios/04-cores-ansi.md)) dá nome a essas tuplas, e `Rgb` é o apelido do
tipo delas, usado na anotação da [próxima página](./07-os-metodos-do-view-state.md):

| Nome | RGB | Cor |
|---|---|---|
| `Ansi.CHARCOAL` | `31, 41, 55` | grafite |
| `Ansi.ORANGE` | `194, 65, 12` | laranja |
| `Ansi.GREEN` | `21, 128, 61` | verde |
| `Ansi.BLUE` | `29, 78, 216` | azul |

A paleta é uma **tupla** (entre parênteses), e não uma lista (entre colchetes), porque uma tupla
não pode ser alterada depois de criada, e a paleta nunca muda.

As quatro cores são escolha do projeto ([parte
1](../01-o-problema/07-o-desenho-e-o-menu.md#as-cores)). Elas são escuras o bastante para aparecer
sobre o fundo branco do desenho e diferentes de todas as cores fixas (cinza no "42", magenta na
entrada, vermelho na saída, ciano no caminho). Assim, qualquer que seja a cor das paredes, as
marcações continuam visíveis.

Os métodos que mudam e leem o estado, e o arquivo completo, estão na
[próxima página](./07-os-metodos-do-view-state.md).
