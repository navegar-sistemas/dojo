---
sidebar_position: 4
title: Type hints, flake8 e mypy
---

# Type hints, flake8 e mypy

O código passa por duas conferências: o **estilo**, pelo flake8, e os **tipos**, pelo mypy.

## Type hints

Um **type hint** (dica de tipo) anota um tipo no código. Numa função, ele anota cada parâmetro e
o valor devolvido:

```python
def double(number: int) -> int:
    return number * 2
```

- `number: int` diz que o parâmetro `number` é um inteiro;
- `-> int` diz que a função devolve um inteiro;
- uma função que não devolve nada leva `-> None`.

Uma variável também pode ser anotada, com a mesma sintaxe dos parâmetros: `height: int = 25`.

O Python **não** confere essas anotações quando roda o programa; elas servem para quem lê e para
o mypy. Toda função e todo método do projeto leva type hints.

## Um arquivo com dois problemas

Crie `experimentos/estilo.py`:

```python title="experimentos/estilo.py"
def double(number: int) -> int:
    return number * 2
def triple(number):
    return number * 3
```

Ele tem dois defeitos: falta espaço entre as funções, e `triple` não tem type hints.

## O flake8

```bash
.venv/bin/flake8 experimentos
```

```text
experimentos/estilo.py:3:1: E302 expected 2 blank lines, found 0
```

Cada aviso diz o arquivo, a linha, a coluna, um código e a explicação: na linha 3, o estilo padrão
do Python (chamado **PEP 8**) pede **duas linhas em branco entre** as funções e classes escritas
fora de qualquer classe, e entre `double` e `triple` não havia nenhuma. Sem aviso nenhum, o flake8
não imprime nada.

O estilo padrão pede que todo arquivo `.py` termine com uma quebra de linha logo depois da última
linha. O botão de copiar, no canto de cada bloco de código, não leva essa quebra final, e alguns
editores não a acrescentam ao salvar. Sem ela, o flake8 acusa mais um aviso, na última linha:
`experimentos/estilo.py:4:22: W292 no newline at end of file` ("sem quebra de linha no fim do
arquivo"). A correção é pôr o cursor no fim da última linha, apertar Enter uma vez e salvar; o
[arquivo completo do exercício 0](../02-ex0/04-o-arquivo-completo.md) mostra os outros avisos
sobre o fim do arquivo.

O flake8 recebe as pastas a conferir. Nunca rode `flake8 .` (o ponto é "a pasta atual"): ele
entraria também na `.venv` e acusaria milhares de avisos no código das bibliotecas instaladas.

## O mypy

O mypy, rodado sem opções, só confere as funções que **têm** type hints; uma função sem nenhuma
anotação passa calada. A opção `--strict` ("rigoroso") liga um conjunto rigoroso de
conferências, entre elas a que acusa a **falta** de type hints:

```bash
.venv/bin/mypy --strict experimentos
```

```text
experimentos/estilo.py:3: error: Function is missing a type annotation  [no-untyped-def]
Found 1 error in 1 file (checked 1 source file)
```

## Corrigir

Com duas linhas em branco e os type hints em `triple`:

```python title="experimentos/estilo.py"
def double(number: int) -> int:
    return number * 2


def triple(number: int) -> int:
    return number * 3
```

```bash
.venv/bin/flake8 experimentos
.venv/bin/mypy --strict experimentos
```

```text
Success: no issues found in 1 source file
```

O flake8 não imprime nada, e o mypy diz que não achou problema. É isso que se espera de cada
exercício.

Usar `--strict` é escolha do projeto: além da falta de type hints, ele acusa outros descuidos de
tipo, e o código dos sete exercícios passa em todos. A opção mínima que cumpre a regra dos type
hints é `--disallow-untyped-defs`, que liga só a conferência de funções e métodos sem type hints
ou com algum faltando.

O mypy guarda o que já conferiu numa pasta `.mypy_cache`, criada na pasta onde ele roda, para
conferir mais rápido da próxima vez. Ela pode ser apagada à vontade e não faz parte da entrega.
