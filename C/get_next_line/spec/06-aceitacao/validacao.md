# Validação

Tudo roda de um diretório de trabalho `check/`, criado ao lado de `project/`;
nada é escrito dentro de `project/`. Primeiro bloco, a partir do diretório que
contém `project/`:

```bash
mkdir -p check && cd check
P=../project
CC="cc -Wall -Wextra -Werror"
```

O corpus vem de [casos.md](casos.md) (bloco "Corpus"), gerado aqui dentro de
`check/corpus/`. Os harnesses abaixo são código hospedeiro: não seguem as
[restrições de estilo](../02-restricoes/estilo.md), que valem só para os seis
arquivos do projeto.

## Harness de reconstrução

Verifica os três invariantes de
[../01-contrato/linha.md](../01-contrato/linha.md) e imprime a concatenação
dos retornos em stdout, para comparar com o arquivo original. O header é
parametrizado para servir às duas variantes.

```bash
cat > rec.c <<'EOF'
#include GNL_HEADER
#include <stdio.h>
#include <fcntl.h>

int	main(int argc, char **argv)
{
	int		fd = 0;
	char	*line;
	size_t	len, i, n = 0;

	if (argc > 1 && (fd = open(argv[1], O_RDONLY)) < 0)
		return (2);
	while ((line = get_next_line(fd)) != NULL)
	{
		n++;
		len = gnl_strlen(line);
		if (len == 0)
			return (fprintf(stderr, "vazia na chamada %zu\n", n), 3);
		for (i = 0; i + 1 < len; i++)
			if (line[i] == '\n')
				return (fprintf(stderr, "\\n interno na %zu\n", n), 4);
		fwrite(line, 1, len, stdout);
		free(line);
	}
	if (get_next_line(fd) != NULL)
		return (fprintf(stderr, "nao-NULL depois do fim\n"), 5);
	fprintf(stderr, "lines=%zu\n", n);
	return (0);
}
EOF
```

## Estado limpo e matriz completa

Compila e roda as duas variantes contra o corpus inteiro, em todos os
`BUFFER_SIZE` do contrato. Nenhuma linha `FALHOU` pode aparecer.

```bash
for BS in DEFAULT 1 2 5 42 43 9999 1048576 10000000; do
  [ $BS = DEFAULT ] && D="" || D="-D BUFFER_SIZE=$BS"
  $CC $D -DGNL_HEADER='"get_next_line.h"' -I$P rec.c \
      $P/get_next_line.c $P/get_next_line_utils.c -o rec_m || echo "FALHOU compilar m $BS"
  $CC $D -DGNL_HEADER='"get_next_line_bonus.h"' -I$P rec.c \
      $P/get_next_line_bonus.c $P/get_next_line_utils_bonus.c -o rec_b || echo "FALHOU compilar b $BS"
  for f in corpus/*.txt; do
    case "$BS/$f" in 1/*07_long*|2/*07_long*) continue ;; esac
    for v in m b; do
      ./rec_$v "$f" > out 2>/dev/null && cmp -s out "$f" || echo "FALHOU $v $BS $f"
    done
  done
  ./rec_m < corpus/04_multi.txt > out 2>/dev/null
  cmp -s out corpus/04_multi.txt || echo "FALHOU stdin $BS"
  echo "BS=$BS ok"
done
```

`BUFFER_SIZE=0` compila e devolve só `NULL`:

```bash
$CC -D BUFFER_SIZE=0 -DGNL_HEADER='"get_next_line.h"' -I$P rec.c \
    $P/get_next_line.c $P/get_next_line_utils.c -o rec0
./rec0 corpus/03_one_line.txt          # stderr: lines=0
```

## Sequências canônicas

```bash
cat > seq.c <<'EOF'
#include GNL_HEADER
#include <stdio.h>
#include <fcntl.h>

int	main(int argc, char **argv)
{
	int		fd, i, calls;
	char	*line, *p;

	fd = open(argv[1], O_RDONLY);
	calls = atoi(argv[2]);
	(void)argc;
	for (i = 1; i <= calls; i++)
	{
		line = get_next_line(fd);
		printf("chamada %d -> ", i);
		if (!line)
			printf("NULL\n");
		else
		{
			printf("\"");
			for (p = line; *p; p++)
				if (*p == '\n')
					printf("\\n");
				else if (*p == '\r')
					printf("\\r");
				else
					putchar(*p);
			printf("\"\n");
		}
		free(line);
	}
	return (0);
}
EOF
$CC -D BUFFER_SIZE=42 -DGNL_HEADER='"get_next_line.h"' -I$P seq.c \
    $P/get_next_line.c $P/get_next_line_utils.c -o seq42
$CC -D BUFFER_SIZE=1 -DGNL_HEADER='"get_next_line.h"' -I$P seq.c \
    $P/get_next_line.c $P/get_next_line_utils.c -o seq1

diff <(./seq42 corpus/04_multi.txt 5) - <<'EOF' && echo "04 ok"
chamada 1 -> "a\n"
chamada 2 -> "\n"
chamada 3 -> "bb\n"
chamada 4 -> NULL
chamada 5 -> NULL
EOF
diff <(./seq42 corpus/02_no_nl.txt 2) - <<'EOF' && echo "02 ok"
chamada 1 -> "abc"
chamada 2 -> NULL
EOF
diff <(./seq42 corpus/05_crlf.txt 3) - <<'EOF' && echo "05 ok"
chamada 1 -> "linha um\r\n"
chamada 2 -> "linha dois\r\n"
chamada 3 -> NULL
EOF
diff <(./seq1 corpus/04_multi.txt 5) <(./seq42 corpus/04_multi.txt 5) && echo "B=1 identico"
```

