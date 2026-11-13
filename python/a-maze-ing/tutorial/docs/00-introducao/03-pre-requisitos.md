---
sidebar_position: 3
title: Pré-requisitos
---

# Pré-requisitos

O que você precisa ter instalado e saber antes de começar.

## Python 3.10 ou mais novo

O enunciado exige Python na versão 3.10 ou mais nova. Confira a sua no terminal:

```bash
python3 --version
```

A resposta precisa ser `Python 3.10.x` ou um número maior. O código do projeto usa recursos que
não existem em versões anteriores, por exemplo:

- `int | None` numa anotação de tipo, que quer dizer "um inteiro ou `None`";
- `@dataclass(slots=True)`, uma opção das classes de dados explicada na
  [parte 4](../04-value-objects/04-cell.md).

## O que você precisa saber de Python

- funções, classes e métodos;
- listas, dicionários, conjuntos (`set`) e tuplas;
- `try`/`except` para tratar erros e `with open(...)` para abrir arquivos;
- anotações de tipo simples, como `def soma(a: int, b: int) -> int:`.

O resto (`@property`, `dataclass`, `Enum`, `typing.Protocol`, operações com bits, busca em
largura) é explicado na página em que aparece pela primeira vez.

### Compreensão de lista

Uma construção aparece em muitas páginas e vale ver antes: a **compreensão de lista** (*list
comprehension*), um jeito curto de montar uma lista com um laço `for` dentro de colchetes.

```python
dobros = [n * 2 for n in range(4)]
```

`dobros` fica `[0, 2, 4, 6]`. A linha faz o mesmo que este laço:

```python
dobros = []
for n in range(4):
    dobros.append(n * 2)
```

Lê-se da esquerda para a direita: "a lista de `n * 2`, para cada `n` de `range(4)`". Duas
variações aparecem no tutorial:

- um `if` no fim filtra os itens: `[n for n in range(10) if n % 2 == 0]` dá `[0, 2, 4, 6, 8]`
  (só os pares);
- com chaves no lugar dos colchetes, o resultado é um conjunto (`set`), e a construção se chama
  **compreensão de conjunto**: `{n % 3 for n in range(10)}` dá `{0, 1, 2}`.

## Ferramentas

O projeto usa algumas ferramentas além do próprio Python. Nenhuma precisa ser instalada à mão:
o comando `make install`, criado na [parte 3](../03-ambiente/01-o-ambiente-virtual.md), instala
tudo dentro de uma pasta do projeto.

| Ferramenta | O que faz | Por que o projeto usa |
|---|---|---|
| ambiente virtual (`python3 -m venv`) | cria uma pasta com um Python e bibliotecas só deste projeto | as ferramentas abaixo ficam isoladas do resto do computador |
| `make` | roda atalhos de comandos definidos num arquivo `Makefile` | o enunciado exige um `Makefile` com os atalhos `install`, `run`, `debug`, `clean`, `lint` |
| `flake8` | confere o estilo do código: tamanho das linhas, espaços, imports sem uso | o enunciado exige que o código passe nele |
| `mypy` | confere as anotações de tipo: avisa, por exemplo, quando uma função promete devolver `int` e devolve texto | o enunciado exige que o código passe nele |
| `build` | empacota o gerador num arquivo instalável com `pip` | o enunciado exige o gerador como pacote |

O `make` é a única ferramenta que precisa existir antes. Confira com `make --version`:

- no Linux, se o comando não for encontrado, instale pelo gerenciador de pacotes da
  distribuição (no Debian e no Ubuntu: `sudo apt install make`);
- no macOS, ele vem com as ferramentas de linha de comando da Apple, instaladas com
  `xcode-select --install`.

## A pasta do projeto

Todo o código fica numa pasta só, que é a pasta entregue (o repositório git). O tutorial a
chama de **raiz do projeto**, e todo caminho de arquivo citado, como `mazegen/errors.py` ou
`amazeing/ui/menu.py`, é relativo a ela.

## Como rodar os exemplos

Muitas páginas têm um bloco **Experimente**: um trecho curto de Python para ver a peça recém-
construída funcionando, seguido da saída que ele imprime. Todo exemplo roda na raiz do projeto
e só usa o que as páginas anteriores já construíram.

Os exemplos usam o Python do ambiente virtual do projeto, `.venv/bin/python`, criado na
[parte 3](../03-ambiente/01-o-ambiente-virtual.md). Um exemplo de uma linha roda com `-c`:

```bash
.venv/bin/python -c 'print(13 // 2)'
```

Um exemplo de várias linhas roda assim: tudo entre a primeira linha e o `EOF` final é entregue ao
Python como se fosse um arquivo.

```bash
.venv/bin/python - <<'EOF'
total = 0
for n in (1, 2, 4, 8):
    total += n
print(total)
EOF
```

Quando um exemplo cria arquivos para experimentar, o próprio bloco termina apagando-os, para
eles não irem parar na entrega.

O programa inteiro só fica pronto no fim da
[parte 14](../14-menu-e-main/06-saidas-e-erros-inesperados.md). A partir daí ele roda com
`make run` ou com `.venv/bin/python a_maze_ing.py config.txt`, que é o
`python3 a_maze_ing.py config.txt` do enunciado usando o Python do ambiente virtual.

## Quando aparecer um termo desconhecido

O [glossário](./05-glossario.md) reúne os termos do tutorial, com uma explicação curta e o
link para a página que os explica em detalhe.
