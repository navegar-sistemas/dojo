---
sidebar_position: 3
title: Numeric Processor
---

# Numeric Processor

O `NumericProcessor` aceita um número (`int` ou `float`) ou uma lista de números, e guarda cada
número como texto: `3.14` vira `"3.14"`, e `[1, 2]` vira dois itens, `"1"` e `"2"`.

## Duas funções de conferência

Antes da classe, duas funções soltas fazem as perguntas de tipo. `is_list_of` fica fora da
classe porque as três filhas a usam; `is_number` fica ao lado dela, junto com as conferências
das outras filhas (`is_text` e `is_log`, nas próximas páginas). No arquivo, as quatro funções
ficam juntas, depois de `DataProcessor` e antes das classes filhas, na ordem `is_number`,
`is_text`, `is_log`, `is_list_of`:

```python
def is_number(value: Any) -> bool:
    if isinstance(value, bool):
        return False
    return isinstance(value, (int, float))


def is_list_of(value: Any, check: Callable[[Any], bool]) -> bool:
    if not isinstance(value, list):
        return False
    for item in value:
        if not check(item):
            return False
    return True
```

- `is_number` recusa `True` e `False` antes de perguntar por `int`, porque `bool` é filho de
  `int` ([A armadilha do bool](../02-conceitos/03-any-uniao-e-isinstance.md#a-armadilha-do-bool)).
  Recusar `bool` é escolha do tutorial;
- `is_list_of(value, check)` responde se `value` é uma lista em que **todos** os itens passam na
  conferência `check`. `check` é uma **função** recebida como parâmetro: no Python, uma função é
  um valor como outro qualquer, e `is_list_of(data, is_number)` passa a função `is_number` (sem
  parênteses, sem chamá-la). Dentro do laço, `check(item)` a chama;
- `Callable[[Any], bool]` é o type hint de "uma função que recebe um argumento de qualquer tipo
  e devolve `bool`". Vem de `typing`. Entre os primeiros colchetes ficam os tipos dos argumentos;
  depois, o tipo do retorno.

Uma lista vazia passa em `is_list_of`: o laço não roda nenhuma vez e a função chega ao
`return True`. Guardar uma lista vazia não guarda nada, e não há erro nisso.

## A classe

```python
class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        return is_number(data) or is_list_of(data, is_number)

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise TypeError("Improper numeric data")
        items = data if isinstance(data, list) else [data]
        for item in items:
            self._store(str(item))
```

### validate

Um dado serve se é um número **ou** uma lista só de números. A assinatura é a da mãe,
`(self, data: Any) -> bool`, como o enunciado pede.

### ingest

A assinatura troca o `Any` da mãe por `int | float | list[int | float]`: o enunciado pede que a
assinatura de cada filha mostre os tipos que ela aceita. O mypy aceita essa troca porque o
parâmetro da mãe é `Any`, que combina com qualquer tipo.

O corpo tem três passos:

1. **Confere antes de tudo.** `self.validate(data)` chama o `validate` desta mesma classe. Se o
   dado não serve, `raise TypeError("Improper numeric data")` interrompe o método. A mensagem é a
   do exemplo do enunciado, e `TypeError` é o tipo que o Python usa para "valor do tipo errado".
   O tipo da exceção é escolha do tutorial; o enunciado só pede que uma exceção seja lançada.
2. **Transforma o dado numa lista.** `data if isinstance(data, list) else [data]` é uma
   **expressão condicional**: vale `data` se `data` já é uma lista, e `[data]` (uma lista com um
   item só) se não é. Assim o passo seguinte trata os dois casos do mesmo jeito.
3. **Guarda cada item como texto.** `str(item)` converte o número: `str(3.14)` dá `"3.14"`,
   `str(-1)` dá `"-1"`. O `_store` da mãe põe o texto na fila com o rank.

## Por que validar a lista inteira antes de guardar

O enunciado pede que o tratamento de exceções proteja os dados contra **corrupção**: um dado
ruim não pode deixar o processador num estado pela metade. Com `[1, "x", 3]`, guardar item por
item e só reclamar ao chegar no `"x"` deixaria o `1` guardado e o `3` perdido. Como `validate`
confere a lista inteira antes do primeiro `_store`, ou todos os itens entram, ou nenhum entra, e
a fila e o rank continuam exatamente como estavam.
