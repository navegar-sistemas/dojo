*This project has been created as part of the 42 curriculum by macoelho.*

# Libft

## Descrição

A Libft é o primeiro projeto do currículo da 42: uma biblioteca C estática (`libft.a`) que reimplementa um conjunto selecionado de funções da biblioteca padrão do C, além de um grupo de funções auxiliares de string/memória e um pequeno kit de funções para listas encadeadas. O objetivo é duplo: entender como a libc funciona por baixo dos panos — aritmética de ponteiros, gerenciamento de memória, semântica de `unsigned char`, tratamento de falha de alocação — ao reconstruí-la do zero; e produzir uma biblioteca sólida que os projetos posteriores da 42 possam reutilizar.

A biblioteca é dividida em três partes (todas obrigatórias na versão 19.0 do subject):

1. **Funções da libc** — reimplementações fiéis (prefixo `ft_`) que seguem estritamente o comportamento das páginas de `man`.
2. **Funções adicionais** — utilitários que não existem na libc ou existem de outra forma (`ft_substr`, `ft_split`, `ft_itoa`, ...).
3. **Lista encadeada** — um nó genérico `t_list` e nove funções para construir, percorrer, transformar e destruir listas.

Tudo é escrito em C, em conformidade com a Norm da 42, sem variáveis globais e sem funções externas além das que cada função pode usar explicitamente (`malloc`, `free`, `write`).

## Instruções

### Compilação

```sh
make        # compila os fontes e cria a libft.a (ar rcs)
make clean  # remove os arquivos-objeto
make fclean # remove os arquivos-objeto e a libft.a
make re     # recompila do zero
```

A biblioteca é compilada com `cc -Wall -Wextra -Werror` e gera a `libft.a` na raiz do repositório. O Makefile não faz relink desnecessário.

### Uso no seu próprio programa

```c
#include "libft.h"

int	main(void)
{
	char	*joined;

	joined = ft_strjoin("Hello, ", "World!");
	ft_putendl_fd(joined, 1);
	free(joined);
	return (0);
}
```

```sh
cc -Wall -Wextra -Werror main.c -L. -lft -o demo
```

## Referência da biblioteca

As funções estão organizadas nas três partes do projeto; os protótipos correspondem às assinaturas declaradas em `libft.h`.

### Parte 1 — Funções da libc

| Função | Protótipo | Descrição |
| --- | --- | --- |
| `ft_isalpha` | `int ft_isalpha(int c)` | 1 se `c` é uma letra; senão, 0 |
| `ft_isdigit` | `int ft_isdigit(int c)` | 1 se `c` é um dígito decimal; senão, 0 |
| `ft_isalnum` | `int ft_isalnum(int c)` | 1 se `c` é alfanumérico; senão, 0 |
| `ft_isascii` | `int ft_isascii(int c)` | 1 se `c` pertence ao conjunto ASCII (0–127); senão, 0 |
| `ft_isprint` | `int ft_isprint(int c)` | 1 se `c` é imprimível (incluindo o espaço); senão, 0 |
| `ft_strlen` | `size_t ft_strlen(const char *s)` | comprimento de `s`, sem contar o `\0` final |
| `ft_memset` | `void *ft_memset(void *b, int c, size_t len)` | preenche `len` bytes de `b` com o byte `c` |
| `ft_bzero` | `void ft_bzero(void *s, size_t n)` | zera `n` bytes de `s` |
| `ft_memcpy` | `void *ft_memcpy(void *dst, const void *src, size_t n)` | copia `n` bytes (sobreposição é comportamento indefinido) |
| `ft_memmove` | `void *ft_memmove(void *dst, const void *src, size_t len)` | copia `n` bytes com segurança, mesmo com regiões sobrepostas |
| `ft_strlcpy` | `size_t ft_strlcpy(char *dst, const char *src, size_t dstsize)` | cópia limitada pelo tamanho; sempre termina em `\0`; retorna `strlen(src)` |
| `ft_strlcat` | `size_t ft_strlcat(char *dst, const char *src, size_t dstsize)` | concatenação limitada pelo tamanho; retorna o comprimento que tentaria criar |
| `ft_toupper` | `int ft_toupper(int c)` | letra minúscula → maiúscula; o resto, inalterado |
| `ft_tolower` | `int ft_tolower(int c)` | letra maiúscula → minúscula; o resto, inalterado |
| `ft_strchr` | `char *ft_strchr(const char *s, int c)` | primeira ocorrência de `c` em `s` (incluindo o `\0`), ou NULL |
| `ft_strrchr` | `char *ft_strrchr(const char *s, int c)` | última ocorrência de `c` em `s` (incluindo o `\0`), ou NULL |
| `ft_strncmp` | `int ft_strncmp(const char *s1, const char *s2, size_t n)` | compara no máximo `n` bytes, como `unsigned char` |
| `ft_memchr` | `void *ft_memchr(const void *s, int c, size_t n)` | primeira ocorrência do byte `c` nos primeiros `n` bytes, ou NULL |
| `ft_memcmp` | `int ft_memcmp(const void *s1, const void *s2, size_t n)` | compara `n` bytes crus (não para no `\0`) |
| `ft_strnstr` | `char *ft_strnstr(const char *haystack, const char *needle, size_t len)` | procura `needle` nos primeiros `len` bytes de `haystack` |
| `ft_atoi` | `int ft_atoi(const char *str)` | lê espaços iniciais, um sinal opcional e os dígitos, convertendo para int |
| `ft_calloc` | `void *ft_calloc(size_t count, size_t size)` | alocação com checagem de overflow, inicializada com zero |
| `ft_strdup` | `char *ft_strdup(const char *s1)` | cópia alocada de `s1` |

