---
sidebar_position: 6
title: O arquivo completo
---

# O arquivo completo

As quatro classes e as funções de conferência do exercício 0 vêm inteiras, com o `name`, o
`total` e o `remaining` acrescentados ([Nome e contadores](./02-nome-e-contadores.md)); depois
vêm `DataStream` e o cenário. As funções de teste do exercício 0 saíram.

```python title="data_stream.py"
from abc import ABC, abstractmethod
from typing import Any, Callable


class DataProcessor(ABC):
    name = "Data Processor"

    def __init__(self) -> None:
        self._items: list[tuple[int, str]] = []
        self._rank = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        return self._items.pop(0)

    def total(self) -> int:
        return self._rank

    def remaining(self) -> int:
        return len(self._items)

    def _store(self, value: str) -> None:
        self._items.append((self._rank, value))
        self._rank += 1


def is_number(value: Any) -> bool:
    if isinstance(value, bool):
        return False
    return isinstance(value, (int, float))


def is_text(value: Any) -> bool:
    return isinstance(value, str)


def is_log(value: Any) -> bool:
    if not isinstance(value, dict):
        return False
    if "log_level" not in value or "log_message" not in value:
        return False
    for key, text in value.items():
        if not isinstance(key, str) or not isinstance(text, str):
            return False
    return True


def is_list_of(value: Any, check: Callable[[Any], bool]) -> bool:
    if not isinstance(value, list):
        return False
    for item in value:
        if not check(item):
            return False
    return True


class NumericProcessor(DataProcessor):
    name = "Numeric Processor"

    def validate(self, data: Any) -> bool:
        return is_number(data) or is_list_of(data, is_number)

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise TypeError("Improper numeric data")
        items = data if isinstance(data, list) else [data]
        for item in items:
            self._store(str(item))


class TextProcessor(DataProcessor):
    name = "Text Processor"

    def validate(self, data: Any) -> bool:
        return is_text(data) or is_list_of(data, is_text)

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise TypeError("Improper text data")
        items = data if isinstance(data, list) else [data]
        for item in items:
            self._store(item)


class LogProcessor(DataProcessor):
    name = "Log Processor"

    def validate(self, data: Any) -> bool:
        return is_log(data) or is_list_of(data, is_log)

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise TypeError("Improper log data")
        items = data if isinstance(data, list) else [data]
        for item in items:
            self._store(f"{item['log_level']}: {item['log_message']}")


class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for element in stream:
            processor = self._find_processor(element)
            if processor is None:
                print("DataStream error - "
                      f"Can't process element in stream: {element}")
            else:
                processor.ingest(element)

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self._processors:
            print("No processor found, no data")
        for processor in self._processors:
            print(f"{processor.name}: total {processor.total()} items "
                  f"processed, remaining {processor.remaining()} on processor")

    def _find_processor(self, element: Any) -> DataProcessor | None:
        for processor in self._processors:
            if processor.validate(element):
                return processor
        return None


def first_batch() -> list[Any]:
    return [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {"log_level": "WARNING",
             "log_message": "Telnet access! Use ssh instead"},
            {"log_level": "INFO", "log_message": "User wil is connected"},
        ],
        42,
        ["Hi", "five"],
    ]


def consume(processor: DataProcessor, count: int) -> None:
    for _ in range(count):
        processor.output()


def main() -> None:
    print("=== Code Nexus - Data Stream ===")
    print("\nInitialize Data Stream...")
    stream = DataStream()
    stream.print_processors_stats()

    print("\nRegistering Numeric Processor")
    numeric = NumericProcessor()
    stream.register_processor(numeric)
    batch = first_batch()
    print(f"\nSend first batch of data on stream: {batch}")
    stream.process_stream(batch)
    stream.print_processors_stats()

    print("\nRegistering other data processors")
    text = TextProcessor()
    log = LogProcessor()
    stream.register_processor(text)
    stream.register_processor(log)
    print("Send the same batch again")
    stream.process_stream(batch)
    stream.print_processors_stats()

    print("\nConsume some elements from the data processors: "
          "Numeric 3, Text 2, Log 1")
    consume(numeric, 3)
    consume(text, 2)
    consume(log, 1)
    stream.print_processors_stats()


if __name__ == "__main__":
    main()
```

Como no [exercício 0](../03-ex0/08-o-arquivo-completo.md), o arquivo termina com uma única quebra
de linha depois de `    main()`, que o botão de copiar não leva.

O que o arquivo usa, todos autorizados: `abc` (`ABC` e `abstractmethod`), `typing` (`Any` e
`Callable`), as funções embutidas `isinstance`, `len`, `str`, `range` e `print`, e os métodos de
lista (`append`, `pop`) e de dicionário (`items`).
