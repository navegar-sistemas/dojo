---
sidebar_position: 5
title: Glossário
---

# Glossário

| Termo | O que é | Onde |
|---|---|---|
| **`__name__`** | variável que vale `"__main__"` quando o arquivo é rodado e o nome do módulo (o nome do arquivo sem `.py`) quando ele é importado | [O uso](../03-ex0/02-o-uso.md) |
| **`..`** | num caminho, a pasta de cima | [Arquivos e caminhos](../02-arquivos/01-arquivos-e-caminhos.md) |
| **ambiente virtual (venv)** | pasta com um Python e bibliotecas só deste projeto; aqui guarda o flake8 e o mypy | [O ambiente virtual](../01-ambiente/03-o-ambiente-virtual.md) |
| **argumento** | cada palavra do comando que roda o programa; o programa as recebe em `sys.argv` | [Os argumentos do terminal](../02-arquivos/06-os-argumentos-do-terminal.md) |
| **arquivo** | conjunto de dados guardado no disco, com um nome | [Arquivos e caminhos](../02-arquivos/01-arquivos-e-caminhos.md) |
| **assinatura** | a linha do `def`: nome, parâmetros com tipos e tipo do retorno | [A assinatura](../06-ex3/03-a-assinatura.md) |
| **buffer** | área de memória onde a escrita espera antes de ir para o destino | [close e o recurso](../02-arquivos/04-close-e-o-recurso.md) |
| **caminho absoluto** | caminho que começa com `/` e parte da raiz | [Arquivos e caminhos](../02-arquivos/01-arquivos-e-caminhos.md) |
| **caminho relativo** | caminho que não começa com `/` e parte da pasta atual | [Arquivos e caminhos](../02-arquivos/01-arquivos-e-caminhos.md) |
| **`cat`** | comando do terminal que imprime o conteúdo de um arquivo | [O enunciado em linguagem simples](./02-o-enunciado-em-linguagem-simples.md) |
| **`chmod`** | comando que muda as permissões de um arquivo | [Quando o open falha](../02-arquivos/05-quando-o-open-falha.md) |
| **`close()`** | método que fecha o arquivo e despeja o buffer | [close e o recurso](../02-arquivos/04-close-e-o-recurso.md) |
| **classe** | o tipo de um objeto, como `TextIOWrapper` para o objeto arquivo | [open e o objeto arquivo](../02-arquivos/02-open-e-o-objeto-arquivo.md) |
| **codificação (*encoding*)** | regra que traduz bytes em caracteres; quase sempre UTF-8 | [open e o objeto arquivo](../02-arquivos/02-open-e-o-objeto-arquivo.md) |
| **código de saída** | número que um programa devolve ao terminar: `0` é sucesso; `echo $?` mostra o do último programa | [Rodar e conferir do exercício 0](../03-ex0/06-rodar-e-conferir.md) |
| **construtor** | o tipo chamado como função para criar um valor dele, como `str(25)` | [O enunciado em linguagem simples](./02-o-enunciado-em-linguagem-simples.md) |
| **descritor** | o número de um fluxo: 0 entrada, 1 saída, 2 erro | [Os três fluxos](../05-ex2/02-os-tres-fluxos.md) |
| **`/dev/full`** | arquivo especial do Linux que simula um disco cheio | [Gravar o arquivo](../04-ex1/05-gravar-o-arquivo.md) |
| **`/dev/null`** | arquivo especial que descarta tudo o que recebe e, lido, está vazio | [Os três fluxos](../05-ex2/02-os-tres-fluxos.md) |
| **`diff`** | comando que compara duas listas de linhas e mostra só as diferenças | [Rodar e conferir do exercício 0](../03-ex0/06-rodar-e-conferir.md) |
| **enunciado (*subject*)** | o documento oficial que diz o que o projeto deve entregar | [O enunciado em linguagem simples](./02-o-enunciado-em-linguagem-simples.md) |
| **`EOFError`** | exceção do `input()` quando a entrada acaba antes de um Enter | [Pedir o nome](../04-ex1/04-pedir-o-nome.md) |
| **Errno** | número do erro que o sistema operacional devolve, como `[Errno 2]` | [Quando o open falha](../02-arquivos/05-quando-o-open-falha.md) |
| **exceção** | objeto que descreve um erro, com um tipo e uma mensagem | [Pré-requisitos](./03-pre-requisitos.md) |
| **`finally`** | bloco que roda sempre que o `try` termina, com erro ou sem erro | [close e o recurso](../02-arquivos/04-close-e-o-recurso.md) |
| **flake8** | ferramenta que confere o estilo do código | [Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
| **`flush()`** | método que despeja o buffer no destino na hora | [Escrever no stderr](../05-ex2/03-escrever-no-stderr.md) |
| **fluxo (*stream*)** | canal de comunicação do programa: entrada padrão, saída padrão ou saída de erro | [Os três fluxos](../05-ex2/02-os-tres-fluxos.md) |
| **funções autorizadas** | as únicas funções prontas do Python que cada exercício pode chamar | [O enunciado em linguagem simples](./02-o-enunciado-em-linguagem-simples.md) |
| **gerenciador de contexto** | objeto que sabe o que fazer ao entrar e ao sair de um bloco `with` | [O with](../06-ex3/02-o-with.md) |
| **`import`** | instrução que traz um módulo para o programa | [Os argumentos do terminal](../02-arquivos/06-os-argumentos-do-terminal.md) |
| **`KeyboardInterrupt`** | exceção lançada quando a pessoa aperta `Ctrl+C` | [Pedir o nome](../04-ex1/04-pedir-o-nome.md) |
| **método** | função que pertence a um valor e é chamada com ponto, como `file.read()` | [O enunciado em linguagem simples](./02-o-enunciado-em-linguagem-simples.md) |
| **modo de abertura** | segundo argumento do `open()`: `"r"` para ler, `"w"` para escrever | [open e o objeto arquivo](../02-arquivos/02-open-e-o-objeto-arquivo.md) |
| **módulo** | conjunto de código que vem com o Python e entra no programa com `import`, como `sys` | [Os argumentos do terminal](../02-arquivos/06-os-argumentos-do-terminal.md) |
| **mypy** | ferramenta que confere os tipos anotados no código, sem rodá-lo | [Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
| **`None`** | o valor que quer dizer "nada" | [Devolver o texto](../04-ex1/02-devolver-o-texto.md) |
| **objeto arquivo** | o que `open()` devolve: representa o arquivo aberto e tem os métodos para usá-lo | [open e o objeto arquivo](../02-arquivos/02-open-e-o-objeto-arquivo.md) |
| **`OSError`** | tipo das falhas que o sistema operacional devolve; pai de `FileNotFoundError`, `PermissionError` e `IsADirectoryError` | [Quando o open falha](../02-arquivos/05-quando-o-open-falha.md) |
| **pasta (diretório)** | lugar que guarda arquivos e outras pastas | [Arquivos e caminhos](../02-arquivos/01-arquivos-e-caminhos.md) |
| **pasta atual** | a pasta em que o terminal está; `pwd` a mostra | [Arquivos e caminhos](../02-arquivos/01-arquivos-e-caminhos.md) |
| **permissões** | o que o dono, o grupo e os outros podem fazer com um arquivo: ler, escrever, executar | [Quando o open falha](../02-arquivos/05-quando-o-open-falha.md) |
| **pipe (`\|`)** | liga a saída padrão de um comando à entrada padrão do seguinte | [Rodar e conferir do exercício 1](../04-ex1/08-rodar-e-conferir.md) |
| **`read()`** | método que lê o arquivo inteiro e devolve um `str` | [read e o texto](../02-arquivos/03-read-e-o-texto.md) |
| **`readline()`** | método que lê uma linha, com o `\n` | [Ler sem input](../05-ex2/04-ler-sem-input.md) |
| **recurso** | algo que o sistema reserva para o programa e precisa ser devolvido, como um arquivo aberto | [close e o recurso](../02-arquivos/04-close-e-o-recurso.md) |
| **redirecionar** | mandar um fluxo para um arquivo ou outro comando, com `>`, `2>`, `<` ou `\|` | [Os três fluxos](../05-ex2/02-os-tres-fluxos.md) |
| **`repr()`** | mostra um valor como ele seria escrito no código, com os caracteres invisíveis à mostra | [read e o texto](../02-arquivos/03-read-e-o-texto.md) |
| **root** | o administrador do sistema, que lê qualquer arquivo | [Quando o open falha](../02-arquivos/05-quando-o-open-falha.md) |
| **`/etc/sudoers`** | arquivo de configuração do `sudo` que só o administrador lê; o exemplo de arquivo inacessível | [Quando o open falha](../02-arquivos/05-quando-o-open-falha.md) |
| **`splitlines()`** | método de `str` que divide o texto em linhas, sem os `\n` | [Transformar o texto](../04-ex1/03-transformar-o-texto.md) |
| **`sys.argv`** | lista com o caminho do programa e os argumentos | [Os argumentos do terminal](../02-arquivos/06-os-argumentos-do-terminal.md) |
| **`sys.stdin`, `sys.stdout`, `sys.stderr`** | os três fluxos: entrada padrão, saída padrão e saída de erro | [Os três fluxos](../05-ex2/02-os-tres-fluxos.md) |
| **`TextIOWrapper`** | a classe (o tipo) do objeto arquivo aberto em modo texto | [open e o objeto arquivo](../02-arquivos/02-open-e-o-objeto-arquivo.md) |
| **tupla** | sequência entre parênteses, como `(True, "ok")` | [A assinatura](../06-ex3/03-a-assinatura.md) |
| **type hint** | anotação do tipo de um parâmetro, variável ou retorno, como `file_name: str` | [Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
| **`typing.IO[str]`** | o type hint de um arquivo aberto que lê e escreve `str` | [open e o objeto arquivo](../02-arquivos/02-open-e-o-objeto-arquivo.md) |
| **`UnicodeDecodeError`** | exceção do `read()` quando os bytes do arquivo não formam texto | [Quando o open falha](../02-arquivos/05-quando-o-open-falha.md) |
| **valor padrão** | valor que um parâmetro recebe quando quem chama não passa nada | [A assinatura](../06-ex3/03-a-assinatura.md) |
| **`with`** | instrução que fecha o arquivo sozinha quando o bloco termina | [O with](../06-ex3/02-o-with.md) |
| **`write()`** | método que escreve um `str` no arquivo, sem acrescentar quebra de linha | [Gravar o arquivo](../04-ex1/05-gravar-o-arquivo.md) |
