---
sidebar_position: 7
title: Abrindo o arquivo de configuração
---

# Abrindo o arquivo de configuração

O programa recebe na linha de comando o caminho do arquivo de configuração (o `config.txt` de
`python3 a_maze_ing.py config.txt`) e precisa ler as linhas dele. O arquivo pode ter sido salvo
por qualquer editor, no Linux, no macOS ou no Windows, e cada um grava o texto de um jeito um
pouco diferente. Esta página abre o arquivo e lê as linhas de modo que todos esses jeitos
funcionem.

## O `FileConfigRepository`

Quem lê o arquivo é o `FileConfigRepository` (`amazeing/repositories/config_repository.py`),
a única classe que abre o arquivo de configuração
([página 1](./01-o-value-object-maze-config.md)). O único método dele, `load(path)`, recebe o
caminho digitado e devolve um `MazeConfig`, em três passos:

1. abrir o arquivo e ler as linhas (esta página), transformando cada falha numa mensagem
   ([próxima página](./10-as-falhas-da-leitura.md));
2. separar cada linha em chave e valor ([página 9](./06-linha-a-linha.md));
3. entregar o dicionário ao `MazeConfig.create`, que converte e valida.

## Abrir e ler

```python
with open(path, encoding="utf-8-sig") as file:
    lines = file.readlines()
```

- `with open(...) as file` abre o arquivo e o fecha sozinho ao sair do bloco, mesmo que dê erro
  no meio. O enunciado pede `with` para arquivos.
- `readlines()` devolve a lista das linhas, cada uma ainda com a quebra de linha `\n` no fim.

### O `encoding`

Um arquivo guarda **bytes**, números de 0 a 255. A **codificação** (*encoding*) é a tabela que
diz que bytes formam cada letra. Letras sem acento têm o mesmo byte em quase todas as tabelas,
mas as acentuadas, não: o `é` é um byte (`e9`) no Latin-1, uma tabela antiga, e dois bytes
(`c3 a9`) no **UTF-8**, a tabela mais usada hoje. Lido com a tabela errada, `café` vira `cafÃ©`.

Sem `encoding`, o Python usa a tabela padrão do computador, que muda de um sistema para outro.
Por isso o projeto sempre diz qual é: UTF-8, numa variante chamada `utf-8-sig`.

### O BOM e o `utf-8-sig`

Alguns editores de texto, como o Bloco de Notas de versões antigas do Windows, gravam no início
do arquivo um caractere invisível, o **BOM** (*byte order mark*, "marca de ordem dos bytes"):
três bytes que dizem "este arquivo é UTF-8". Lido com `utf-8` comum, ele vira parte da primeira
linha:

```bash
printf '\xef\xbb\xbf# Width\nWIDTH=20\n' > exemplo_bom.txt
.venv/bin/python -c '
with open("exemplo_bom.txt", encoding="utf-8") as f:
    print(f.readlines())
with open("exemplo_bom.txt", encoding="utf-8-sig") as f:
    print(f.readlines())
'
rm exemplo_bom.txt
```

```text
['\ufeff# Width\n', 'WIDTH=20\n']
['# Width\n', 'WIDTH=20\n']
```

(O `printf` grava os bytes do BOM, `ef bb bf`, seguidos de duas linhas; o `rm` apaga o arquivo
no fim. No Python, o BOM aparece como `\ufeff`.)

Com `utf-8`, a primeira linha começa com `\ufeff`, e não com `#`: deixa de ser comentário e vira
um erro de sintaxe. Se a primeira linha fosse `WIDTH=20`, a chave lida seria `\ufeffWIDTH`, e o
programa diria que falta `WIDTH`, com a linha `WIDTH=20` bem à vista no arquivo. Tirar espaços
não adianta: para o Python, o BOM não é espaço.

`utf-8-sig` é o UTF-8 que descarta um BOM no começo, se houver. Sem BOM, lê igual ao `utf-8`.
Aceitar o BOM é escolha do projeto, para um arquivo salvo no Windows funcionar.

### Fins de linha do Windows

No Windows, o fim de uma linha é gravado com dois caracteres, `\r\n`; no Linux e no macOS, só
com `\n`. Ao ler em **modo texto** (o modo padrão do `open`), o Python reconhece `\n`, `\r\n` e
`\r` e entrega todos como `\n`:

```text
bytes no disco:   WIDTH=20\r\nHEIGHT=15\r\n
readlines():      ['WIDTH=20\n', 'HEIGHT=15\n']
```

Um arquivo salvo no Windows funciona sem tratamento nenhum.

Abrir e ler pode falhar de vários jeitos. A [próxima página](./10-as-falhas-da-leitura.md)
transforma cada falha numa mensagem.
