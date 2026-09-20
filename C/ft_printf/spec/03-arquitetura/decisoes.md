# Decisões de desenho

As escolhas que o contrato não impõe, com a razão de cada uma.

## A glibc como contrato

A linguagem deixa em aberto boa parte do que uma `printf` faz: `%p` de
`NULL`, `%s` de `NULL`, flag `0` em `%c`, diretiva desconhecida, formato
incompleto, `+` em `%p`. Em vez de decidir caso a caso, o projeto adota uma
regra única: **o que a glibc 2.36 faz é o contrato**. Cada canto foi sondado
na referência e virou linha de tabela em
[../06-aceitacao/casos.md](../06-aceitacao/casos.md).

Duas consequências: a reimplementação não tem nenhuma decisão ambígua
sobrando, e a verificação vira um `cmp`
([../06-aceitacao/validacao.md](../06-aceitacao/validacao.md)). Os cantos
contrariam a intuição com frequência — `%08p` com `NULL` alinha com
**espaços**, `%.3p` não trunca `(nil)`, `%+p` imprime `+0x…`, `%0-5r` e
`%-5r` produzem a mesma saída.

## Sem alocação no heap

O texto mais longo que uma conversão gera sozinha é um número: 20 dígitos
decimais de um `unsigned long` de 64 bits, ou 16 em hexadecimal. Buffers de
pilha de 24 bytes cobrem qualquer conversão, e o padding de largura é emitido
em laço, nunca materializado — `%2000d` não precisa de um buffer de 2000
bytes.

- Não existe caminho de falha de `malloc`, então o único erro possível é o da
  `write` e o contrato de retorno fica com uma causa só.
- Vazamento é impossível por construção: o valgrind roda zerado sem nenhum
  `free` no código.

## Escrita imediata, sem buffer próprio

Cada byte vai direto ao `write`. A referência buferiza e faz menos syscalls;
aqui a simplicidade vale mais: o retorno de cada escritor é o número de bytes
escritos ou `-1`, a soma do laço é a contagem final, e a propagação de erro é
uma comparação por chamada. O conteúdo do fluxo é idêntico ao da referência —
o custo é de desempenho, irrelevante no domínio do projeto.

## `va_list` por ponteiro

Todo `va_arg` acontece via `va_list *`. Passar `va_list` por valor entre
funções funciona no x86-64 por acidente da ABI e quebra no ARM64 da Apple; o
ponteiro funciona nos dois. O argumento completo está em
[fluxo.md](fluxo.md).

## Obrigatória e bônus como implementações separadas

As duas variantes não compartilham nenhum arquivo: a obrigatória são 7
funções diretas, o bônus reconstrói a biblioteca com outros 7 arquivos. A
alternativa — uma implementação só, onde a obrigatória é o bônus sem flags —
faria a metade simples do projeto depender da metade difícil.

O custo é duplicar o núcleo de escrita, e ele é pequeno: `pf_putchar`, com 3
linhas, é o único código idêntico nos dois lados; o resto diverge de verdade
(recursão contra buffer, string contra campo). O que se compra é isolamento
total — um defeito introduzido no bônus não tem como quebrar a variante
obrigatória.

## Um montador único para todos os numéricos

`%d`, `%i`, `%u`, `%x`, `%X` e `%p` não nulo passam pelo mesmo `put_num`, com
o **prefixo como string**: `"-"`, `"+"`, `" "`, `"0x"`, `"0X"`, `"+0x"`,
`" 0x"` ou `""`. A matriz de interações flag × conversão colapsa em "cada
conversão escolhe seu prefixo e entrega os dígitos":

- `%+05d` com 42 → prefixo `"+"`, zeros de largura depois dele → `[+0042]`;
- `%#08x` com 255 → prefixo `"0x"` → `[0x0000ff]`;
- `% 015p` → prefixo `" 0x"` → `[ 0x000000001234]`.

Todas as linhas numéricas de
[../06-aceitacao/casos.md](../06-aceitacao/casos.md) saem das contagens de
[../05-bonus/montagem.md](../05-bonus/montagem.md); não há caso especial
fora do montador.

## Dígitos: recursão na obrigatória, buffer no bônus

A obrigatória emite na ordem certa por recursão, sem buffer nenhum — não há
largura nem precisão, então nada precisa ser sabido antes de escrever. No
bônus, largura e precisão dependem do **comprimento** dos dígitos antes do
primeiro byte sair, então `render_base` preenche um buffer de trás para a
frente e o montador o mede com `pf_strlen`
([../04-emissao/numeros.md](../04-emissao/numeros.md)).

## Reconstrução canônica da diretiva desconhecida

A referência não ecoa a diretiva desconhecida como veio: reimprime a partir
do estado analisado — flags deduplicadas, em ordem fixa, com regras de
supressão. `%0-5r` → `[%-5r]`, `%+ r` → `[%+r]`, `%##7r` → `[%#7r]`, `%.r` →
`[%.0r]`. Ecoar o texto original divergiria em todos esses. É também o motivo
de a análise rodar antes do teste de conversão conhecida
([fluxo.md](fluxo.md)).

## Precisão com sentinela −1

`0` é precisão legal e diferente de ausente, então `prec` usa −1 para
"ausente" ([tipos.md](tipos.md)). O sentinela também dá a `conv_ptr` um jeito
de uma linha de reproduzir o fato de `(nil)` ignorar a precisão.
