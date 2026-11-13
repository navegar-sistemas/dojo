---
sidebar_position: 1
title: O que o README precisa ter
---

# O que o README precisa ter

Com o programa pronto, falta a apresentação do projeto: o arquivo `README.md`, na raiz do
repositório. O enunciado exige esse arquivo e lista o que ele precisa conter. Esta página
traduz essa lista, seção por seção; as próximas mostram como escrever cada uma.

## O que é o README

O `README.md` ("leia-me") é o texto de apresentação de um repositório. O GitHub e sites
parecidos o mostram logo abaixo da lista de arquivos. Ele é escrito em **Markdown**: texto comum
com algumas marcações simples, como `#` no começo da linha para um título, `*texto*` para
itálico, `**texto**` para negrito e linhas com `|` para tabelas.

Neste projeto ele tem três leitores:

- **o avaliador**, que o lê antes de rodar qualquer coisa e confere cada seção exigida;
- **qualquer pessoa** que chegue ao repositório. O enunciado diz o objetivo: alguém que não
  conhece o projeto (um colega, um avaliador, um recrutador) precisa entender rapidamente
  do que se trata, como executá-lo e onde aprender mais sobre o assunto;
- **quem instala o pacote `mazegen`**. O `pyproject.toml`, o arquivo que descreve o pacote,
  declara `readme = "README.md"` ([parte 3](../03-ambiente/04-pyproject.md)), então o README vai
  dentro dos arquivos de instalação do pacote (o *wheel* e o *sdist*,
  [parte 9](../09-gerador/08-o-pacote.md)), como a descrição longa dele.

## A primeira linha

O enunciado exige que a **primeiríssima** linha do arquivo esteja em itálico e traga, em inglês,
uma frase fixa que ele dá, seguida do login de cada autor:

```markdown
*This project has been created as part of the 42 curriculum by macoelho.*
```

- O **login** é o seu nome de usuário. Troque `macoelho` pelo **seu**. Com mais de um autor, separe por vírgula e espaço: `by login1, login2.`
- Em Markdown, o texto entre um asterisco de abertura e um de fechamento sai em itálico. O ponto
  final fica **dentro** dos asteriscos. (O sublinhado, `_texto_`, também faz itálico; o projeto
  escolheu o asterisco.)
- Nada vem antes dela: nem título, nem linha em branco, nem comentário.

O mesmo login aparece no campo `authors` do `pyproject.toml` ([parte 3](../03-ambiente/04-pyproject.md))
e na linha `Copyright` do `LICENSE.md`, o arquivo da licença
([parte 9](../09-gerador/06-a-licenca.md)). Os três arquivos precisam dizer a mesma coisa.

## O idioma

O enunciado recomenda inglês e aceita o idioma principal do lugar onde o projeto é feito. O projeto escolheu inglês,
como o código e as mensagens do programa.

## O que o enunciado exige, seção por seção

O enunciado pede três seções com nome fixo:

- **Description** ("descrição"): apresenta o projeto com clareza, com o objetivo e uma visão
  geral curta.
- **Instructions** ("instruções"): tudo o que é preciso para compilar, instalar e executar.
- **Resources** ("recursos"): referências clássicas sobre o assunto (documentação, artigos,
  tutoriais) e uma descrição de **como a inteligência artificial foi usada**: para quais tarefas
  e em quais partes do projeto.

E, para este projeto, mais estes assuntos, sem nome de seção definido:

- a **estrutura e o formato completos do arquivo de configuração**;
- o **algoritmo** de geração escolhido e **por que** ele foi escolhido;
- **qual parte do código é reutilizável**, e como reutilizá-la. Outro capítulo do enunciado
  acrescenta que o README precisa ter também a documentação curta do módulo reutilizável: como
  criar e usar o gerador, como passar parâmetros, como ler o labirinto gerado e uma solução, com
  um exemplo;
- a **equipe e a gestão do projeto**: o papel de cada membro, o planejamento previsto e como ele
  mudou até o fim, o que funcionou bem e o que poderia melhorar, e as ferramentas usadas.

Por fim, o enunciado pede que o README descreva as funcionalidades avançadas, se houver, e dá
como exemplos "múltiplos algoritmos" e "opções de exibição". Aqui isso inclui o **bônus** do
projeto ([parte 16](../16-bonus/01-o-tabuleiro-sem-becos.md)).

## As oito seções deste README

O README do projeto tem um título `# A-Maze-ing` e oito seções `##`, nesta ordem. Os nomes das
três seções fixas são os do enunciado; os das outras cinco são escolha do projeto.

| Seção | O que responde |
|---|---|
| `Description` | o que o projeto é e o que ele faz |
| `Instructions` | como instalar, executar e usar o menu |
| `Configuration file` | o formato do arquivo de configuração, as chaves e as regras de leitura |
| `Algorithm` | o algoritmo de cada parte da geração e o motivo de cada escolha |
| `Reusable module` | qual parte é reutilizável, como instalá-la e a documentação curta dela |
| `Team and project management` | papéis, planejamento, o que funcionou e o que melhoraria, ferramentas |
| `Bonus` | as funcionalidades além da parte obrigatória |
| `Resources` | as referências e como a IA foi usada |

A ordem segue o caminho de quem chega ao projeto: o que é, como roda, como se configura, como
funciona por dentro, como se reutiliza, quem fez, e onde aprender mais.

## O que vale para todas as seções

- **Só o que existe.** Uma funcionalidade descrita no README e ausente do programa é a primeira
  coisa que o avaliador testa. O enunciado sugere três bônus (um tabuleiro de Pac-Man sem
  nenhum beco sem saída, vários algoritmos de geração e uma animação da geração) e, entre as
  interações do menu, uma opcional: escolher cores específicas para o "42". Este projeto fez só
  o primeiro bônus. Ele não tem vários algoritmos nem animação, e o "42" sai sempre em cinza,
  sem opção no menu para trocar essa cor. Por isso o README não fala de nada disso.
- **Valores reais.** Comandos que funcionam se colados no terminal, o `config.txt` exatamente
  como está no repositório, mensagens exatamente como o programa as imprime.
- **Você explica tudo.** O enunciado tem um capítulo sobre o uso de IA: ela pode ajudar, mas só
  entra no projeto o que você entende por completo e consegue explicar. Isso vale também para o
  README: o que estiver escrito ali, você defende na avaliação.
