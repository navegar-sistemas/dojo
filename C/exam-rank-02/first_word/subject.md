Nome da atividade  : first_word
Arquivos esperados : first_word.c
Funções permitidas : write
Proibições e normas: for, switch, case, linhas com mais de 80 colunas... Para ver todas as proibições, consulte a norm.
--------------------------------------------------------------------------------

Escreva um programa que receba uma string e exiba sua primeira palavra, seguida por uma nova linha.

Uma palavra é um trecho de string delimitado por espaços/tabulações ou por início/fim de uma string.

Se o número de parâmetros não for 1, ou se não há palavras, simplesmente exiba uma nova linha.

exemplos:

$> cc *.c -Wall -Wextra -Werror && ./a.out "FOR PONY" | cat -e
FOR$
$> cc *.c -Wall -Wextra -Werror && ./a.out "this        ...       is sparta, then again, maybe    not" | cat -e
this$
$> cc *.c -Wall -Wextra -Werror && ./a.out "   " | cat -e
$
$> cc *.c -Wall -Wextra -Werror && ./a.out "a" "b" | cat -e
$
$> cc *.c -Wall -Wextra -Werror && ./a.out "  lorem,ipsum  " | cat -e
lorem,ipsum$
$>