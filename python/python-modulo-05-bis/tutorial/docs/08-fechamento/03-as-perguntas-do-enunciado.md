---
sidebar_position: 3
title: As perguntas do enunciado
---

# As perguntas do enunciado

O enunciado deixa uma pergunta no fim de cada exercício, e avisa que, na avaliação, pode ser pedido
que você sele um laboratório novo do zero, explique qualquer mecanismo de import, mude o que o
pacote expõe, ou quebre e conserte uma dependência circular. Também pede, no exercício 1, que você
saiba explicar por que o `.env` está no `.gitignore`, e, no exercício 4, as alternativas à solução
escolhida.

## Exercício 0: o que um ambiente virtual isola, e o que não isola?

**Isola** as bibliotecas instaladas. Cada ambiente tem a sua pasta `site-packages`, o `pip` dele
instala ali, e as bibliotecas do Python global não aparecem dentro dele
(`include-system-site-packages = false`). Duas versões diferentes da mesma biblioteca podem
conviver na mesma máquina, uma em cada ambiente, e apagar a pasta do ambiente desfaz tudo o que foi
instalado nela ([O ambiente virtual por dentro](../02-ex0/02-o-ambiente-virtual-por-dentro.md)).

**Não isola**:

- **o próprio Python**: o `python` do ambiente é um atalho para o Python global, com a mesma versão
  e a mesma biblioteca padrão. Se o Python global for removido ou trocado de versão, o ambiente
  quebra. Para outra versão do Python, é preciso outro Python instalado;
- **o sistema**: o programa num ambiente virtual lê e grava qualquer arquivo que o usuário pode
  ler e gravar, usa a rede, roda outros programas, enxerga as variáveis de ambiente. Um ambiente
  virtual não é uma proteção de segurança, só uma separação de bibliotecas;
- **o que está fora do Python**: programas e bibliotecas do sistema operacional de que alguma
  biblioteca Python dependa continuam sendo os da máquina.

## Exercício 0: por que escolher o Poetry em vez de um requirements.txt?

O `requirements.txt` diz o que instalar, e o `pip` escolhe as versões na hora: duas instalações em
dias diferentes podem dar versões diferentes. O Poetry separa as duas coisas
([Poetry e pyproject.toml](../02-ex0/07-poetry-e-pyproject.md)):

- o `pyproject.toml` diz o que o projeto aceita (`pandas>=2.1`);
- o `poetry.lock` guarda o que foi escolhido, com a versão exata de cada biblioteca, inclusive das
  dependências transitivas, e uma impressão digital de cada arquivo. Toda instalação a partir dele é
  idêntica, em qualquer máquina, e um arquivo adulterado é recusado;
