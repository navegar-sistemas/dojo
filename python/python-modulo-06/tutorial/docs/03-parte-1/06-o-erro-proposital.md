---
sidebar_position: 6
title: O erro proposital
---

# O erro proposital

O `__init__.py` pôs `create_air` na interface do pacote e deixou `create_earth` de fora. O
`ft_alembic_4.py` mostra as duas coisas: `alchemy.create_air()` funciona, e
`alchemy.create_earth()` lança uma exceção. O enunciado pede que esse erro aconteça.

## O script

```python title="ft_alembic_4.py"
import alchemy


if __name__ == "__main__":
    print("=== Alembic 4 ===")
    print("Accessing the alchemy module using 'import alchemy'")
    print(f"Testing create_air: {alchemy.create_air()}")
    print("Now show that not all functions can be reached")
    print("This will raise an exception!")
    print("Testing the hidden create_earth: ", end="")
    # alchemy/__init__.py does not expose create_earth: AttributeError here.
    print(f"{alchemy.create_earth()}")
```

- `print("Testing the hidden create_earth: ", end="")` imprime o texto sem terminar a linha
  ([Pré-requisitos](../00-introducao/03-pre-requisitos.md)), e o traceback começa logo depois
  dele, na mesma linha, como na saída do enunciado;
- o comentário avisa quem lê que o erro da linha seguinte é de propósito;
- a última linha é igual à que aparece no traceback do enunciado, `print(f"{alchemy.create_earth()}")`,
  e fica na linha 12 do arquivo, como lá. `print(alchemy.create_earth())` daria o mesmo erro; a
  f-string só repete o enunciado, para que o traceback saia igual.

## Rodar

```bash
python3 ft_alembic_4.py
```

```text
=== Alembic 4 ===
Accessing the alchemy module using 'import alchemy'
Testing create_air: Air element created
Now show that not all functions can be reached
This will raise an exception!
Testing the hidden create_earth: Traceback (most recent call last):
  File "/home/ana/the-codex/ft_alembic_4.py", line 12, in <module>
    print(f"{alchemy.create_earth()}")
             ^^^^^^^^^^^^^^^^^^^^
AttributeError: module 'alchemy' has no attribute 'create_earth'. Did you mean: 'create_air'?
```

No lugar de `/home/ana/the-codex` aparece o caminho completo da sua pasta: o traceback mostra
onde o arquivo está no disco.

## Lendo o traceback

- `File ".../ft_alembic_4.py", line 12, in <module>`: o erro aconteceu na linha 12 do script, no
  corpo do arquivo (`<module>`), e não dentro de uma função;
- a linha de código vem logo abaixo, e os `^` marcam o trecho que falhou: `alchemy.create_earth`.
  A chamada nem chegou a acontecer; o que falhou foi ler o nome `create_earth` no pacote;
- a última linha: `AttributeError`, "o módulo `alchemy` não tem o atributo `create_earth`".
  Desde o Python 3.10, a mensagem procura no módulo um nome parecido com o que faltou e sugere:
  "você quis dizer `create_air`?".

No Python 3.10, a linha dos `^` não aparece. No enunciado, ela começa uma coluna antes, embaixo
do `{`; no Python 3.14, os `^` ficam exatamente embaixo de `alchemy.create_earth`. As duas formas
marcam o mesmo erro.

## Por que o texto e o traceback saem na mesma linha

O `print` escreve na **saída padrão** (*stdout*), e o traceback é escrito em outro canal, a
**saída de erro** (*stderr*). No terminal, os dois aparecem na mesma janela. O texto sem fim de
linha fica guardado à espera do resto da linha; antes de escrever o traceback, o Python esvazia a
saída padrão, e o texto aparece primeiro, seguido do `Traceback`, na mesma linha.

## O que existe dentro do pacote

```bash
python3 -c 'import alchemy; print(sorted(n for n in vars(alchemy) if not n.startswith("__")))'
```

```text
['create_air', 'elements']
```

`vars(alchemy)` dá os atributos do pacote; o comando lista os que não começam com `__` (os que o
Python preenche sozinho, como `__name__`), em ordem alfabética com `sorted`. Há dois:

- `create_air`, que o `__init__.py` importou;
- `elements`, o módulo `alchemy.elements`, que virou atributo do pacote quando o `__init__.py` o
  carregou ([O que import alchemy.elements faz](./03-o-pacote.md#o-que-import-alchemyelements-faz)).

`create_earth` não está na lista, mas continua dentro de `alchemy.elements`:

```bash
python3 -c "import alchemy; print(alchemy.elements.create_earth())"
```

```text
Earth element created
```

O `__init__.py` controla a interface do pacote, o que `alchemy.` oferece direto; ele não tranca
os módulos de dentro. Quem pede o caminho completo, como o `ft_alembic_2.py`, chega à função.

## O erro do mypy

O enunciado avisa que o mypy também reclama deste script, de propósito:

```bash
.venv/bin/mypy --disallow-untyped-defs ft_alembic_4.py
```

```text
ft_alembic_4.py:12: error: Module has no attribute "create_earth"; maybe "create_air"?  [attr-defined]
Found 1 error in 1 file (checked 1 source file)
```

O mypy lê o `alchemy/__init__.py` sem rodar nada, vê que `create_earth` não está lá e acusa a
linha 12 antes de o programa rodar: "o módulo não tem o atributo `create_earth`; talvez
`create_air`?". Como o script precisa mostrar a exceção acontecendo de verdade, a linha fica no
código. Esta é a **única** reclamação aceita do mypy em todo o projeto: qualquer outra precisa
ser corrigida.

O flake8 não confere atributos de módulos, e para ele o arquivo está limpo.
