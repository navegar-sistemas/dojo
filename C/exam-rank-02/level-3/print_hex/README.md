Nome da atividade  : print_hex
Arquivos esperados : print_hex.c
Funções permitidas : write
Proibições e normas: for, switch, case, linhas com mais de 80 colunas... Para ver todas as proibições, consulte a norm.
--------------------------------------------------------------------------------

Escreva um programa que recebe um número positivo (ou zero) expresso em base 10 e o exibe em base 16 (letras minúsculas), seguido de uma nova linha.

Se a quantidade de parâmetros não for 1, o programa exibe uma nova linha.

Examples:

$> ./print_hex "10" | cat -e
a$
$> ./print_hex "255" | cat -e
ff$
$> ./print_hex "5156454" | cat -e
4eae66$
$> ./print_hex | cat -e
$
