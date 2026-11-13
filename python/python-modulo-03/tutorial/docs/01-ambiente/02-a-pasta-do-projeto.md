---
sidebar_position: 2
title: A pasta do projeto
---

# A pasta do projeto

Cada exercício fica num arquivo próprio, dentro de uma pasta com o número do exercício: `ex0/`,
`ex1/`, até `ex6/`. Crie uma pasta para o projeto, entre nela e crie as sete pastas:

```bash
mkdir data-quest
cd data-quest
mkdir ex0 ex1 ex2 ex3 ex4 ex5 ex6
```

O nome `data-quest` é só uma sugestão; o que o enunciado fixa são as pastas `ex0` a `ex6` e os
nomes dos arquivos. **Todos os comandos daqui em diante são rodados a partir desta pasta**, a
`data-quest`.

Crie também uma pasta `experimentos`, para os programas pequenos que mostram cada ideia antes de
ela entrar num exercício. Eles não fazem parte da entrega:

```bash
mkdir experimentos
```

Ao fim do projeto, a pasta fica assim:

```mermaid
flowchart LR
    root["data-quest/"]
    root --> ex0["ex0/"] --> f0["ft_command_quest.py"]
    root --> ex1["ex1/"] --> f1["ft_score_analytics.py"]
    root --> ex2["ex2/"] --> f2["ft_coordinate_system.py"]
    root --> ex3["ex3/"] --> f3["ft_achievement_tracker.py"]
    root --> ex4["ex4/"] --> f4["ft_inventory_system.py"]
    root --> ex5["ex5/"] --> f5["ft_data_stream.py"]
    root --> ex6["ex6/"] --> f6["ft_data_alchemist.py"]
    root --> exp["experimentos/"]
    root --> venv[".venv/"]
```

A pasta `.venv/` é criada em [O ambiente virtual](./03-o-ambiente-virtual.md). Só os sete arquivos
`.py` das pastas `ex0` a `ex6` são entregues.
