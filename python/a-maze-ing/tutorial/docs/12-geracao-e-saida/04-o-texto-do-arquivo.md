---
sidebar_position: 5
title: O texto do arquivo de saída
---

# O texto do arquivo de saída

O enunciado manda gravar cada labirinto num arquivo de texto, num formato exato, que outro
programa (o `maze_analyzer.py`, que acompanha o enunciado) lê para conferir o labirinto. Antes de
gravar, é preciso **montar** esse texto a partir do retrato `GeneratedMaze`
([página 1](./01-o-retrato-generated-maze.md)). Esta página monta o texto; a
[próxima](./05-gravando-o-arquivo.md) o grava no disco.

## O formato, relembrado

O arquivo tem cinco partes ([parte 1](../01-o-problema/04-o-arquivo-de-saida.md)):

1. a **grade**: uma linha do arquivo por linha do labirinto, um caractere por célula. O caractere
   é o número das paredes fechadas da célula (de 0 a 15) escrito em **hexadecimal**: `0` a `9` e
   depois `a` (10) a `f` (15) ([parte 1](../01-o-problema/02-paredes-em-bits.md));
2. uma linha vazia;
3. a entrada, como `x,y`;
4. a saída, como `x,y`;
5. o caminho mais curto, uma letra `N`, `E`, `S` ou `W` por passo.

Toda linha termina com uma quebra de linha (`\n`), inclusive a última.

Um exemplo: o labirinto que `MazeGenerator(11, 9, seed=3)` gera. Os parâmetros que não foram
passados ficam com o valor que o gerador usa quando eles são omitidos: entrada `0,0`, saída no
canto de baixo à direita (`10,8`) e `perfect=False`, o modo Pac-Man (o enunciado também chama
esse modo de padrão, mas no arquivo de configuração a chave `PERFECT` é obrigatória).

![Labirinto 11 por 9 com o dígito hexadecimal de cada célula, a entrada em magenta, a saída em vermelho e o 42 em cinza](/img/geracao/arquivo-11x9.svg)

Na figura, cada célula mostra o seu dígito; a entrada está em magenta, a saída em vermelho e as
células do "42" em cinza.

```text
95395391553
a968546c552
aafa93fff96
86fc6857fc3
c3fffafff92
9693fafd52a
a92afafffaa
aa829451542
c6c44554556

0,0
10,8
SSSSESWSSSENNESESEEEEEEE
```

Cada dígito do arquivo é o número escrito na célula da figura: a linha `y` do arquivo é a linha
`y` da grade, e o caractere de número `x` dessa linha (contando de 0) é a célula `x,y`. Os `f` do
meio são as células do "42", com as quatro paredes fechadas.

## A classe `FileMazeRepository`

Quem monta e grava é o `FileMazeRepository` (`amazeing/repositories/maze_repository.py`), o
*repository* do arquivo de saída: o único que abre esse arquivo. O trabalho se divide em dois
métodos: `to_text`, que monta o texto, e `save`, que grava.

## A grade em hexadecimal

```python
lines = ["".join(format(cell, "x") for cell in row)
         for row in maze.grid]
```

De dentro para fora:

- `format(cell, "x")` escreve o número `cell` em hexadecimal: `13` vira `"d"`.
- `"".join(...)` cola os dígitos de uma linha sem nada entre eles: os números
  `(9, 1, 3)` viram `"913"`.
- `[... for row in maze.grid]` faz isso para cada linha da grade e junta os resultados numa
  lista de textos, um por linha.

O `"x"` dá letras **minúsculas** e nenhum prefixo. As outras formas de escrever hexadecimal no
Python dariam outra coisa:

| Valor | `format(v, "x")` | `hex(v)` | `format(v, "X")` |
|---|---|---|---|
| 0 | `0` | `0x0` | `0` |
| 9 | `9` | `0x9` | `9` |
| 10 | `a` | `0xa` | `A` |
| 15 | `f` | `0xf` | `F` |

- `hex()` põe o prefixo `0x` na frente, que teria de ser cortado.
- `"X"` dá maiúsculas. O `maze_analyzer.py` aceita as duas; minúsculas são escolha do projeto,
  igual ao exemplo do enunciado.

Como o valor de uma célula vai de 0 a 15, o resultado tem sempre **um** dígito: nunca é preciso
completar com zero à esquerda.

## O rodapé

```python
ex, ey = maze.entry
sx, sy = maze.exit
lines += ["", f"{ex},{ey}", f"{sx},{sy}", maze.solution]
```

- `ex, ey = maze.entry` separa a tupla da entrada nos seus dois números, e
  `sx, sy = maze.exit` faz o mesmo com a saída. `ex, ey` são o x e o y da entrada (*entry*);
  `sx, sy` os da saída (o `s` de saída, porque `exit` também começaria com `e`).
- `lines += [...]` acrescenta quatro linhas no fim da lista.
- `""` é a linha vazia que separa a grade do rodapé.
- `f"{ex},{ey}"` escreve `0,0`: sem espaço e sem parênteses, o mesmo formato do arquivo de
  configuração. Escrever `str(maze.entry)` daria `(0, 0)`, que o `maze_analyzer.py` não lê.
- O caminho é o `solution`, as mesmas letras que o desenho pinta de ciano.

O exemplo de arquivo do enunciado mostra anotações como `# entry (x,y)` ao lado do rodapé. Elas
explicam a figura e não fazem parte do arquivo: com elas, o `maze_analyzer.py` não consegue ler
a entrada.

## Juntar com `\n`

```python
return "\n".join(lines) + "\n"
```

`"\n".join(lines)` põe uma quebra de linha **entre** as linhas, mas não depois da última:
`"\n".join(["a", "b"])` dá `"a\nb"`. O `+ "\n"` do fim faz a última linha, a do caminho,
terminar em quebra também, como o enunciado pede.

## Por que `to_text` é separado e estático

Montar o texto não precisa de arquivo nem de dado nenhum do objeto: recebe um retrato e devolve
um texto. Por isso é um `@staticmethod`, um método que se chama direto pela classe
(`FileMazeRepository.to_text(maze)`), e fica separado do `save` por dois motivos:

- o `save` fica curto: abrir, escrever, tratar o erro;
- dá para ver o conteúdo exato sem gravar nada, como mostra o Experimente da
  [próxima página](./05-gravando-o-arquivo.md#experimente), depois do arquivo completo.
