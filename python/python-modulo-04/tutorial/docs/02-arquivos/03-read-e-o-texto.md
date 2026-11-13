---
sidebar_position: 3
title: read e o texto
---

# read e o texto

Com o arquivo aberto, `read()` entrega o conteúdo. Um detalhe desse texto aparece em toda saída do
projeto: a linha vazia antes do `---` final.

## Ler

Crie `experimentos/ler.py`:

```python
file = open("ancient_fragment.txt")
content = file.read()
file.close()
print(len(content))
print(repr(content))
print(content)
print("end")
```

```bash
python3 experimentos/ler.py
```

```text
180
'[FRAGMENT 001] Digital preservation protocols established 2087\n[FRAGMENT 002] Knowledge must survive the entropy wars\n[FRAGMENT 003] Every byte saved is a victory against oblivion\n'
[FRAGMENT 001] Digital preservation protocols established 2087
[FRAGMENT 002] Knowledge must survive the entropy wars
[FRAGMENT 003] Every byte saved is a victory against oblivion

end
```

- `file.read()` devolve o arquivo inteiro num único `str`, guardado em `content`;
- `len(content)` conta os caracteres: 180;
- `repr(content)` mostra o texto como ele seria escrito no código, entre aspas e com os caracteres
  invisíveis à mostra. É ali que aparecem os `\n`: cada linha do arquivo termina com uma quebra de
  linha, **inclusive a última**. (`repr()` é usado só neste experimento; os exercícios não precisam
  dele.)

## A linha vazia

![O str devolvido por read(): as três linhas do fragmento, cada uma terminada por um \n destacado em azul. Embaixo, o que print(content) mostra no terminal: as três linhas e uma linha vazia, porque o \n do arquivo termina a terceira linha e o \n que o print acrescenta gera a linha vazia](/img/arquivos/o-texto-lido.svg)

`print(content)` imprime o texto e acrescenta mais uma quebra de linha no fim. O `\n` do próprio
arquivo já terminou a terceira linha; o do `print` produz uma linha vazia, que aparece antes de
`end`.

É essa linha vazia que fica antes do `---` final nas saídas do projeto:

```text
---

[FRAGMENT 001] Digital preservation protocols established 2087
[FRAGMENT 002] Knowledge must survive the entropy wars
[FRAGMENT 003] Every byte saved is a victory against oblivion

---
```

A linha vazia de cima vem de imprimir `"---\n"` com `print`: o `\n` do texto mais o do `print`. A de
baixo vem do `\n` final do arquivo mais o do `print(content)`. Um arquivo cuja última linha não
termina com `\n` não teria a linha vazia de baixo; o programa mostra o arquivo como ele é.

## Ler duas vezes

O objeto arquivo guarda a **posição** de leitura. Depois de um `read()`, a posição está no fim do
arquivo, e um segundo `read()` devolve `""` (texto vazio). Os exercícios leem cada arquivo uma vez
só.
