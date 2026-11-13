---
sidebar_position: 6
title: A demonstração
---

# A demonstração

A segunda metade do arquivo testa as três classes e imprime a saída do enunciado: uma função de
teste por processador e duas funções auxiliares para as linhas que se repetem.

## As funções auxiliares

```python
def try_validate(processor: DataProcessor, data: Any) -> None:
    print(f" Trying to validate input '{data}': {processor.validate(data)}")


def extract(processor: DataProcessor, count: int, label: str) -> None:
    word = "value" if count == 1 else "values"
    print(f" Extracting {count} {word}...")
    for _ in range(count):
        rank, value = processor.output()
        print(f" {label} {rank}: {value}")
```

- as duas recebem um `DataProcessor` qualquer: funcionam com as três filhas sem saber qual é.
  Esse é o polimorfismo da [parte de conceitos](../02-conceitos/04-polimorfismo.md):
  `processor.validate(data)` roda o `validate` da classe do objeto recebido;
- `try_validate` imprime o dado entre aspas e o `True` ou `False` devolvido;
- `extract` tira `count` itens com `output` e imprime cada um com o rótulo recebido
  (`Numeric value`, `Text value` ou `Log entry`). `rank, value = processor.output()` separa a
  tupla devolvida nas duas variáveis;
- `word` escolhe o singular quando `count` é 1, como no enunciado: `Extracting 1 value...` e
  `Extracting 3 values...`.

Todas as linhas dos testes começam com um espaço, dentro do próprio texto do `print`.

## O teste do Numeric Processor

```python
def test_numeric() -> None:
    print("Testing Numeric Processor...")
    processor = NumericProcessor()
    try_validate(processor, 42)
    try_validate(processor, "Hello")
    print(" Test invalid ingestion of string 'foo' without prior validation:")
    try:
        processor.ingest("foo")
    except TypeError as error:
        print(f" Got exception: {error}")
    data: list[int | float] = [1, 2, 3, 4, 5]
    print(f" Processing data: {data}")
    processor.ingest(data)
    extract(processor, 3, "Numeric value")
```

- `processor.ingest("foo")` é a chamada inválida sem validação: o `ingest` lança `TypeError`, o
  `except` captura, e `{error}` imprime a mensagem `Improper numeric data`. É a linha do
  [erro proposital do mypy](./07-o-erro-proposital-do-mypy.md);
- `data` é anotada como `list[int | float]`. Sem a anotação, o mypy deduziria `list[int]` e
  recusaria a chamada `processor.ingest(data)`
  ([A lista de int não é uma lista de int | float](../02-conceitos/03-any-uniao-e-isinstance.md#lista-invariante));
- `print(f" Processing data: {data}")` imprime a lista como o Python a escreve:
  `[1, 2, 3, 4, 5]`;
- o processador guarda cinco itens e o teste tira três. Os dois que sobram não são usados.

## Os testes de texto e de log

```python
def test_text() -> None:
    print("Testing Text Processor...")
    processor = TextProcessor()
    try_validate(processor, 42)
    data = ["Hello", "Nexus", "World"]
    print(f" Processing data: {data}")
    processor.ingest(data)
    extract(processor, 1, "Text value")


def test_log() -> None:
    print("Testing Log Processor...")
    processor = LogProcessor()
    try_validate(processor, "Hello")
    data = [
        {"log_level": "NOTICE", "log_message": "Connection to server"},
        {"log_level": "ERROR", "log_message": "Unauthorized access!!"},
    ]
    print(f" Processing data: {data}")
    processor.ingest(data)
    extract(processor, 2, "Log entry")
```

Aqui as listas não precisam de anotação: o mypy deduz `list[str]` e `list[dict[str, str]]`, que
são exatamente os tipos que os `ingest` pedem. A lista de logs ocupa várias linhas: dentro de
colchetes, o Python aceita quebrar a linha, e a vírgula depois do último item é permitida.

O enunciado manda testar o `validate` com dados válidos e inválidos em **cada** classe, mas a
saída do exemplo só mostra um `validate` com dado válido no Numeric Processor: nos testes de texto
e de log aparece só o dado inválido. A demonstração imprime exatamente as linhas do exemplo, e
essa é uma escolha do tutorial. O dado válido de texto e o de log passam pelo `validate` dentro do
`ingest`, que confere antes de guardar: se o `validate` recusasse `['Hello', 'Nexus', 'World']`
ou a lista de logs, o `ingest` lançaria `TypeError` fora de qualquer `try`, e o programa pararia
com um traceback. Para mostrar o `True` na tela, basta uma linha `try_validate(processor, data)`
antes do `ingest`, mas aí a saída deixa de ser igual à do exemplo.

## O main

```python
def main() -> None:
    print("=== Code Nexus - Data Processor ===")
    print()
    test_numeric()
    print()
    test_text()
    print()
    test_log()


if __name__ == "__main__":
    main()
```

`print()` sem argumento imprime uma linha vazia, a que separa os blocos na saída.
`if __name__ == "__main__":` roda o `main` só quando o arquivo é executado com `python3`, e não
quando outro arquivo o importa: `__name__` é uma variável que o Python preenche com `"__main__"`
no arquivo que foi rodado.
