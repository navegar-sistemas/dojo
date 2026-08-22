# T03 — As três fases e a função pública

## Objetivo

`get_next_line.c` completo: a parte obrigatória inteira funcionando.

## Depende de

T02.

## Arquivos

- `project/get_next_line.c`

## Especificação

- [../04-algoritmo/leitura.md](../04-algoritmo/leitura.md) — pseudocódigo e os detalhes que quebram
- [../03-arquitetura/fluxo.md](../03-arquitetura/fluxo.md) — orquestração, invariante de repouso, quem libera o quê
- [../03-arquitetura/modulos.md](../03-arquitetura/modulos.md) — contratos das quatro funções

## Implementação

Quatro funções, três `static`, corpos 22/8/12/11:

| Função | Papel |
|---|---|
| `gnl_read_loop` (static) | fase 1 — encher o stash até `\n`, fim ou erro |
| `gnl_extract_line` (static) | fase 2 — copiar a primeira linha, `\n` incluído |
| `gnl_trim_stash` (static) | fase 3 — ficar com o resto; nunca guardar `""` |
| `get_next_line` | guardas + estática + as três fases, nessa ordem |

Ordem de escrita sugerida: fase 2 e fase 3 primeiro (puras, sobre string),
depois a fase 1 (a única com I/O), a orquestração por último. Os oito
"detalhes que quebram" de
[../04-algoritmo/leitura.md](../04-algoritmo/leitura.md) são a lista de
conferência antes de rodar qualquer teste.

## Pronto quando

Do diretório `check/`, com o corpus de
[../06-aceitacao/casos.md](../06-aceitacao/casos.md) já gerado:

1. o harness `rec.c` e a **matriz completa** da parte obrigatória
   ([../06-aceitacao/validacao.md](../06-aceitacao/validacao.md), duas
   primeiras seções) — como o bônus ainda não existe, apague do laço o
   compile de `rec_b` e troque `for v in m b` por `for v in m`: nove
   `BS=... ok` sem nenhum `FALHOU`, mais o caso `BUFFER_SIZE=0` com
   `lines=0`;
2. as **sequências canônicas** (seção "Sequências canônicas"): `04 ok`,
   `02 ok`, `05 ok`, `B=1 identico`;
3. as **bordas de fd** (seção "Bordas de fd", só a variante obrigatória):
   `bordas ok`;
4. a **memória** (seção "Memória"): quatro execuções com
   `in use at exit: 0 bytes` e `ERROR SUMMARY: 0 errors`;
5. a **leitura mínima** (seção "Leitura mínima"): `reads=1285`, `reads=6`,
   `reads=1`;
6. o **pior caso cronometrado** (seção homônima): `cmp` silencioso, ≈ 8 s.
