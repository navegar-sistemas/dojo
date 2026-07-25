# T11 — `--adaptive`

## Objetivo

Despacho por desordem, com as três rotas ligadas e o rótulo do `--bench` refletindo o caminho
tomado.

## Depende de

T07, T09, T10.

## Arquivos

- `sort_adaptive.c`
- `main.c` (ligar `STRAT_ADAPTIVE` ao despacho real)

## Especificação

- [../04-algoritmos/adaptive.md](../04-algoritmos/adaptive.md)
- [../01-contrato/bench.md](../01-contrato/bench.md) — como o nome e a classe são compostos

## Implementação

```c
void	sort_adaptive(t_ctx *c, t_conf *conf, double disorder)
{
	if (disorder < 0.2)
		sort_simple(c, conf);
	else if (disorder < 0.5)
		sort_medium(c, conf);
	else
		sort_complex(c, conf);
	conf->name = "Adaptive";
}
```

Uma função só.

**A sobrescrita do nome vem depois da chamada.** A rota grava `name` e `cclass`; o adaptativo
troca apenas o nome e preserva a classe, que é o que faz o `--bench` imprimir
`Adaptive / O(n√n)` ou `Adaptive / O(n log n)` conforme o caminho.

**A desordem chega pronta do `main`**, medida antes de qualquer movimento e antes da conversão
em ranks. Recalcular aqui daria valor errado se a pilha já tivesse sido convertida.

**Os limiares são do enunciado**, com `<` estrito nos dois cortes: `0.2` exato cai na rota
O(n√n), `0.5` exato cai na O(n log n).

No `main`, `run_strategy` passa a chamar `sort_adaptive` para `STRAT_ADAPTIVE`, removendo o
desvio provisório para `sort_simple` do T06.

## Pronto quando

```bash
make re
norminette *.c *.h
```

**Cada faixa despacha para a rota certa.** Comparando a contagem do `--adaptive` com a da rota
esperada sobre a mesma entrada:

```bash
# desordem alta (aleatório costuma passar de 0.5): deve bater com --complex ou --medium
ARG=$(shuf -i 0-9999 -n 100 | tr '\n' ' ')
echo "adaptive: $(./push_swap $ARG | wc -l)"
echo "medium:   $(./push_swap --medium $ARG | wc -l)"
echo "complex:  $(./push_swap --complex $ARG | wc -l)"
# o valor do adaptive precisa ser idêntico a um dos dois

# desordem baixa: quase ordenada, deve bater com --simple
ARG=$(seq 1 100 | tr '\n' ' ')
ARG=$(echo $ARG | awk '{t=$3; $3=$70; $70=t; print}')
echo "adaptive: $(./push_swap $ARG | wc -l)"
echo "simple:   $(./push_swap --simple $ARG | wc -l)"
# idênticos
```

**A2 pelo caminho padrão:**

```bash
./push_swap --adaptive 4 67 3 87 23 | wc -l    # 13
./push_swap 4 67 3 87 23 | wc -l               # 13 (adaptive é o padrão)
```

**Desempenho combinado — pior caso de 20 rodadas:**

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
# n=100 precisa ficar abaixo de 1500; esperado até 1084
# n=500 precisa ficar abaixo de 8000; esperado até 7555
```

**Corretude nas quatro flags:**

```bash
shuf -i 0-9999 -n 500 > /tmp/a500.txt
for f in --simple --medium --complex --adaptive; do
  echo -n "$f: "
  ./push_swap $f $(cat /tmp/a500.txt) | ./assets/checker_Mac $(cat /tmp/a500.txt)
done
```

**Entrada já ordenada, todas as flags:**

```bash
for f in --simple --medium --complex --adaptive; do
  echo "$f: $(./push_swap $f 1 2 3 4 5 | wc -l)"    # todos 0
done
```
