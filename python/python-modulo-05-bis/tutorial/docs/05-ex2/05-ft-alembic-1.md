---
sidebar_position: 5
title: ft_alembic_1.py
---

# ft_alembic_1.py

O segundo programa entra pelo portal: `import alchemy` e só o que o `__init__.py` expõe. Ele cria
ar com sucesso e depois tenta criar terra pelo mesmo caminho, o que precisa falhar. Crie
`ft_alembic_1.py`, na raiz:

```python title="ft_alembic_1.py"
import alchemy

if __name__ == "__main__":
    print("=== Alembic 1 ===")
    print("Accessing the alchemy module using 'import alchemy'")
    print(f"Testing create_air: {alchemy.create_air()}")
    print("Now show that not all functions can be reached")
    print("This will raise an exception!")
    print("Testing the hidden create_earth: ", end="")
    print(f"{alchemy.create_earth()}")
```

- `import alchemy` roda o `alchemy/__init__.py`, e o nome `alchemy` passa a ser o pacote, com os
  nomes que o `__init__.py` criou;
- `alchemy.create_air()` funciona: é o nome exposto;
- `end=""` troca o fim da linha do `print`: em vez de uma quebra de linha, nada. O texto
  `Testing the hidden create_earth: ` fica com a linha aberta, e o que vier depois continua nela,
  como na saída do enunciado;
- `alchemy.create_earth()` não existe no pacote e lança `AttributeError`. Capturar a exceção é
  opcional no enunciado; a escolha do tutorial é **não** capturar, e o programa termina com o
  traceback, como no exemplo.

```bash
python3 ft_alembic_1.py
```

```text
=== Alembic 1 ===
Accessing the alchemy module using 'import alchemy'
Testing create_air: Air element created
Now show that not all functions can be reached
This will raise an exception!
Testing the hidden create_earth: Traceback (most recent call last):
  File "/path/to/the-codex/ft_alembic_1.py", line 10, in <module>
    print(f"{alchemy.create_earth()}")
             ^^^^^^^^^^^^^^^^^^^^
AttributeError: module 'alchemy' has no attribute 'create_earth'. Did you mean '.create_air' instead of '.create_earth'?
```

Comparada com a do enunciado:

- o caminho do arquivo é o da pasta do projeto (`/path/to/the-codex` está no lugar dele), e a
  linha é a 10, a da chamada neste arquivo;
- a linha de `^` marca o trecho que falhou, `alchemy.create_earth`. No enunciado, ela começa uma
  coluna antes, embaixo da `{`; do Python 3.11 ao 3.15, ela começa embaixo do `a` de `alchemy`, e
  no 3.10 a linha nem aparece;
- a sugestão do fim vem escrita de outro jeito no Python 3.15 ("você quis dizer `.create_air` em
  vez de `.create_earth`?"); do 3.10 ao 3.14, ela é `Did you mean: 'create_air'?`, como no
  enunciado;
- num terminal, o Python colore o traceback a partir da versão 3.13.

O texto `Testing the hidden create_earth: ` sai antes do traceback, na mesma linha, porque o
Python esvazia a saída do programa antes de imprimir uma exceção não capturada. O `print` vai para
a **saída padrão** do programa, e o traceback para a **saída de erros**, um segundo canal que o
terminal mostra no mesmo lugar.

## O erro proposital do mypy

O enunciado avisa que este arquivo tem um erro do mypy de propósito:

```bash
.venv/bin/mypy --disallow-untyped-defs ft_alembic_1.py
```

```text
ft_alembic_1.py:10: error: Module has no attribute "create_earth"; maybe "create_air"?  [attr-defined]
Found 1 error in 1 file (checked 1 source file)
```

O mypy lê o `alchemy/__init__.py`, vê que ele não cria `create_earth` e acusa a linha 10 antes de
o programa rodar, com a mesma sugestão do Python. Como o programa existe para mostrar essa falha,
a chamada fica no código. Esta é a **única** reclamação do mypy aceita no projeto: qualquer outra
precisa ser corrigida. O flake8 não confere atributos de módulos, e para ele o arquivo está limpo.
