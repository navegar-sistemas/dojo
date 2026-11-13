---
sidebar_position: 4
title: Quebrar o ciclo
---

# Quebrar o ciclo

O par das trevas explode porque um `from ... import nome`, rodando enquanto o arquivo carrega,
pede um nome a um módulo que ainda está pela metade. O livro e o validador continuam precisando
um do outro; o que dá para mudar é **quando** cada um pede o que precisa, ou **onde** fica o que
os dois precisam. O enunciado pede que se escolha um jeito para a luz e que se saiba explicar os
outros.

## 1. Importar dentro da função

O import sai do topo do arquivo e vai para dentro da função que usa o nome:

```python
def validate_ingredients(ingredients: str) -> str:
    from .light_spellbook import light_spell_allowed_ingredients
    ...
```

Um import dentro de uma função só roda quando a função é **chamada**, e não quando o arquivo
carrega. Enquanto o livro e o validador carregam, o validador não importa nada, e o ciclo some.
Quando alguém finalmente valida um feitiço, os dois arquivos já terminaram de rodar, e o nome
existe. Basta mudar um dos lados: um validador que não importa nada ao carregar nunca é a metade
que trava o outro, seja qual for o arquivo importado primeiro.

É o jeito que o tutorial escolhe para a luz: muda uma linha de lugar e não depende de nenhum
detalhe do sistema de imports além do momento em que a linha roda
([O grimório da luz](./05-o-grimorio-da-luz.md)).

## 2. Importar o módulo, e não o nome

```python
from . import light_spellbook


def validate_ingredients(ingredients: str) -> str:
    for allowed in light_spellbook.light_spell_allowed_ingredients():
        ...
```

`from . import light_spellbook` pede o **módulo**, e não uma função de dentro dele. Um módulo pela
metade já existe em `sys.modules`, e o import funciona. A função só é procurada dentro do módulo
na hora da chamada, `light_spellbook.light_spell_allowed_ingredients()`, quando ele já terminou de
rodar.

Esse jeito precisa valer **nos dois arquivos**: se o livro continuar com
`from .light_validator import validate_ingredients`, quem entrar pelo validador acha o validador
pela metade quando o livro pede o nome, e a explosão volta. Um experimento com um par pequeno,
`experimentos/eclipse`, mostra os dois lados funcionando:

```bash
mkdir experimentos/eclipse
touch experimentos/eclipse/__init__.py
```

```python title="experimentos/eclipse/spellbook.py"
from . import validator


def allowed_ingredients() -> list[str]:
    return ["moon", "shadow"]


def record(spell_name: str, ingredients: str) -> str:
    return f"{spell_name}: {validator.validate_ingredients(ingredients)}"
```

```python title="experimentos/eclipse/validator.py"
from . import spellbook


def validate_ingredients(ingredients: str) -> str:
    text = ingredients.lower()
    for allowed in spellbook.allowed_ingredients():
        if allowed in text:
            return f"{ingredients} - VALID"
    return f"{ingredients} - INVALID"
```

```python title="experimentos/eclipse_teste.py"
from eclipse.spellbook import record

print(record("Eclipse", "Moon dust"))
```

O script entra pelo livro; o comando `-c`, rodado de dentro de `experimentos` (onde o pacote
`eclipse` está), entra pelo validador:

```bash
python3 experimentos/eclipse_teste.py
cd experimentos && python3 -c "from eclipse.validator import validate_ingredients; print(validate_ingredients('Shadow'))"
cd ..
```

```text
Eclipse: Moon dust - VALID
Shadow - VALID
```

As duas portas de entrada funcionam, e as ferramentas aceitam o par:

```bash
.venv/bin/flake8 experimentos
.venv/bin/mypy --disallow-untyped-defs experimentos
```

```text
Success: no issues found in 8 source files
```

## 3. Tirar o que os dois precisam para um terceiro módulo

O ciclo existe porque a lista de ingredientes mora no livro, e o livro usa o validador. Com a
lista num terceiro arquivo, por exemplo `ingredients.py`, o livro e o validador importariam a
lista de lá, e o validador deixaria de importar o livro: as setas passam a ir numa direção só, e
não há ciclo para quebrar. É a solução mais limpa num projeto livre. Aqui ela não serve: o
enunciado fixa os arquivos da árvore e pede que `light_spell_allowed_ingredients()` fique no
livro.

## 4. Receber o dado como parâmetro

Se o validador recebesse a lista como argumento, `validate_ingredients(ingredients, allowed)`,
ele não precisaria importar nada, e quem chama (o livro) passaria a lista. É a **injeção de
dependência**: quem usa entrega o que a função precisa. Também não serve aqui: o enunciado fixa a
assinatura `validate_ingredients(ingredients: str)`, com um parâmetro só.

## 5. Mudar a ordem das linhas

No livro, escrever o `def` de `dark_spell_allowed_ingredients` **antes** do import do validador
faria o nome existir quando o validador o pedisse. Funciona, mas só por uma porta: entrando pelo
validador, o livro é que pediria um nome ainda inexistente, e a explosão volta. Além disso, o
flake8 acusa o import fora do topo (`E402 module level import not at top of file`). É o jeito
mais frágil dos cinco.

## Os cinco lado a lado

| Jeito | O que muda | Neste projeto |
|---|---|---|
| import dentro da função | o momento do import: da carga do arquivo para a chamada da função | usado na luz |
| importar o módulo | o que é pedido no import: o módulo, que já existe pela metade | funciona nos dois arquivos; mostrado no experimento |
| terceiro módulo | onde fica o que os dois usam | não cabe na árvore fixa do enunciado |
| parâmetro | quem fornece o dado | não cabe na assinatura fixa do enunciado |
| ordem das linhas | o que já existe quando o outro pede | funciona por uma porta só e gera aviso do flake8 |