- a resolução considera todas as versões do Python de `requires-python` de uma vez, e o
  `poetry.lock` guarda uma escolha para cada faixa
  ([Instalar com o Poetry](../02-ex0/11-instalar-com-poetry.md#a-segunda-instalação));
- o Poetry cria e gerencia o ambiente virtual sozinho (`poetry install`, `poetry run`).

O `requirements.txt` também pode fixar versões (`pandas==3.1.1`, gerado por `pip freeze`, que lista
o que está instalado), mas aí mistura o que o projeto pede com o que foi resolvido, e atualizar uma
biblioteca vira trabalho manual. Para um script pequeno, o `requirements.txt` basta; para um
projeto que várias pessoas instalam, o arquivo de travamento evita o "na minha máquina funciona".

A vantagem depende de o `poetry.lock` ir junto com o projeto. Nesta entrega ele fica de fora,
porque o enunciado não o lista: na avaliação, o `poetry install` num clone novo resolve as versões
do zero, como o `pip`, e pode chegar a versões diferentes das que você instalou
([O poetry.lock](../02-ex0/07-poetry-e-pyproject.md#o-poetrylock)). Para reproduzir o laboratório
exatamente, o `poetry.lock` teria de ser entregue.

## Exercício 1: por que o .env está no .gitignore?

Porque ele guarda os segredos de verdade (a `API_KEY`, senhas dentro da `DATABASE_URL`), e tudo o
que entra no repositório fica no histórico para sempre, à vista de quem tem acesso a ele. O
`.gitignore` impede o `git add` de levá-lo por engano. No lugar dele vai o `.env.example`, com os
nomes das variáveis e os segredos em branco ([O .gitignore e o .env.example](../03-ex1/04-o-gitignore.md)).

## Exercício 1: por que uma variável de ambiente é melhor lugar para um segredo do que uma constante no código? O que ainda não é seguro nela?

**Melhor**, porque:

- o segredo não está em nenhum arquivo do repositório, e não vai junto com o código para quem o lê
  ou copia;
- cada lugar onde o programa roda tem o seu valor (a chave de teste na máquina de quem desenvolve,
  a de produção no servidor), sem mudar uma linha de código;
- trocar uma chave vazada é trocar uma variável, sem um registro novo no repositório.

**Ainda não é seguro**:

- o `.env` é um arquivo de texto comum no disco: qualquer pessoa ou programa que leia os arquivos
  do usuário lê o segredo;
- as variáveis de ambiente passam para todos os programas que o programa iniciar, e outros
  programas do mesmo usuário podem lê-las enquanto ele roda (no Linux, pelo arquivo
  `/proc/<número do processo>/environ`);
- o comando do roteiro, `MATRIX_MODE=production API_KEY=secret123 python3 ex1/oracle.py`, fica
  gravado no histórico do terminal com a chave escrita nele;
- um programa que imprime ou registra a sua configuração (num log, numa mensagem de erro) espalha o
  segredo. Por isso o Oráculo mostra `Authenticated`, e nunca a chave.

O segredo sai do código, mas continua em texto puro em algum lugar. Sistemas de produção usam
gerenciadores de segredos, que guardam os valores cifrados e os entregam só a quem tem permissão.

## Exercício 2: o que exatamente o \_\_init\_\_.py mudou?

Ele definiu **quais nomes existem no pacote**. `import alchemy` roda o `__init__.py`, e o pacote
`alchemy` tem como atributos os nomes que esse arquivo cria: o `from .elements import create_air`
criou `alchemy.create_air`. Nenhuma linha cria `alchemy.create_earth`, e por isso
`alchemy.create_earth()` lança `AttributeError`.

Nada foi escondido: a função continua no módulo `alchemy.elements`, e
`alchemy.elements.create_earth()` funciona, porque carregar o submódulo o deixou como atributo do
pacote ([Rodar e conferir do exercício 2](../05-ex2/07-rodar-e-conferir.md#o-create_earth-continua-lá)).
O Python não tem nomes privados: o `__init__.py` escolhe o atalho, a interface que o pacote
oferece, e a `__all__` declara essa interface para quem lê, para o flake8 e para o
`from alchemy import *`.

## Exercício 3: quando usar um caminho absoluto, e quando um relativo?

- **Absoluto** fora de pacotes (nos programas, como os `ft_*.py`, onde o relativo nem funciona), e
  para alcançar módulos fora do pacote, como o `elements.py` da raiz a partir de `potions.py` e de
  `recipes.py`: o relativo não sai do pacote mais alto. Também quando o caminho completo ajuda a
  ler, mesmo dentro do pacote. É o que a PEP 8, o guia de estilo do Python, recomenda como regra
  geral.
- **Relativo** dentro de um pacote, para os vizinhos e para os pacotes de cima: deixa claro que o
  módulo é do mesmo pacote (e distingue o `alchemy/elements.py` do `elements.py` da raiz, com o
  mesmo nome), e o pacote continua funcionando se mudar de nome ou de lugar.

O `recipes.py` usa os dois para mostrar a diferença
([O subpacote transmutation](../06-ex3/04-o-subpacote-transmutation.md#recipespy)). Pela regra
acima, o `from alchemy.potions import strength_potion` dele seria relativo (`from ..potions
import ...`). Ele é absoluto por escolha do tutorial, uma exceção à regra para o arquivo mostrar
as duas formas de alcançar um vizinho do pacote; o "pelo menos um de cada" do enunciado já estaria
cumprido pelo `from elements import create_fire`, o absoluto obrigatório para sair do pacote.

## Exercício 4: os dois grimórios descrevem dois arquivos que precisam um do outro. Por que só um explode?

Porque o que explode não é a dependência mútua, e sim o **momento** em que ela é resolvida. Um
`import` no topo roda quando o arquivo é carregado; no par das trevas, os dois arquivos se pedem
durante o carregamento, e um deles recebe o outro ainda pela metade, sem a função pedida
(`ImportError ... partially initialized module`). No par da luz, o validador só pede o livro dentro
de `validate_ingredients`, quando ela é chamada, e a essa altura os dois já terminaram de carregar
([O grimório das trevas](../07-ex4/04-o-grimorio-das-trevas.md#a-comparação)).

### As alternativas

| Alternativa | Como | Neste projeto |
|---|---|---|
| import dentro da função (a escolhida) | o validador importa o livro dentro de `validate_ingredients` | funciona; o validador carrega sem o livro, e o livro só é buscado na primeira validação |
| import tardio do outro lado | o livro importa o validador dentro de `light_spell_record`, e o validador importa o livro no topo | funciona do mesmo jeito; é só escolher qual dos dois adia |
| importar o módulo, e não o nome | `from . import light_spellbook` no topo, e `light_spellbook.light_spell_allowed_ingredients()` dentro da função. O módulo pela metade é aceito no import, e a função só é procurada nele na hora da chamada | só no validador, funciona com o `__init__.py` do tutorial, que carrega o livro antes; com um `__init__.py` vazio e o validador carregado primeiro, quebra com `ImportError ... partially initialized module`. Nos **dois** arquivos, funciona em qualquer ordem |
| um terceiro módulo | mover a lista de ingredientes para um módulo que os dois importam, e que não importa nenhum deles: o círculo desaparece | o melhor desenho em geral, mas acrescenta um arquivo à árvore do enunciado, e o enunciado quer a lista numa função do livro |
| passar o valor como parâmetro | o livro passa a lista ao validador: `validate_ingredients(ingredients, allowed)` | o validador deixa de precisar do livro, mas muda a assinatura que o enunciado fixa |

## Na avaliação: selar um laboratório novo do zero

```bash
rm -rf lab_env
python3 -m venv lab_env
source lab_env/bin/activate
python3 -m pip install --upgrade pip
pip install -r ex0/requirements.txt -r ex1/requirements.txt
```

Se o `lab_env` estiver ativado, rode `deactivate` antes do `rm -rf`. A última linha do `pip
install` lista as cinco bibliotecas:

```text
Successfully installed numpy-2.5.4 pandas-3.1.1 python-dateutil-4.0.0 python-dotenv-1.2.4 tzdata-2026.6
```

Depois, os programas do roteiro: `python3 ex0/construct.py` (a saída "sealed"),
`python3 ex0/loading.py` e `python3 ex1/oracle.py`.

## Na avaliação: mudar o que o pacote expõe

Para expor também `create_earth`, o `alchemy/__init__.py` ganha o nome no import e na `__all__`:

```python
from .elements import create_air, create_earth

__all__ = ["create_air", "create_earth"]
```

```bash
python3 ft_alembic_1.py | tail -n 1
.venv/bin/mypy --disallow-untyped-defs ft_alembic_1.py
```

```text
Testing the hidden create_earth: Earth element created
Success: no issues found in 1 source file
```

O programa não falha mais, e o erro proposital do mypy desaparece: a falha do exercício 2 vinha só
dessa escolha do `__init__.py`. Volte o arquivo ao original, com só o `create_air`, para a entrega.

## Na avaliação: quebrar e consertar uma dependência circular

**Quebrar a luz.** Mova o import do `light_validator.py` para o topo, como no par das trevas:

```python
from .light_spellbook import light_spell_allowed_ingredients


def validate_ingredients(ingredients: str) -> str:
    lowered = ingredients.lower()
    for allowed in light_spell_allowed_ingredients():
        if allowed in lowered:
            return f"{ingredients} - VALID"
    return f"{ingredients} - INVALID"
```

```bash
python3 ft_kaboom_0.py 2>&1 | tail -n 1
```

```text
ImportError: cannot import name 'light_spell_allowed_ingredients' from partially initialized module 'alchemy.grimoire.light_spellbook' (most likely due to a circular import) (/path/to/the-codex/alchemy/grimoire/light_spellbook.py)
```

Agora a luz também explode. Volte o import para dentro da função.

**Consertar as trevas.** Mova o import do `dark_validator.py` para dentro da função, como no par da
luz:

```python
def validate_ingredients(ingredients: str) -> str:
    from .dark_spellbook import dark_spell_allowed_ingredients

    lowered = ingredients.lower()
    for allowed in dark_spell_allowed_ingredients():
        if allowed in lowered:
            return f"{ingredients} - VALID"
    return f"{ingredients} - INVALID"
```

```bash
python3 ft_kaboom_1.py
```

```text
=== Kaboom 1 ===
Access to alchemy/grimoire/dark_spellbook.py directly
Test import now - THIS WILL RAISE AN UNCAUGHT EXCEPTION
Testing record dark spell: Spell recorded: Curse (bats and frogs - VALID)
```

O laboratório não explode, e a última linha do programa, que nunca tinha rodado, registra o
feitiço. A mudança foi uma decisão, quando o validador busca o livro, e não uma correção de
sintaxe. Volte o import para o topo: o par das trevas é entregue quebrado, de propósito.

## Na avaliação: explicar qualquer mecanismo de import

A parte [Módulos e pacotes](../04-conceitos/01-modulo-e-import.md) cobre cada um, com um
experimento:

| Mecanismo | Página |
|---|---|
| `import x` e `from x import y`, o módulo que roda uma vez só | [Módulo e import](../04-conceitos/01-modulo-e-import.md) |
| onde o Python procura (`sys.path`) e por que não mexer nele | [Onde o Python procura](../04-conceitos/02-onde-o-python-procura.md) |
| pacote, `__init__.py`, `__all__`, submódulo como atributo | [Pacote e \_\_init\_\_.py](../04-conceitos/03-pacote-e-init.md) |
| import absoluto e relativo | [Absoluto e relativo](../04-conceitos/04-absoluto-e-relativo.md) |
| `sys.modules`, módulo parcialmente inicializado, import circular | [O import circular](../04-conceitos/05-o-import-circular.md) |
| import pelo nome em texto (`importlib.import_module`) | [loading.py](../02-ex0/08-loading.md#importar-pelo-nome) |
