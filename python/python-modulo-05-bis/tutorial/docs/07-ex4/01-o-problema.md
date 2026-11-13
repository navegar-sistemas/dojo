---
sidebar_position: 1
title: O problema
---

# O problema

Dois módulos que precisam um do outro são comuns: um livro de feitiços que pede a um validador para
decidir se um feitiço entra, e um validador que pede ao livro a lista do que é permitido. Escrita
de um jeito, essa dependência mútua funciona; escrita de outro, derruba o programa no `import`,
antes de qualquer feitiço. O exercício 4 escreve a mesma funcionalidade duas vezes, uma que
sobrevive e uma que explode, e a diferença entre as duas é uma decisão de projeto: **quando** cada
módulo busca o outro.

## O que o enunciado pede

Um subpacote `alchemy/grimoire` (grimório, o livro de feitiços) e dois programas. Os `import`
permitidos continuam sendo só os dos módulos do projeto.

### O grimório da luz, que sobrevive

| Arquivo | Conteúdo |
|---|---|
| `light_spellbook.py` | `light_spell_allowed_ingredients()`, que devolve a lista dos ingredientes da magia da luz: `"earth"`, `"air"`, `"fire"`, `"water"`; e `light_spell_record(spell_name: str, ingredients: str)`, que devolve um texto dizendo se o feitiço foi registrado ou rejeitado, com a decisão vinda do validador |
| `light_validator.py` | `validate_ingredients(ingredients: str)`, que devolve um texto com os ingredientes e a palavra `VALID` ou `INVALID`. Os ingredientes são válidos se incluem pelo menos um dos permitidos pelo livro, sem diferenciar maiúsculas de minúsculas |

O livro precisa do validador para decidir, e o validador precisa do livro para saber o que é
permitido. Há vários jeitos de impedir a explosão: o tutorial usa um, e os outros estão nas
[Perguntas de revisão](../08-fechamento/03-perguntas-de-revisao.md#as-alternativas).

### O grimório das trevas, que não sobrevive

`dark_spellbook.py` e `dark_validator.py`, as versões sombrias: funções com o prefixo `dark_` e os
ingredientes `"bats"`, `"frogs"`, `"arsenic"`, `"eyeball"` (morcegos, sapos, arsênico, globo
ocular). Desta vez, a dependência mútua é escrita do jeito ingênuo, com os imports **no topo** dos
dois arquivos, e fica quebrada: o par existe para mostrar a falha, e precisa falhar de verdade.

O enunciado avisa: não basta copiar os arquivos da luz e trocar os nomes. O par das trevas tem de
ser escrito de propósito, de modo que o ciclo de imports seja **a** diferença escolhida. O
contraste é o exercício inteiro.

O prefixo `dark_` vale para as funções que têm o prefixo `light_` na versão da luz. A função do
validador, que na luz se chama `validate_ingredients`, sem prefixo, continua `validate_ingredients`
no validador das trevas, como mostra o traceback do enunciado
(`from .dark_validator import validate_ingredients`).

### Os programas

| Programa | O que faz |
|---|---|
| `ft_kaboom_0.py` | acessa o pacote `grimoire` e registra um feitiço da luz, sem falhas |
| `ft_kaboom_1.py` | chega direto ao `dark_spellbook.py` e tenta registrar um feitiço das trevas; isso precisa falhar com uma exceção, "o laboratório explodiu". Capturar a exceção é livre |

## A saída esperada

```text
=== Kaboom 0 ===
Using grimoire module directly
Testing record light spell: Spell recorded: Fantasy (Earth, wind and fire - VALID)
```

```text
=== Kaboom 1 ===
Access to alchemy/grimoire/dark_spellbook.py directly
Test import now - THIS WILL RAISE AN UNCAUGHT EXCEPTION
Traceback (most recent call last):
  File "/tmp/Python/module-05-bis/ft_kaboom_1.py", line 7, in <module>
    from alchemy.grimoire.dark_spellbook import dark_spell_record
  File "/tmp/Python/module-05-bis/alchemy/grimoire/dark_spellbook.py", line 2, in <module>
    from .dark_validator import validate_ingredients
  File "/tmp/Python/module-05-bis/alchemy/grimoire/dark_validator.py", line 2, in <module>
    from .dark_spellbook import dark_spell_allowed_ingredients
ImportError: cannot import name 'dark_spell_allowed_ingredients' from partially initialized module 'alchemy.grimoire.dark_spellbook' (most likely due to a circular import) (/tmp/Python/module-05-bis/alchemy/grimoire/dark_spellbook.py)
```

- do primeiro, sai o formato do registro: `Spell recorded: <nome> (<ingredientes> - VALID)`. O
  feitiço `Fantasy`, com os ingredientes `Earth, wind and fire`, é válido porque tem `earth` e
  `fire` (`wind`, vento, não é ingrediente permitido, mas basta um);
- o segundo é o mesmo traceback do [import circular](../04-conceitos/05-o-import-circular.md):
  `dark_spellbook` importa `dark_validator`, que importa `dark_spellbook` de volta, ainda pela
  metade. O caminho e os números de linha são os do arquivo de quem escreveu o enunciado; a última
  linha está inteira numa linha só, quebrada no enunciado pela largura da página.

A saída de um feitiço rejeitado não aparece no enunciado; o formato dela é escolha do tutorial
([O grimório da luz](./02-o-grimorio-da-luz.md)).
