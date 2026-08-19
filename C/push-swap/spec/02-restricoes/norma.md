# Norma

Regras da `norminette 3.3.59`, com o identificador do erro que cada violação produz.

| Regra | Erro |
|---|---|
| Cabeçalho padrão no topo de todo `.c` e `.h` | `INVALID_HEADER` |
| Máximo 5 funções por arquivo, contando as `static` | `TOO_MANY_FUNCS` |
| Máximo 25 linhas no corpo de uma função | `TOO_MANY_LINES` |
| Máximo 4 parâmetros por função | `TOO_MANY_ARGS` |
| `for`, `do...while`, `switch`, `case`, `goto` proibidos | `FORBIDDEN_CS` |
| Operador ternário `?:` proibido | `TERNARY_FBIDDEN` |
| Declaração e atribuição na mesma linha | `DECL_ASSIGN_LINE` |
| Linha vazia no fim do arquivo | `EMPTY_LINE_EOF` |
| Espaço onde se espera tabulação e vice-versa | `TAB_REPLACE_SPACE`, `SPACE_REPLACE_TAB` |

Variável em escopo de arquivo produz o aviso `GLOBAL_VAR_DETECTED`, que a norminette classifica
como *Notice* e não como erro — mas este projeto proíbe variáveis globais, então elas
continuam fora.

## O que isso impõe ao desenho

**Sem `for`.** Todo contador é declarado no topo da função, inicializado depois da linha em
branco, e percorrido com `while`. O pseudocódigo desta spec já está escrito assim.

**Sem ternário.** Escolhas como "gira por cima ou por baixo" viram `if`/`else` explícito.

**Corpo de 25 linhas.** Funções que fariam três coisas precisam virar três funções. Como cada
extração consome a cota de 5 funções do arquivo, o par de limites é o que determina a
granularidade dos módulos em [../03-arquitetura/modulos.md](../03-arquitetura/modulos.md) — as
11 operações não cabem num arquivo só e ocupam quatro, `ps_die` mora em `utils.c` porque
`main.c` e `prog.c` fecham as próprias cotas, e as variantes `sort_greedy`/`sort_greedy_alt`
moram em `greedy_exec.c` porque `sort_greedy.c` esgotou a dele.

**Quatro parâmetros.** Toda operação recebe um único `t_ctx *`, que carrega as duas pilhas e o
destino das contagens.

**Sem parâmetro ignorado.** `-Wextra` liga `-Wunused-parameter`, e `-Werror` transforma o aviso
em falha de compilação. Uma assinatura uniforme `void op_xx(t_stack *a, t_stack *b)` quebraria
em `op_sa`, que não usa `b`. O `t_ctx *` único resolve isso: o parâmetro é sempre usado.

## Tabela de nomes das operações

O caminho para traduzir `t_op` em string é uma cadeia de `if` com literais:

```c
char	*op_name(t_op op)
{
	if (op == OP_SA)
		return ("sa");
	if (op == OP_SB)
		return ("sb");
	...
	return ("");
}
```

Onze pares mais o retorno final dão 23 linhas de corpo, dentro do limite. As duas alternativas
mais naturais não passam:

- `char *names[] = {"sa", "sb", ...};` dentro da função viola `DECL_ASSIGN_LINE`.
- A mesma tabela em escopo de arquivo é variável global, proibida neste projeto.

## Cobertura

Os arquivos de bônus entram na checagem da norma junto com os obrigatórios, cabeçalho padrão
incluído. Nenhum arquivo, nem os `_bonus`, pode ter linha `Error:`.

## Verificação

```bash
norminette *.c *.h
```

Precisa terminar sem nenhuma linha `Error:`. Avisos `Notice:` só apareceriam se houvesse
variável em escopo de arquivo, o que não é o caso neste desenho.
