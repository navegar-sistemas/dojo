# Validação

## Estado limpo

```bash
make re                      # zero warning com -Wall -Wextra -Werror
norminette *.c *.h           # nenhuma linha "Error:"
make && make                 # a segunda precisa dizer "Nothing to be done"
make bonus && make bonus     # idem
```

## Checker de referência

Os binários em `assets/` são o gabarito. No macOS eles chegam sem permissão de execução e sob
quarentena do Gatekeeper; sem tratar os dois, o processo é morto sem imprimir nada, com código
137:

```bash
chmod +x assets/checker_Mac
xattr -d com.apple.quarantine assets/checker_Mac
```

## Corretude

```bash
i=0
falhas=0
while [ $i -lt 200 ]; do
  ARG=$(shuf -i 1-1000 -n $((RANDOM % 20 + 1)) | tr '\n' ' ')
  r=$(./push_swap $ARG | ./assets/checker_Mac $ARG)
  [ "$r" = "OK" ] || { echo "FALHOU: $ARG"; falhas=$((falhas + 1)); }
  i=$((i + 1))
done
echo "falhas: $falhas"
```

Cobertura por tamanho, incluindo as bordas:

```bash
for n in 1 2 3 4 5 6 7 10 50 100 500; do
  ARG=$(shuf -i 1-10000 -n $n | tr '\n' ' ')
  echo -n "n=$n: "
  ./push_swap $ARG | ./assets/checker_Mac $ARG
done
```

Casos degenerados:

```bash
./push_swap 1 2 3 4 5 | ./assets/checker_Mac 1 2 3 4 5     # já ordenada
./push_swap 5 4 3 2 1 | ./assets/checker_Mac 5 4 3 2 1     # inversa
./push_swap -2147483648 2147483647 0 | ./assets/checker_Mac -2147483648 2147483647 0
```

## Cada estratégia em entrada grande

As quatro precisam devolver `OK` com 500 elementos. O `--simple` demora e gera dezenas de
milhares de linhas — é esperado.

```bash
shuf -i 0-9999 -n 500 > /tmp/a500.txt
for f in --simple --medium --complex --adaptive; do
  echo -n "$f: "
  ./push_swap $f $(cat /tmp/a500.txt) | ./assets/checker_Mac $(cat /tmp/a500.txt)
done
```

## Desempenho

Ver [desempenho.md](desempenho.md) para o laço de pior caso e os números esperados.

## Erros e casos silenciosos

Ver [casos.md](casos.md), seções A5 e A6.

Verificação de que o erro não vaza para stdout:

```bash
./push_swap 0 one 2 3 2>/dev/null | wc -c    # precisa imprimir 0
```

## Memória

O `valgrind` não roda em Apple Silicon; a ferramenta equivalente é o `leaks`:

```bash
leaks --atExit -- ./push_swap 4 67 3 87 23
leaks --atExit -- ./push_swap $(shuf -i 1-1000 -n 200 | tr '\n' ' ')
leaks --atExit -- ./push_swap 0 one 2 3
leaks --atExit -- ./push_swap "1 2" 3 four
leaks --atExit -- ./push_swap 1 1
```

Os três últimos são os que costumam falhar: no caminho de erro, o array do `ft_split` em curso
e a pilha parcialmente preenchida precisam ser liberados antes do `exit`.

## Bônus

```bash
printf 'sa\nrra\n' | ./checker 3 2 1     # OK
printf 'sa\n'      | ./checker 3 2 1     # KO
printf ''          | ./checker 1 2 3     # OK
printf 'xx\n'      | ./checker 3 2 1     # Error
./checker 3 2 one  </dev/null            # Error
./checker          </dev/null            # nada
```

O `</dev/null` nos casos sem movimentos não é decoração: sem ele o `checker` fica esperando
entrada até o EOF e o terminal trava.

Comparação direta com a referência em [../05-bonus/checker.md](../05-bonus/checker.md).

## Ciclo completo

```bash
ARG="4 67 3 87 23"
./push_swap --bench $ARG 2> /tmp/bench.txt | ./checker $ARG
cat /tmp/bench.txt
```
