# Validação

## Estado limpo

```bash
make re                      # zero warning com -Wall -Wextra -Werror
norminette *.c *.h           # nenhuma linha "Error:"
make && make                 # a segunda precisa dizer "Nothing to be done"
make bonus && make bonus     # idem
```

## Checker de referência

Os comandos rodam do diretório da implementação; o gabarito executável fica em
`../assets/checker_linux`.

```bash
chmod +x ../assets/checker_linux
```

O binário de referência é x86-64: numa máquina de outra arquitetura ele não executa, e o
oráculo passa a ser o `checker` próprio depois de validado contra a referência num ambiente
x86-64.

## Corretude

```bash
i=0
falhas=0
while [ $i -lt 200 ]; do
  ARG=$(shuf -i 1-1000 -n $((RANDOM % 20 + 1)) | tr '\n' ' ')
  r=$(./push_swap $ARG | ../assets/checker_linux $ARG)
  [ "$r" = "OK" ] || { echo "FALHOU: $ARG"; falhas=$((falhas + 1)); }
  i=$((i + 1))
done
echo "falhas: $falhas"
```

Cobertura por tamanho, incluindo as bordas:

```bash
for n in 1 2 3 4 5 6 7 10 50 100 500 1499 1500 1501; do
  ARG=$(shuf -i 1-100000 -n $n | tr '\n' ' ')
  echo -n "n=$n: "
  ./push_swap $ARG | ../assets/checker_linux $ARG
done
```

Os três últimos tamanhos cruzam o `GREEDY_MAX_N` (1500): acima dele o portfólio roda só o
certificador, e a ordenação precisa continuar correta.

Casos degenerados:

```bash
./push_swap 1 2 3 4 5 | ../assets/checker_linux 1 2 3 4 5     # já ordenada
./push_swap 5 4 3 2 1 | ../assets/checker_linux 5 4 3 2 1     # inversa
./push_swap -2147483648 2147483647 0 | ../assets/checker_linux -2147483648 2147483647 0
```

## Cada estratégia em entrada grande

As quatro precisam devolver `OK` com 500 elementos. O `--simple` demora e gera dezenas de
milhares de linhas — é esperado.

```bash
shuf -i 0-9999 -n 500 > args.txt
for f in --simple --medium --complex --adaptive; do
  echo -n "$f: "
  ./push_swap $f $(cat args.txt) | ../assets/checker_linux $(cat args.txt)
done
```

## Invariante do portfólio

A invocação padrão nunca emite mais que a rota certificadora do regime, forçada sobre a mesma
entrada — laço pronto no caso A7 de [casos.md](casos.md).

## Desempenho

Ver [desempenho.md](desempenho.md) para o laço de pior caso e os números esperados.

## Erros e casos silenciosos

Ver [casos.md](casos.md), seções A5 e A6.

Verificação de que o erro não vaza para stdout:

```bash
./push_swap 0 one 2 3 2>/dev/null | wc -c    # precisa imprimir 0
```

## Memória

```bash
valgrind --leak-check=full ./push_swap 4 67 3 87 23
valgrind --leak-check=full ./push_swap $(shuf -i 1-10000 -n 500 | tr '\n' ' ')
valgrind --leak-check=full ./push_swap --simple $(shuf -i 1-10000 -n 200 | tr '\n' ' ')
valgrind --leak-check=full ./push_swap 0 one 2 3
valgrind --leak-check=full ./push_swap "1 2" 3 four
valgrind --leak-check=full ./push_swap 1 1
```

O primeiro da lista exercita o portfólio inteiro (três simulações, dois candidatos
descartados); o segundo, o crescimento do programa gravado em escala. Nos caminhos de erro, o
array do `ft_split` em curso e a pilha parcialmente preenchida precisam ser liberados antes do
`exit`.

## Bônus

```bash
printf 'sa\nrra\n' | ./checker 3 2 1     # OK
printf 'sa\n'      | ./checker 3 2 1     # KO
printf ''          | ./checker 1 2 3     # OK
printf 'xx\n'      | ./checker 3 2 1     # Error
./checker 3 2 one  </dev/null            # Error
./checker          </dev/null            # nada

valgrind --leak-check=full ./checker 3 2 1 </dev/null
printf 'sa\nrra\n' | valgrind --leak-check=full ./checker 3 2 1
```

Comparação direta com a referência em [../05-bonus/checker.md](../05-bonus/checker.md).

## Ciclo completo

```bash
./push_swap --bench 4 67 3 87 23 2> /tmp/bench.txt | ./checker 4 67 3 87 23
cat /tmp/bench.txt
```
