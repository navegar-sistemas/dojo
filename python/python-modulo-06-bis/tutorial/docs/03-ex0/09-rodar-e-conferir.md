---
sidebar_position: 9
title: Rodar e conferir
---

# Rodar e conferir

## Comparar com o enunciado

```bash
diff <(python3 data_processor.py) - <<'FIM'
=== Code Nexus - Data Processor ===

Testing Numeric Processor...
 Trying to validate input '42': True
 Trying to validate input 'Hello': False
 Test invalid ingestion of string 'foo' without prior validation:
 Got exception: Improper numeric data
 Processing data: [1, 2, 3, 4, 5]
 Extracting 3 values...
 Numeric value 0: 1
 Numeric value 1: 2
 Numeric value 2: 3

Testing Text Processor...
 Trying to validate input '42': False
 Processing data: ['Hello', 'Nexus', 'World']
 Extracting 1 value...
 Text value 0: Hello

Testing Log Processor...
 Trying to validate input 'Hello': False
 Processing data: [{'log_level': 'NOTICE', 'log_message': 'Connection to server'}, {'log_level': 'ERROR', 'log_message': 'Unauthorized access!!'}]
 Extracting 2 values...
 Log entry 0: NOTICE: Connection to server
 Log entry 1: ERROR: Unauthorized access!!
FIM
```

- `<(python3 data_processor.py)` entrega ao `diff` a saída do programa como se fosse um
  arquivo;
- o `-` diz ao `diff` para ler o segundo texto da entrada do comando, em vez de um arquivo;
- `<<'FIM'` escreve nessa entrada as linhas seguintes, até a linha `FIM`: a saída copiada do
  enunciado. Cole o bloco inteiro, até a linha `FIM`; sem ela, o terminal fica esperando mais
  linhas;
- o `diff` compara os dois textos linha a linha e só imprime as diferenças.

Sem nenhuma linha impressa, a saída é a esperada, inclusive o espaço no começo das linhas dos
testes.

## Conferir estilo e tipos

```bash
.venv/bin/flake8 data_processor.py
.venv/bin/mypy --disallow-untyped-defs data_processor.py
```

```text
data_processor.py:111: error: Argument 1 to "ingest" of "NumericProcessor" has incompatible type "str"; expected "int | float | list[int | float]"  [arg-type]
Found 1 error in 1 file (checked 1 source file)
```

O flake8 não imprime nada. O mypy acusa só a chamada proposital da linha 111
([O erro proposital do mypy](./07-o-erro-proposital-do-mypy.md)); qualquer outra linha na saída
dele é um problema a corrigir.

## A classe abstrata não é instanciada

Um teste rápido no terminal, com `python3 -c`, que roda o código passado entre aspas. Com
`-c`, o Python procura os módulos importados também na pasta atual, e por isso
`from data_processor import ...` acha o arquivo `data_processor.py`. O `-B` impede que o Python
grave na pasta do projeto a pasta de cache `__pycache__`, que ele cria ao importar um arquivo:

```bash
python3 -B -c 'from data_processor import DataProcessor; DataProcessor()'
```

A última linha da saída é:

```text
TypeError: Can't instantiate abstract class DataProcessor without an implementation for abstract methods 'ingest', 'validate'
```

No Python 3.10 e no 3.11, a mensagem é
`Can't instantiate abstract class DataProcessor with abstract methods ingest, validate`.

## Um dado inválido não entra pela metade

```bash
python3 -B -c 'from data_processor import NumericProcessor
p = NumericProcessor()
try:
    p.ingest([1, "x", 3])
except TypeError as error:
    print(error)
p.ingest([7])
print(p.output())'
```

```text
Improper numeric data
(0, '7')
```

A lista com o `"x"` foi recusada inteira: o `1` não foi guardado, e o rank não andou. O `7`,
guardado depois, recebeu o rank 0.
