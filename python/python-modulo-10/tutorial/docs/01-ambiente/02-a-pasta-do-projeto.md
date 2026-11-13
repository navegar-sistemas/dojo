---
sidebar_position: 2
title: A pasta do projeto
---

# A pasta do projeto

O enunciado pede cada exercício num arquivo próprio, dentro de uma pasta com o número do
exercício: `ex0/` a `ex4/`. Crie uma pasta para o projeto, entre nela e crie as cinco pastas:

```bash
mkdir funcmage
cd funcmage
mkdir ex0 ex1 ex2 ex3 ex4
```

`mkdir` cria uma pasta (ou várias, com os nomes em sequência). O nome `funcmage` é só uma
sugestão; o que o enunciado fixa são as pastas `ex0` a `ex4` e os nomes dos arquivos. **Todos os
comandos do tutorial são rodados a partir desta pasta**, a `funcmage`.

Crie também uma pasta `experimentos`, para os programas pequenos que a parte
[Funções como valores](../02-conceitos/01-funcoes-sao-valores.md) usa para mostrar cada ideia.
Eles não fazem parte da entrega:

```bash
mkdir experimentos
```

Ao fim do projeto, a pasta fica assim:

```mermaid
flowchart LR
    root["funcmage/"]
    root --> ex0["ex0/"] --> f0["lambda_spells.py"]
    root --> ex1["ex1/"] --> f1["higher_magic.py"]
    root --> ex2["ex2/"] --> f2["scope_mysteries.py"]
    root --> ex3["ex3/"] --> f3["functools_artifacts.py"]
    root --> ex4["ex4/"] --> f4["decorator_mastery.py"]
    root --> exp["experimentos/"]
    root --> ger["gerador/"] --> fg["data_generator.py"]
    root --> tar["generator.tar.gz"]
    root --> venv[".venv/"]
    root --> cache[".mypy_cache/"]
```

A pasta `.venv/` é criada na [próxima página](./03-o-ambiente-virtual.md); a `.mypy_cache/` é
criada pelo mypy na primeira vez que ele roda, para guardar resultados e conferir mais rápido da
próxima vez; o `generator.tar.gz` e a pasta `gerador/` são o anexo do enunciado
([O gerador de dados](./05-o-gerador-de-dados.md)). Só os cinco arquivos `.py` das pastas `ex0` a
`ex4` são entregues.