## Bordas de fd

```bash
cat > edge.c <<'EOF'
#include GNL_HEADER
#include <stdio.h>
#include <fcntl.h>

int	g_bad = 0;

void	nul(const char *what, char *got)
{
	if (got != NULL)
	{
		printf("FALHOU %s\n", what);
		g_bad = 1;
	}
	free(got);
}

int	main(void)
{
	int		fd;
	char	*line;

	nul("fd -1", get_next_line(-1));
	nul("fd 999", get_next_line(999));
	fd = open("corpus/03_one_line.txt", O_RDONLY);
	close(fd);
	nul("fd fechado", get_next_line(fd));
	fd = open(".", O_RDONLY);
	nul("diretorio", get_next_line(fd));
	close(fd);
	fd = open("/dev/null", O_RDONLY);
	nul("/dev/null", get_next_line(fd));
	close(fd);
	fd = open("corpus/02_no_nl.txt", O_RDONLY);
	line = get_next_line(fd);
	if (!line || gnl_strlen(line) != 3)
	{
		printf("FALHOU sem quebra final\n");
		g_bad = 1;
	}
	free(line);
	nul("depois da ultima", get_next_line(fd));
	nul("de novo", get_next_line(fd));
	close(fd);
	if (!g_bad)
		printf("bordas ok\n");
	return (g_bad);
}
EOF
$CC -DGNL_HEADER='"get_next_line.h"' -I$P edge.c \
    $P/get_next_line.c $P/get_next_line_utils.c -o edge && ./edge
$CC -DGNL_HEADER='"get_next_line_bonus.h"' -I$P edge.c \
    $P/get_next_line_bonus.c $P/get_next_line_utils_bonus.c -o edge && ./edge
```

## Memória

Consumo total: zero em uso na saída, zero erro. Fd fechado com resto pendente
(`10_tail.txt`): o resto é liberado no caminho de erro.

```bash
$CC -D BUFFER_SIZE=42 -DGNL_HEADER='"get_next_line.h"' -I$P rec.c \
    $P/get_next_line.c $P/get_next_line_utils.c -o rec_m
valgrind --leak-check=full --show-leak-kinds=all ./rec_m corpus/04_multi.txt > /dev/null
valgrind --leak-check=full --show-leak-kinds=all ./rec_m corpus/09_mixed.txt > /dev/null
valgrind --leak-check=full --show-leak-kinds=all ./edge > /dev/null

cat > tail_err.c <<'EOF'
#include GNL_HEADER
#include <stdio.h>
#include <fcntl.h>

int	main(void)
{
	int		fd;
	char	*line;

	fd = open("corpus/10_tail.txt", O_RDONLY);
	line = get_next_line(fd);
	printf("1a: %s", line);
	free(line);
	close(fd);
	line = get_next_line(fd);
	printf("2a: %s\n", line ? line : "NULL");
	free(line);
	return (0);
}
EOF
$CC -D BUFFER_SIZE=42 -DGNL_HEADER='"get_next_line.h"' -I$P tail_err.c \
    $P/get_next_line.c $P/get_next_line_utils.c -o tail_err
valgrind --leak-check=full --show-leak-kinds=all ./tail_err
```

Gabarito dos quatro: `in use at exit: 0 bytes` e `ERROR SUMMARY: 0 errors`.
Se um programa sair **sem** consumir o fd até `NULL`, o resto aparece como
`still reachable` (nunca `definitely lost`) — comportamento documentado em
[../03-arquitetura/fluxo.md](../03-arquitetura/fluxo.md).

## Leitura mínima

Interpõe um contador no lugar de `read` via `-Dread=`; o resto do projeto
compila intacto. Gabarito das contagens em
[../04-algoritmo/leitura.md](../04-algoritmo/leitura.md).

