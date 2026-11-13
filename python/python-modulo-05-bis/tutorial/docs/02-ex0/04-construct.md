---
sidebar_position: 4
title: construct.py
---

# construct.py

O programa responde a uma pergunta, "estou num ambiente virtual?", e imprime uma de duas saídas.
Crie o arquivo `ex0/construct.py` com as peças desta página, na ordem em que aparecem; a
[próxima página](./05-construct-completo.md) mostra o arquivo inteiro.

## Os imports

```python
import os
import site
import sys
```

Três módulos que vêm com o Python, todos na lista de permitidos do exercício 0:

- `sys`: informações do Python em uso, como `sys.prefix`, `sys.base_prefix` e `sys.executable`;
- `site`: as pastas `site-packages`, com `site.getsitepackages()`;
- `os`: funções do sistema operacional; aqui, só `os.path.basename`, explicada abaixo.

## A detecção

```python
def in_virtual_env() -> bool:
    return sys.prefix != sys.base_prefix
```

O teste da [página anterior](./03-ativar-o-ambiente.md#ativar-não-é-o-que-cria-o-isolamento):
dentro de um ambiente virtual, `sys.prefix` é a pasta do ambiente e `sys.base_prefix` é a do
Python global; fora, as duas são iguais.

## Fora do laboratório

```python
def show_open_laboratory() -> None:
    print("LABORATORY STATUS: You are working in the open")
    print()
    print(f"Current Python: {sys.executable}")
    print("Virtual Environment: None detected")
    print()
    print("WARNING: You are in the global environment!")
    print("Every reagent you install here leaks into the whole system.")
    print()
    print("To seal the laboratory, run:")
    print("python3 -m venv lab_env")
    print("source lab_env/bin/activate # On Unix")
    print("lab_env\\Scripts\\activate  # On Windows")
    print()
    print("Then run this program again.")
```

- `sys.executable` é o caminho completo do executável do Python que está rodando o programa. É a
  "informação do ambiente Python atual" que o enunciado pede;
- `print()` sem argumento imprime uma linha vazia;
- as instruções são as do enunciado: criar o ambiente e ativá-lo, no Unix (Linux e macOS) e no
  Windows;
- na linha do Windows, cada `\\` imprime **uma** barra invertida. Dentro de um texto do Python, a
  barra invertida começa uma **sequência de escape**, um código para um caractere especial (`\n` é
  a quebra de linha); `\\` é o código da própria barra. Com uma barra só,
  `"lab_env\Scripts\activate"` sai errado de dois jeitos: `\a` é uma sequência de escape de
  verdade (o caractere de "bipe", invisível), e o texto impresso vira `lab_env\Scriptsctivate`;
  e `\S` não é sequência nenhuma, e o Python 3.14 e o 3.15 avisam com `SyntaxWarning: "\S" is an invalid
  escape sequence`. Os dois espaços antes do `#` copiam o enunciado.

## Dentro do laboratório

```python
def show_sealed_laboratory() -> None:
    print("LABORATORY STATUS: The laboratory is sealed")
    print()
    print(f"Current Python: {sys.executable}")
    print(f"Virtual Environment: {os.path.basename(sys.prefix)}")
    print(f"Environment Path: {sys.prefix}")
    print()
    print("SUCCESS: You are working in an isolated environment!")
    print("Safe to install reagents without affecting")
    print("the global system.")
    print()
    print("Reagent installation path:")
    print(site.getsitepackages()[0])
```

- `sys.prefix` é a pasta do ambiente, a linha `Environment Path`;
- `os.path.basename(caminho)` devolve a última parte de um caminho: de `/path/to/lab_env`, devolve
  `lab_env`. É o nome do ambiente, a linha `Virtual Environment`;
- `site.getsitepackages()[0]` é a primeira pasta `site-packages` da lista, a do ambiente: onde o
  `pip` dele instala os reagentes.

## Os dois locais de pacotes

O enunciado pede que o programa mostre a diferença entre o local de pacotes do ambiente global e
o do ambiente virtual, mas a saída de exemplo dele só mostra um local, o do ambiente virtual
(`Reagent installation path`). O tutorial segue a saída de exemplo à risca: a diferença aparece
comparando as duas execuções. Dentro do laboratório, os reagentes vão para uma pasta dentro de
`lab_env`; fora dele, o programa avisa que tudo o que for instalado vai para o sistema inteiro
(`Every reagent you install here leaks into the whole system`). A
[página de rodar e conferir](./12-rodar-e-conferir.md#os-dois-locais-de-pacotes) mostra os dois
caminhos lado a lado.

## O main

```python
def main() -> None:
    print()
    if in_virtual_env():
        show_sealed_laboratory()
    else:
        show_open_laboratory()


if __name__ == "__main__":
    main()
```

O `print()` do começo é a linha vazia com que as duas saídas do enunciado começam. Depois, uma
pergunta escolhe a saída inteira.
