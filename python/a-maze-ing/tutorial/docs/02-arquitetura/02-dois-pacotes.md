---
sidebar_position: 2
title: "Dois pacotes: mazegen e amazeing"
---

# Dois pacotes: `mazegen` e `amazeing`

## `mazegen`: o gerador reutilizável

Tudo o que é necessário para **gerar** um labirinto, e nada mais:

- coordenadas e direções;
- a grade de paredes;
- os algoritmos de geração, de braiding e de solução;
- a classe pública `MazeGenerator`.

Esse pacote vira o arquivo `mazegen-1.0.0-py3-none-any.whl`. Quem instala o pacote ganha a
geração, sem config, sem arquivo e sem terminal. Por isso `mazegen`:

- só importa a biblioteca padrão do Python;
- nunca importa nada de `amazeing` nem de `a_maze_ing`;
- não lê nem grava arquivos, e não imprime nada.

## `amazeing`: a aplicação

Tudo o que é específico **deste programa**:

- ler e validar o `config.txt`;
- gravar o arquivo de saída;
- desenhar no terminal;
- o menu.

Esse pacote **não** vai para o wheel. Ele usa o `mazegen` como usaria qualquer biblioteca
instalada.

## `a_maze_ing.py`: o ponto de entrada

Um arquivo pequeno na raiz, que o subject manda executar (`python3 a_maze_ing.py config.txt`).
Ele confere os argumentos, monta as peças e captura qualquer erro para imprimir uma mensagem
limpa.

## Por que os nomes diferentes

| Nome | Motivo |
|---|---|
| `mazegen` | o subject exige que o pacote se chame `mazegen-*` |
| `amazeing` | o nome do projeto sem hífen nem acento; um nome de pacote Python não pode ter `-` |
| `a_maze_ing.py` | o nome que o subject manda executar |

## O que o `mazegen` mostra para fora

O `mazegen/__init__.py` exporta só duas coisas:

```python
from mazegen import MazeGenerator, MazeError
```

`Maze`, `Cell`, `Direction` e os algoritmos ficam internos. Quem reutiliza o pacote só precisa
conhecer a classe de geração e a exceção que ela pode levantar.
