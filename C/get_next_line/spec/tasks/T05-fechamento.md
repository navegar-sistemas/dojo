# T05 — Fechamento

## Objetivo

Validação de ponta a ponta no estado final e a documentação de apresentação.

## Depende de

T04.

## Arquivos

- `project/README.md`

## Especificação

- [../06-aceitacao/validacao.md](../06-aceitacao/validacao.md) — tudo
- [../03-arquitetura/modulos.md](../03-arquitetura/modulos.md) — tabela-gabarito das contagens

## Implementação

**README.md** em `project/`, apresentando o diretório para quem chega sem
contexto: o que a função faz e devolve, como compilar junto de um programa
(com e sem `-D BUFFER_SIZE`), um exemplo mínimo de uso com o `free` de cada
linha, a explicação e justificativa do algoritmo (stash estático + leitura
mínima + custo quadrático assumido), o bônus e suas condições, e as
referências usadas.

**Passada final de estilo**, contra
[../02-restricoes/estilo.md](../02-restricoes/estilo.md): contagens de funções
e corpos iguais à tabela de módulos, largura ≤ 80 (medida: 61), tabulações
reais, nenhuma variável global, `#define` só de constantes.

## Pronto quando

1. **Todos** os blocos de
   [../06-aceitacao/validacao.md](../06-aceitacao/validacao.md), do primeiro
   ao último, executados em sequência num `check/` recém-criado, sem nenhum
   `FALHOU`, nenhum diff impresso, valgrinds zerados e contagens de `read`
   exatas — o resultado íntegro, não amostras;
2. conferência mecânica dos tetos:

   ```bash
   awk '/^{/{n=0; next} /^}/{if (n > 25) print FILENAME": corpo com "n" linhas"; next} {n++}' \
       ../project/*.c   # silêncio = nenhum corpo acima de 25
   grep -c "^{" ../project/*.c          # 4 nos núcleos, 5 nos utils
   awk 'length(gensub(/\t/, "    ", "g")) > 80 {print FILENAME": "FNR}' \
       ../project/*.c ../project/*.h    # silêncio = nada acima de 80 colunas
   ```

3. o `README.md` existe em `project/` e cobre os itens da seção
   Implementação.
