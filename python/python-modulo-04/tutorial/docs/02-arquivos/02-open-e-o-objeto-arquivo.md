---
sidebar_position: 2
title: open e o objeto arquivo
---

# open e o objeto arquivo

Antes de ler ou escrever um arquivo, o programa precisa **abri-lo**: pedir ao sistema operacional
acesso ao arquivo. É o que faz a função `open()`.

## Abrir

Crie `experimentos/abrir.py`:

```python
file = open("ancient_fragment.txt")
print(file)
file.close()
```

```bash
python3 experimentos/abrir.py
```

```text
<_io.TextIOWrapper name='ancient_fragment.txt' mode='r' encoding='utf-8'>
```

`open("ancient_fragment.txt")` **não** devolve o texto do arquivo. Devolve um **objeto arquivo**: um
valor que representa o arquivo aberto e tem os métodos para usá-lo. O `print` mostra o que ele é:

- `_io.TextIOWrapper` é o **tipo** do objeto, também chamado de **classe**: um arquivo aberto em
  **modo texto**, que entrega e recebe `str`. A classe é a `TextIOWrapper` do módulo `io`; o `print`
  mostra `_io`, o nome interno desse mesmo módulo. É a resposta à pergunta que o enunciado faz no
  exercício 0: "qual é o tipo do dado devolvido por `open()`?";
- `name` é o caminho usado para abrir;
- `mode='r'` é o **modo de abertura**: `r` (*read*) abre só para leitura, e é o modo usado quando
  nenhum é informado;
- `encoding` é a **codificação**: a regra que traduz os bytes do disco em caracteres. UTF-8 é a
  usada em quase todo sistema hoje. A partir do Python 3.15, o `open()` usa UTF-8 por padrão, e o
  `print` mostra `utf-8`. Até o 3.14, a codificação vem da **configuração de idioma** do sistema;
  na mais comum do Linux e do macOS (`pt_BR.UTF-8`, `en_US.UTF-8`), também é UTF-8, mas o `print`
  a mostra em maiúsculas: `encoding='UTF-8'`.

A última linha, `file.close()`, fecha o arquivo; a página [close e o
recurso](./04-close-e-o-recurso.md) explica por que isso importa.

## Os métodos do objeto arquivo

O enunciado lista os métodos permitidos como `io.read()`, `io.write()` e assim por diante. São
métodos do objeto que `open()` devolve, chamados com ponto, como `file.read()`:

| Método | O que faz | Onde aparece |
|---|---|---|
| `read()` | lê o arquivo inteiro e devolve um `str` | [read e o texto](./03-read-e-o-texto.md) |
| `close()` | fecha o arquivo | [close e o recurso](./04-close-e-o-recurso.md) |
| `write(texto)` | escreve um `str` no arquivo | [Gravar o arquivo](../04-ex1/05-gravar-o-arquivo.md) |
| `readline()` | lê uma linha só | [Ler sem input](../05-ex2/04-ler-sem-input.md) |
| `flush()` | despeja no destino o que estava esperando para ser escrito | [Escrever no stderr](../05-ex2/03-escrever-no-stderr.md) |

## O type hint do objeto arquivo

Um type hint pode anotar uma variável, além de parâmetros e retornos: `count: int = 0`. Para anotar
a variável que guarda um arquivo aberto, o enunciado autoriza `typing.IO`, do módulo `typing` (o
módulo de tipos para type hints):

```python
import typing

file: typing.IO[str] = open("ancient_fragment.txt")
```

`typing.IO[str]` quer dizer "um arquivo aberto que lê e escreve `str`". O `TextIOWrapper` é um caso
particular disso, e o mypy aceita a atribuição. O type hint usa `typing.IO[str]`, e não
`TextIOWrapper`, por dois motivos: anotar com `TextIOWrapper` exigiria `import io`, que não está
entre os autorizados; e o que importa para o resto do código é o que o objeto faz (ler e escrever
texto), não a classe exata que o Python usou por dentro.
