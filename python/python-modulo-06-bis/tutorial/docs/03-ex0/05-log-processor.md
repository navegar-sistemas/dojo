---
sidebar_position: 5
title: Log Processor
---

# Log Processor

Um **log** é um registro de algo que aconteceu num sistema, com um nível de importância e uma
mensagem. No projeto, cada log é um dicionário com duas chaves:

```python
{"log_level": "ERROR", "log_message": "Unauthorized access!!"}
```

- `log_level`: o nível, como `NOTICE` (aviso comum), `WARNING` (alerta), `INFO` (informação) ou
  `ERROR` (erro);
- `log_message`: a mensagem.

O `LogProcessor` aceita um log ou uma lista de logs e guarda cada um como o texto
`"NÍVEL: mensagem"`, como na saída do enunciado: `ERROR: Unauthorized access!!`.

## A conferência

A função entra depois de `is_text` e antes de `is_list_of`:

```python
def is_log(value: Any) -> bool:
    if not isinstance(value, dict):
        return False
    if "log_level" not in value or "log_message" not in value:
        return False
    for key, text in value.items():
        if not isinstance(key, str) or not isinstance(text, str):
            return False
    return True
```

Um valor é um log quando:

1. é um dicionário;
2. tem as chaves `log_level` e `log_message`. `"log_level" not in value` pergunta se a chave
   **não** está no dicionário;
3. todas as chaves e todos os valores são `str`. `value.items()` dá os pares `(chave, valor)` do
   dicionário, e o `for` os separa em `key` e `text`.

O enunciado diz só "um `dict` de pares chave-valor do tipo `str`". Exigir as duas chaves é
escolha do tutorial: sem elas não há como montar o texto `"NÍVEL: mensagem"`, e o `ingest`
quebraria com `KeyError` no meio do caminho. Chaves a mais são aceitas e ignoradas.

## A classe

A classe entra depois de `TextProcessor`:

```python
class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        return is_log(data) or is_list_of(data, is_log)

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise TypeError("Improper log data")
        items = data if isinstance(data, list) else [data]
        for item in items:
            self._store(f"{item['log_level']}: {item['log_message']}")
```

- `dict[str, str]` é o type hint de um dicionário com chaves `str` e valores `str`; a assinatura
  aceita um deles ou uma lista deles;
- `item['log_level']` lê o valor da chave `log_level`. Dentro de uma f-string com aspas duplas,
  as chaves do dicionário vão entre aspas simples;
- a linha do `def ingest` tem 74 caracteres, dentro do limite de 79 do flake8.
