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
    if len(sys.argv) != 2 or not sys.argv[1].isprintable():
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
do programa: nenhum, ou mais de um. A segunda parte, `not sys.argv[1].isprintable()`, recusa um
nome que não pode ser mostrado na tela (explicada logo abaixo). Em qualquer dos dois casos, o
programa imprime o uso e o `return` encerra o `main` ali. O `sys.exit()`, a forma comum de encerrar
um programa, não está entre as funções autorizadas; o `return` no `main` tem o mesmo efeito, porque
nada roda depois dele.

`<file>` é a convenção das mensagens de uso para "aqui vai um nome de arquivo". `sys.argv[0]` é o
caminho do programa como foi digitado: rodando da pasta `data-archivist`, a mensagem sai
`Usage: ex0/ft_ancient_text.py <file>`. O exemplo do enunciado mostra
`Usage: ft_ancient_text.py <file>` porque foi rodado de dentro da pasta do exercício.

Com o argumento certo, o programa imprime o cabeçalho e entrega o nome, `sys.argv[1]`, para
`recover_archive`.

## Um nome que não pode ser mostrado

`isprintable()` é um método de `str` que devolve `True` quando todos os caracteres do texto podem
ser impressos, e `False` quando algum não pode, como uma quebra de linha ou uma tabulação.

O terminal entrega cada argumento ao programa como bytes, e o Python os traduz em caracteres pela
codificação UTF-8 ([open e o objeto arquivo](../02-arquivos/02-open-e-o-objeto-arquivo.md)). Um
byte que não forma texto em UTF-8 vira um caractere especial, que não pode ser impresso. No bash e
no zsh, `$'\xff'` escreve um argumento feito de um byte desses, o de valor 255. Na configuração de
idioma mais comum do Linux e do macOS (`pt_BR.UTF-8`, `en_US.UTF-8`), o primeiro `print` com esse
nome lançaria `UnicodeEncodeError` e travaria o programa. O `isprintable()` barra o nome antes: o
programa mostra o uso e termina normalmente ([Rodar e
conferir](./06-rodar-e-conferir.md#as-outras-falhas)).

O `or` só confere a segunda parte quando a primeira é falsa, isto é, quando há exatamente um
argumento. Sem argumento, o `sys.argv[1]` nem existe, e não chega a ser lido.

## O main

As duas últimas linhas fazem o arquivo rodar o `main()` quando é executado com `python3`. O Python
cria uma variável `__name__` em todo arquivo: ela vale `"__main__"` quando o arquivo é o programa
rodado, e o nome do módulo (o nome do arquivo sem `.py`) quando ele é importado por outro código.
Assim, o `main()` roda quando o programa é chamado no terminal, e não roda se outro código importar
o arquivo só para usar as funções dele.
