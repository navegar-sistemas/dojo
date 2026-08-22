*This project has been created as part of the 42 curriculum by macoelho.*

# get_next_line

## Description

`get_next_line` é uma função C que devolve, a cada chamada, a próxima linha
lida de um descritor de arquivo:

```c
char	*get_next_line(int fd);
```

Chamadas sucessivas percorrem o arquivo (ou `stdin`, ou um pipe) uma linha por
vez. A linha devolvida **inclui** o `\n` final — exceto a última linha de um
arquivo que não termina em `\n`. Quando não há mais nada para ler, ou em caso
de erro, a função devolve `NULL`. O tamanho do buffer de leitura é fixado em
tempo de compilação via `-D BUFFER_SIZE=n` (padrão: 42), e a função se comporta
de forma idêntica para qualquer valor de `n ≥ 1`.

O estado entre chamadas vive numa única variável estática — nenhuma variável
global, nenhum `lseek`: só `read`, `malloc` e `free`.

A parte bônus (`*_bonus.{c,h}`) gerencia **múltiplos descritores ao mesmo
tempo**: é possível intercalar leituras dos fds 3, 4 e 5 sem que uma linha de
um vaze para o outro, mantendo uma única variável estática (um array indexado
pelo fd, limitado por `FD_MAX`, padrão 1024).

## Instructions

Não há Makefile: os arquivos são compilados junto com o programa que usa a
função.

```sh
cc -Wall -Wextra -Werror -D BUFFER_SIZE=42 \
   get_next_line.c get_next_line_utils.c seu_main.c

# bônus (multi-fd); sem -D BUFFER_SIZE vale o padrão 42
cc -Wall -Wextra -Werror \
   get_next_line_bonus.c get_next_line_utils_bonus.c seu_main.c
```

Uso típico:

```c
int		fd = open("arquivo.txt", O_RDONLY);
char	*line;

while ((line = get_next_line(fd)) != NULL)
{
	printf("%s", line);
	free(line);
}
close(fd);
```

## Algoritmo e justificativa

O estado entre chamadas é um **stash**: uma string alocada na heap, apontada
pela variável estática, com tudo o que já foi lido do fd mas ainda não foi
devolvido. Cada chamada faz três passos:

1. **Ler até ter uma linha** (`gnl_read_loop`) — enquanto o stash não contém
   `\n` e o `read` devolve dados, lê `BUFFER_SIZE` bytes e concatena no stash.
   A checagem do `\n` acontece **antes** de cada `read`: se a linha já está
   bufferizada de uma chamada anterior, nada é lido — a função consome do fd o
   mínimo necessário (medido: `⌈tamanho/BUFFER_SIZE⌉` chamadas a `read` de
   dados para consumir um arquivo inteiro — cada byte lido uma única vez —
   e zero leituras quando a linha já está no stash).
2. **Extrair a linha** (`gnl_extract_line`) — copia do início do stash até o
   primeiro `\n` (incluído), ou até o fim se não houver `\n` (fim de arquivo
   sem quebra final).
3. **Podar o stash** (`gnl_trim_stash`) — o que sobra depois do `\n` vira o
   novo stash; se não sobra nada, o stash é liberado e volta a `NULL`.

**Por que um stash único, e não uma lista de buffers?** Robustez e
verificabilidade: com uma única string sempre terminada em `\0`, os invariantes
são triviais ("o stash nunca é a string vazia", "só há `\n` pendente se ainda
não extraído") e todos os caminhos de erro — `read` negativo, `malloc` falho —
convergem para "libera o stash, devolve `NULL`, estado zerado". O preço é
tempo quadrático na concatenação quando `BUFFER_SIZE` é muito menor que a
linha (custo ≈ L²/2B cópias por linha de tamanho L); para os regimes de uso
reais (linhas de até alguns KB) isso é irrelevante, e a corretude não depende
do valor: a suíte cobre `BUFFER_SIZE` de 1 a 10 000 000 com saída idêntica.

Erros e memória: `read < 0` ou `malloc` falho liberam o stash pendente antes
de devolver `NULL` (valgrind: 0 bytes em uso na saída após consumir um arquivo
até o fim; sem vazamento em nenhum caminho de erro). Descritor inválido,
`BUFFER_SIZE ≤ 0` ou (no bônus) `fd ≥ FD_MAX` devolvem `NULL` sem tocar em
nada.

## Resources

- `man 2 read`, `man 3 malloc` — contratos de retorno parcial de `read` e de
  falha de alocação, que definem os dois caminhos de erro da função.
- K&R, *The C Programming Language* — duração de armazenamento estático
  (variáveis `static` locais preservadas entre chamadas).
- **Uso de IA:** assistência de IA (Claude) foi usada para gerar a suíte de
  testes (corpus determinístico, matriz de `BUFFER_SIZE`, valgrind e
  sanitizers) e para rascunhar esta documentação.
  <!-- TODO: ajustar esta seção para refletir fielmente o seu processo. -->
