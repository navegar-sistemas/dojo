---
sidebar_position: 2
title: Descrição, instruções e config
---

# Descrição, instruções e config

Quem abre o README de um projeto desconhecido pergunta primeiro: o que é isto, como eu rodo e
como eu configuro. As três primeiras seções respondem nessa ordem. O texto completo de cada uma
está no [README completo](./05-o-readme-completo.md); esta página explica o que entra e por quê.

## Description

O enunciado pede o objetivo do projeto e uma visão geral curta. A seção abre com o objetivo em
uma frase:

```markdown
A-Maze-ing generates a maze from a configuration file, writes it to an
output file in hexadecimal and shows it in the terminal.
```

("O A-Maze-ing gera um labirinto a partir de um arquivo de configuração, grava-o num arquivo de
saída em hexadecimal e o mostra no terminal.") **Hexadecimal** é o jeito de escrever os números
de 0 a 15 com um caractere só, `0` a `9` e depois `a` a `f`; cada célula vira um desses
caracteres no arquivo ([parte 1](../01-o-problema/02-paredes-em-bits.md)).

Depois vem a visão geral, em tópicos curtos, um para cada parte visível do projeto. Cada tópico
diz **o que é** e, quando cabe, **a regra** que a define:

- **Perfect mode** e **Pac-Man mode**: os dois tipos de labirinto, a chave que escolhe cada um
  (`PERFECT=True` ou `False`) e qual é o padrão ([parte 1](../01-o-problema/05-perfeito-e-pac-man.md));
- **The "42"**: as 18 células fechadas que desenham o número, o tamanho mínimo de labirinto
  (9x7) e o aviso quando ele não cabe;
- **Output file**: um dígito hexadecimal por célula, depois a entrada, a saída e o caminho mais
  curto;
- **Display**: as cores do desenho e as quatro opções do menu;
- **Reusable module**: o pacote `mazegen` e os dois arquivos que o distribuem.

O avaliador usa essa lista como roteiro: cada item é algo que ele vai querer ver funcionando.

## Instructions

Tudo o que alguém precisa para sair de uma cópia recém-baixada do repositório e ver o labirinto
na tela:

- **o que precisa estar instalado**: Python 3.10 ou mais novo (o mínimo do enunciado) e o
  programa `make`;
- **os dois comandos**, num bloco de código, com um comentário do que cada um faz: `make install`
  cria o ambiente virtual `.venv`, uma pasta com um Python e as ferramentas só deste projeto
  ([parte 3](../03-ambiente/01-o-ambiente-virtual.md)); `make run` executa o programa;
- **o que o `make run` faz por baixo**: é o mesmo que `python3 a_maze_ing.py config.txt`, com o
  Python do `.venv`;
- **como usar outro arquivo de configuração**: `.venv/bin/python a_maze_ing.py my_config.txt`;
- **a tabela das opções do menu**, de `1` a `4`;
- **a tabela das outras regras do `Makefile`**, o arquivo de atalhos de comandos
  ([parte 3](../03-ambiente/02-makefile-instalar-e-rodar.md)): `lint`, `lint-strict`, `debug`,
  `clean` e `build`.

O comando `python3 a_maze_ing.py config.txt` aparece escrito por extenso: é o comando que o
enunciado manda executar, e o avaliador procura por ele.

Para rodar com outro arquivo, o README manda usar `.venv/bin/python`, o Python do ambiente
virtual que o `make install` cria e que todas as regras do `Makefile` usam. Assim o comando roda
do mesmo jeito que o `make run`, com as mesmas ferramentas, e é o mesmo comando que o tutorial
usa em todos os exemplos. O `python3` também funcionaria (o `.venv` é criado a partir dele, e o
programa só usa a biblioteca padrão do Python), mas o README fica com um jeito só de rodar.

## Configuration file

O enunciado pede "a estrutura e o formato completos" do arquivo de configuração. Isso é mais do
que listar as chaves: inclui as regras de leitura que o usuário só descobriria errando. A seção
tem cinco partes.

1. **O formato**: um par `CHAVE=valor` por linha; linhas que começam com `#` são comentários;
   linhas em branco são puladas; coordenadas no formato `x,y`, com `x` a coluna e `y` a linha,
   contando de 0 a partir do canto de cima à esquerda.
2. **A tabela das chaves**: as seis obrigatórias do enunciado (`WIDTH`, `HEIGHT`, `ENTRY`,
   `EXIT`, `OUTPUT_FILE`, `PERFECT`) e a opcional `SEED`, que este projeto acrescentou, cada uma
   com os valores aceitos.
3. **As regras de leitura**, todas decididas na [parte 11](../11-configuracao/06-linha-a-linha.md):
   - chaves e `True`/`False` em maiúsculas ou minúsculas;
   - espaços em volta da chave e do valor ignorados;
   - a linha dividida no **primeiro** `=`;
   - chave desconhecida ignorada; chave repetida vale a **última**;
   - um `#` depois de um valor faz parte do valor (que então fica inválido);
   - todas as chaves que faltam listadas num único erro;
   - os limites: tamanho de 1 a 100, entrada diferente da saída e fora do "42", e o tamanho
     mínimo para o modo Pac-Man (parte 11, [regras 1 a 3](../11-configuracao/03-a-ordem-das-validacoes.md)
     e [4 a 7](../11-configuracao/04-o-42-e-o-arquivo-completo.md)).
4. **O formato dos erros**: todo erro de configuração ou de execução é uma linha
   `Error: <causa>` na saída de erros, com código de saída 1
   ([parte 14](../14-menu-e-main/05-a-barreira-de-erros.md)). A exceção é a linha de uso,
   impressa quando o programa recebe zero ou mais de um argumento: ela começa com `Usage:`, no
   formato tradicional dos programas de terminal
   ([parte 14](../14-menu-e-main/04-o-composition-root.md)).
5. **O `config.txt` do repositório**, inteiro, num bloco de código.

Várias dessas regras são escolhas do projeto (o limite de 100, a chave repetida que vale a
última, a chave desconhecida ignorada), e não do enunciado. Por isso mesmo precisam estar
escritas: o README é o lugar onde o usuário as encontra sem ler o código.
