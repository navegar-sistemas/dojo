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

O `make` já vem instalado no Linux e no macOS.

## A pasta do projeto

Todo o código fica numa pasta só, que é a pasta entregue (o repositório git). O tutorial a
chama de **raiz do projeto**, e todo caminho de arquivo citado, como `mazegen/errors.py` ou
`amazeing/ui/menu.py`, é relativo a ela.

## Quando aparecer um termo desconhecido

O [glossário](./05-glossario.md) reúne todos os termos do tutorial, com uma explicação curta e o
link para a página que os explica em detalhe.
