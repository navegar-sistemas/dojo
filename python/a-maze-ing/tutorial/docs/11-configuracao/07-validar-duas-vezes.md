---
sidebar_position: 5
title: Validar duas vezes
---

# Validar duas vezes

O `MazeGenerator`, a classe do `mazegen` que gera o labirinto, já confere várias regras quando é
criado. O `MazeConfig` confere as mesmas regras de novo, antes de criar o gerador. Esta página
explica por que essa repetição existe, mostra o fim do `create` e reúne todas as mensagens de
erro que ele pode dar.

## As duas mensagens para o mesmo erro

O `MazeGenerator` ([parte 9](../09-gerador/02-validar-os-parametros.md)) confere, quando é
criado, o tamanho, as coordenadas, a entrada diferente da saída, o espaço para o Pac-Man e o
"42". Conferir de novo no `MazeConfig` parece repetição, mas as mensagens são diferentes. O
gerador, com a entrada em cima do "42" (na raiz do projeto):

```bash
.venv/bin/python -c '
from mazegen import MazeError, MazeGenerator

try:
    MazeGenerator(20, 15, entry=(6, 5))
except MazeError as error:
    print(error)
'
```

```text
entry (6, 5) lies on the "42" pattern
```

O `MazeConfig`, com o mesmo erro (`ENTRY=6,5` no dicionário), dá esta mensagem; o
[Experimente da próxima página](./08-o-maze-config-completo.md#experimente) a mostra saindo de
verdade:

```text
ENTRY=6,5 lies on the "42" pattern
```

O gerador é uma biblioteca: fala dos **parâmetros** dele, como `entry`, em minúsculas. Quem
escreveu o arquivo de configuração nunca viu esse parâmetro; viu a linha `ENTRY=6,5`. Conferindo
antes de criar o gerador, a mensagem cita a chave como está no arquivo, com o valor escrito do
mesmo jeito (`6,5`, e não `(6, 5)`).

A validação do gerador continua lá, porque outro programa pode usar o `mazegen` sem arquivo de
configuração nenhum. No A-Maze-ing ela nunca dispara: o `MazeConfig` barra antes.

## O objeto pronto

```python
return cls(width, height, entry, exit, output_file, perfect, seed)
```

Chegando aqui, todas as regras passaram. `cls(...)` chama o construtor do `MazeConfig` com os
valores já convertidos.

Chaves que não são obrigatórias nem `SEED` nunca são lidas pelo `create`, e por isso são
ignoradas sem código nenhum: um dicionário com `"COLOR": "red"` a mais dá o mesmo `MazeConfig`
que sem ela. O enunciado permite acrescentar chaves; ignorar as desconhecidas é escolha do
projeto.

## Todas as mensagens

| Regra | Mensagem |
|---|---|
| 1 | `missing mandatory key(s): WIDTH, HEIGHT` |
| 2 | `WIDTH must be an integer, got 'abc'` |
| 2 | `WIDTH has more than 18 digits` |
| 2 | `ENTRY must be 'x,y' with integers, got '0;0'` |
| 2 | `OUTPUT_FILE must not be empty` |
| 2 | `PERFECT must be True or False, got 'yes'` |
| 2 | `SEED must be an integer, got '4.2'` |
| 3 | `WIDTH must be between 1 and 100, got 0` |
| 4 | `ENTRY=20,0 is outside the maze (x in 0..19, y in 0..14)` |
| 5 | `ENTRY and EXIT must differ` |
| 6 | `PERFECT=False needs (WIDTH - 1) x (HEIGHT - 1) >= 2 for a Pac-Man board, got 1x10` |
| 7 | `ENTRY=6,5 lies on the "42" pattern` |

Nenhuma cita o nome do arquivo: o `MazeConfig` não sabe de onde vieram os textos. Quem acrescenta
`config.txt: ` na frente é o repositório, no [fim desta parte](./09-o-repositorio-completo.md).
