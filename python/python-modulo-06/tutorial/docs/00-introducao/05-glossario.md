---
sidebar_position: 5
title: Glossário
---

# Glossário

| Termo | O que é | Onde |
|---|---|---|
| **`__all__`** | lista, em texto, dos nomes que formam a interface de um módulo; tira o aviso `F401` do flake8 e satisfaz o mypy no modo estrito | [A interface do pacote](../03-parte-1/05-a-interface-do-pacote.md) |
| **`__init__.py`** | arquivo que transforma uma pasta em pacote; roda quando o pacote é importado | [O pacote](../03-parte-1/03-o-pacote.md) |
| **`__module__`** | atributo de uma função com o nome do módulo onde ela foi escrita | [As poções](../04-parte-2/02-as-pocoes.md) |
| **`__name__`** | variável que vale `"__main__"` no arquivo rodado com `python3`, e o nome do módulo num arquivo importado | [import e from](../03-parte-1/04-import-e-from.md) |
| **`__package__`** | atributo de um módulo com o nome do pacote dele; o ponto de partida do import relativo | [Absoluto e relativo](../05-parte-3/02-absoluto-e-relativo.md) |
| **`__pycache__`** | pasta de cache que o Python cria ao importar um arquivo; não é entregue | [O módulo e o import](../02-conceitos/01-o-modulo-e-o-import.md#a-pasta-__pycache__) |
| **`2>&1`** | junta a saída de erro à saída padrão de um comando | [Rodar e conferir da Parte I](../03-parte-1/08-rodar-e-conferir.md) |
| **ambiente virtual (venv)** | pasta com um Python e bibliotecas só deste projeto; aqui guarda o flake8 e o mypy | [O ambiente virtual](../01-ambiente/03-o-ambiente-virtual.md) |
| **apelido (*alias*)** | outro nome para algo importado, criado com `as` | [O módulo e o import](../02-conceitos/01-o-modulo-e-o-import.md) |
| **atributo** | nome guardado dentro de um objeto e lido com ponto, como `alchemy.create_air` | [O módulo e o import](../02-conceitos/01-o-modulo-e-o-import.md) |
| **`AttributeError`** | exceção de um nome lido com ponto que não existe no objeto | [O pacote](../03-parte-1/03-o-pacote.md) |
| **`$?`** | variável do terminal com o código de saída do último comando | [Conferir tudo](../07-fechamento/01-conferir-tudo.md#os-códigos-de-saída) |
| **código de saída** | número que um programa devolve ao terminar: `0` é sucesso | [Pré-requisitos](./03-pre-requisitos.md) |
| **dependência circular** | dois módulos que precisam um do outro; com os dois imports no topo, o import falha | [A explosão](../06-parte-4/03-a-explosao.md) |
| **`diff`** | comando que compara dois textos linha a linha e mostra só as diferenças | [Rodar e conferir da Parte I](../03-parte-1/08-rodar-e-conferir.md) |
| **`E402`** | aviso do flake8 para um import no meio do corpo do arquivo, fora do topo | [A explosão](../06-parte-4/03-a-explosao.md) |
| **`E501`** | aviso do flake8 para uma linha com mais de 79 caracteres | [import e from](../03-parte-1/04-import-e-from.md) |
| **enunciado (*subject*)** | o documento que diz o que o projeto deve entregar | [O enunciado em linguagem simples](./02-o-enunciado-em-linguagem-simples.md) |
| **exceção** | objeto que descreve um erro, com um tipo e uma mensagem | [Pré-requisitos](./03-pre-requisitos.md) |
| **`F401`** | aviso do flake8 para um import que o arquivo não usa | [A interface do pacote](../03-parte-1/05-a-interface-do-pacote.md) |
| **flake8** | ferramenta que confere o estilo do código | [Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
| **import absoluto** | import com o nome completo do módulo, a partir de uma pasta do `sys.path` | [Absoluto e relativo](../05-parte-3/02-absoluto-e-relativo.md) |
| **import dentro da função** | import que só roda quando a função é chamada; quebra o ciclo da luz | [Quebrar o ciclo](../06-parte-4/04-quebrar-o-ciclo.md) |
| **import relativo** | import que começa com pontos e parte do pacote do arquivo que importa | [Absoluto e relativo](../05-parte-3/02-absoluto-e-relativo.md) |
| **`ImportError`** | exceção de um import que não consegue terminar: um nome que não existe no módulo, um import relativo sem pacote ou além do pacote mais externo | [A explosão](../06-parte-4/03-a-explosao.md) |
| **injeção de dependência** | quem chama entrega à função o que ela precisa, em vez de a função importar | [Quebrar o ciclo](../06-parte-4/04-quebrar-o-ciclo.md) |
| **interface** | os nomes que um módulo ou pacote oferece a quem o importa | [A interface do pacote](../03-parte-1/05-a-interface-do-pacote.md) |
| **módulo** | arquivo `.py` usado por outro através do `import`; o nome é o do arquivo sem `.py` | [O módulo e o import](../02-conceitos/01-o-modulo-e-o-import.md) |
| **módulo parcialmente inicializado** | módulo que já está em `sys.modules`, mas cujo arquivo ainda não terminou de rodar | [A explosão](../06-parte-4/03-a-explosao.md) |
| **`ModuleNotFoundError`** | exceção do import que não acha o módulo em nenhuma pasta do `sys.path` | [Onde o Python procura](../02-conceitos/02-onde-o-python-procura.md) |
| **mypy** | ferramenta que confere os tipos anotados no código, sem rodá-lo | [Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
| **mypy `--strict`** | modo do mypy que liga um grupo de conferências extras, inclusive a de nomes reexportados | [A interface do pacote](../03-parte-1/05-a-interface-do-pacote.md) |
| **namespace package** | pasta sem `__init__.py` que o Python aceita como pacote; não é usada neste projeto | [O pacote](../03-parte-1/03-o-pacote.md) |
| **objeto módulo** | o valor criado pelo Python a partir de um arquivo importado, com o que o arquivo definiu | [O módulo e o import](../02-conceitos/01-o-modulo-e-o-import.md) |
| **pacote (*package*)** | pasta com `__init__.py` que se importa pelo nome, como `alchemy` | [O pacote](../03-parte-1/03-o-pacote.md) |
| **PEP 8** | o guia de estilo do Python, que o flake8 confere | [Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
| **raiz** | a pasta principal do projeto e do repositório entregue, onde ficam os scripts | [A pasta do projeto](../01-ambiente/02-a-pasta-do-projeto.md) |
| **saída padrão e saída de erro** | os dois canais de texto de um programa (*stdout* e *stderr*); o traceback vai para o segundo | [O erro proposital](../03-parte-1/06-o-erro-proposital.md) |
| **script de teste** | programa curto `ft_*.py` que importa as peças de um jeito e imprime o resultado | [O que vamos construir](./01-o-que-vamos-construir.md) |
| **`sed`** | programa que edita texto linha a linha; `s\|A\|B\|` troca `A` por `B` | [Rodar e conferir da Parte I](../03-parte-1/08-rodar-e-conferir.md) |
| **subpacote** | pacote dentro de outro pacote, como `alchemy.transmutation` | [O subpacote](../05-parte-3/04-o-subpacote.md) |
| **`sys.modules`** | dicionário com os módulos já carregados; o import procura ali antes de rodar um arquivo | [O módulo e o import](../02-conceitos/01-o-modulo-e-o-import.md) |
| **`sys.path`** | lista de pastas onde o import procura os módulos; o enunciado proíbe modificá-la | [Onde o Python procura](../02-conceitos/02-onde-o-python-procura.md) |
| **traceback** | relatório de erro que o Python imprime quando uma exceção não é capturada | [Pré-requisitos](./03-pre-requisitos.md) |
| **type hint** | anotação do tipo de um parâmetro ou do retorno, como `-> str` | [Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
