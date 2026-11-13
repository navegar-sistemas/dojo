---
sidebar_position: 4
title: O plugin CSV
---

# O plugin CSV

**CSV** (*comma-separated values*, "valores separados por vírgula") é um formato de texto para
tabelas: cada linha é um registro, e os campos da linha são separados por vírgulas. Planilhas como
o Excel e o LibreOffice abrem arquivos CSV. Na saída do enunciado, cada bloco é uma linha com os
textos de um processador:

```text
CSV Output:
Hello world,Hi,five
```

O rank não aparece: a linha só tem os textos.

## O campo que contém uma vírgula

Se um texto contém uma vírgula, ela seria lida como separador, e o campo viraria dois. A regra do
CSV (descrita no documento RFC 4180, a referência do formato) é pôr esse campo entre aspas
duplas. E, se o próprio texto contém aspas duplas, cada uma é escrita **dobrada** dentro do
campo:

| Texto | Campo no CSV |
|---|---|
| `Hello world` | `Hello world` |
| `a,b` | `"a,b"` |
| `say "hi"` | `"say ""hi"""` |

O mesmo vale para um texto com quebra de linha (`\n` ou `\r`): sem as aspas, ele quebraria o
registro em dois. O enunciado pede "strings CSV e JSON válidas"; nenhum texto do cenário tem
esses caracteres, mas os dados de um fluxo podem ter.

```python
def csv_field(value: str) -> str:
    for special in (",", '"', "\n", "\r"):
        if special in value:
            return '"' + value.replace('"', '""') + '"'
    return value
```

- o `for` percorre os quatro caracteres especiais; `special in value` pergunta se o caractere
  aparece no texto;
- se aparece, devolve o texto entre aspas, com cada `"` trocado por `""` (`replace` troca todas
  as ocorrências);
- se nenhum aparece, devolve o texto como está.

## O plugin

`csv_field` e a classe entram no arquivo depois de `DataStream`.

```python
class CSVExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        fields = []
        for _, value in data:
            fields.append(csv_field(value))
        print("CSV Output:")
        print(",".join(fields))
```

- `CSVExportPlugin` não herda de `ExportPlugin` nem de nada: tem o `process_output` com a
  assinatura certa, e isso basta ([Protocol e duck typing](./02-protocol-e-duck-typing.md));
- `for _, value in data` separa cada tupla `(rank, texto)` e descarta o rank no `_`;
- `",".join(fields)` junta os campos numa linha só, com uma vírgula entre cada dois.

`fields` não precisa de anotação: o primeiro uso é o `append`, e o mypy deduz `list[str]`
([O tipo de uma lista que começa vazia](../02-conceitos/05-a-fila.md#o-tipo-de-uma-lista-que-começa-vazia)).
O mesmo vale para `pairs`, no [plugin JSON](./05-o-plugin-json.md).