### Parte 2 — Funções adicionais

| Função | Protótipo | Descrição |
| --- | --- | --- |
| `ft_substr` | `char *ft_substr(char const *s, unsigned int start, size_t len)` | substring alocada de `s` a partir de `start`, com no máximo `len` caracteres |
| `ft_strjoin` | `char *ft_strjoin(char const *s1, char const *s2)` | concatenação alocada de `s1` e `s2` |
| `ft_strtrim` | `char *ft_strtrim(char const *s1, char const *set)` | cópia alocada de `s1` sem os caracteres de `set` no começo e no fim |
| `ft_split` | `char **ft_split(char const *s, char c)` | array terminado em NULL com as palavras de `s`, separadas pelo delimitador `c` |
| `ft_itoa` | `char *ft_itoa(int n)` | string decimal alocada de `n` (trata `INT_MIN`) |
| `ft_strmapi` | `char *ft_strmapi(char const *s, char (*f)(unsigned int, char))` | nova string criada aplicando `f(índice, char)` a cada caractere |
| `ft_striteri` | `void ft_striteri(char *s, void (*f)(unsigned int, char *))` | aplica `f(índice, &char)` a cada caractere, no próprio lugar |
| `ft_putchar_fd` | `void ft_putchar_fd(char c, int fd)` | escreve o caractere `c` no `fd` |
| `ft_putstr_fd` | `void ft_putstr_fd(char *s, int fd)` | escreve a string `s` no `fd` |
| `ft_putendl_fd` | `void ft_putendl_fd(char *s, int fd)` | escreve `s` seguida de uma quebra de linha no `fd` |
| `ft_putnbr_fd` | `void ft_putnbr_fd(int n, int fd)` | escreve o inteiro `n` no `fd` (trata `INT_MIN`) |

### Parte 3 — Lista encadeada

```c
typedef struct s_list
{
	void			*content;
	struct s_list	*next;
}	t_list;
```

