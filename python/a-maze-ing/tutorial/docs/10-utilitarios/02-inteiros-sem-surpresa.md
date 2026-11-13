---
sidebar_position: 3
title: Inteiros sem surpresa
---

# Inteiros sem surpresa

O arquivo de configuração é texto: a linha `WIDTH=20` chega ao programa como o **texto** `"20"`,
não como o número 20. Antes de usar a largura, o programa precisa converter esse texto num
número, e recusar o que não for um número escrito do jeito esperado. Esta página mostra por que o
`int()` do Python não basta e escreve a regra que define um inteiro aceito; a
[próxima](./06-fullmatch-e-limite-de-digitos.md) completa a conversão, e as páginas
[5](./07-booleanos.md) e [6](./03-booleanos-e-coordenadas.md) convertem booleanos e
coordenadas.

Lembrando o arquivo ([parte 1](../01-o-problema/03-o-arquivo-de-configuracao.md)): uma opção
por linha, no formato `CHAVE=valor`. Viram inteiros a largura (`WIDTH`), a altura (`HEIGHT`), a
semente do sorteio (`SEED`) e cada metade de uma coordenada `x,y` (`ENTRY=0,0`).

## A classe `ValueParser`

Os conversores ficam em `amazeing/utils/value_parser.py`, na classe `ValueParser`. Ela é uma
classe **utilitária**: só agrupa funções, sem guardar dado nenhum. Cada função é um
`@staticmethod`, um método que não recebe `self` e se chama direto pela classe:

```python
ValueParser.to_int("20")    # 20
```

Quem usa os conversores é o `MazeConfig`, que valida o arquivo de configuração
([parte 11](../11-configuracao/02-convertendo-um-valor.md)).

## Por que `int()` sozinho não basta

`int(texto)` converte texto em inteiro, mas foi feito para aceitar tudo o que o **Python**
aceita como inteiro. Isso inclui textos que ninguém escreveria num arquivo de configuração de
propósito:

```bash
.venv/bin/python - <<'EOF'
for v in ["1_0", " 5", "7\n", "٢٠", "２０", "+7", "007"]:
    print(repr(v), "->", int(v))
EOF
```

```text
'1_0' -> 10
' 5' -> 5
'7\n' -> 7
'٢٠' -> 20
'２０' -> 20
'+7' -> 7
'007' -> 7
```

(`repr` mostra o texto com aspas e com os caracteres invisíveis escritos, como o `\n` da quebra
de linha.)

| Texto | O que `int()` faz | Por que é um problema |
|---|---|---|
| `1_0` | lê 10 | o `_` separa milhares no código Python (`1_000_000`), não num arquivo de configuração |
| ` 5`, `7\n` | lê 5 e 7 | ignora espaços e quebras de linha em volta; numa coordenada, `0, 5` passaria |
| `٢٠`, `２０` | lê 20 | aceita dígitos de outros alfabetos: árabe e os "largos" de teclados asiáticos |
| `+7`, `007` | lê 7 | inofensivos; esses o projeto aceita |

Nenhum desses casos quebra o programa, mas todos são **surpresas**: o usuário escreveu algo
estranho, provavelmente por engano, e o programa seguiria em frente como se fosse normal. Este
projeto escolheu ser **estrito**: só aceita dígitos de `0` a `9`, com um sinal opcional na
frente. O enunciado não fala disso; ele só exige que valor inválido vire mensagem clara.

Os espaços em volta de um valor inteiro (`WIDTH = 20`) não chegam aqui: quem lê o arquivo já os
tira ([parte 11](../11-configuracao/06-linha-a-linha.md)). O espaço só chegaria ao conversor
vindo de **dentro** de uma coordenada, como em `ENTRY=0, 5`, e o formato pedido é `x,y` sem
espaço.

### O caso extremo: textos gigantes

Desde o Python 3.10.7, o `int()` se recusa a converter textos com mais de 4300 dígitos, para
não travar numa conta enorme:

```text
Exceeds the limit (4300 digits) for integer string conversion: value has 5000 digits; use sys.set_int_max_str_digits() to increase the limit
```

Esse erro é um `ValueError`, o mesmo tipo de erro de um texto como `abc`. Sem um cuidado à parte,
ele seguiria o caminho de qualquer valor inválido: o `MazeConfig`, que confere o arquivo de
configuração na [parte 11](../11-configuracao/02-convertendo-um-valor.md), escreveria a mensagem
final no formato `WIDTH must be an integer, got '...'`, com o texto lido no lugar dos três
pontos. Com um valor de 5000 dígitos, a linha de erro mostrada ao usuário teria mais de 5000
caracteres. A [página 4](./06-fullmatch-e-limite-de-digitos.md) mostra como o `ValueParser` evita
isso.

## A regra: uma expressão regular

Uma **expressão regular** é um padrão que descreve a **forma** de um texto. O módulo `re` do
Python confere se um texto tem essa forma. A forma de um inteiro aceito:

```python
_INTEGER = re.compile(r"[+-]?[0-9]+")
```

| Pedaço | Quer dizer |
|---|---|
| `[+-]` | um caractere, que pode ser `+` ou `-` |
| `?` | o pedaço anterior é opcional: aparece uma vez ou nenhuma |
| `[0-9]` | um caractere entre `0` e `9` |
| `+` | o pedaço anterior aparece uma ou mais vezes |

Os colchetes `[...]` querem dizer "**um** caractere, escolhido desta lista". Dentro e fora deles,
o mesmo símbolo muda de papel:

- o `+` dentro de `[+-]` é só o sinal de mais, um dos caracteres da lista. O `+` do fim, fora dos
  colchetes, é um **quantificador**: um símbolo que diz quantas vezes o pedaço anterior se repete;
- o `-` dentro de colchetes indica um **intervalo** quando fica entre dois caracteres: `0-9` é
  "de `0` a `9`". No fim da lista, como em `[+-]`, ele não tem um segundo caractere para fechar o
  intervalo e vale como o próprio sinal de menos.

Lendo junto: "talvez um sinal, depois um ou mais dígitos de 0 a 9". Comparando o padrão com o
texto **inteiro**, casam `20`, `-3` e `+007`; não casam `2.5`, `1_0`, ` 5`, `+` e o texto vazio.
Comparar só o começo do texto daria outro resultado (`2.5` casaria pelo `2`); a
[próxima página](./06-fullmatch-e-limite-de-digitos.md) mostra essa diferença.

- O `r` antes das aspas cria uma *raw string*, em que `\` vale como o próprio caractere. Este
  padrão não tem `\`, mas o `r` é o costume em toda expressão regular.
- `re.compile` prepara o padrão uma vez, quando o arquivo é carregado. Cada conversão
  reaproveita o padrão pronto.
- O `_` no começo de `_INTEGER` é a convenção do Python para "interno a este arquivo".

### `[0-9]` e não `\d`

Muita expressão regular usa o atalho `\d` para "dígito". Em Python, `\d` aceita dígitos de
**qualquer** alfabeto, inclusive o `٢`. `[0-9]` lista os dez caracteres exatos, os dígitos do
**ASCII** (a tabela básica de 128 caracteres: letras sem acento, dígitos, pontuação e espaço):

```python
re.fullmatch(r"\d+", "٢٠")       # casa
re.fullmatch(r"[0-9]+", "٢٠")    # não casa: devolve None
```

`re.fullmatch(padrão, texto)` confere se o texto inteiro tem a forma do padrão; a
[próxima página](./06-fullmatch-e-limite-de-digitos.md) explica por que é ele, e não outro
método do `re`, que o `ValueParser` usa.
