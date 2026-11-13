---
sidebar_position: 3
title: As perguntas do enunciado
---

# As perguntas do enunciado

O enunciado deixa uma pergunta na Parte III ("Quando um alquimista deve usar caminhos absolutos e
quando deve usar caminhos relativos?") e pede, na Parte IV, que se saiba explicar os diferentes
jeitos de evitar dependências circulares. Também avisa que, na avaliação, pode ser pedido que
você explique os mecanismos de import, mostre diferentes estilos de import ou modifique o
laboratório, e que o importante é entender os quatro mistérios (inicialização de pacotes, caminhos
de import, absoluto e relativo, dependências circulares), e não só a implementação.

## Quando usar import absoluto e quando usar relativo?

O **absoluto** escreve o nome completo do módulo a partir de uma pasta do `sys.path`
(`from alchemy.potions import strength_potion`); o **relativo** parte do pacote do arquivo que
importa (`from ..potions import strength_potion`)
([Absoluto e relativo](../05-parte-3/02-absoluto-e-relativo.md)).

Use o **absoluto**:

- nos scripts que são rodados direto, como os `ft_*.py`: eles não pertencem a pacote nenhum, e o
  import relativo falha neles ([Rodar um arquivo do pacote direto](../05-parte-3/04-o-subpacote.md#rodar-um-arquivo-do-pacote-direto));
- para módulos fora do pacote, como o `elements.py` da raiz: o relativo não sai do pacote mais
  externo;
- quando a clareza vale mais: o nome completo diz de onde o código vem sem que o leitor precise
  saber onde está o arquivo. É o estilo que o PEP 8, o guia de estilo do Python, recomenda como
  padrão.

O **relativo** cabe:

- entre módulos do mesmo pacote, como no `alchemy/__init__.py` (`.elements`), no grimório
  (`.light_validator`) e no subpacote (`.recipes`, `..potions`);
- quando o pacote pode mudar de nome ou de lugar: se `alchemy` virasse `alquimia`, os imports
  relativos de dentro dele continuariam funcionando, e os absolutos precisariam ser reescritos;
- em caminhos longos, que o ponto encurta.

Os dois podem conviver no mesmo arquivo, como em `recipes.py`. O que não pode é misturar sem
critério. O critério deste projeto ([O critério do tutorial](../05-parte-3/02-absoluto-e-relativo.md#o-critério-do-tutorial)):
dentro do pacote `alchemy`, relativo, para que nenhum arquivo do pacote dependa do nome dele; fora
do pacote (o `elements.py` da raiz) e nos scripts, absoluto, porque o relativo não funciona ali. O
`recipes.py` tem um de cada tipo, como o enunciado pede: o absoluto é o do `elements` da raiz.

## Quais são os jeitos de evitar uma dependência circular?

Uma dependência circular explode quando um módulo pede um **nome** a outro que ainda está pela
metade, porque os dois se importam enquanto carregam ([A explosão](../06-parte-4/03-a-explosao.md)).
Os jeitos de evitar mudam o momento do pedido, o que é pedido ou onde fica o que os dois usam:

1. **Import dentro da função:** o import só roda na chamada, quando os dois módulos já terminaram
   de carregar. É o jeito usado na luz.
2. **Importar o módulo, e não o nome:** `from . import light_spellbook` funciona com o módulo pela
   metade, e o nome só é procurado na chamada. Precisa valer nos dois arquivos.
3. **Terceiro módulo:** o que os dois usam vai para um arquivo que não importa nenhum deles, e o
   ciclo desaparece do mapa de dependências. É a solução estrutural, e a melhor quando a árvore
   pode mudar.
4. **Parâmetro (injeção de dependência):** quem chama entrega o dado, e a função não precisa
   importar nada.
5. **Ordem das linhas:** definir o nome antes do import. Funciona por uma porta só e gera aviso do
   flake8.

Cada um, com exemplo e o motivo de ter sido usado ou não aqui, está em
[Quebrar o ciclo](../06-parte-4/04-quebrar-o-ciclo.md).

## Explicar os mecanismos de import

O que acontece em `import alchemy.potions`, do começo ao fim:

1. O Python procura `alchemy` nas pastas do `sys.path`, em ordem. A primeira é a pasta do script
   que está rodando, e é por isso que tudo funciona a partir da raiz
   ([Onde o Python procura](../02-conceitos/02-onde-o-python-procura.md)).
2. Se `alchemy` ainda não está em `sys.modules`, o Python cria o módulo, o guarda em
   `sys.modules` e roda o `alchemy/__init__.py`. O que esse arquivo importa ou define vira a
   interface do pacote ([O pacote](../03-parte-1/03-o-pacote.md)).
3. Depois, o mesmo para `alchemy.potions`: procura `potions.py` dentro da pasta do pacote, guarda
   o módulo em `sys.modules`, roda o arquivo e o pendura no pacote como o atributo `potions`.
4. Por fim, cria no arquivo que importou o nome `alchemy` (com `import`) ou os nomes pedidos (com
   `from ... import`).

Um módulo já carregado não roda de novo: o Python o acha em `sys.modules`. E um módulo entra em
`sys.modules` antes de rodar, e por isso pode ser encontrado pela metade: a origem do import
circular.

## Mostrar os estilos de import

Todos os estilos aparecem nos scripts e arquivos do projeto:

| Estilo | Exemplo no projeto | Onde |
|---|---|---|
| `import módulo` | `import elements` | `ft_alembic_0.py` |
| `from módulo import nome` | `from elements import create_water` | `ft_alembic_1.py` |
| `import pacote.módulo` | `import alchemy.elements` | `ft_alembic_2.py` |
| `from pacote.módulo import nome` | `from alchemy.elements import create_air` | `ft_alembic_3.py` |
| `import pacote` | `import alchemy` | `ft_alembic_4.py` |
| `from pacote import nome` | `from alchemy import create_air` | `ft_alembic_5.py` |
| `from ... import nome as apelido` | `from .potions import healing_potion as heal` | `alchemy/__init__.py` |
| `import pacote.subpacote.módulo` | `import alchemy.transmutation.recipes` | `ft_transmutation_0.py` |
| relativo, mesmo pacote | `from .recipes import lead_to_gold` | `alchemy/transmutation/__init__.py` |
| relativo, pacote acima | `from ..potions import strength_potion` | `alchemy/transmutation/recipes.py` |
| dentro de uma função | `from .light_spellbook import light_spell_allowed_ingredients` | `alchemy/grimoire/light_validator.py` |
| dentro de um bloco `if` | `from alchemy.grimoire.dark_spellbook import dark_spell_record` | `ft_kaboom_1.py` |

## Modificar o laboratório

Duas mudanças que mostram que você entende o que cada peça faz. As duas desfazem um erro pedido
pelo enunciado: servem para a demonstração na avaliação, e depois os arquivos voltam ao que eram.

### Mostrar o create_earth no pacote

O `create_earth` fica fora da interface porque o `alchemy/__init__.py` não o importa. Com ele no
import e no `__all__`, o `alchemy/__init__.py` fica assim:

```python
from .elements import create_air, create_earth
from .potions import healing_potion as heal, strength_potion
from .transmutation import lead_to_gold

__all__ = ["create_air", "create_earth", "heal", "strength_potion",
           "lead_to_gold"]
```

O `ft_alembic_4.py` deixa de falhar: a última linha passa a ser
`Testing the hidden create_earth: Earth element created`, ele termina com código `0`, e o mypy
para de acusar a linha 12, porque agora `create_earth` existe no pacote.

### Desarmar a explosão das trevas

O validador das trevas pode usar o mesmo jeito da luz, com o import dentro da função:

```python
def validate_ingredients(ingredients: str) -> str:
    from .dark_spellbook import dark_spell_allowed_ingredients

    text = ingredients.lower()
    for allowed in dark_spell_allowed_ingredients():
        if allowed in text:
            return f"{ingredients} - VALID"
    return f"{ingredients} - INVALID"
```

O `ft_kaboom_1.py` deixa de explodir e chega à linha que nunca rodava:
`Testing record dark spell: Spell recorded: Curse (Bats and frogs - VALID)`. Com isso, o
laboratório não demonstra mais o que o enunciado pede na Parte IV, e o validador das trevas volta
a ter o import no topo depois da demonstração.
