---
sidebar_position: 3
title: As perguntas do enunciado
---

# As perguntas do enunciado

O enunciado deixa uma pergunta em duas partes no exercício 1: "Como o polimorfismo permite que o
`DataStream` trate diferentes tipos de dados no fluxo sem conhecer as suas implementações
específicas? Quais são os benefícios dessa abordagem de design?". As duas partes são respondidas
abaixo. O enunciado também avisa que, na avaliação, pode ser pedido que você explique o
polimorfismo, mostre a sobrescrita de métodos, acrescente um tipo de dado novo ao
sistema ou mude o jeito de processar um dado. Também pede que você saiba explicar como a herança
reaproveita código e, ao mesmo tempo, deixa cada classe especializar o comportamento.

## Como o polimorfismo deixa o DataStream tratar tipos diferentes sem conhecê-los?

`DataStream` guarda uma `list[DataProcessor]` e só chama os métodos que a classe abstrata
garante: `validate`, `ingest`, `total`, `remaining` e `output`. Em `processor.validate(element)`,
o Python roda o `validate` da classe do objeto guardado ali, seja ela `NumericProcessor`,
`TextProcessor` ou `LogProcessor`. O fluxo pergunta "você aceita?" e "guarde", e cada processador
responde do seu jeito ([Registrar e rotear](../04-ex1/03-registrar-e-rotear.md)).

## Quais são os benefícios desse desenho?

- **Extensão sem alteração:** um tipo de dado novo é uma classe nova; `DataStream` não muda
  (exemplo abaixo);
- **Cada regra num lugar só:** o que é um número válido está só no `NumericProcessor`; a fila e o
  rank estão só no `DataProcessor`;
- **Erros cedo:** a classe abstrata impede criar um processador que esqueceu um método
  (`TypeError` ao instanciar), e o mypy confere assinaturas e plugins antes de rodar;
- **Testes separados:** cada processador é testado sozinho, como no exercício 0, e o fluxo é
  testado com qualquer processador.

## Mostrar a sobrescrita

`NumericProcessor.validate` sobrescreve o `validate` abstrato de `DataProcessor`: mesmo nome,
mesma assinatura, corpo próprio. `ingest` também é sobrescrito, com uma assinatura mais
específica em cada filha. `output` **não** é sobrescrito: as três filhas usam o da mãe. O atributo
`name` também é sobrescrito em cada filha
([Nome e contadores](../04-ex1/02-nome-e-contadores.md)).

## Acrescentar um tipo de dado novo

Nenhum processador aceita `True` e `False`
([A armadilha do bool](../02-conceitos/03-any-uniao-e-isinstance.md#a-armadilha-do-bool)). Um
processador novo resolve isso sem tocar em `DataStream` nem nos plugins. Crie
`experimentos/bool_processor.py`:

```python title="experimentos/bool_processor.py"
import sys
from typing import Any

sys.path.insert(0, "ex2")
from data_pipeline import (  # noqa: E402
    CSVExportPlugin,
    DataProcessor,
    DataStream,
    NumericProcessor,
)


class BoolProcessor(DataProcessor):
    name = "Bool Processor"

    def validate(self, data: Any) -> bool:
        return isinstance(data, bool)

    def ingest(self, data: bool) -> None:
        if not self.validate(data):
            raise TypeError("Improper bool data")
        self._store("yes" if data else "no")


stream = DataStream()
stream.register_processor(NumericProcessor())
stream.register_processor(BoolProcessor())
stream.process_stream([True, 7, False, "?"])
stream.print_processors_stats()
stream.output_pipeline(5, CSVExportPlugin())
```

O `import` em várias linhas, entre parênteses, traz quatro nomes do `data_pipeline`; o
`sys.path.insert` e o `# noqa: E402` são os mesmos do
[plugin errado](../05-ex2/08-rodar-e-conferir.md#plugin-errado).

```bash
python3 -B experimentos/bool_processor.py
```

```text
DataStream error - Can't process element in stream: ?
== DataStream statistics ==
Numeric Processor: total 1 items processed, remaining 1 on processor
Bool Processor: total 2 items processed, remaining 2 on processor
CSV Output:
7
CSV Output:
yes,no
```

`BoolProcessor` herdou a fila, o rank, o `output`, o `total` e o `remaining` sem escrever nada
disso; escreveu só o que é dele: o nome, a conferência e a conversão para texto. O fluxo e o
plugin CSV trataram os valores novos sem nenhuma mudança.

## Mudar o jeito de processar

Uma mudança de comportamento de um tipo de dado fica dentro da classe dele. Para guardar os logs
como `[ERROR] Unauthorized access!!` em vez de `ERROR: Unauthorized access!!`, só a linha do
`_store` do `LogProcessor` muda:

```python
            self._store(f"[{item['log_level']}] {item['log_message']}")
```

O fluxo, os plugins e os outros processadores continuam iguais. A saída do programa muda nas
linhas de log, e por isso o `diff` com o enunciado passa a mostrar diferenças: a mudança é só
para a demonstração na avaliação.

## Como a herança reaproveita código e deixa cada classe se especializar?

A mãe, `DataProcessor`, escreve uma vez o que é igual para todos os processadores: a fila, o rank,
`output`, `total`, `remaining` e `_store`. As filhas herdam tudo isso e escrevem só o que muda de
um tipo de dado para outro: `validate`, `ingest` e `name`. Os métodos abstratos são o contrato:
garantem que toda filha escreve a sua parte, e é esse contrato que permite ao `DataStream` usar
qualquer filha sem conhecê-la.