| Função | Protótipo | Descrição |
| --- | --- | --- |
| `ft_lstnew` | `t_list *ft_lstnew(void *content)` | aloca um nó com `content`, e `next` em NULL |
| `ft_lstadd_front` | `void ft_lstadd_front(t_list **lst, t_list *new)` | insere `new` no início da lista |
| `ft_lstsize` | `int ft_lstsize(t_list *lst)` | número de nós |
| `ft_lstlast` | `t_list *ft_lstlast(t_list *lst)` | último nó da lista |
| `ft_lstadd_back` | `void ft_lstadd_back(t_list **lst, t_list *new)` | insere `new` no fim da lista |
| `ft_lstdelone` | `void ft_lstdelone(t_list *lst, void (*del)(void *))` | libera um nó: `del` no conteúdo e `free` no nó |
| `ft_lstclear` | `void ft_lstclear(t_list **lst, void (*del)(void *))` | libera o nó e todos os sucessores; define `*lst` como NULL |
| `ft_lstiter` | `void ft_lstiter(t_list *lst, void (*f)(void *))` | aplica `f` ao conteúdo de cada nó |
| `ft_lstmap` | `t_list *ft_lstmap(t_list *lst, void *(*f)(void *), void (*del)(void *))` | cria uma nova lista aplicando `f` a cada conteúdo; faz a limpeza em caso de falha |

## Recursos

- Páginas de `man` das funções originais (`man 3 strlen`, `man 3 memmove`, ...).
- *The C Programming Language* — Brian W. Kernighan, Dennis M. Ritchie (2ª edição).
- [strlcpy and strlcat — consistent, safe, string copy and concatenation](https://www.usenix.org/legacy/event/usenix99/full_papers/millert/millert.pdf) — Todd C. Miller, Theo de Raadt (USENIX '99), o artigo que introduziu as funções `strl*`.
- Tabela ASCII: `man ascii`.

### Uso de IA

Em conformidade com o Capítulo V do subject, descrevo abaixo como a IA foi
utilizada neste projeto.

Todo o código-fonte entregue (as funções `ft_*.c` e o `libft.h`) foi escrito e
compreendido por mim. A IA serviu como ferramenta de **apoio ao aprendizado** —
sempre depois de eu raciocinar sobre o problema e, quando possível, discuti-lo
com colegas —, e **não** para produzir as soluções. As tarefas em que recorri
a ela foram:

- **Redação e revisão de texto:** correção ortográfica e gramatical dos textos
  do projeto, além de apoio no desenvolvimento e na fluidez da redação deste 
  README — a partir da estrutura e dos tópicos que defini.
- **Traduções:** tradução de material de referência — páginas de `man`, o
  próprio subject e artigos técnicos — para apoiar a leitura e a compreensão.
- **Revisão de Norm:** verificação complementar de conformidade com a Norm, em
  adição à `norminette` oficial.
- **Ampliação dos testes:** expansão de arquivos de teste — que são de
  desenvolvimento e **não fazem parte do repositório de entrega** — para cobrir
  mais casos extremos e validar o comportamento das funções.
- **Dúvidas conceituais específicas:** esclarecimento de questões pontuais que
  eu não havia compreendido, depois de esgotar a pesquisa por conta própria e a
  discussão com colegas próximos. Por exemplo:
  - por que a sobreposição de regiões de memória no `ft_memcpy` é *undefined
    behavior* pelo padrão C — e não apenas "resultado errado" — e como o
    `ft_memmove` decide copiar do início ou do fim para sobreviver à
    sobreposição;
  - por que negar `INT_MIN` (`-n`) é *undefined behavior*, enquanto o estouro de
    um `unsigned` é bem definido (dá a volta) — e como isso molda o tratamento
    do `INT_MIN` no `ft_atoi` e no `ft_putnbr_fd`, e a checagem de estouro antes
    da multiplicação no `ft_calloc`.
- **Revisão de performance e qualidade:** um agente automatizado em loop que
  identifica os arquivos `.c` cujo desenvolvimento concluí, roda os arquivos de
  teste para confirmar a conclusão, executa a `norminette` e verifica se o
  arquivo ainda não passou por revisão de performance. Atendidas todas essas
  condições, o agente faz a revisão e registra, em um arquivo `.md`, sugestões
  de melhoria ligadas a recursos da linguagem que eu provavelmente ainda não
  conheço, a boas práticas de implementação e à legibilidade do código. As
  sugestões são inferidas a partir de referências cruzadas entre os arquivos a
  que o agente teve acesso e os dados coletados em revisões anteriores. Cada
  sugestão foi avaliada e, quando pertinente, implementada por mim.
