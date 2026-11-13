---
sidebar_position: 4
title: Text Processor
---

# Text Processor

O `TextProcessor` aceita um texto ou uma lista de textos e guarda cada texto como está. É o mesmo
desenho do [Numeric Processor](./03-numeric-processor.md), com outra conferência.

A função de conferência entra logo depois de `is_number`:

```python
def is_text(value: Any) -> bool:
    return isinstance(value, str)
```

A classe entra depois de `NumericProcessor`:

```python
class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        return is_text(data) or is_list_of(data, is_text)

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise TypeError("Improper text data")
        items = data if isinstance(data, list) else [data]
        for item in items:
            self._store(item)
```

- `validate`: um texto, ou uma lista só de textos. `is_list_of` é a mesma função do Numeric
  Processor, agora recebendo `is_text`;
- `ingest`: a assinatura diz `str | list[str]`. Cada item já é um `str`, e vai para a fila sem
  conversão. A mensagem `Improper text data` segue o modelo da mensagem do enunciado para
  números.

O número `42` não passa: `isinstance(42, str)` é `False`. O texto `"42"` passa: é um `str`, mesmo
que tenha cara de número.
