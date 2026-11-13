---
sidebar_position: 9
title: Linha a linha
---

# Linha a linha

Com as linhas do arquivo lidas ([página 7](./05-abrindo-o-arquivo.md)), falta separar
cada uma em chave e valor e montar o dicionário que o `MazeConfig.create` espera, como
`{"WIDTH": "20", "ENTRY": "0,0", ...}`. O arquivo é escrito por pessoas, e pessoas põem espaços,
misturam maiúsculas e minúsculas, deixam linhas em branco. Esta página mostra como a leitura
aceita o que é inofensivo e recusa o que é ambíguo.

## As regras de leitura

Cada regra resolve um problema concreto. Algumas vêm do enunciado; as outras são escolha do
projeto:

| Regra | Problema que resolve | Origem |
|---|---|---|
| uma opção por linha, no formato `CHAVE=valor` | é o formato do arquivo | enunciado |
| linha começando com `#` é pulada | comentários explicam as opções | enunciado |
| linha vazia é pulada | linhas em branco separam grupos de opções | escolha |
| espaços em volta da chave e do valor são ignorados | `WIDTH = 20` é o mesmo que `WIDTH=20` | escolha |
| chave em qualquer caixa | `width=20` é o mesmo que `WIDTH=20` | escolha |
| o valor vai até o fim da linha, a partir do **primeiro** `=` | um nome de arquivo pode ter `=` | escolha |
| linha sem `=` ou sem chave é erro, citando o número da linha | `HEIGHT 15` não diz o que é chave e o que é valor | escolha* |
| chave repetida: vale a última | a correção feita mais abaixo no arquivo vence | escolha |
| chave desconhecida é ignorada | o enunciado permite acrescentar chaves | escolha |

\* O enunciado exige que "sintaxe incorreta" vire uma mensagem clara; o formato da mensagem é
escolha.

## O caminho de uma linha

```mermaid
flowchart TD
    text["texto da linha n"]
    strip["line = texto.strip()"]
    skip{"vazia ou<br/>começa com #35;?"}
    next(["pula para a próxima linha"])
    split["key, sep, value = line.partition('=')"]
    valid{"tem '=' e a chave<br/>não é vazia?"}
    error(["ConfigError<br/>path, line n: expected KEY=VALUE"])
    store["raw[key.strip().upper()] = value.strip()"]

    text --> strip --> skip
    skip -- sim --> next
    skip -- não --> split --> valid
    valid -- não --> error
    valid -- sim --> store
```

(O `#35;` no diagrama é como o Mermaid escreve o caractere `#`.)

## O laço

```python
raw: dict[str, str] = {}
for number, text in enumerate(lines, 1):
    line = text.strip()
    if not line or line.startswith("#"):
        continue
    key, sep, value = line.partition("=")
    if not sep or not key.strip():
        raise ConfigError(f"{path}, line {number}: expected "
                          f"KEY=VALUE, got '{line}'")
    raw[key.strip().upper()] = value.strip()
```

`raw: dict[str, str] = {}` cria o dicionário vazio; a anotação diz ao `mypy` (a ferramenta que
confere os tipos do código) que as chaves e os valores são textos.

### Numerar todas as linhas

`enumerate(lines, 1)` entrega, a cada volta, o número da linha e o texto dela, contando a partir
de 1, como um editor de texto. A contagem acontece **antes** de pular comentários e linhas
vazias: a "linha 7" de uma mensagem de erro é a linha 7 que o usuário vê no editor, e não a
sétima linha com uma opção.

### `strip()` primeiro

`strip()` tira espaços, tabulações e a quebra de linha das duas pontas do texto. Depois dele:

- uma linha só com espaços fica vazia (`not line` é verdadeiro) e é pulada;
- `    # comentário com recuo` passa a começar com `#` e é pulada;
- `continue` pula direto para a próxima linha do `for`.

Comentário só existe como linha inteira. `WIDTH=20 # largura` não é cortado no `#`: o valor fica
`20 # largura`, que não é inteiro, e o erro aparece com o valor entre aspas. Cortar no `#`
quebraria um nome de arquivo legítimo como `OUTPUT_FILE=saida#1.txt`.

### Separar no primeiro `=`

`partition("=")` devolve sempre três partes: o que vem antes do primeiro `=`, o próprio `=` e o
resto. `key, sep, value = ...` guarda as três em três nomes.

```text
"OUTPUT_FILE=a=b.txt".partition("=")  → ('OUTPUT_FILE', '=', 'a=b.txt')
"HEIGHT 15".partition("=")            → ('HEIGHT 15', '', '')
"=15".partition("=")                  → ('', '=', '15')
```

- Os `=` depois do primeiro ficam no valor, então um nome de arquivo com `=` funciona.
- Sem `=`, a parte do meio (`sep`) vem vazia: é o sinal do erro de sintaxe.
- `=15` tem `=`, mas a chave é vazia: também erro.

Com `split("=")`, `a=b.txt` seria cortado em pedaços demais, e faltaria um sinal claro de "não
tinha `=`".

### Chave em maiúsculas, valor sem espaços

`key.strip().upper()` tira os espaços e passa para maiúsculas: `"width"`, `"Width"` e
`" WIDTH "` viram a mesma chave, `"WIDTH"`. `value.strip()` faz `WIDTH = 20` dar o valor `20`.

### Repetida vale a última; desconhecida é ignorada

Guardar uma chave que já está no dicionário substitui o valor anterior: `WIDTH=20` seguido de
`width=30` termina com `30`, sem código extra.

Uma chave como `COLOR=red` entra no dicionário, mas o `MazeConfig` nunca a lê. Um arquivo com
chaves a mais continua funcionando.

O preço é que um erro de digitação só é acusado numa chave obrigatória. Com `WIDHT=20`, a
`WIDTH` continua faltando, e a mensagem `missing mandatory key(s): WIDTH` aponta o problema. Já
com `SEDD=42`, a chave errada é ignorada em silêncio: a `SEED` fica de fora, e cada execução
sorteia um labirinto diferente, sem nenhum aviso.

Falta acrescentar o nome do arquivo às mensagens do `MazeConfig`; isso e o arquivo completo do
repositório estão na [próxima página](./09-o-repositorio-completo.md).
