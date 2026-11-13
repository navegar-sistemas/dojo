---
sidebar_position: 5
title: O plugin JSON
---

# O plugin JSON

**JSON** (*JavaScript Object Notation*) é um formato de texto para dados estruturados, usado
por quase todo programa que troca dados pela internet. Um **objeto JSON** é parecido com um
dicionário do Python: pares `"chave": valor` entre chaves, separados por vírgula. Na saída do enunciado, cada bloco é um
objeto com uma chave por item, formada pelo rank:

```text
JSON Output:
{"item_2": "ERROR: 500 server crash", "item_3": "NOTICE: Certificate expires in 10 days"}
```

O `item_2` é o log de rank 2: o terceiro log que o processador recebeu.

## Os textos no JSON

Todo caractere tem um número, o seu **código**: `A` é 65, a quebra de linha é 10. Os códigos de
0 a 31 são os **caracteres de controle**, que não aparecem como letra: a quebra de linha, a
tabulação e outros. No JSON, os códigos são escritos em **hexadecimal** (base 16): os dígitos vão
de `0` a `9` e continuam com `a` (10) até `f` (15), e 10 se escreve `a`, 16 se escreve `10`.

No JSON, todo texto vai entre **aspas duplas**, e três tipos de caractere não podem aparecer
dentro dele como estão:

| Caractere | Escrito no JSON como |
|---|---|
| aspas duplas `"` | `\"` |
| barra invertida `\` | `\\` |
| caracteres de controle (códigos 0 a 31) | `\u` seguido do código em hexadecimal com quatro dígitos: a quebra de linha (código 10) vira `\u000a` |

Imprimir um `str` do Python dentro de chaves não basta: um texto com aspas ou com quebra de linha
geraria um JSON inválido. O enunciado pede "strings JSON válidas", sem `import json`; a função
abaixo faz o escape à mão.

```python
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
```

- o `for` percorre o texto caractere por caractere;
- `"\\"` no código Python é **uma** barra invertida: dentro de aspas, a barra começa um código
  especial (como o `\n`), e `\\` é o código da própria barra. Assim, `"\\" + char` é a barra
  seguida do caractere;
- `ord(char)` dá o código do caractere (`ord("A")` é 65, `ord("\n")` é 10);
- `{ord(char):04x}` escreve esse número em hexadecimal (`x`), com quatro dígitos e zeros à
  esquerda (`04`): 10 vira `000a`;
- no fim, o texto montado vai entre aspas duplas.

## O plugin

`json_string` e a classe entram no arquivo depois de `CSVExportPlugin`.

```python
class JSONExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        pairs = []
        for rank, value in data:
            pairs.append(f"{json_string(f'item_{rank}')}: "
                         f"{json_string(value)}")
        print("JSON Output:")
        print("{" + ", ".join(pairs) + "}")
```

- cada par é a chave `"item_<rank>"` e o valor, os dois passados por `json_string`, separados por
  `: `. A chave nunca tem caractere especial, mas passa pela mesma função para sair entre aspas;
- `", ".join(pairs)` junta os pares com vírgula e espaço, o separador da saída do enunciado;
- `"{" + ... + "}"` põe as chaves em volta. Elas são somadas fora da f-string porque, numa
  f-string, `{` e `}` marcam o lugar de um valor.

Como o CSV, o plugin não herda de nada: tem o `process_output` certo.
