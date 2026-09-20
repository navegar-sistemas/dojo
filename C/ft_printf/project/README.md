*This project has been created as part of the 42 curriculum by macoelho.*

# ft_printf

## Description

`libftprintf.a` é uma biblioteca estática que expõe uma única função:

```c
int	ft_printf(const char *format, ...);
```

Ela imita a `printf()` da libc: percorre a string de formato, imprime os
caracteres literais em `stdout` e substitui cada diretiva `%…` pelo próximo
argumento variádico, devolvendo o total de bytes escritos (ou `-1` em erro de
escrita / formato terminado no meio de uma diretiva).

**Parte obrigatória** — as nove conversões `c s p d i u x X %`, sem flags.

**Parte bônus** — a gramática completa de formatação sobre as mesmas
conversões: flags `-`, `0`, `#`, `+` e espaço, largura mínima de campo e
precisão (`%-8.3d`, `%#010x`, `%+.5i`, …).

O alvo de comportamento é a `printf` da glibc, espelhada **byte a byte**
(inclusive valor de retorno) em todo o domínio suportado — até nos cantos que
a linguagem deixa em aberto, medidos na referência e fixados como gabarito:
`%p` de `NULL` imprime `(nil)` e ignora a precisão, `%s` de `NULL` com
precisão < 6 imprime vazio, diretiva desconhecida é reimpressa em forma
canônica (`%0-5r` → `%-5r`), formato terminando em `%` devolve `-1`, etc.

## Instructions

```sh
make            # biblioteca com a parte obrigatória (cc -Wall -Wextra -Werror)
make bonus      # reconstrói libftprintf.a com a implementação completa (flags)
make fclean     # remove objetos, biblioteca e o marcador .bonus
```

Uso em um programa:

```c
#include "ft_printf.h"

int	main(void)
{
	int	n;

	n = ft_printf("%s tem %d anos\n", "42", 0x2a);
	return (n < 0);
}
```

```sh
cc -Wall -Wextra -Werror main.c -L. -lftprintf && ./a.out
```

## Escolhas técnicas e justificativa

- **Sem alocação no heap.** O maior texto que uma conversão gera sozinha é um
  número de 64 bits (20 dígitos decimais); buffers de pilha de 24 bytes cobrem
  qualquer caso, eliminando por construção falhas de `malloc` e vazamentos
  (valgrind zerado sem esforço). Padding de largura é emitido em laço, não
  materializado.
- **Escrita imediata com propagação de erro.** Cada escritor devolve o número
  de bytes escritos ou `-1`; qualquer `-1` sobe até o retorno da `ft_printf`,
  como na referência quando a `write` falha.
- **`va_list` sempre por ponteiro.** O laço passa `&ap` para o despacho e todo
  `va_arg` acontece via `*ap`. Passar `va_list` por valor entre funções
  dessincroniza o cursor em ABIs onde o tipo é um ponteiro simples (ARM64
  Darwin), embora funcione onde ele é um array (x86-64 SysV) — por ponteiro,
  funciona nas duas.
- **Bônus: analisar → renderizar → montar.** `parse_fmt` reduz a diretiva a
  uma struct `t_fmt`; os números são renderizados de trás para a frente num
  buffer (`render_base`); um único montador (`put_num`) aplica prefixo de
  sinal/base, zeros de precisão, zeros de largura e espaços numa ordem fixa.
  Toda a matriz flag × conversão colapsa em "escolha o prefixo certo" — `%d`
  negativo passa `"-"`, `%#x` passa `"0x"`, `%p` passa `"+0x"`/`" 0x"`/`"0x"`.
- **Limites de `int` devolvem `-1`, nunca estouram.** O retorno é `int`, então
  largura ou precisão acima de `INT_MAX` (`%2147483648d`), saída total acima
  de 2 GB e strings gigantes em `%s` terminam em `-1` — o `EOVERFLOW` da
  referência. Cada guarda é escrita do lado que não estoura
  (`r > PF_INT_MAX - total`, nunca `total + r > PF_INT_MAX`), porque overflow
  de `int` com sinal é comportamento indefinido. `PF_INT_MAX` é constante do
  próprio header: a Norma (III.7) só admite macro de biblioteca padrão quando
  o projeto a permite, e `<limits.h>` não está na lista do subject.
- **`%.Ns` não lê além de N.** `conv_s` mede a string com um `strnlen` próprio
  que confere o limite antes de ler cada byte. `%.3s` sobre um array de 3
  bytes sem terminador é C válido, e um `strlen` comum leria a memória
  vizinha.
- **Duas implementações independentes.** A parte obrigatória fica em 4 + 4
  funções diretas (dígitos por recursão, sem buffer); o bônus reconstrói a
  biblioteca inteira via `make bonus` com os arquivos `*_bonus.c`. Nenhum
  arquivo é compartilhado entre as duas variantes, e o Makefile remove o
  arquivo `.a` antes de recriá-lo para nunca misturar objetos das duas.

A validação é diferencial: um mesmo lote de casos (curados + fuzz de milhares
de formatos gerados) roda com `printf` e com `ft_printf`, e `stdout` + retornos
precisam ser idênticos byte a byte. ASan/UBSan e valgrind completam o ciclo.

## Resources

- `man 3 printf` — semântica das conversões, flags, largura e precisão.
- ISO C — *Formatted input/output functions* (`fprintf`): o que é contrato da
  linguagem e o que é comportamento indefinido deixado à implementação.
- Manual da glibc, *Formatted Output* — a referência espelhada por este
  projeto.
- **Uso de IA:** assistência de IA (Claude) foi usada para sondar e fixar o
  comportamento da glibc nos casos que a linguagem não define (baterias de
  medição), gerar a suíte de testes diferencial/fuzz e redigir documentação.
