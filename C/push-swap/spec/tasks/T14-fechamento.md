# T14 — Fechamento

## Objetivo

Projeto inteiro verde e entregável.

## Depende de

T13.

## Arquivos

- `README.md` na raiz do repositório
- Nenhuma alteração de código, salvo o que a validação apontar

## Especificação

- [../06-aceitacao/validacao.md](../06-aceitacao/validacao.md) — bateria completa
- [../06-aceitacao/casos.md](../06-aceitacao/casos.md) — A1 a A8
- [../06-aceitacao/desempenho.md](../06-aceitacao/desempenho.md) — números esperados

## Implementação

### Limpeza

Remover todo `main` temporário criado nas tarefas anteriores, qualquer arquivo de teste que não
faça parte da entrega, e arquivos gerados (`a100.txt`, `a500.txt`, binários) do controle de
versão.

### README na raiz

Exigências do Capítulo VII do enunciado:

- Primeira linha em itálico: *This project has been created as part of the 42 curriculum by
  \<login1\>, \<login2\>.*
- **Description** — o que é o projeto e o que ele resolve.
- **Instructions** — compilação e execução.
- **Resources** — referências, e **como a IA foi usada**: para quais tarefas e em quais partes.
- Explicação e justificativa dos algoritmos escolhidos.
- Raciocínio dos limiares do adaptativo com argumento de complexidade para tempo e espaço no
  modelo push_swap.
- Contribuições de cada um dos 2 alunos.

O `README.md` atual da raiz cobre o funcionamento e serve de base; falta acrescentar a linha do
currículo, Instructions, Resources, a justificativa dos limiares e a divisão do trabalho.

### Repositório

- Os dois alunos como colaboradores.
- Os dois logins na submissão.

## Pronto quando

**Estado limpo:**

```bash
make fclean && make && make       # segunda: "Nothing to be done"
make bonus && make bonus
norminette *.c *.h                # nenhuma linha "Error:"
```

**Todos os casos de aceitação**, A1 a A8 de [casos.md](../06-aceitacao/casos.md).

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

**Cobertura por tamanho, cada flag:**

```bash
for n in 1 2 3 4 5 6 7 10 50 100 500; do
  ARG=$(shuf -i 1-10000 -n $n | tr '\n' ' ')
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
    ARG=$(shuf -i 0-9999 -n $n | tr '\n' ' ')
    m=$(./push_swap $ARG | wc -l | tr -d ' ')
    [ "$m" -gt "$pior" ] && pior=$m
    i=$((i+1))
  done
  echo "n=$n pior=$pior"
done
# n=100 abaixo de 1500, n=500 abaixo de 8000
```

**Memória — inclusive nos caminhos de erro:**

```bash
leaks --atExit -- ./push_swap 4 67 3 87 23
leaks --atExit -- ./push_swap $(shuf -i 1-1000 -n 500 | tr '\n' ' ')
leaks --atExit -- ./push_swap --simple $(shuf -i 1-1000 -n 100 | tr '\n' ' ')
leaks --atExit -- ./push_swap 0 one 2 3
leaks --atExit -- ./push_swap "1 2" 3 four
leaks --atExit -- ./push_swap 1 1
leaks --atExit -- ./checker 3 2 1 </dev/null
```

Zero vazamento em todos.

**Checklist de entrega:**

- [ ] Compila com `-Wall -Wextra -Werror`, sem warning
- [ ] Não relinka
- [ ] Norminette limpa em todos os arquivos, incluindo `_bonus`
- [ ] Nenhuma variável global
- [ ] `Error\n` em stderr para token inválido, estouro de `int`, duplicata e flag inválida
- [ ] Sem argumento → não imprime nada
- [ ] `OK` no checker para n = 1, 2, 3, 5, 100, 500, já ordenada e inversa
- [ ] As quatro estratégias no mesmo binário, todas funcionando em qualquer entrada
- [ ] `--bench` só com a flag, sempre em stderr, soma das contagens igual a `total_ops`
- [ ] Metas de 100 e 500 batidas no pior caso de várias rodadas
- [ ] Zero vazamento, inclusive nos caminhos de erro
- [ ] README na raiz com todas as seções do Capítulo VII
- [ ] Os dois alunos como colaboradores no repositório
