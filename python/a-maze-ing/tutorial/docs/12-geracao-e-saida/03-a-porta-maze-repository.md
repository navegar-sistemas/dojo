---
sidebar_position: 3
title: A porta MazeRepository
---

# A porta `MazeRepository`

A operação "gerar um labirinto" precisa terminar **gravando** o arquivo de saída. Quem comanda
essa operação é o `GenerateMaze` (página
["O caso de uso GenerateMaze"](./06-o-caso-de-uso-generate-maze.md)); quem sabe gravar é o
`FileMazeRepository` (página ["Gravando o arquivo de saída"](./05-gravando-o-arquivo.md)). Só que a arquitetura
do projeto proíbe o `GenerateMaze` de importar o `FileMazeRepository`. Esta página mostra como um
consegue usar o outro sem importá-lo.

## A regra que impede o import

O projeto é dividido em **camadas**, e uma camada só pode importar as que estão mais para dentro
([parte 2](../02-arquitetura/03-regra-de-dependencia.md)).

- O `GenerateMaze` é um **use case**: uma operação completa da aplicação, como "gerar e gravar
  um labirinto". Ele fica na camada `use_cases`, mais para dentro.
- O `FileMazeRepository` fica na camada `repositories`, a que mexe em arquivos, mais para fora.
  O detalhe de **como** gravar (formato, disco, mensagens de erro) pode mudar sem a operação
  mudar.

Então o `GenerateMaze` precisa gravar, mas não pode citar a classe que grava.

## A analogia: a tomada

A [parte 2](../02-arquitetura/07-a-porta-e-a-inversao.md) comparou a porta a uma tomada da
parede. Quem instala a tomada não sabe qual aparelho vai ser ligado nela; define só o
**formato** do encaixe. Qualquer aparelho com o plugue certo funciona, e trocar de aparelho não
exige mexer na parede.

No código é igual:

| Tomada | Código |
|---|---|
| a parede, que precisa de "algo ligado ali" | `GenerateMaze`, que precisa de "algo que grave" |
| o formato do encaixe | a **porta** `MazeRepository`: "um método `save(path, maze)`" |
| o aparelho com o plugue certo | `FileMazeRepository`, que grava em arquivo |
| quem liga o aparelho na tomada | o `a_maze_ing.py`, o arquivo principal ([parte 14](../14-menu-e-main/04-o-composition-root.md)) |

O formato do encaixe é definido por quem **usa** (o use case), não por quem é ligado. Por isso
a porta mora junto do use case, em `amazeing/use_cases/ports.py`.

## A porta em Python: `typing.Protocol`

```python
class MazeRepository(Protocol):
    """Storage of a generated maze."""

    def save(self, path: str, maze: GeneratedMaze) -> None:
        """Store a maze, replacing what the path held before."""
```

Um `Protocol` descreve uma **forma**: "qualquer objeto que tenha um método
`save(path: str, maze: GeneratedMaze) -> None`". Ele não grava nada; não tem código, só a
assinatura. O corpo do método é só a docstring, que já é um comando válido e dispensa `pass`.

`-> None` quer dizer que o método não devolve nada: ele só faz o trabalho (gravar).

### Sem herança

A diferença para uma classe base comum está em como uma classe passa a "ser" um
`MazeRepository`:

| Classe base abstrata (`ABC`) | `Protocol` |
|---|---|
| a classe concreta precisa **herdar** dela: `class FileMazeRepository(MazeRepository)` | basta **ter** o método com a assinatura certa, sem herdar nada |
| o repositório importaria `use_cases/ports.py` | o repositório não importa nada de `use_cases` |

Uma `ABC` (*abstract base class*) é uma classe feita só para ser herdada. Com ela, o
`FileMazeRepository` teria de importar `ports.py`, que mora em `use_cases`.

Pela direção das setas, isso não seria proibido: `repositories` fica mais para fora que
`use_cases`, e uma camada de fora pode depender de uma de dentro. Quem proíbe é a tabela de
imports permitidos da [parte 2](../02-arquitetura/03-regra-de-dependencia.md): `repositories` só
importa `domain`, `utils` e `errors`. É uma escolha do projeto: o repositório sabe gravar e ler
arquivos e não precisa saber que existe um use case.

Com o `Protocol`, essa regra continua cumprida: vale a **forma** do objeto, não a árvore de
herança. É a ideia do "se anda como pato e grasna como pato, é um pato".

Como as peças se ligam, o arquivo completo da porta e um exemplo do `mypy` conferindo a forma
estão na [próxima página](./08-a-porta-completa.md).
