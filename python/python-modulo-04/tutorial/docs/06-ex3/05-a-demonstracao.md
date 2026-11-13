---
sidebar_position: 5
title: A demonstração
---

# A demonstração

O `main` faz as quatro chamadas da saída do enunciado: três leituras (inexistente, sem permissão,
normal) e uma escrita com o texto da leitura normal.

```python
def main() -> None:
    print("=== Cyber Archives Security ===")
    print("\nUsing 'secure_archive' to read from a nonexistent file:")
    print(secure_archive("/not/existing/file"))
    print("\nUsing 'secure_archive' to read from an inaccessible file:")
    print(secure_archive("/etc/sudoers"))
    print("\nUsing 'secure_archive' to read from a regular file:")
    result = secure_archive("ancient_fragment.txt")
    print(result)
    print("\nUsing 'secure_archive' to write previous content to a new file:")
    print(secure_archive("new_archive.txt", "write", result[1]))


if __name__ == "__main__":
    main()
```

## Imprimir a tupla

`print` de uma tupla mostra os elementos como seriam escritos no código, entre parênteses:

```text
(True, '[FRAGMENT 001] Digital preservation protocols established 2087\n[FRAGMENT 002] ...')
```

Por isso o texto do arquivo aparece numa linha só, com os `\n` escritos como `\n`, entre aspas. As
aspas mudam quando o texto contém aspas simples: a mensagem
`[Errno 2] No such file or directory: '/not/existing/file'` tem aspas simples dentro, e o Python a
mostra entre aspas duplas, para não confundir. É exatamente o que a saída do enunciado traz.

## Reaproveitar o texto lido

`result` guarda a tupla da leitura normal, e `result[1]` é o segundo elemento, o conteúdo do arquivo
(as posições de uma tupla começam em 0). A escrita grava esse conteúdo em `new_archive.txt`, um
arquivo novo na pasta atual; o enunciado não fixa o nome. Rodar o programa de novo substitui o
arquivo, com o mesmo conteúdo.

O `main` não confere `result[0]` antes de gravar. Se a leitura falhar (o programa rodado fora da
pasta `data-archivist`, por exemplo), `result[1]` é a mensagem de erro, e é ela que vai para
`new_archive.txt`. Rodado da pasta certa, a leitura dá certo e a demonstração grava o fragmento.

## Os caminhos

`/not/existing/file` e `/etc/sudoers` são caminhos absolutos, e funcionam de qualquer pasta.
`ancient_fragment.txt` e `new_archive.txt` são relativos: o programa precisa ser rodado da pasta
`data-archivist` ([Arquivos e caminhos](../02-arquivos/01-arquivos-e-caminhos.md)).
