---
sidebar_position: 8
title: O arquivo completo
---

# O arquivo completo

```python title="ex0/data_processor.py"
from abc import ABC, abstractmethod
from typing import Any, Callable


class DataProcessor(ABC):
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
    def validate(self, data: Any) -> bool:
        return is_number(data) or is_list_of(data, is_number)

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise TypeError("Improper numeric data")
        items = data if isinstance(data, list) else [data]
        for item in items:
            self._store(str(item))


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        return is_text(data) or is_list_of(data, is_text)

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise TypeError("Improper text data")
        items = data if isinstance(data, list) else [data]
        for item in items:
            self._store(item)


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        return is_log(data) or is_list_of(data, is_log)

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise TypeError("Improper log data")
        items = data if isinstance(data, list) else [data]
        for item in items:
            self._store(f"{item['log_level']}: {item['log_message']}")


def try_validate(processor: DataProcessor, data: Any) -> None:
    print(f" Trying to validate input '{data}': {processor.validate(data)}")


def extract(processor: DataProcessor, count: int, label: str) -> None:
    word = "value" if count == 1 else "values"
    print(f" Extracting {count} {word}...")
    for _ in range(count):
        rank, value = processor.output()
        print(f" {label} {rank}: {value}")


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

O arquivo termina com **uma** quebra de linha logo depois da última linha, `    main()`, e nada
depois dela. O botão de copiar, no canto do bloco, não leva essa quebra final: se, depois de
colar, o cursor ficar no fim de `    main()`, aperte Enter uma vez antes de salvar. Alguns editores
já acrescentam a quebra ao salvar; nesse caso, não aperte. Sem a quebra, o flake8 acusa
`W292 no newline at end of file` ("sem quebra de linha no fim do arquivo"); com mais de uma, acusa
`W391 blank line at end of file` ("linha em branco no fim do arquivo"). Se o editor puser espaços
de recuo na linha nova depois do Enter, apague-os: o flake8 também acusa
`W293 blank line contains whitespace` ("linha em branco com espaços").

O que o arquivo usa, todos autorizados: `abc` (`ABC` e `abstractmethod`), `typing` (`Any` e
`Callable`), as funções embutidas `isinstance`, `str`, `range` e `print`, e os métodos de lista
(`append`, `pop`) e de dicionário (`items`).
