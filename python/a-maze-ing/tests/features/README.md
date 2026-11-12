# Casos de teste do A-Maze-ing (Gherkin)

Cada requisito do subject A-Maze-ing v2.3 (`en.subject.pdf`, tradução `pt_br.subject.md`) tem
pelo menos um cenário: obrigatórios, recomendados, opcionais, bônus e informativos. Os
arquivos seguem a ordem de implementação.

- [`../README.md`](../README.md): instalar e rodar a suíte, achar e criar um passo.
- [`decisoes.md`](decisoes.md): tabelas D e I, citadas pelas tags `@decisao-Dnn` e `@decisao-Inn`.
- [`vocabulario.md`](vocabulario.md): frases dos passos, tipos de parâmetro e listas fechadas.

## Ordem

| # | Arquivo | Escopo |
|---|---|---|
| 00 | `00-contexto.feature` | capa, sumário, prefácio |
| 01 | `01-ambiente.feature` | Python 3.10+, venv, `.gitignore`, suíte de testes |
| 02 | `02-makefile.feature` | regras `install`, `run`, `debug`, `clean`, `lint`, `lint-strict` |
| 03 | `03-qualidade.feature` | flake8, mypy, type hints, docstrings, exceções, context managers |
| 04 | `04-uso-cli.feature` | comando, nome do arquivo principal, argumento único, erros de arquivo |
| 05 | `05-configuracao.feature` | formato `KEY=VALUE`, chaves obrigatórias, validação, config padrão |
| 06 | `06-grade-e-paredes.feature` | paredes por célula, entrada/saída, borda, coerência |
| 07 | `07-geracao-e-seed.feature` | aleatoriedade, seed, conectividade, classe geradora |
| 08 | `08-padrao-42.feature` | padrão "42", omissão em labirinto pequeno |
| 09 | `09-modo-perfeito.feature` | `PERFECT=True` |
| 10 | `10-caminho-mais-curto.feature` | caminho mais curto válido |
| 11 | `11-modo-pacman.feature` | `PERFECT=False` (tabuleiro Pac-Man) |
| 12 | `12-areas-abertas.feature` | corredores de no máximo 2 células, nenhum 3x3 aberto |
| 13 | `13-arquivo-de-saida.feature` | formato hexadecimal, rodapé, analyzer, exemplo do subject |
| 14 | `14-representacao-visual.feature` | renderização ASCII ou MLX |
| 15 | `15-interacoes.feature` | regenerar, mostrar/ocultar caminho, cores, sair |
| 16 | `16-modulo-reutilizavel.feature` | `MazeGenerator`, documentação, pacote `mazegen-*` |
| 17 | `17-licenca.feature` | `LICENSE.md` |
| 18 | `18-readme.feature` | `README.md` |
| 19 | `19-bonus.feature` | sem becos sem saída, vários algoritmos, animação |
| 20 | `20-uso-de-ia.feature` | Capítulo II — instruções sobre IA |
| 21 | `21-submissao-e-defesa.feature` | Capítulo IX — submissão e avaliação |

## Config base

"O config base" nos cenários é este arquivo; cada cenário diz só o que muda nele.

```text
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

"A opção de sair pelo stdin" é a linha `4` (Quit) enviada ao menu; os testes a enviam para que
o programa termine sem intervenção humana.

## Referências

- "Raiz do repositório" nos cenários é a pasta `project/`, que vira a raiz do repositório entregue
  à 42.
- `@pdf-p09-L13-L15`: página **física** do PDF (p01–p20, a numeração do visualizador; o número
  impresso no rodapé é a página física − 1) e linhas 13 a 15 dessa página.
- Linha do PDF = n-ésima linha não vazia da página, de cima para baixo, contando o cabeçalho
  "A-Maze-ing … This is the way" nas páginas que o têm. Figuras não contam linha; são citadas
  como `@pdf-p11-figura`.
- `@md-L186`: linha 186 do `pt_br.subject.md`.
- Acima de cada cenário, `# pdf: "..."` é o trecho do PDF em inglês e `# md:  "..."` é o trecho
  correspondente do `pt_br.subject.md`, sem a marcação Markdown (marcador de lista, negrito,
  itálico, `>`). As aspas tipográficas do PDF (`’`, `‘`, `“`, `”`) aparecem como aspas retas.
  `# figura: "..."` é texto em inglês que só existe dentro de uma imagem; o `# md:` dela traz a
  descrição ou a legenda traduzida da figura.
- `# regua: "..."` é o trecho em inglês da régua de avaliação (`regua/regua_N.png`),
  `# regua-md: "..."` é o trecho correspondente de `regua/regua_N.pt_br.md` e `@regua-pN` é a
  página da régua. A régua é o roteiro do avaliador: os cenários a citam quando ela exige algo
  que o subject não detalha ou resolve uma dúvida do subject.

## Tags

| Tag | Significado |
|---|---|
| `@obrigatorio` | "must" no PDF, ou frase imperativa que define requisito do programa ou da entrega |
| `@recomendado` | "should", "recommended", "prefer" no PDF, e os conselhos dos Capítulos II e IX (a tradução usa "deve" nesses pontos; vale o PDF) |
| `@opcional` | "may", "optional", "can" |
| `@bonus` | Capítulo VIII ou recompensado como bônus |
| `@informativo` | contexto sem exigência própria |
| `@derivado` | consequência lógica de requisito, exemplo ou figura |
| `@decisao-Dnn` | o subject sozinho não define o comportamento; a tabela D de [`decisoes.md`](decisoes.md) diz o que vale e com que base |
| `@decisao-Inn` | o cenário é genérico ("a opção de regenerar", "a exceção do módulo"); a tabela I fixa o valor concreto |
| `@regua-pN` | o cenário cita a página N da régua de avaliação |
| `@automatizado` | verificável por pytest, subprocesso com stdin roteirizado, validador da suíte, `maze_analyzer.py`, `make` ou build em venv limpo |
| `@manual` | verificável por inspeção ou na defesa |

## Validador da suíte

O `maze_analyzer.py` termina com código 0 sempre que consegue ler o arquivo, mesmo com veredito
ruim: os testes leem a linha `Verdict:`. Ele não verifica borda fechada, áreas 3x3, entrada
diferente da saída, o caminho do rodapé, a forma do "42", saída em célula fechada nem o
formato estrito do texto. Esses itens exigem um validador próprio da suíte, citado nos
cenários como "o validador da suíte".
