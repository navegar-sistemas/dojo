---
sidebar_position: 1
title: O problema
---

# O problema

O sistema recebe três tipos de dado: números, textos e registros de log. Cada tipo é conferido e
guardado de um jeito, mas os três precisam responder às mesmas perguntas: "este dado serve?",
"guarde este dado" e "me dê o dado mais antigo". O exercício 0 escreve essas três perguntas uma
vez, numa classe abstrata, e uma classe filha para cada tipo de dado.

## O que o enunciado pede

Um arquivo `data_processor.py`, na raiz do projeto, com:

- a classe abstrata **`DataProcessor`**, filha de `ABC`, com três métodos:

  | Método | Tipo | O que faz |
  |---|---|---|
  | `validate(self, data: Any) -> bool` | abstrato | responde se o dado pode ser guardado por este processador |
  | `ingest(self, data: Any) -> None` | abstrato | guarda o dado; se o dado não serve, lança uma exceção |
  | `output(self) -> tuple[int, str]` | comum | tira o item mais antigo e o devolve com o seu rank |

- três classes filhas, que sobrescrevem `validate` e `ingest`:

  | Classe | Aceita | Guarda |
  |---|---|---|
  | `NumericProcessor` | um `int`, um `float`, ou uma lista deles (misturados ou não) | cada número convertido em texto |
  | `TextProcessor` | um `str`, ou uma lista de `str` | cada texto |
  | `LogProcessor` | um `dict` com chaves e valores `str`, ou uma lista deles | cada log convertido em texto |

Regras sobre as assinaturas (a linha do `def`, com os tipos):

- `validate` tem a mesma assinatura nas filhas: recebe `Any`, porque quem chama pode mandar
  qualquer coisa;
- `ingest` tem, em cada filha, a **sua** assinatura, com os tipos que aquela filha aceita;
- `output` não é sobrescrito: as filhas usam o da mãe.

Um dado que é uma lista vira **vários** itens guardados, um por elemento: `[1, 2, 3]` guarda
três itens.

## O teste pedido

O próprio programa testa as classes, imprimindo cada passo:

- cria um objeto de cada filha;
- chama `validate` com dados válidos e inválidos;
- chama `ingest` com um dado inválido, **sem** validar antes, e mostra a exceção;
- guarda dados com `ingest` e os tira com `output`.

## A saída esperada

```text
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
```

As linhas de cada teste começam com um espaço. Nas linhas `Trying to validate input '42'`, o
dado testado é o número `42`; as aspas fazem parte do texto da mensagem.
