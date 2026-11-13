---
sidebar_position: 7
title: O arquivo completo
---

# O arquivo completo

O código do exercício 1 vem inteiro até `DataStream`, com `Protocol` no `import`, a classe
`ExportPlugin` antes de `DataStream` e o método `output_pipeline` dentro dela. Depois vêm os
plugins e o cenário novo.

```python title="data_pipeline.py"
from abc import ABC, abstractmethod
from typing import Any, Callable, Protocol


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


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...


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

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for processor in self._processors:
            data: list[tuple[int, str]] = []
            while len(data) < nb and processor.remaining() > 0:
                data.append(processor.output())
            if data:
                plugin.process_output(data)

    def _find_processor(self, element: Any) -> DataProcessor | None:
        for processor in self._processors:
            if processor.validate(element):
                return processor
        return None


def csv_field(value: str) -> str:
    for special in (",", '"', "\n", "\r"):
        if special in value:
            return '"' + value.replace('"', '""') + '"'
    return value


class CSVExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        fields = []
        for _, value in data:
            fields.append(csv_field(value))
        print("CSV Output:")
        print(",".join(fields))


def json_string(value: str) -> str:
    result = ""
    for char in value:
        if char == '"' or char == "\\":
            result += "\\" + char
        elif ord(char) < 32:
            result += f"\\u{ord(char):04x}"
        else:
            result += char
    return '"' + result + '"'


class JSONExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        pairs = []
        for rank, value in data:
            pairs.append(f"{json_string(f'item_{rank}')}: "
                         f"{json_string(value)}")
        print("JSON Output:")
        print("{" + ", ".join(pairs) + "}")


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


def second_batch() -> list[Any]:
    return [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [
            {"log_level": "ERROR", "log_message": "500 server crash"},
            {"log_level": "NOTICE",
             "log_message": "Certificate expires in 10 days"},
        ],
        [32, 42, 64, 84, 128, 168],
        "World hello",
    ]


def show_stats(stream: DataStream) -> None:
    print()
    stream.print_processors_stats()


def main() -> None:
    print("=== Code Nexus - Data Pipeline ===")
    print("\nInitialize Data Stream...")
    stream = DataStream()
    show_stats(stream)

    print("\nRegistering Processors")
    stream.register_processor(NumericProcessor())
    stream.register_processor(TextProcessor())
    stream.register_processor(LogProcessor())

    batch = first_batch()
    print(f"\nSend first batch of data on stream: {batch}")
    stream.process_stream(batch)
    show_stats(stream)

    print("\nSend 3 processed data from each processor to a CSV plugin:")
    stream.output_pipeline(3, CSVExportPlugin())
    show_stats(stream)

    batch = second_batch()
    print(f"\nSend another batch of data: {batch}")
    stream.process_stream(batch)
    show_stats(stream)

    print("\nSend 5 processed data from each processor to a JSON plugin:")
    stream.output_pipeline(5, JSONExportPlugin())
    show_stats(stream)


if __name__ == "__main__":
    main()
```

O que o arquivo usa, todos autorizados: `abc` (`ABC` e `abstractmethod`), `typing` (`Any`,
`Callable` e `Protocol`), as funções embutidas `isinstance`, `len`, `str`, `ord`, `range` e
`print`, e os métodos de lista (`append`, `pop`), de dicionário (`items`) e de texto (`replace`,
`join`). Nenhum `import` de CSV ou JSON.
