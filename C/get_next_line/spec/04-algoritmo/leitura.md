# O algoritmo

As três fases, na granularidade em que quebram ou passam. `B` é
`BUFFER_SIZE`.

## Fase 1 — encher o stash

```
gnl_read_loop(fd, stash):
    buf = malloc(B + 1)                      # cast para size_t antes do + 1
    n = 1
    enquanto buf != NULL e n > 0 e stash não contém '\n':
        n = read(fd, buf, B)
        se n <= 0: interrompe
        buf[n] = '\0'
        stash = gnl_strjoin_free(stash, buf)
        se stash == NULL: interrompe         # malloc da junção falhou
    se buf == NULL ou n < 0:                 # falha de alocação ou de leitura
        free(stash)
        stash = NULL
    free(buf)
    devolve stash
```

## Fase 2 — extrair a linha

```
gnl_extract_line(stash):                     # pré: stash != NULL e != ""
    len = 0
    enquanto stash[len] != '\0' e stash[len] != '\n':
        len += 1
    se stash[len] == '\n':
        len += 1                             # o '\n' entra na linha
    devolve gnl_substr(stash, 0, len)
```

## Fase 3 — podar o stash

```
gnl_trim_stash(stash):
    nl = gnl_strchr(stash, '\n')
    se nl == NULL ou nl[1] == '\0':          # sem resto: fim da linha era o fim do stash
        free(stash)
        devolve NULL
    resto = gnl_substr(nl + 1, 0, gnl_strlen(nl + 1))
    free(stash)
    devolve resto
```

## Detalhes que quebram se forem trocados

**A condição do laço testa o `\n` antes do primeiro `read`.** Invertido,
lê-se além do necessário: o custo em `read`s muda, o caso "fd fechado com
linha bufferizada" passa a devolver `NULL` cedo demais, e o bônus intercalado
rouba bytes do momento errado.

**`n <= 0` interrompe antes de `buf[n] = '\0'` e da junção.** Com `n < 0`,
`buf[n]` seria escrita fora do buffer; com `n == 0`, a junção criaria o stash
`""` que o invariante de [../03-arquitetura/fluxo.md](../03-arquitetura/fluxo.md)
proíbe — o sintoma seria a função devolvendo string vazia no fim de arquivo
que termina em `\n`.

**`buf[n] = '\0'` depois de cada `read`.** A junção trata `buf` como string;
sem o terminador, bytes da leitura anterior (ou lixo) entram na linha. O
sintoma clássico aparece só com B pequeno e linhas maiores que B —
exatamente o que a matriz de aceitação varre.

**A junção libera o antigo, e o laço para se ela falhar.** Continuar com
stash `NULL` depois de uma falha de `malloc` "recomeçaria" a linha do zero e
devolveria um fragmento silenciosamente corrompido em vez de `NULL`.

**A limpeza final testa `buf == NULL` *ou* `n < 0`.** São os dois caminhos que
prometem "estado zerado no erro": esquecer o primeiro vaza o stash quando o
`malloc` do buffer falha; esquecer o segundo vaza o resto pendente quando o
fd morre no meio de um arquivo (o caso valgrind do fd fechado em
[../06-aceitacao/validacao.md](../06-aceitacao/validacao.md)).

**`len++` quando parou em `\n`** (fase 2). Sem ele, a linha sai sem o
terminador e a concatenação dos retornos diverge do arquivo — o invariante 3
de [../01-contrato/linha.md](../01-contrato/linha.md) acusa na hora.

**`nl[1] == '\0'` devolve `NULL`, não `""`** (fase 3). Ver o invariante de
repouso: guardar `""` faz a chamada seguinte devolver string vazia.

**`stash = gnl_read_loop(...)` antes do teste de `NULL`** (orquestração). A
estática precisa receber o resultado mesmo quando ele é `NULL` — senão ela
aponta para memória já liberada e a chamada seguinte faz double free.

## Custos

**Chamadas a `read`** (medidas, B = 42). Consumir um arquivo até o `NULL`
custa `⌈tamanho/B⌉` leituras de dados mais as leituras vazias que enxergam o
fim: **uma** se o arquivo termina em `\n` ou é vazio (53 893 bytes → 1284 + 1
= 1285), **duas** se não termina (o fim fecha a última linha e é visto de novo
na chamada que devolve `NULL`; 128 bytes sem `\n` final → 4 + 2 = 6). Cada
byte é lido do kernel uma única vez, qualquer que seja B; uma linha já
bufferizada custa 0.

**Cópias.** Cada junção recopia o stash corrente: uma linha de tamanho L
custa ≈ `L²/2B` cópias de byte. Medido no pior caso da suíte — linha única
de 65 536 bytes, B = 1: **≈ 8 s**; mesmo arquivo com B = 42: instantâneo
(≈ L²/84 cópias); B = 10 000 000: uma leitura, uma junção.

**Alocações por chamada:** O(1) — o buffer, uma junção por `read` efetuado, a
linha extraída e o resto podado. Consumir um arquivo inteiro é O(nº de
`read`s + nº de linhas) alocações no total.

**Memória de pico:** stash + buffer + linha ≈ `2·(maior linha) + B` bytes.
