---
sidebar_position: 2
title: O uso
---

# O uso

O programa precisa de exatamente um argumento: o nome do arquivo. Sem ele, não há o que abrir, e o
programa mostra a forma certa de usá-lo, a **mensagem de uso** (*usage*).

As próximas páginas mostram o arquivo em pedaços: o topo e o `main` aqui, `recover_archive` e
`display` nas seguintes. Os pedaços só rodam juntos, montados na ordem da página [O arquivo
completo](./05-o-arquivo-completo.md).

```python
import sys
import typing


def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file>")
        return
    print("=== Cyber Archives Recovery ===")
    recover_archive(sys.argv[1])


if __name__ == "__main__":
    main()
```

## Os imports

`import sys` dá acesso a `sys.argv`. `import typing` dá acesso a `typing.IO`, usado no type hint do
arquivo aberto na [próxima página](./03-abrir-e-tratar-o-erro.md). Os dois são autorizados pelo
enunciado e ficam no topo do arquivo.

## A conferência

`len(sys.argv) != 2` é verdadeiro quando o comando não traz exatamente um argumento depois do nome
do programa: nenhum, ou dois e mais. Nesse caso o programa imprime o uso e o `return` encerra o
`main` ali. O `sys.exit()`, a forma comum de encerrar um programa, não está entre as funções
autorizadas; o `return` no `main` tem o mesmo efeito, porque nada roda depois dele.

`<file>` é a convenção das mensagens de uso para "aqui vai um nome de arquivo". `sys.argv[0]` é o
caminho do programa como foi digitado: rodando da pasta `data-archivist`, a mensagem sai
`Usage: ex0/ft_ancient_text.py <file>`. O exemplo do enunciado mostra
`Usage: ft_ancient_text.py <file>` porque foi rodado de dentro da pasta do exercício.

Com o argumento certo, o programa imprime o cabeçalho e entrega o nome, `sys.argv[1]`, para
`recover_archive`.

## O main

As duas últimas linhas fazem o arquivo rodar o `main()` quando é executado com `python3`. O Python
cria uma variável `__name__` em todo arquivo: ela vale `"__main__"` quando o arquivo é o programa
rodado, e o nome do módulo (o nome do arquivo sem `.py`) quando ele é importado por outro código.
Assim, o `main()` roda quando o programa é chamado no terminal, e não roda se outro código importar
o arquivo só para usar as funções dele.
