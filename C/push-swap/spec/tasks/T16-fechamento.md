# T16 — Fechamento

## Objetivo

Projeto inteiro verde na bateria completa de validação.

## Depende de

T15.

## Arquivos

- Nenhuma alteração de código, salvo o que a validação apontar.

## Especificação

- [../06-aceitacao/validacao.md](../06-aceitacao/validacao.md) — bateria completa
- [../06-aceitacao/casos.md](../06-aceitacao/casos.md) — A1 a A8
- [../06-aceitacao/desempenho.md](../06-aceitacao/desempenho.md) — números esperados

## Implementação

### Limpeza

Remover todo `main` temporário criado nas tarefas anteriores, qualquer arquivo de teste que não
faça parte da entrega, e arquivos gerados (`args.txt`, binários) do controle de versão.

## Pronto quando

**Estado limpo:**

```bash
make fclean && make && make       # segunda: "Nothing to be done"
make bonus && make bonus
norminette *.c *.h                # nenhuma linha "Error:"
```

**Todos os casos de aceitação**, A1 a A8 de [casos.md](../06-aceitacao/casos.md) — incluindo os
dois invariantes de A7.

**Corretude — 200 permutações aleatórias:**

```bash
i=0; falhas=0
while [ $i -lt 200 ]; do
  ARG=$(shuf -i 1-1000 -n $((RANDOM % 20 + 1)) | tr '\n' ' ')
  [ "$(./push_swap $ARG | ./checker $ARG)" = "OK" ] || { echo "FALHOU: $ARG"; falhas=$((falhas+1)); }
  i=$((i+1))
done
echo "falhas: $falhas"
```

**Cobertura por tamanho, cada flag — cruzando o `GREEDY_MAX_N`:**

```bash
for n in 1 2 3 4 5 6 7 10 50 100 500 1499 1500 1501; do
  ARG=$(shuf -i 1-100000 -n $n | tr '\n' ' ')
  for f in --simple --medium --complex --adaptive; do
    r=$(./push_swap $f $ARG | ./checker $ARG)
    [ "$r" = "OK" ] || echo "FALHOU n=$n $f"
  done
done
echo "cobertura concluída"
```

**Desempenho — pior caso de 20 rodadas:**

```bash
for n in 100 500; do
  pior=0; i=0
  while [ $i -lt 20 ]; do
    ARG=$(shuf -i 1-10000 -n $n | tr '\n' ' ')
    m=$(./push_swap $ARG | wc -l | tr -d ' ')
    [ "$m" -gt "$pior" ] && pior=$m
    i=$((i+1))
  done
  echo "n=$n pior=$pior"
done
# n=100 abaixo de 700; n=500 abaixo de 5500 — a cauda pode encostar, ver desempenho.md
```

**Memória — inclusive nos caminhos de erro e no portfólio:**

```bash
valgrind --leak-check=full ./push_swap 4 67 3 87 23
valgrind --leak-check=full ./push_swap $(shuf -i 1-10000 -n 500 | tr '\n' ' ')
valgrind --leak-check=full ./push_swap --simple $(shuf -i 1-10000 -n 100 | tr '\n' ' ')
valgrind --leak-check=full ./push_swap 0 one 2 3
valgrind --leak-check=full ./push_swap "1 2" 3 four
valgrind --leak-check=full ./push_swap 1 1
valgrind --leak-check=full ./checker 3 2 1 </dev/null
```

Zero vazamento em todos.

**Checklist final:**

- [ ] Compila com `-Wall -Wextra -Werror`, sem warning
- [ ] Não relinka
- [ ] Norminette limpa em todos os arquivos, incluindo `_bonus`
- [ ] Nenhuma variável global
- [ ] `Error\n` em stderr para token inválido, estouro de `int`, duplicata e flag inválida
- [ ] Sem argumento → não imprime nada
- [ ] `OK` no checker para n = 1, 2, 3, 5, 100, 500, 1501, já ordenada e inversa
- [ ] As quatro estratégias no mesmo binário, todas funcionando em qualquer entrada
- [ ] `--adaptive` nunca emite mais que o certificador do regime
- [ ] `--bench` só com a flag, sempre em stderr, soma das contagens igual a `total_ops`
- [ ] Metas de 100 e 500 batidas no pior caso de várias rodadas
- [ ] Zero vazamento, inclusive nos caminhos de erro
