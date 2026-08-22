# Casos de aceitação

Corpus determinístico + resultados exatos. Os comandos de execução estão em
[validacao.md](validacao.md); as tabelas canônicas dos casos pequenos, em
[../01-contrato/linha.md](../01-contrato/linha.md).

## Corpus

Gerado assim, num diretório `corpus/`:

```bash
mkdir -p corpus && cd corpus
: > 00_empty.txt
printf '\n'                          > 01_nl.txt
printf 'abc'                         > 02_no_nl.txt
printf 'abc\n'                       > 03_one_line.txt
printf 'a\n\nbb\n'                   > 04_multi.txt
printf 'linha um\r\nlinha dois\r\n'  > 05_crlf.txt
{ python3 -c "print('x'*42); print('y'*41); import sys; sys.stdout.write('z'*43)"; } > 06_boundary.txt
{ python3 -c "print('A'*65536); print('fim')"; } > 07_long_line.txt
seq 1 5000 | awk '{print "linha", $1}' > 08_many_lines.txt
python3 -c "
import random
random.seed(42)
out = []
for i in range(6000):
    n = random.randint(0, 300)
    out.append(''.join(random.choice('abcdefghij KLMNOP.,;-') for _ in range(n)))
open('09_mixed.txt', 'w').write('\n'.join(out) + 'sem quebra final')
"
printf 'aaa\nbbb'                    > 10_tail.txt
cd ..
```

| Arquivo | Bytes | O que exercita | Linhas |
|---|---|---|---|
| `00_empty.txt` | 0 | primeiro `NULL` imediato | 0 |
| `01_nl.txt` | 1 | linha que é só `"\n"` | 1 |
| `02_no_nl.txt` | 3 | última linha sem `\n` | 1 |
| `03_one_line.txt` | 4 | caso mínimo completo | 1 |
| `04_multi.txt` | 6 | linha vazia no meio | 3 |
| `05_crlf.txt` | 22 | `\r` não é terminador | 2 |
| `06_boundary.txt` | 128 | linhas de 42, 41 e 43 bytes úteis — as bordas do B padrão | 3 |
| `07_long_line.txt` | 65 541 | linha ≫ B; pior caso quadrático com B = 1 | 2 |
| `08_many_lines.txt` | 53 893 | volume de linhas curtas; contagem de `read`s | 5000 |
| `09_mixed.txt` | 922 259 | comprimentos 0–300 pseudo-aleatórios, fim sem `\n` | 6000 |
| `10_tail.txt` | 7 | resto sem `\n` pendente no stash + erro de leitura | 2 |

"Linhas" é o que o harness reporta (`lines=N`) após consumir o arquivo; a
concatenação dos retornos reproduz cada arquivo byte a byte.

## Matriz de `BUFFER_SIZE`

A mesma bateria roda com `-D BUFFER_SIZE=` **1, 2, 5, 42, 43, 9999, 1048576,
10000000 e sem a flag** (default 42) — obrigatório e bônus. Saídas idênticas
em todas as células. Única exceção de execução: `07_long_line.txt` fica fora
das células B = 1 e B = 2 do laço geral e roda uma vez à parte, cronometrado
(≈ 8 s em B = 1 — quadrático esperado, ver
[../04-algoritmo/leitura.md](../04-algoritmo/leitura.md)).

Com `-D BUFFER_SIZE=0`, toda chamada devolve `NULL` (guarda de entrada):
compila e o harness reporta `lines=0` com saída vazia.

## Borda de buffer (B = 42, `06_boundary.txt`)

| chamada | retorno |
|---|---|
| 1 | `"x…x\n"` — 42 `x` + `\n` (43 bytes: um além do primeiro `read`) |
| 2 | `"y…y\n"` — 41 `y` + `\n` (exatamente um `read` completa) |
| 3 | `"z…z"` — 43 `z`, sem `\n` (fim de arquivo no meio da linha) |
| 4 | `NULL` |

## Bordas de fd e de estado

| Caso | Retorno esperado |
|---|---|
| `fd = -1` | `NULL` |
| fd nunca aberto (999) | `NULL` |
| fd aberto e já fechado, stash vazio | `NULL` |
| fd de diretório (`open(".", O_RDONLY)`) | `NULL` (o `read` falha) |
| `/dev/null` | `NULL` na primeira chamada |
| fd aberto só para escrita | `NULL` |
| chamadas repetidas após o fim | `NULL` sempre, sem crash |
| `10_tail.txt`: 1ª linha lida, fd fechado, nova chamada | `NULL`, e o resto `"bbb"` pendente é liberado (valgrind zerado) |
| leitura de `stdin` via pipe | mesmas sequências dos arquivos |

## Intercalação (bônus)

Round-robin entre `03_one_line.txt`, `04_multi.txt` e `06_boundary.txt`
abertos ao mesmo tempo (fds 3, 4, 5):

```
gnl(3) → "abc\n"      gnl(4) → "a\n"     gnl(5) → "x…x\n"
gnl(3) → NULL         gnl(4) → "\n"      gnl(5) → "y…y\n"
                      gnl(4) → "bb\n"    gnl(5) → "z…z"
                      gnl(4) → NULL      gnl(5) → NULL
```

A aceitação verifica a reconstrução byte a byte por fd, com 3 e com 8
arquivos, em B = 1 e B = 42, e a guarda `-D FD_MAX=4` (fd 4 devolve `NULL`
direto).