```bash
cat > cnt.c <<'EOF'
#define _GNU_SOURCE
#include <stdio.h>
#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/syscall.h>

long	g_reads = 0;

ssize_t	counting_read(int fd, void *buf, size_t n)
{
	g_reads++;
	return (syscall(SYS_read, fd, buf, n));
}

char	*get_next_line(int fd);

int	main(int argc, char **argv)
{
	int		fd, max = -1, i = 0;
	char	*line;

	fd = open(argv[1], O_RDONLY);
	if (argc > 2)
		max = atoi(argv[2]);
	while ((line = get_next_line(fd)) != NULL && (max < 0 || ++i < max))
		free(line);
	free(line);
	printf("reads=%ld\n", g_reads);
	return (0);
}
EOF
$CC -D BUFFER_SIZE=42 -Dread=counting_read -c $P/get_next_line.c -o gnl_c.o -I$P
$CC -D BUFFER_SIZE=42 -c $P/get_next_line_utils.c -o utl_c.o -I$P
$CC cnt.c gnl_c.o utl_c.o -o cnt42
./cnt42 corpus/08_many_lines.txt        # reads=1285  (⌈53893/42⌉ + 1: termina em \n)
./cnt42 corpus/06_boundary.txt          # reads=6     (⌈128/42⌉ + 2: fim sem \n é visto duas vezes)
./cnt42 corpus/04_multi.txt 1           # reads=1     (para no primeiro \n; nada além do necessário)
```

## Bônus

Intercalação round-robin com reconstrução por fd, e a guarda de `FD_MAX`.

```bash
cat > il.c <<'EOF'
#include GNL_HEADER
#include <stdio.h>
#include <string.h>
#include <fcntl.h>

int	main(int argc, char **argv)
{
	static char	acc[16][1 << 20];
	static int	fd[16], len[16], done[16];
	int			i, active = argc - 1;
	char		*line;
	FILE		*f;

	for (i = 0; i < argc - 1; i++)
		if ((fd[i] = open(argv[i + 1], O_RDONLY)) < 0)
			return (2);
	while (active > 0)
		for (i = 0; i < argc - 1; i++)
		{
			if (done[i])
				continue ;
			line = get_next_line(fd[i]);
			if (!line)
			{
				done[i] = 1;
				active--;
				continue ;
			}
			len[i] += sprintf(acc[i] + len[i], "%s", line);
			free(line);
		}
	for (i = 0; i < argc - 1; i++)
	{
		char	ref[1 << 20];
		int		n;

		f = fopen(argv[i + 1], "rb");
		n = fread(ref, 1, sizeof(ref), f);
		fclose(f);
		if (n != len[i] || memcmp(ref, acc[i], n))
			return (printf("FALHOU %s\n", argv[i + 1]), 1);
	}
	printf("intercalado ok (%d fds)\n", argc - 1);
	return (0);
}
EOF
for BS in 1 42; do
  $CC -D BUFFER_SIZE=$BS -DGNL_HEADER='"get_next_line_bonus.h"' -I$P il.c \
      $P/get_next_line_bonus.c $P/get_next_line_utils_bonus.c -o il
  ./il corpus/03_one_line.txt corpus/04_multi.txt corpus/06_boundary.txt
  ./il corpus/0[1-6]*.txt corpus/08_many_lines.txt corpus/09_mixed.txt
done
valgrind --leak-check=full --show-leak-kinds=all \
  ./il corpus/03_one_line.txt corpus/04_multi.txt corpus/06_boundary.txt

cat > fdmax.c <<'EOF'
#include GNL_HEADER
#include <stdio.h>
#include <fcntl.h>

int	main(void)
{
	int		a = open("corpus/03_one_line.txt", O_RDONLY);
	int		b = open("corpus/04_multi.txt", O_RDONLY);
	char	*la = get_next_line(a);
	char	*lb = get_next_line(b);

	printf("fd %d dentro:  %s", a, la ? la : "NULL\n");
	printf("fd %d barrado: %s\n", b, lb ? "FALHOU" : "NULL ok");
	free(la);
	free(lb);
	return (lb != NULL || la == NULL);
}
EOF
$CC -D FD_MAX=4 -DGNL_HEADER='"get_next_line_bonus.h"' -I$P fdmax.c \
    $P/get_next_line_bonus.c $P/get_next_line_utils_bonus.c -o fdmax
./fdmax     # fd 3 lê; fd 4 (>= FD_MAX) devolve NULL sem tocar em nada
```

## Pior caso cronometrado

```bash
$CC -D BUFFER_SIZE=1 -DGNL_HEADER='"get_next_line.h"' -I$P rec.c \
    $P/get_next_line.c $P/get_next_line_utils.c -o rec1
time ./rec1 corpus/07_long_line.txt > out && cmp out corpus/07_long_line.txt
```

Esperado: correto, em torno de 8 s (quadrático documentado em
[../04-algoritmo/leitura.md](../04-algoritmo/leitura.md)); o mesmo arquivo com
B = 42 é instantâneo.

## Sanitizers (opcional, além do contrato)

```bash
gcc -fsanitize=address,undefined -Wall -Wextra -Werror -D BUFFER_SIZE=5 \
    -DGNL_HEADER='"get_next_line.h"' -I$P rec.c \
    $P/get_next_line.c $P/get_next_line_utils.c -o rec_asan
./rec_asan corpus/09_mixed.txt > out && cmp out corpus/09_mixed.txt && echo "asan ok"
```
