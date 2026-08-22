# Decisões de desenho

Escolhas que não são óbvias a partir do contrato, com a evidência que as
sustenta.

## A glibc medida como contrato, não "escolhas razoáveis"

A linguagem deixa em aberto boa parte do que uma `printf` faz: `%p` de
`NULL`, `%s` de `NULL`, flag `0` em `%c`, diretiva desconhecida, formato
incompleto, `+` em `%p`. Em vez de decidir caso a caso, o projeto fixa uma
regra única: **o que a glibc 2.36 faz, medido, é o contrato**. Cada canto foi
sondado na referência e virou linha de tabela em
[../06-aceitacao/casos.md](../06-aceitacao/casos.md).

O ganho é duplo: a reimplementação não tem nenhuma decisão ambígua sobrando, e
a verificação vira um `cmp` — o harness diferencial de
[../06-aceitacao/validacao.md](../06-aceitacao/validacao.md) compila o mesmo
lote com `printf` e com `ft_printf` e exige igualdade byte a byte, inclusive
dos retornos. Vários desses cantos surpreendem quem confia na intuição:
`%08p` com `NULL` alinha com **espaços**, `%.3p` não trunca `(nil)`, `%+p`
imprime `+0x…`, e `%-5r` vira `%-5r` mas `%0-5r` **também** vira `%-5r`.

## Sem alocação no heap

O texto mais longo que uma conversão gera sozinha é um número: 20 dígitos
decimais de um `unsigned long` de 64 bits (o hexadecimal fica em 16). Buffers
de pilha de 24 bytes cobrem qualquer conversão; padding de largura é emitido
em laço, nunca materializado — `"%2000d"` não precisa de um buffer de 2000
bytes. Consequências:

- não existe caminho de falha de `malloc`, então o único erro possível é o da
  `write`, e o contrato de retorno fica com uma causa só;
- vazamento é impossível por construção — o valgrind de
  [../06-aceitacao/validacao.md](../06-aceitacao/validacao.md) roda zerado sem
  nenhum `free` no código.

## Escrita imediata, sem buffer próprio

Cada byte vai direto ao `write`. A referência buferiza e faz menos syscalls;
aqui a simplicidade vale mais: o retorno de cada escritor é o número de bytes
escritos ou `-1`, a soma do laço é a contagem final, e a propagação de erro é
uma comparação por chamada. O conteúdo do fluxo é idêntico ao da referência —
o custo é só de desempenho, irrelevante no domínio do projeto.

## `va_list` por ponteiro

Decisão de portabilidade com forma de assinatura: todo `va_arg` acontece via
`va_list *`. O argumento de ABI completo está em
[fluxo.md](fluxo.md#va_list-por-ponteiro); a versão curta é que passar
`va_list` por valor entre funções funciona no x86-64 por acidente da ABI e
quebra no ARM64 da Apple, e o ponteiro funciona nos dois.

## Obrigatória e bônus como implementações separadas

As duas variantes não compartilham nenhum arquivo: a obrigatória são 7
funções diretas, o bônus reconstrói a biblioteca com outros 7 arquivos. A
alternativa — uma implementação única onde a obrigatória é o bônus sem flags —
faria a metade simples do projeto depender da metade difícil.

O custo da separação é duplicar o núcleo de escrita, e ele é pequeno e medido:
`pf_putchar` (3 linhas) é o único código idêntico nos dois lados; o resto
diverge de verdade (recursão vs buffer, string vs campo). O preço aceito
compra isolamento total: um defeito introduzido no bônus não tem como quebrar
a variante obrigatória.

## Um montador único para todos os numéricos

`%d`, `%i`, `%u`, `%x`, `%X` e `%p` (não nulo) passam pelo mesmo `put_num`,
com o **prefixo como string**: `"-"`, `"+"`, `" "`, `"0x"`, `"0X"`, `"+0x"`,
`" 0x"` ou `""`. A matriz inteira de interações flag × conversão colapsa em
"cada conversão escolhe seu prefixo e entrega os dígitos":

- `"%+05d"` com 42 → prefixo `"+"`, zeros de largura depois dele → `[+0042]`;
- `"%#08x"` com 255 → prefixo `"0x"` → `[0x0000ff]`;
- `"% 015p"` → prefixo `" 0x"` → `[ 0x000000001234]`.

Todas as linhas medidas dos numéricos em
[../06-aceitacao/casos.md](../06-aceitacao/casos.md) saem dessas três contagens
de [../05-bonus/montagem.md](../05-bonus/montagem.md) — não há caso especial
fora do montador.

## Dígitos: recursão na obrigatória, buffer no bônus

A obrigatória emite na ordem certa por recursão (`pf_putnbr_base`), sem
buffer nenhum — não há largura nem precisão, então nada precisa ser sabido
antes de escrever. No bônus a largura e a precisão dependem do **comprimento**
dos dígitos antes do primeiro byte sair, então `render_base` preenche um
buffer de trás para a frente e o montador mede com `pf_strlen`
([../04-emissao/numeros.md](../04-emissao/numeros.md)).

## Reconstrução canônica da diretiva desconhecida

A referência **não ecoa** a diretiva desconhecida como veio: ela a reimprime a
partir do estado analisado — flags deduplicadas, em ordem fixa, com regras de
supressão. Medido: `%0-5r` → `[%-5r]`, `%+ r` → `[%+r]`, `%##7r` → `[%#7r]`,
`%.r` → `[%.0r]`. Ecoar o texto original divergiria em todos esses; a
implementação reconstrói ([../05-bonus/semantica.md](../05-bonus/semantica.md)).
É também o motivo de a análise rodar antes do teste de conversão conhecida
([fluxo.md](fluxo.md)).

## Precisão com sentinela −1

`0` é precisão legal (`"%.0d"` zera os dígitos do 0) e diferente de ausente
(`"%d"` imprime `[0]`). O campo `prec` usa −1 para "ausente", o que também dá
à `conv_ptr` um jeito de uma linha para o fato medido de `(nil)` ignorar a
precisão: `f->prec = -1` e delega ao caminho de string
([../03-arquitetura/tipos.md](tipos.md)).
