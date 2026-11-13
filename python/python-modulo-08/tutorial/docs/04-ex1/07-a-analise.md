---
sidebar_position: 7
title: A análise
---

# A análise

Com as três bibliotecas instaladas, o programa gera 1000 "dados da Matrix" com o numpy, calcula
uma tendência com o pandas e desenha os dois num gráfico com o matplotlib. A função entra depois
de `show_install_help`:

```python
def run_analysis() -> None:
    np = importlib.import_module("numpy")
    pd = importlib.import_module("pandas")
    matplotlib = importlib.import_module("matplotlib")
    matplotlib.use("Agg")
    plt = importlib.import_module("matplotlib.pyplot")

    print("Analyzing Matrix data...")
    rng = np.random.default_rng(1999)
    steps = rng.normal(0.0, 1.0, DATA_POINTS)
    data = pd.DataFrame({"signal": np.cumsum(steps)})
    data["trend"] = data["signal"].rolling(window=50).mean()
    print(f"Processing {len(data)} data points...")

    print("Generating visualization...")
    figure, axes = plt.subplots(figsize=(10, 5))
    axes.plot(data.index, data["signal"], color="#2a78d6",
              linewidth=1.5, label="signal")
    axes.plot(data.index, data["trend"], color="#eb6834",
              linewidth=2, label="trend (50-point mean)")
    axes.set_title("Matrix data")
    axes.set_xlabel("data point")
    axes.set_ylabel("signal")
    axes.grid(color="#e5e5e5")
    axes.legend()
    figure.savefig(OUTPUT)
    plt.close(figure)
```

## As importações

As três bibliotecas entram por `importlib.import_module`, com os nomes curtos de costume: `np`
para o numpy, `pd` para o pandas e `plt` para o `matplotlib.pyplot`, a parte do matplotlib que
desenha gráficos. Quando esta função roda, `check_dependencies` já confirmou que as três existem.

`matplotlib.use("Agg")` escolhe, **antes** de carregar o `pyplot`, o jeito de desenhar: o `Agg`
desenha direto num arquivo de imagem, sem abrir janela. O programa só grava o gráfico, e assim ele
roda igual num terminal sem tela gráfica, como o de um servidor acessado pela rede.

## O numpy gera os dados

- `np.random.default_rng(1999)` cria um **gerador de números aleatórios**. O número entre
  parênteses é a **semente** (*seed*): o mesmo gerador com a mesma semente produz sempre a mesma
  sequência. A semente fixa é **escolha do tutorial**: toda execução gera os mesmos dados e o
  mesmo gráfico, o que permite conferir o resultado. 1999 é o ano do filme;
- `rng.normal(0.0, 1.0, DATA_POINTS)` sorteia 1000 números de uma **distribuição normal** com
  média 0 e desvio padrão 1: números em torno de 0, quase todos entre -3 e 3. O resultado é um
  **array** do numpy, uma lista de números em que as contas valem para todos os itens de uma vez;
- `np.cumsum(steps)` é a **soma acumulada**: o item `i` do resultado é a soma dos itens de 0 até
  `i`. Com passos aleatórios, a soma acumulada é um **passeio aleatório**, uma linha que sobe e
  desce como um sinal medido ao longo do tempo.

O enunciado exige que os dados venham do numpy, e não de uma lista escrita no código nem de
`range()`: todos os 1000 números saem do gerador.

## O pandas organiza os dados

- `pd.DataFrame({"signal": ...})` cria um **DataFrame**, uma tabela do pandas: cada chave do
  dicionário vira uma coluna, aqui a coluna `signal` com os 1000 valores. Cada linha tem um número,
  o **índice**, de 0 a 999 (`data.index`);
- `data["signal"].rolling(window=50).mean()` calcula a **média móvel**: para cada linha, a média
  dos 50 valores até ela. É uma tendência, uma versão suavizada do sinal. As 49 primeiras linhas
  ainda não têm 50 valores para trás e ficam sem média (o valor `NaN`, *not a number*, que o
  gráfico não desenha);
- `data["trend"] = ...` guarda a média numa coluna nova da mesma tabela;
- `len(data)` é o número de linhas: 1000.

## O matplotlib desenha

- `plt.subplots(figsize=(10, 5))` cria uma **figura** (a imagem inteira, de 10 por 5 polegadas)
  e um par de **eixos** (a área do gráfico), devolvidos como uma tupla;
- cada `axes.plot(x, y, ...)` desenha uma linha: o índice no eixo horizontal e a coluna no
  vertical. `color` é a cor no formato `#rrggbb` (as quantidades de vermelho, verde e azul, cada
  uma com dois dígitos em base 16, de `00` a `ff`), `linewidth` a espessura e `label` o nome que
  aparece na legenda;
- `set_title`, `set_xlabel` e `set_ylabel` escrevem o título e os nomes dos eixos; `grid` desenha
  uma grade clara ao fundo; `legend` mostra a legenda;
- `figure.savefig(OUTPUT)` grava a imagem em `matrix_analysis.png`, na pasta onde o programa foi
  rodado. O formato sai da extensão do nome: `.png`;
- `plt.close(figure)` libera a memória da figura.

O gráfico gravado:

![Gráfico de linhas com 1000 pontos: o sinal, em azul, sobe e desce entre cerca de -20 e 25, e a tendência, em laranja, é a média dos 50 pontos anteriores, uma linha suave que acompanha o sinal a partir do ponto 49](/img/ex1/matrix_analysis.png)

As mensagens `Analyzing Matrix data...`, `Processing 1000 data points...` e
`Generating visualization...` são as da saída do enunciado, na mesma ordem; o `1000` vem do
tamanho da tabela.

## Os tipos

O mypy vê `np`, `pd`, `matplotlib` e `plt` como módulos quaisquer, e tudo o que sai deles (o
gerador, a tabela, a figura) como `Any` ([Importar pelo nome](../02-conceitos/03-importar-pelo-nome.md)).
Por isso as variáveis da função não têm anotação, e a função só troca com o resto do programa
tipos simples: não recebe nada e devolve `None`.
