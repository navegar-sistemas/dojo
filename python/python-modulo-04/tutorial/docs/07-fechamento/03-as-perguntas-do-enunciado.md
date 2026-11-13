---
sidebar_position: 3
title: As perguntas do enunciado
---

# As perguntas do enunciado

O enunciado deixa uma pergunta no exercício 0 e avisa que, na avaliação, pode ser pedido que você
explique as operações com arquivos, demonstre o tratamento de erros ou mostre como o `with`
funciona.

## Qual é o tipo do dado devolvido por open()?

Um objeto arquivo, não o texto. Em modo texto, a classe é `TextIOWrapper`, do módulo `io` (o `print`
a mostra como `_io.TextIOWrapper`); o type hint usado é `typing.IO[str]`, "um arquivo que lê e
escreve `str`". O texto só vem com `read()` ([open e o objeto
arquivo](../02-arquivos/02-open-e-o-objeto-arquivo.md)).

## Como funcionam as operações com arquivos?

Três passos. `open(caminho, modo)` pede ao sistema operacional acesso ao arquivo: `"r"` para ler (o
padrão), `"w"` para escrever, criando o arquivo ou apagando o conteúdo antigo. `read()`,
`readline()` e `write()` leem e escrevem pelo objeto arquivo. `close()` devolve o recurso ao sistema
e despeja no disco o que ainda estava no buffer ([close e o
recurso](../02-arquivos/04-close-e-o-recurso.md), [Gravar o
arquivo](../04-ex1/05-gravar-o-arquivo.md)).

## Como os programas tratam os erros?

Cada etapa tem o seu `try`, para a mensagem dizer o que falhou. Ao abrir, `except OSError` captura a
família inteira de falhas do sistema: `FileNotFoundError` (Errno 2), `PermissionError` (Errno 13),
`IsADirectoryError` (Errno 21) e as outras ([Quando o open
falha](../02-arquivos/05-quando-o-open-falha.md)). Ao ler, `UnicodeDecodeError` também é
capturado, porque um arquivo que não é texto não é uma falha do sistema. Ao gravar, o `open()`
recusa com `ValueError` um nome com o caractere nulo, e a falha de disco cheio pode aparecer só no
`close()`, que um `try` por fora do `finally` captura ([Gravar o
arquivo](../04-ex1/05-gravar-o-arquivo.md)). Na pergunta do nome, `Ctrl+D`, `Ctrl+C` e bytes que
não formam texto viram resposta vazia ([Pedir o nome](../04-ex1/04-pedir-o-nome.md)). Um
argumento que não pode ser impresso leva à mensagem de uso ([O uso](../03-ex0/02-o-uso.md)). Em
todos esses casos, o programa avisa e termina com código `0` ([Rodar e conferir do exercício
0](../03-ex0/06-rodar-e-conferir.md#nenhum-caso-trava)).

## Por que mandar os erros para a saída de erro?

Para separar o resultado dos avisos. Quem redireciona a saída padrão para um arquivo guarda só o
resultado e continua vendo os erros na tela; quem redireciona a saída de erro guarda um registro só
dos erros ([Os três fluxos](../05-ex2/02-os-tres-fluxos.md)).

## Como ler o teclado sem input()?

Escrevendo a pergunta com `sys.stdout.write`, despejando-a com `sys.stdout.flush()` (sem `\n`, ela
ficaria no buffer) e lendo a resposta com `sys.stdin.readline()`, que devolve a linha com o `\n` do
Enter, ou `""` quando a entrada acabou ([Ler sem input](../05-ex2/04-ler-sem-input.md)).

## Como funciona o with?

`with open(...) as file:` abre o arquivo, guarda-o em `file` e, quando o bloco termina, chama
`file.close()`, termine o bloco normalmente, com `return` ou com uma exceção. O objeto arquivo é um
gerenciador de contexto: sabe o que fazer ao sair do bloco. O `with` substitui o `try` com `finally`
dos exercícios anteriores, mas não captura exceções: o `try` com `except` continua em volta ([O
with](../06-ex3/02-o-with.md)).
