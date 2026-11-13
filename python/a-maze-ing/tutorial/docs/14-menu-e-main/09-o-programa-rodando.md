---
sidebar_position: 10
title: O programa rodando
---

# O programa rodando

Com o `a_maze_ing.py` completo ([página anterior](./06-saidas-e-erros-inesperados.md)), o
programa inteiro funciona. Várias páginas desta parte e da [parte 13](../13-tela/06-as-linhas-de-texto.md)
mostraram comandos que só podiam rodar agora. Esta página roda cada um deles e mostra a saída.

Todos os comandos rodam na raiz do projeto, com o Python do ambiente virtual:
`.venv/bin/python a_maze_ing.py <arquivo>` é o mesmo que o `python3 a_maze_ing.py config.txt` do
enunciado. Para o `config.txt`, `make run` faz o mesmo. Os arquivos que um exemplo cria são
apagados no fim do próprio exemplo; o `maze.txt`, gravado a cada execução com o `config.txt`,
fica, porque o `.gitignore` o deixa fora do repositório.

## Responder ao menu por um pipe

O `printf` escreve as respostas, e o `|` as entrega ao programa como se alguém as digitasse
([página 1](./01-o-laco-do-menu.md)). Com `2` e `4`, o programa desenha, mostra o caminho,
desenha de novo e sai; o `grep -c` conta as linhas da saída que contêm o título do menu:

```bash
printf '2\n4\n' | .venv/bin/python a_maze_ing.py config.txt | grep -c 'A-Maze-ing'
```

```text
2
```

O menu aparece duas vezes: depois do primeiro desenho e depois do desenho com o caminho.

Com uma resposta inválida, `9`, e depois `4`, as últimas linhas da saída são as da
[página 3](./02-ler-a-escolha.md). O `tail -n 7` guarda só as sete últimas linhas, e o `cat -e`
marca com `$` o fim de cada uma:

```bash
printf '9\n4\n' | .venv/bin/python a_maze_ing.py config.txt | tail -n 7 | cat -e
```

```text
=== A-Maze-ing ===$
1. Re-generate a new maze$
2. Show / Hide the shortest path$
3. Rotate the wall colours$
4. Quit$
Choice? (1-4): Invalid choice$
Choice? (1-4): 
```

A última linha não tem `$`: a resposta `4` sai sem imprimir a quebra de linha.

## O aviso do "42"

O `pequeno.txt` descreve um labirinto 5x5, pequeno demais para o "42"
([página 4](./03-mostrar-o-labirinto.md)). O `> /dev/null` descarta a saída normal, e só a saída
de erros aparece:

```bash
printf 'WIDTH=5\nHEIGHT=5\nENTRY=0,0\nEXIT=4,4\nOUTPUT_FILE=pequeno_maze.txt\nPERFECT=False\n' > pequeno.txt
printf '2\n4\n' | .venv/bin/python a_maze_ing.py pequeno.txt > /dev/null
echo "exit=$?"
rm pequeno.txt pequeno_maze.txt
```

```text
Error: maze too small for the "42" pattern
Error: maze too small for the "42" pattern
exit=0
```

Um aviso por desenho, e o código continua 0: o labirinto sem o "42" é válido.

## A linha de comando

Sem argumento e com argumentos demais ([página 5](./04-o-composition-root.md)):

```bash
.venv/bin/python a_maze_ing.py; echo "exit=$?"
.venv/bin/python a_maze_ing.py config.txt outro.txt; echo "exit=$?"
```

```text
Usage: python3 a_maze_ing.py <config_file>
exit=1
Usage: python3 a_maze_ing.py <config_file>
exit=1
```

## Os erros conhecidos

Um arquivo de configuração que não existe ([página 7](./05-a-barreira-de-erros.md)):

```bash
.venv/bin/python a_maze_ing.py nao_existe.txt; echo "exit=$?"
```

```text
Error: configuration file not found: nao_existe.txt
exit=1
```

Um arquivo de saída que não pode ser gravado ([página 8](./10-so-o-main-trata.md)). Os comandos
criam a pasta `trancado/` sem permissão de escrita e uma cópia do `config.txt` com
`OUTPUT_FILE=trancado/maze.txt`, rodam o programa e apagam tudo. O `sed` (um programa de
terminal que edita texto linha a linha) copia o `config.txt` trocando a linha que começa com
`OUTPUT_FILE=`:

- a instrução `s|A|B|` quer dizer "substitua o texto A pelo texto B" em cada linha. Aqui A é
  `^OUTPUT_FILE=.*` e B é `OUTPUT_FILE=trancado/maze.txt`;
- o `^` marca o começo da linha, e o `.*` quer dizer "qualquer coisa até o fim dela": A pega a
  linha `OUTPUT_FILE=` inteira, seja qual for o valor;
- o separador mais comum é a barra (`s/A/B/`), mas qualquer caractere serve. Aqui é a barra
  vertical `|`, porque o texto B já tem uma barra (`trancado/maze.txt`), que o `sed` confundiria
  com o separador;
- o `>` grava o resultado em `trancado_config.txt`; o `config.txt` não muda.

```bash
mkdir trancado
chmod 555 trancado
sed 's|^OUTPUT_FILE=.*|OUTPUT_FILE=trancado/maze.txt|' config.txt > trancado_config.txt
printf '4\n' | .venv/bin/python a_maze_ing.py trancado_config.txt; echo "exit=$?"
chmod 755 trancado
rm -r trancado trancado_config.txt
```

```text
Error: cannot write output file 'trancado/maze.txt': Permission denied
exit=1
```

Aqui a falha acontece já na primeira geração, antes do primeiro desenho; numa regeneração pela
opção `1`, a mensagem e o código seriam os mesmos.

## O desenho num arquivo

O comando da [parte 13](../13-tela/06-as-linhas-de-texto.md): o `>` manda o desenho e o menu
para um arquivo, com as sequências de cor junto. `cat desenho_terminal.txt` mostra o desenho
colorido, igual ao do terminal; aqui o `tail -n 6` mostra só o fim do arquivo:

```bash
printf '4\n' | .venv/bin/python a_maze_ing.py config.txt > desenho_terminal.txt
tail -n 6 desenho_terminal.txt | cat -e
rm desenho_terminal.txt
```

```text
=== A-Maze-ing ===$
1. Re-generate a new maze$
2. Show / Hide the shortest path$
3. Rotate the wall colours$
4. Quit$
Choice? (1-4): 
```
