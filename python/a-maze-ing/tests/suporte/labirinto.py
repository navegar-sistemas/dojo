"""Labirinto lido pela suíte e o validador próprio da suíte.

O validador é lógica pura: cada função recebe um ``Labirinto`` e devolve
números, relatos ou a lista de violações de uma propriedade (vazia quando
a propriedade vale). Os passos de ``step_defs/labirinto.py`` só escolhem a
função e transformam as violações em falha.
"""

import re
from collections import deque
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from pathlib import Path

NORTE, LESTE, SUL, OESTE = 1, 2, 4, 8
DIRECOES = {"N": NORTE, "E": LESTE, "S": SUL, "W": OESTE}
DESLOCAMENTOS = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
OPOSTAS = {"N": "S", "E": "W", "S": "N", "W": "E"}
NOMES = {"N": "Norte", "E": "Leste", "S": "Sul", "W": "Oeste"}
FECHADA = 15
COORDENADA = re.compile(r"(\d+),(\d+)")

# Glifos do "42" (D07): as células F do exemplo do subject (pt_br.subject.md,
# grade 25x20, colunas 9 a 15 e linhas 7 a 11), com a coluna livre no meio.
GLIFO_4 = ("X..", "X..", "XXX", "..X", "..X")
GLIFO_2 = ("XXX", "..X", "XXX", "X..", "XXX")
GLIFOS_42 = tuple(
    f"{quatro}.{dois}" for quatro, dois in zip(GLIFO_4, GLIFO_2)
)
LARGURA_DO_42 = 7
ALTURA_DO_42 = 5
LARGURA_MINIMA = 9
ALTURA_MINIMA = 7
MAXIMO_DE_BECOS = 2
MINIMO_DE_ROTAS = 2
LIMITE_DA_LISTA = 5

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"
# Modelos da V23. Os dois "exemplo do subject" transcrevem a figura da p11
# (pt_br.subject.md, linhas 226-249): um com o rodapé x,y puro (D13), outro
# com as anotações "# entry (x,y)" da figura. "perfeito do config base" é o
# OUTPUT_FILE que project-validate/a_maze_ing.py gravou com o config base
# (WIDTH=20 HEIGHT=15 ENTRY=0,0 EXIT=19,14 PERFECT=True SEED=42); a variante
# abre a parede entre (0,0) e (0,1), fora do "42", nos dois lados, e o
# rodapé dela traz o caminho da BFS (I08) recalculado.
MODELOS = {
    "exemplo do subject": "exemplo_do_subject.txt",
    "exemplo do subject com o rodapé anotado": (
        "exemplo_do_subject_anotado.txt"
    ),
    "perfeito do config base": "perfeito_do_config_base.txt",
    "perfeito do config base com uma parede interna aberta": (
        "perfeito_com_parede_interna_aberta.txt"
    ),
}

Celula = tuple[int, int]
Chaves = dict[str, str] | None


@dataclass
class Labirinto:
    """Labirinto produzido num cenário, por arquivo ou pela classe.

    ``texto`` é o conteúdo bruto do arquivo de saída (None quando o
    labirinto veio de ``generate()``); ``padrao`` são as células do "42"
    devolvidas pela classe (None quando o labirinto veio de um arquivo);
    ``arquivo`` é o arquivo que o validador gravou ou releu (V22, V23 e
    V39 numa sessão), None nos demais.
    """

    grade: list[list[int]]
    entrada: Celula | None
    saida: Celula | None
    caminho: str | None
    texto: str | None = None
    rodape: list[str] = field(default_factory=list)
    padrao: frozenset[Celula] | None = None
    arquivo: Path | None = None

    @property
    def largura(self) -> int:
        """Número de colunas da grade.

        Returns:
            A largura, 0 para uma grade vazia.
        """
        return len(self.grade[0]) if self.grade else 0

    @property
    def altura(self) -> int:
        """Número de linhas da grade.

        Returns:
            A altura.
        """
        return len(self.grade)

    def dentro(self, celula: Celula) -> bool:
        """Diz se a célula está dentro da grade.

        Args:
            celula: Coordenada (x, y).

        Returns:
            True quando 0 <= x < largura e 0 <= y < altura.
        """
        x, y = celula
        return 0 <= x < self.largura and 0 <= y < self.altura

    def valor(self, celula: Celula) -> int:
        """Bits de parede da célula.

        Args:
            celula: Coordenada (x, y) dentro da grade.

        Returns:
            O valor de 0 a 15 (N=1, E=2, S=4, W=8).
        """
        x, y = celula
        return self.grade[y][x]

    def aberta(self, celula: Celula, direcao: str) -> bool:
        """Diz se a parede da célula na direção está aberta.

        Args:
            celula: Coordenada (x, y) dentro da grade.
            direcao: "N", "E", "S" ou "W".

        Returns:
            True quando o bit da direção está desligado.
        """
        return not self.valor(celula) & DIRECOES[direcao]

    def vizinhas(self, celula: Celula) -> list[Celula]:
        """Células alcançáveis por uma parede aberta, na ordem N, E, S, W.

        Só conta a passagem que está aberta dos dois lados e que não sai
        da grade.

        Args:
            celula: Coordenada (x, y) dentro da grade.

        Returns:
            As vizinhas ligadas à célula.
        """
        ligadas: list[Celula] = []
        x, y = celula
        for direcao, (dx, dy) in DESLOCAMENTOS.items():
            vizinha = (x + dx, y + dy)
            if (
                self.dentro(vizinha)
                and self.aberta(celula, direcao)
                and self.aberta(vizinha, OPOSTAS[direcao])
            ):
                ligadas.append(vizinha)
        return ligadas

    def celulas(self) -> list[Celula]:
        """Todas as células da grade, linha a linha.

        Returns:
            As coordenadas (x, y).
        """
        return [
            (x, y) for y in range(self.altura) for x in range(self.largura)
        ]


def coordenada(texto: str) -> Celula | None:
    """Converte "x,y" em coordenada.

    Args:
        texto: Linha do rodapé ou valor de ENTRY/EXIT.

    Returns:
        (x, y), ou None se o texto não é exatamente "x,y".
    """
    casado = COORDENADA.fullmatch(texto)
    if casado is None:
        return None
    return int(casado.group(1)), int(casado.group(2))


def ler_saida(texto: str) -> Labirinto:
    """Lê o arquivo de saída: grade, linha vazia e rodapé.

    A grade é lida de forma estrita (cada caractere é um dígito
    hexadecimal); o rodapé é guardado como veio, e entrada, saída e
    caminho ficam None quando a linha não tem o formato esperado. Um
    "\\r" no fim das linhas é tolerado aqui e fica em ``texto``, onde as
    propriedades de formato o acusam.

    Args:
        texto: Conteúdo do arquivo.

    Returns:
        O labirinto lido.

    Raises:
        ValueError: Quando a grade está vazia, tem linhas de tamanhos
            diferentes ou um caractere que não é hexadecimal.
    """
    linhas = [linha.rstrip("\r") for linha in texto.split("\n")]
    fim = linhas.index("") if "" in linhas else len(linhas)
    grade: list[list[int]] = []
    for numero, linha in enumerate(linhas[:fim], start=1):
        if not re.fullmatch(r"[0-9a-fA-F]+", linha):
            raise ValueError(
                f"linha {numero} da grade não é hexadecimal: {linha!r}"
            )
        grade.append([int(digito, 16) for digito in linha])
    if not grade:
        raise ValueError("o arquivo não tem grade")
    if len({len(linha) for linha in grade}) != 1:
        raise ValueError("as linhas da grade têm tamanhos diferentes")
    rodape = linhas[fim + 1:]
    if rodape and rodape[-1] == "":
        rodape.pop()
    entrada = coordenada(rodape[0]) if len(rodape) > 0 else None
    saida = coordenada(rodape[1]) if len(rodape) > 1 else None
    caminho = rodape[2] if len(rodape) > 2 else None
    return Labirinto(grade, entrada, saida, caminho, texto, rodape)


def xy(celula: Celula) -> str:
    """Escreve a célula como nos relatos do validador.

    Args:
        celula: Coordenada (x, y).

    Returns:
        O texto "(x,y)".
    """
    return f"({celula[0]},{celula[1]})"


def lista(celulas: Iterable[Celula]) -> str:
    """Lista curta de células para mensagens de falha.

    Args:
        celulas: Células em qualquer ordem.

    Returns:
        As primeiras células em ordem de leitura e quantas faltaram.
    """
    ordenadas = sorted(celulas, key=lambda celula: (celula[1], celula[0]))
    texto = ", ".join(xy(celula) for celula in ordenadas[:LIMITE_DA_LISTA])
    sobra = len(ordenadas) - LIMITE_DA_LISTA
    return f"{texto} e mais {sobra}" if sobra > 0 else texto


def desenho_em_celulas(
    desenho: Iterable[str], x0: int, y0: int
) -> frozenset[Celula]:
    """Células marcadas com "X" num desenho posto em (x0, y0).

    Args:
        desenho: Linhas do desenho, de cima para baixo.
        x0: Coluna do canto superior esquerdo.
        y0: Linha do canto superior esquerdo.

    Returns:
        As células marcadas.
    """
    return frozenset(
        (x0 + dx, y0 + dy)
        for dy, linha in enumerate(desenho)
        for dx, marca in enumerate(linha)
        if marca == "X"
    )


def padrao_42(largura: int, altura: int) -> frozenset[Celula]:
    """Células do "42" numa grade, pela D07.

    Args:
        largura: Número de colunas.
        altura: Número de linhas.

    Returns:
        As células do desenho centralizado; vazio abaixo de 9x7 (D06).
    """
    if largura < LARGURA_MINIMA or altura < ALTURA_MINIMA:
        return frozenset()
    return desenho_em_celulas(
        GLIFOS_42,
        (largura - LARGURA_DO_42) // 2,
        (altura - ALTURA_DO_42) // 2,
    )


def padrao_de(labirinto: Labirinto) -> frozenset[Celula]:
    """Células do "42" esperadas para as dimensões do labirinto.

    Args:
        labirinto: Labirinto conferido.

    Returns:
        O padrão da D07 para a largura e a altura da grade.
    """
    return padrao_42(labirinto.largura, labirinto.altura)


def forma(celulas: Iterable[Celula]) -> tuple[str, ...]:
    """Desenho das células recortado na caixa que as contém.

    Args:
        celulas: Células do desenho.

    Returns:
        Uma linha por y, com "X" na célula marcada e "." na livre.
    """
    conjunto = set(celulas)
    if not conjunto:
        return ()
    xs = [x for x, _ in conjunto]
    ys = [y for _, y in conjunto]
    return tuple(
        "".join(
            "X" if (x, y) in conjunto else "."
            for x in range(min(xs), max(xs) + 1)
        )
        for y in range(min(ys), max(ys) + 1)
    )


def celulas_f(labirinto: Labirinto) -> frozenset[Celula]:
    """Células com as quatro paredes fechadas (valor F).

    Args:
        labirinto: Labirinto conferido.

    Returns:
        As células de valor 15.
    """
    return frozenset(
        celula for celula in labirinto.celulas()
        if labirinto.valor(celula) == FECHADA
    )


def componentes(celulas: Iterable[Celula]) -> list[frozenset[Celula]]:
    """Componentes 4-conexos de um conjunto de células, por adjacência.

    Args:
        celulas: Células a agrupar.

    Returns:
        Os componentes, do mais à esquerda para o mais à direita.
    """
    restantes = set(celulas)
    grupos: list[frozenset[Celula]] = []
    while restantes:
        inicio = min(restantes)
        grupo = {inicio}
        fila = deque([inicio])
        restantes.discard(inicio)
        while fila:
            x, y = fila.popleft()
            for dx, dy in DESLOCAMENTOS.values():
                vizinha = (x + dx, y + dy)
                if vizinha in restantes:
                    restantes.discard(vizinha)
                    grupo.add(vizinha)
                    fila.append(vizinha)
        grupos.append(frozenset(grupo))
    return sorted(grupos, key=min)


def alcancaveis(
    labirinto: Labirinto,
    inicio: Celula,
    sem: tuple[Celula, Celula] | None = None,
) -> frozenset[Celula]:
    """Células ligadas ao início por passagens abertas dos dois lados.

    Args:
        labirinto: Labirinto conferido.
        inicio: Célula de partida, dentro da grade.
        sem: Passagem (a, b) tratada como fechada, ou None.

    Returns:
        A região alcançável, com o início.
    """
    proibidas = {sem, (sem[1], sem[0])} if sem is not None else set()
    vistas = {inicio}
    fila = deque([inicio])
    while fila:
        atual = fila.popleft()
        for vizinha in labirinto.vizinhas(atual):
            if vizinha not in vistas and (atual, vizinha) not in proibidas:
                vistas.add(vizinha)
                fila.append(vizinha)
    return frozenset(vistas)


def caminho_mais_curto(
    labirinto: Labirinto, entrada: Celula, saida: Celula
) -> str | None:
    """Caminho da busca em largura, vizinhos na ordem N, E, S, W (I08).

    Args:
        labirinto: Labirinto conferido.
        entrada: Célula de partida, dentro da grade.
        saida: Célula de chegada.

    Returns:
        As letras do caminho, ou None quando a saída não é alcançável.
    """
    anteriores: dict[Celula, tuple[Celula, str]] = {}
    vistas = {entrada}
    fila = deque([entrada])
    while fila:
        atual = fila.popleft()
        if atual == saida:
            break
        x, y = atual
        ligadas = labirinto.vizinhas(atual)
        for letra, (dx, dy) in DESLOCAMENTOS.items():
            vizinha = (x + dx, y + dy)
            if vizinha not in vistas and vizinha in ligadas:
                vistas.add(vizinha)
                anteriores[vizinha] = (atual, letra)
                fila.append(vizinha)
    if saida not in vistas:
        return None
    letras: list[str] = []
    atual = saida
    while atual != entrada:
        atual, letra = anteriores[atual]
        letras.append(letra)
    return "".join(reversed(letras))


def incoerencias(labirinto: Labirinto) -> list[tuple[Celula, Celula]]:
    """Pares de vizinhas que codificam a parede comum de jeitos diferentes.

    Args:
        labirinto: Labirinto conferido.

    Returns:
        Os pares (célula, vizinha a leste ou ao sul), em ordem de leitura.
    """
    pares: list[tuple[Celula, Celula]] = []
    for x, y in labirinto.celulas():
        for direcao in ("E", "S"):
            dx, dy = DESLOCAMENTOS[direcao]
            vizinha = (x + dx, y + dy)
            if labirinto.dentro(vizinha) and labirinto.aberta(
                (x, y), direcao
            ) != labirinto.aberta(vizinha, OPOSTAS[direcao]):
                pares.append(((x, y), vizinha))
    return pares


def relato_de_coerencia(labirinto: Labirinto) -> str:
    """Relato do validador em "coerência das paredes" (V73).

    Args:
        labirinto: Labirinto conferido.

    Returns:
        "coerente", ou "incoerente entre (x,y) e (x,y)" para cada par,
        separados por "; ".
    """
    pares = incoerencias(labirinto)
    if not pares:
        return "coerente"
    return "; ".join(
        f"incoerente entre {xy(a)} e {xy(b)}" for a, b in pares
    )


def bloco_aberto(
    labirinto: Labirinto, canto: Celula, largura: int, altura: int
) -> bool:
    """Diz se o bloco tem todas as paredes internas abertas.

    Args:
        labirinto: Labirinto conferido.
        canto: Canto superior esquerdo (x, y) do bloco.
        largura: Colunas do bloco.
        altura: Linhas do bloco.

    Returns:
        True quando o bloco cabe na grade e cada par de células vizinhas
        dentro dele tem passagem aberta dos dois lados.
    """
    x0, y0 = canto
    if not labirinto.dentro((x0 + largura - 1, y0 + altura - 1)):
        return False
    for y in range(y0, y0 + altura):
        for x in range(x0, x0 + largura):
            ligadas = labirinto.vizinhas((x, y))
            if x + 1 < x0 + largura and (x + 1, y) not in ligadas:
                return False
            if y + 1 < y0 + altura and (x, y + 1) not in ligadas:
                return False
    return True


def blocos_abertos(
    labirinto: Labirinto, largura: int, altura: int
) -> list[Celula]:
    """Cantos de todas as janelas abertas do tamanho dado.

    Args:
        labirinto: Labirinto conferido.
        largura: Colunas da janela.
        altura: Linhas da janela.

    Returns:
        O canto superior esquerdo de cada janela aberta.
    """
    return [
        canto for canto in labirinto.celulas()
        if bloco_aberto(labirinto, canto, largura, altura)
    ]


def relato_de_areas(labirinto: Labirinto) -> str:
    """Relato do validador em "áreas abertas" (V73, D11).

    Args:
        labirinto: Labirinto conferido.

    Returns:
        "aceito", ou "recusado: área 3x3" com algum bloco 3x3 aberto.
    """
    return "recusado: área 3x3" if blocos_abertos(labirinto, 3, 3) else (
        "aceito"
    )


def regiao(labirinto: Labirinto) -> frozenset[Celula]:
    """Região alcançável a partir da entrada.

    Args:
        labirinto: Labirinto com entrada dentro da grade.

    Returns:
        As células alcançáveis; vazio sem entrada válida.
    """
    if labirinto.entrada is None or not labirinto.dentro(labirinto.entrada):
        return frozenset()
    return alcancaveis(labirinto, labirinto.entrada)


def passagens(labirinto: Labirinto, celulas: frozenset[Celula]) -> int:
    """Passagens abertas entre células do conjunto, cada uma uma vez.

    Args:
        labirinto: Labirinto conferido.
        celulas: Células consideradas.

    Returns:
        O número de passagens.
    """
    return sum(
        1
        for celula in celulas
        for vizinha in labirinto.vizinhas(celula)
        if vizinha in celulas and vizinha > celula
    )


def rotas_independentes(labirinto: Labirinto) -> int:
    """Ciclos independentes da região alcançável (D10).

    Args:
        labirinto: Labirinto com entrada.

    Returns:
        Passagens menos células mais 1; 0 sem região.
    """
    alcancadas = regiao(labirinto)
    if not alcancadas:
        return 0
    return passagens(labirinto, alcancadas) - len(alcancadas) + 1


def becos_reais(labirinto: Labirinto) -> list[Celula]:
    """Becos sem saída que poderiam ser abertos (D09).

    Beco é célula alcançável com uma só passagem; ele é real quando alguma
    parede fechada dá para uma célula da grade que não é F, como no
    ``maze_analyzer``.

    Args:
        labirinto: Labirinto com entrada.

    Returns:
        Os becos reais, em ordem de leitura.
    """
    becos: list[Celula] = []
    for celula in sorted(regiao(labirinto), key=lambda c: (c[1], c[0])):
        if len(labirinto.vizinhas(celula)) != 1:
            continue
        x, y = celula
        for direcao, (dx, dy) in DESLOCAMENTOS.items():
            vizinha = (x + dx, y + dy)
            if (
                not labirinto.aberta(celula, direcao)
                and labirinto.dentro(vizinha)
                and labirinto.valor(vizinha) != FECHADA
            ):
                becos.append(celula)
                break
    return becos


def candidatas_do_centro(largura: int, altura: int) -> frozenset[Celula]:
    """Células do centro pela D08.

    Args:
        largura: Número de colunas.
        altura: Número de linhas.

    Returns:
        A célula central na dimensão ímpar; as duas do meio na par.
    """
    colunas = (
        {largura // 2} if largura % 2 else {largura // 2 - 1, largura // 2}
    )
    linhas = {altura // 2} if altura % 2 else {altura // 2 - 1, altura // 2}
    return frozenset((x, y) for x in colunas for y in linhas)


def cantos(labirinto: Labirinto) -> list[Celula]:
    """Os quatro cantos da grade.

    Args:
        labirinto: Labirinto conferido.

    Returns:
        Os cantos, sem repetição numa grade de uma linha ou coluna.
    """
    xs = sorted({0, labirinto.largura - 1})
    ys = sorted({0, labirinto.altura - 1})
    return [(x, y) for y in ys for x in xs]


def corredor(
    labirinto: Labirinto, celula: Celula, alcancadas: frozenset[Celula]
) -> bool:
    """Diz se a célula é corredor alcançável a partir da entrada.

    Args:
        labirinto: Labirinto conferido.
        celula: Célula a conferir.
        alcancadas: Região da entrada, calculada uma vez por quem chama.

    Returns:
        True quando ela está na grade, não é F e está na região.
    """
    return (
        labirinto.dentro(celula)
        and labirinto.valor(celula) != FECHADA
        and celula in alcancadas
    )


def relato_de_pacman(labirinto: Labirinto) -> str:
    """Relato do validador em "modo Pac-Man" (V73, D08-D10).

    As checagens seguem esta ordem e a primeira que falha dá o relato:
    rotas independentes, becos reais, cantos e centro, conectividade.

    Args:
        labirinto: Labirinto com entrada.

    Returns:
        "aceito" ou "recusado: <motivo>".
    """
    rotas = rotas_independentes(labirinto)
    if rotas < MINIMO_DE_ROTAS:
        return f"recusado: {rotas} rota(s) independente(s)"
    becos = becos_reais(labirinto)
    if len(becos) > MAXIMO_DE_BECOS:
        return f"recusado: {len(becos)} beco(s) real(is)"
    alcancadas = regiao(labirinto)
    chave = [
        celula for celula in cantos(labirinto)
        if not corredor(labirinto, celula, alcancadas)
    ]
    centro = candidatas_do_centro(labirinto.largura, labirinto.altura)
    if not any(corredor(labirinto, celula, alcancadas) for celula in centro):
        chave.extend(sorted(centro))
    if chave:
        return f"recusado: canto ou centro fechado em {lista(chave)}"
    soltas = inalcancaveis_fora_do_42(labirinto)
    if soltas:
        return f"recusado: {len(soltas)} célula(s) inalcançável(is)"
    return "aceito"


def inalcancaveis_fora_do_42(labirinto: Labirinto) -> frozenset[Celula]:
    """Células fora do "42" da D07 que a entrada não alcança.

    Args:
        labirinto: Labirinto com entrada.

    Returns:
        As células soltas.
    """
    return (
        frozenset(labirinto.celulas()) - padrao_de(labirinto)
        - regiao(labirinto)
    )


@dataclass
class Percurso:
    """Resultado de seguir a solução letra a letra a partir da entrada."""

    celulas: list[Celula]
    letras: list[str] = field(default_factory=list)
    fora: list[str] = field(default_factory=list)
    paredes: list[str] = field(default_factory=list)

    @property
    def fim(self) -> Celula:
        """Célula onde o percurso parou.

        Returns:
            A última célula visitada.
        """
        return self.celulas[-1]


def percorrer(
    labirinto: Labirinto, entrada: Celula, caminho: str
) -> Percurso:
    """Segue o caminho, anotando letras inválidas, saídas e paredes.

    Uma letra inválida é pulada; um passo para fora da grade encerra o
    percurso; um passo por parede fechada é anotado e seguido.

    Args:
        labirinto: Labirinto conferido.
        entrada: Célula de partida.
        caminho: Letras N, E, S e W.

    Returns:
        O percurso, com as células visitadas a partir da entrada.
    """
    percurso = Percurso([entrada])
    atual = entrada
    for numero, letra in enumerate(caminho, start=1):
        if letra not in DESLOCAMENTOS:
            percurso.letras.append(f"letra {numero} é {letra!r}")
            continue
        dx, dy = DESLOCAMENTOS[letra]
        proxima = (atual[0] + dx, atual[1] + dy)
        if not labirinto.dentro(proxima):
            percurso.fora.append(
                f"passo {numero} ({letra}) sai da grade de {xy(atual)}"
            )
            break
        if proxima not in labirinto.vizinhas(atual):
            percurso.paredes.append(
                f"passo {numero} ({letra}) atravessa a parede fechada "
                f"entre {xy(atual)} e {xy(proxima)}"
            )
        percurso.celulas.append(proxima)
        atual = proxima
    return percurso


Verificacao = Callable[[Labirinto, Chaves], list[str]]


def _entrada_e_caminho(
    labirinto: Labirinto,
) -> tuple[Celula, str] | str:
    """Entrada e solução do labirinto, ou o problema que impede usá-las.

    Args:
        labirinto: Labirinto conferido.

    Returns:
        (entrada, caminho), ou a mensagem de violação.
    """
    if labirinto.entrada is None or not labirinto.dentro(labirinto.entrada):
        return f"a entrada {labirinto.entrada} não é célula da grade"
    if labirinto.caminho is None:
        return "o labirinto não tem solução"
    return labirinto.entrada, labirinto.caminho


def _percurso(labirinto: Labirinto) -> Percurso | str:
    """Percurso da solução, ou o problema que impede segui-la.

    Args:
        labirinto: Labirinto conferido.

    Returns:
        O percurso, ou a mensagem de violação.
    """
    dados = _entrada_e_caminho(labirinto)
    if isinstance(dados, str):
        return dados
    return percorrer(labirinto, *dados)


def _no_percurso(
    labirinto: Labirinto, extrair: Callable[[Percurso], list[str]]
) -> list[str]:
    """Violações de um aspecto do percurso da solução.

    Args:
        labirinto: Labirinto conferido.
        extrair: Função que tira do percurso as violações do aspecto.

    Returns:
        As violações, ou o problema que impede seguir a solução.
    """
    percurso = _percurso(labirinto)
    if isinstance(percurso, str):
        return [percurso]
    return extrair(percurso)


def valores_de_0_a_15(labirinto: Labirinto, chaves: Chaves) -> list[str]:
    """Todo valor da grade é um inteiro de 0 a 15.

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        Uma violação por célula fora da faixa.
    """
    return [
        f"a célula {xy(celula)} vale {labirinto.valor(celula)!r}"
        for celula in labirinto.celulas()
        if not isinstance(labirinto.valor(celula), int)
        or not 0 <= labirinto.valor(celula) <= FECHADA
    ]


def borda_fechada(labirinto: Labirinto, chaves: Chaves) -> list[str]:
    """Toda parede voltada para fora da grade está fechada (D12).

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        Uma violação por parede externa aberta.
    """
    violacoes: list[str] = []
    for celula in labirinto.celulas():
        for direcao, (dx, dy) in DESLOCAMENTOS.items():
            fora = (celula[0] + dx, celula[1] + dy)
            if not labirinto.dentro(fora) and labirinto.aberta(
                celula, direcao
            ):
                violacoes.append(
                    f"a célula {xy(celula)} tem a parede externa "
                    f"{NOMES[direcao]} aberta"
                )
    return violacoes


def _coerencia(labirinto: Labirinto, direcao: str) -> list[str]:
    """Pares incoerentes numa direção.

    Args:
        labirinto: Labirinto conferido.
        direcao: "E" para leste-oeste, "S" para norte-sul.

    Returns:
        Uma violação por par incoerente.
    """
    dx, dy = DESLOCAMENTOS[direcao]
    return [
        f"incoerente entre {xy(a)} e {xy(b)}"
        for a, b in incoerencias(labirinto)
        if (b[0] - a[0], b[1] - a[1]) == (dx, dy)
    ]


def vizinhas_leste_oeste(labirinto: Labirinto, chaves: Chaves) -> list[str]:
    """O bit E de (x, y) é igual ao bit W de (x+1, y).

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        Uma violação por par incoerente.
    """
    return _coerencia(labirinto, "E")


def vizinhas_norte_sul(labirinto: Labirinto, chaves: Chaves) -> list[str]:
    """O bit S de (x, y) é igual ao bit N de (x, y+1).

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        Uma violação por par incoerente.
    """
    return _coerencia(labirinto, "S")


def paredes_coerentes(labirinto: Labirinto, chaves: Chaves) -> list[str]:
    """Toda parede compartilhada é codificada igual pelas duas células.

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        Uma violação por par incoerente.
    """
    return [
        f"incoerente entre {xy(a)} e {xy(b)}"
        for a, b in incoerencias(labirinto)
    ]


def bits_na_convencao(labirinto: Labirinto, chaves: Chaves) -> list[str]:
    """Lida com N=1, E=2, S=4, W=8, a grade fecha a borda e é coerente.

    Outra convenção (bits trocados) abriria a borda ou desencontraria
    as vizinhas; a solução, quando há, também atravessa só passagens.

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        As violações de borda, coerência e percurso.
    """
    violacoes = borda_fechada(labirinto, chaves) + paredes_coerentes(
        labirinto, chaves
    )
    if labirinto.caminho is not None:
        violacoes += solucao_atravessa_so_paredes_abertas(labirinto, chaves)
    return violacoes


def _inteiro(chaves: dict[str, str], chave: str) -> int | str:
    """Valor inteiro de uma chave do config.

    Args:
        chaves: Config do cenário.
        chave: Nome da chave.

    Returns:
        O inteiro, ou a mensagem de violação.
    """
    valor = chaves.get(chave)
    if valor is None or not re.fullmatch(r"\d+", valor):
        return f"o config não tem {chave} inteiro: {valor!r}"
    return int(valor)


def dimensoes_do_config(
    labirinto: Labirinto, chaves: dict[str, str]
) -> list[str]:
    """A grade tem HEIGHT linhas de WIDTH colunas.

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário.

    Returns:
        As violações de largura e altura.
    """
    violacoes: list[str] = []
    for chave, medida in (
        ("WIDTH", labirinto.largura),
        ("HEIGHT", labirinto.altura),
    ):
        esperado = _inteiro(chaves, chave)
        if isinstance(esperado, str):
            violacoes.append(esperado)
        elif esperado != medida:
            violacoes.append(f"{chave}={esperado}, mas a grade tem {medida}")
    return violacoes


def x_coluna_y_linha(labirinto: Labirinto, chaves: Chaves) -> list[str]:
    """Colunas = WIDTH, linhas = HEIGHT e a solução lê x como coluna.

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário, ou None.

    Returns:
        As violações de dimensão, de coordenada e de percurso.
    """
    violacoes = dimensoes_do_config(labirinto, chaves) if chaves else []
    violacoes += x_dentro_da_largura(labirinto, chaves)
    violacoes += y_dentro_da_altura(labirinto, chaves)
    if not violacoes:
        violacoes = solucao_termina_na_saida(labirinto, chaves)
    return violacoes


def _extremos(labirinto: Labirinto) -> list[tuple[str, Celula | None]]:
    """Entrada e saída com o nome usado nas mensagens.

    Args:
        labirinto: Labirinto conferido.

    Returns:
        Os pares (nome, célula).
    """
    return [("entrada", labirinto.entrada), ("saída", labirinto.saida)]


def x_dentro_da_largura(labirinto: Labirinto, chaves: Chaves) -> list[str]:
    """O x da entrada e da saída fica de 0 a largura - 1.

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        Uma violação por coordenada ausente ou fora.
    """
    return [
        f"a {nome} {celula} não tem x de 0 a {labirinto.largura - 1}"
        for nome, celula in _extremos(labirinto)
        if celula is None or not 0 <= celula[0] < labirinto.largura
    ]


def y_dentro_da_altura(labirinto: Labirinto, chaves: Chaves) -> list[str]:
    """O y da entrada e da saída fica de 0 a altura - 1.

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        Uma violação por coordenada ausente ou fora.
    """
    return [
        f"a {nome} {celula} não tem y de 0 a {labirinto.altura - 1}"
        for nome, celula in _extremos(labirinto)
        if celula is None or not 0 <= celula[1] < labirinto.altura
    ]


def entrada_diferente_da_saida(
    labirinto: Labirinto, chaves: Chaves
) -> list[str]:
    """Entrada e saída existem e são células diferentes.

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        A violação, se houver.
    """
    if labirinto.entrada is None or labirinto.saida is None:
        return ["o labirinto não tem entrada e saída x,y"]
    if labirinto.entrada == labirinto.saida:
        return [f"entrada e saída são a mesma célula {labirinto.entrada}"]
    return []


def entrada_e_saida_validas(
    labirinto: Labirinto, chaves: Chaves
) -> list[str]:
    """Entrada e saída dentro da grade, fora do F, ligadas e como no config.

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário, ou None (sem comparação com ENTRY/EXIT).

    Returns:
        As violações.
    """
    violacoes = x_dentro_da_largura(labirinto, chaves)
    violacoes += y_dentro_da_altura(labirinto, chaves)
    violacoes += entrada_diferente_da_saida(labirinto, chaves)
    if violacoes:
        return violacoes
    for nome, celula in _extremos(labirinto):
        assert celula is not None
        if labirinto.valor(celula) == FECHADA:
            violacoes.append(f"a {nome} {xy(celula)} tem valor F")
    assert labirinto.saida is not None
    if labirinto.saida not in regiao(labirinto):
        violacoes.append(
            f"a saída {xy(labirinto.saida)} não é alcançável a partir da "
            "entrada"
        )
    if chaves is not None:
        for nome, chave, celula in (
            ("entrada", "ENTRY", labirinto.entrada),
            ("saída", "EXIT", labirinto.saida),
        ):
            esperado = coordenada(chaves.get(chave, ""))
            if esperado != celula:
                violacoes.append(
                    f"a {nome} é {celula}, mas o config tem "
                    f"{chave}={chaves.get(chave)}"
                )
    return violacoes


def toda_celula_fora_do_42_alcancavel(
    labirinto: Labirinto, chaves: Chaves
) -> list[str]:
    """Toda célula fora do "42" da D07 é alcançável a partir da entrada.

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        A violação com as células soltas, se houver.
    """
    problema = _sem_entrada(labirinto)
    if problema:
        return problema
    soltas = inalcancaveis_fora_do_42(labirinto)
    if soltas:
        return [
            f"{len(soltas)} célula(s) fora do 42 inalcançável(is): "
            f"{lista(soltas)}"
        ]
    return []


def _sem_entrada(labirinto: Labirinto) -> list[str]:
    """Violação de entrada ausente ou fora da grade.

    Args:
        labirinto: Labirinto conferido.

    Returns:
        A violação, ou lista vazia quando há entrada na grade.
    """
    if labirinto.entrada is None or not labirinto.dentro(labirinto.entrada):
        return [f"a entrada {labirinto.entrada} não é célula da grade"]
    return []


def inalcancaveis_sao_do_42(
    labirinto: Labirinto, chaves: Chaves
) -> list[str]:
    """As células que a entrada não alcança são exatamente as do "42".

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        As violações de sobra e de falta.
    """
    problema = _sem_entrada(labirinto)
    if problema:
        return problema
    inalcancadas = frozenset(labirinto.celulas()) - regiao(labirinto)
    padrao = padrao_de(labirinto)
    violacoes: list[str] = []
    if inalcancadas - padrao:
        violacoes.append(
            f"inalcançáveis fora do 42: {lista(inalcancadas - padrao)}"
        )
    if padrao - inalcancadas:
        violacoes.append(
            f"células do 42 alcançáveis: {lista(padrao - inalcancadas)}"
        )
    return violacoes


def _dois_componentes(
    labirinto: Labirinto,
) -> list[frozenset[Celula]] | str:
    """Os dois componentes das células F, ou o problema.

    Args:
        labirinto: Labirinto conferido.

    Returns:
        Os componentes da esquerda e da direita, ou a violação.
    """
    grupos = componentes(celulas_f(labirinto))
    if len(grupos) != 2:
        return (
            f"as células F formam {len(grupos)} componente(s) 4-conexo(s), "
            "não 2"
        )
    return grupos


def f_em_dois_componentes(labirinto: Labirinto, chaves: Chaves) -> list[str]:
    """As células F formam dois componentes 4-conexos.

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        A violação, se houver.
    """
    grupos = _dois_componentes(labirinto)
    return [grupos] if isinstance(grupos, str) else []


def _forma_do_componente(
    labirinto: Labirinto, indice: int, glifo: tuple[str, ...], nome: str
) -> list[str]:
    """Compara um dos dois componentes F com um glifo.

    Args:
        labirinto: Labirinto conferido.
        indice: 0 para o da esquerda, 1 para o da direita.
        glifo: Desenho esperado.
        nome: Dígito, para a mensagem.

    Returns:
        A violação, se houver.
    """
    grupos = _dois_componentes(labirinto)
    if isinstance(grupos, str):
        return [grupos]
    desenho = forma(grupos[indice])
    if desenho != glifo:
        return [
            f"o componente não tem a forma do {nome}: "
            f"{' / '.join(desenho)} em vez de {' / '.join(glifo)}"
        ]
    return []


def forma_do_4(labirinto: Labirinto, chaves: Chaves) -> list[str]:
    """O componente F da esquerda desenha o glifo 3x5 do 4.

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        A violação, se houver.
    """
    return _forma_do_componente(labirinto, 0, GLIFO_4, "4")


def forma_do_2(labirinto: Labirinto, chaves: Chaves) -> list[str]:
    """O componente F da direita desenha o glifo 3x5 do 2.

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        A violação, se houver.
    """
    return _forma_do_componente(labirinto, 1, GLIFO_2, "2")


def _padrao_da_classe(labirinto: Labirinto) -> list[str]:
    """O ``pattern`` da classe, quando há, é o "42" da D07.

    Args:
        labirinto: Labirinto conferido.

    Returns:
        A violação, se houver.
    """
    esperado = padrao_de(labirinto)
    if labirinto.padrao is not None and labirinto.padrao != esperado:
        return [
            f"pattern da classe difere da D07: sobra "
            f"{lista(labirinto.padrao - esperado) or 'nada'}, falta "
            f"{lista(esperado - labirinto.padrao) or 'nada'}"
        ]
    return []


def f_iguais_ao_padrao(labirinto: Labirinto, chaves: Chaves) -> list[str]:
    """As células F são exatamente as do "42" da D07 (e do ``pattern``).

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        As violações de sobra e de falta.
    """
    violacoes = nenhuma_f_fora_do_padrao(labirinto, chaves)
    falta = padrao_de(labirinto) - celulas_f(labirinto)
    if falta:
        violacoes.append(f"células do 42 sem valor F: {lista(falta)}")
    return violacoes + _padrao_da_classe(labirinto)


def nenhuma_f_fora_do_padrao(
    labirinto: Labirinto, chaves: Chaves
) -> list[str]:
    """Nenhuma célula F fica fora do "42" da D07 nem do ``pattern``.

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        A violação, se houver.
    """
    permitidas = padrao_de(labirinto)
    if labirinto.padrao is not None:
        permitidas &= labirinto.padrao
    sobra = celulas_f(labirinto) - permitidas
    return [f"células F fora do padrão: {lista(sobra)}"] if sobra else []


def _celulas_do_42(labirinto: Labirinto) -> frozenset[Celula]:
    """Células do "42": as da D07, as F e as do ``pattern`` da classe.

    Args:
        labirinto: Labirinto conferido.

    Returns:
        A união.
    """
    return padrao_de(labirinto) | celulas_f(labirinto) | (
        labirinto.padrao or frozenset()
    )


def sem_passagem_no_42(labirinto: Labirinto, chaves: Chaves) -> list[str]:
    """As células do "42" são F e as vizinhas fecham a parede para elas.

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        Uma violação por célula aberta ou por passagem que entra no 42.
    """
    celulas = _celulas_do_42(labirinto)
    if not celulas:
        return ["o labirinto não tem células do 42"]
    violacoes: list[str] = []
    for celula in sorted(celulas, key=lambda c: (c[1], c[0])):
        if not labirinto.dentro(celula):
            violacoes.append(f"a célula do 42 {xy(celula)} sai da grade")
            continue
        if labirinto.valor(celula) != FECHADA:
            violacoes.append(
                f"a célula do 42 {xy(celula)} vale "
                f"{labirinto.valor(celula):x}, não f"
            )
        for direcao, (dx, dy) in DESLOCAMENTOS.items():
            vizinha = (celula[0] + dx, celula[1] + dy)
            if labirinto.dentro(vizinha) and labirinto.aberta(
                vizinha, OPOSTAS[direcao]
            ):
                violacoes.append(
                    f"a vizinha {xy(vizinha)} abre a parede para a célula "
                    f"do 42 {xy(celula)}"
                )
    return violacoes


def glifos_3x5(labirinto: Labirinto, chaves: Chaves) -> list[str]:
    """As células F desenham o 4 e o 2 3x5 com uma coluna livre entre eles.

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        A violação, se houver.
    """
    desenho = forma(celulas_f(labirinto))
    if desenho != GLIFOS_42:
        return [
            f"as células F desenham {' / '.join(desenho) or 'nada'} em vez "
            f"de {' / '.join(GLIFOS_42)}"
        ]
    return []


def presenca_do_42(
    labirinto: Labirinto, presente: bool
) -> list[str]:
    """O "42" da D07 está desenhado, ou nenhuma célula é F.

    Args:
        labirinto: Labirinto conferido.
        presente: True para "42 presente", False para "42 ausente".

    Returns:
        A violação, se houver.
    """
    if not presente:
        violacoes: list[str] = []
        if celulas_f(labirinto):
            violacoes.append(
                f"há células F: {lista(celulas_f(labirinto))}"
            )
        if labirinto.padrao:
            violacoes.append(
                f"o pattern da classe não está vazio: "
                f"{lista(labirinto.padrao)}"
            )
        return violacoes
    if not padrao_de(labirinto):
        return [
            f"o 42 não cabe em {labirinto.largura}x{labirinto.altura} "
            "(D06, D07)"
        ]
    return glifos_3x5(labirinto, None) + f_iguais_ao_padrao(labirinto, None)


def _caixa(celulas: frozenset[Celula]) -> tuple[int, int, int, int]:
    """Caixa que contém as células.

    Args:
        celulas: Conjunto não vazio.

    Returns:
        (x mínimo, y mínimo, x máximo, y máximo).
    """
    xs = [x for x, _ in celulas]
    ys = [y for _, y in celulas]
    return min(xs), min(ys), max(xs), max(ys)


def margem_de_corredor(labirinto: Labirinto, chaves: Chaves) -> list[str]:
    """Em volta da caixa do "42" há um anel de corredores alcançáveis.

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        A violação, se houver.
    """
    celulas = celulas_f(labirinto)
    if not celulas:
        return ["o labirinto não tem células F"]
    x0, y0, x1, y1 = _caixa(celulas)
    anel = [
        (x, y)
        for y in range(y0 - 1, y1 + 2)
        for x in range(x0 - 1, x1 + 2)
        if x in (x0 - 1, x1 + 1) or y in (y0 - 1, y1 + 1)
    ]
    alcancadas = regiao(labirinto)
    sem_corredor = [
        celula for celula in anel
        if not corredor(labirinto, celula, alcancadas)
    ]
    if sem_corredor:
        return [
            f"o anel em volta do 42 tem células que não são corredor "
            f"alcançável: {lista(sem_corredor)}"
        ]
    return []


def cantos_fora_do_42(labirinto: Labirinto, chaves: Chaves) -> list[str]:
    """Nenhum canto da grade é célula do "42".

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        A violação, se houver.
    """
    ocupados = set(cantos(labirinto)) & _celulas_do_42(labirinto)
    return [f"cantos no 42: {lista(ocupados)}"] if ocupados else []


def centro_livre(labirinto: Labirinto, chaves: Chaves) -> list[str]:
    """Alguma célula do centro (D08) é corredor alcançável fora do "42".

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        A violação, se houver.
    """
    centro = candidatas_do_centro(labirinto.largura, labirinto.altura)
    do_42 = _celulas_do_42(labirinto)
    alcancadas = regiao(labirinto)
    if any(
        corredor(labirinto, celula, alcancadas) and celula not in do_42
        for celula in centro
    ):
        return []
    return [f"nenhuma célula do centro é corredor livre: {lista(centro)}"]


def arvore_geradora(labirinto: Labirinto, chaves: Chaves) -> list[str]:
    """As células fora do "42" são todas alcançáveis e não há ciclo.

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        As violações de conectividade e de ciclo.
    """
    violacoes = toda_celula_fora_do_42_alcancavel(labirinto, chaves)
    if not violacoes:
        rotas = rotas_independentes(labirinto)
        if rotas:
            violacoes.append(f"a região alcançável tem {rotas} ciclo(s)")
    return violacoes


def caminho_unico(labirinto: Labirinto, chaves: Chaves) -> list[str]:
    """Há exatamente um caminho simples entre a entrada e a saída.

    O caminho é único quando toda passagem do caminho mais curto é ponte:
    fechada ela, a saída deixa de ser alcançável.

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        A violação, se houver.
    """
    problema = _sem_entrada(labirinto)
    if problema:
        return problema
    entrada, saida = labirinto.entrada, labirinto.saida
    assert entrada is not None
    if saida is None or not labirinto.dentro(saida):
        return [f"a saída {saida} não é célula da grade"]
    caminho = caminho_mais_curto(labirinto, entrada, saida)
    if caminho is None:
        return [f"a saída {xy(saida)} não é alcançável a partir da entrada"]
    celulas = percorrer(labirinto, entrada, caminho).celulas
    for anterior, proxima in zip(celulas, celulas[1:]):
        if saida in alcancaveis(labirinto, entrada, (anterior, proxima)):
            return [
                f"há outra rota da entrada à saída sem a passagem entre "
                f"{xy(anterior)} e {xy(proxima)}"
            ]
    return []


def ramos_terminam_em_beco(
    labirinto: Labirinto, chaves: Chaves
) -> list[str]:
    """Cada ramo fora da solução é uma árvore presa a ela por uma passagem.

    Assim todo corredor que sai da solução acaba num beco sem saída.

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        Uma violação por ramo com ciclo ou com mais de uma ligação.
    """
    percurso = _percurso(labirinto)
    if isinstance(percurso, str):
        return [percurso]
    if percurso.letras or percurso.fora or percurso.paredes:
        return ["a solução não é um percurso válido"]
    na_solucao = frozenset(percurso.celulas)
    violacoes: list[str] = []
    for ramo in _ramos(labirinto, regiao(labirinto) - na_solucao):
        ligacoes = sum(
            1
            for celula in ramo
            for vizinha in labirinto.vizinhas(celula)
            if vizinha in na_solucao
        )
        ciclos = passagens(labirinto, ramo) - len(ramo) + 1
        if ligacoes != 1 or ciclos:
            violacoes.append(
                f"o ramo com {lista(ramo)} tem {ligacoes} ligação(ões) com "
                f"a solução e {ciclos} ciclo(s)"
            )
    return violacoes


def _ramos(
    labirinto: Labirinto, celulas: frozenset[Celula]
) -> list[frozenset[Celula]]:
    """Componentes ligados por passagens dentro do conjunto.

    Args:
        labirinto: Labirinto conferido.
        celulas: Células fora da solução.

    Returns:
        Os ramos.
    """
    restantes = set(celulas)
    ramos: list[frozenset[Celula]] = []
    while restantes:
        inicio = restantes.pop()
        ramo = {inicio}
        fila = deque([inicio])
        while fila:
            for vizinha in labirinto.vizinhas(fila.popleft()):
                if vizinha in restantes:
                    restantes.discard(vizinha)
                    ramo.add(vizinha)
                    fila.append(vizinha)
        ramos.append(frozenset(ramo))
    return ramos


def solucao_atravessa_so_paredes_abertas(
    labirinto: Labirinto, chaves: Chaves
) -> list[str]:
    """Cada passo da solução passa por uma parede aberta dos dois lados.

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        Uma violação por letra inválida ou parede fechada atravessada.
    """
    return _no_percurso(
        labirinto, lambda percurso: percurso.letras + percurso.paredes
    )


def solucao_nao_sai_da_grade(
    labirinto: Labirinto, chaves: Chaves
) -> list[str]:
    """Nenhum passo da solução sai da grade.

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        A violação, se houver.
    """
    return _no_percurso(labirinto, lambda percurso: percurso.fora)


def solucao_nao_entra_no_42(
    labirinto: Labirinto, chaves: Chaves
) -> list[str]:
    """Nenhuma célula visitada pela solução é do "42" ou F.

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        A violação, se houver.
    """
    do_42 = _celulas_do_42(labirinto)

    def no_42(percurso: Percurso) -> list[str]:
        """Células do percurso que são do 42.

        Args:
            percurso: Percurso da solução.

        Returns:
            A violação, se houver.
        """
        dentro = set(percurso.celulas) & do_42
        return [f"a solução passa no 42 em {lista(dentro)}"] if dentro else []

    return _no_percurso(labirinto, no_42)


def solucao_termina_na_saida(
    labirinto: Labirinto, chaves: Chaves
) -> list[str]:
    """O percurso da solução para na saída, sem sair da grade.

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        A violação, se houver.
    """

    def na_saida(percurso: Percurso) -> list[str]:
        """Confere a última célula do percurso.

        Args:
            percurso: Percurso da solução.

        Returns:
            A violação, se houver.
        """
        if percurso.fora:
            return percurso.fora
        if labirinto.saida is None or percurso.fim != labirinto.saida:
            return [
                f"a solução termina em {xy(percurso.fim)}, não na saída "
                f"{labirinto.saida}"
            ]
        return []

    return _no_percurso(labirinto, na_saida)


def solucao_mais_curta(labirinto: Labirinto, chaves: Chaves) -> list[str]:
    """A solução tem o comprimento da busca em largura (D15).

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        A violação, se houver.
    """
    dados = _entrada_e_caminho(labirinto)
    if isinstance(dados, str):
        return [dados]
    entrada, caminho = dados
    saida = labirinto.saida
    if saida is None or not labirinto.dentro(saida):
        return [f"a saída {saida} não é célula da grade"]
    curto = caminho_mais_curto(labirinto, entrada, saida)
    if curto is None:
        return [f"a saída {xy(saida)} não é alcançável a partir da entrada"]
    if len(caminho) != len(curto):
        return [
            f"a solução tem {len(caminho)} passos; a busca em largura "
            f"chega em {len(curto)}"
        ]
    return []


def solucao_sem_celula_repetida(
    labirinto: Labirinto, chaves: Chaves
) -> list[str]:
    """Nenhuma célula aparece duas vezes no percurso da solução.

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        A violação, se houver.
    """

    def sem_repeticao(percurso: Percurso) -> list[str]:
        """Células visitadas mais de uma vez.

        Args:
            percurso: Percurso da solução.

        Returns:
            A violação, se houver.
        """
        vistas: set[Celula] = set()
        repetidas: set[Celula] = set()
        for celula in percurso.celulas:
            if celula in vistas:
                repetidas.add(celula)
            vistas.add(celula)
        if repetidas:
            return [f"a solução repete {lista(repetidas)}"]
        return []

    return _no_percurso(labirinto, sem_repeticao)


SOLUCAO_VALIDA: list[Verificacao] = [
    solucao_atravessa_so_paredes_abertas,
    solucao_nao_sai_da_grade,
    solucao_nao_entra_no_42,
    solucao_termina_na_saida,
    solucao_mais_curta,
    solucao_sem_celula_repetida,
]


def todas(*verificacoes: Verificacao) -> Verificacao:
    """Junta verificações numa só, sem repetir a mesma violação.

    Args:
        *verificacoes: Verificações a aplicar, na ordem.

    Returns:
        A verificação que devolve todas as violações.
    """

    def juntas(labirinto: Labirinto, chaves: Chaves) -> list[str]:
        """Aplica cada verificação.

        Args:
            labirinto: Labirinto conferido.
            chaves: Config do cenário, ou None.

        Returns:
            As violações, na ordem, sem repetição.
        """
        violacoes: list[str] = []
        for verificacao in verificacoes:
            for violacao in verificacao(labirinto, chaves):
                if violacao not in violacoes:
                    violacoes.append(violacao)
        return violacoes

    return juntas


solucao_valida_e_mais_curta = todas(*SOLUCAO_VALIDA)


def rotas_minimas(labirinto: Labirinto, chaves: Chaves) -> list[str]:
    """A região alcançável tem pelo menos 2 ciclos independentes (D10).

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        A violação, se houver.
    """
    rotas = rotas_independentes(labirinto)
    if rotas < MINIMO_DE_ROTAS:
        return [f"só {rotas} rota(s) independente(s)"]
    return []


def _becos_ate(maximo: int) -> Verificacao:
    """Cria a verificação de no máximo N becos reais.

    Args:
        maximo: Becos reais tolerados.

    Returns:
        A verificação.
    """

    def becos(labirinto: Labirinto, chaves: Chaves) -> list[str]:
        """Conta os becos reais.

        Args:
            labirinto: Labirinto conferido.
            chaves: Config do cenário (não usado).

        Returns:
            A violação, se houver.
        """
        achados = becos_reais(labirinto)
        if len(achados) > maximo:
            return [f"{len(achados)} becos reais: {lista(achados)}"]
        return []

    return becos


def sem_area_3x3(labirinto: Labirinto, chaves: Chaves) -> list[str]:
    """Nenhum bloco 3x3 tem as 12 paredes internas abertas (D11).

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        A violação, se houver.
    """
    abertas = blocos_abertos(labirinto, 3, 3)
    if abertas:
        return [f"áreas 3x3 abertas com canto em {lista(abertas)}"]
    return []


def blocos_menores_aceitos(
    labirinto: Labirinto, chaves: Chaves
) -> list[str]:
    """O validador aceita as áreas abertas e há um bloco 2x2 aberto.

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        As violações.
    """
    violacoes: list[str] = []
    relato = relato_de_areas(labirinto)
    if relato != "aceito":
        violacoes.append(f"o validador relata {relato!r}")
    if not blocos_abertos(labirinto, 2, 2):
        violacoes.append("nenhum bloco 2x2 aberto")
    return violacoes


def modo_do_config(labirinto: Labirinto, chaves: Chaves) -> list[str]:
    """PERFECT=True dá árvore geradora; False dá Pac-Man aceito.

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário.

    Returns:
        As violações.
    """
    if chaves is None:
        return ["o cenário não tem config"]
    perfeito = chaves.get("PERFECT", "").lower()
    if perfeito == "true":
        return arvore_geradora(labirinto, chaves)
    if perfeito == "false":
        relato = relato_de_pacman(labirinto)
        return [] if relato == "aceito" else [f"modo Pac-Man {relato}"]
    return [f"PERFECT={chaves.get('PERFECT')!r} não é booleano"]


def rodape_valido(labirinto: Labirinto, chaves: Chaves) -> list[str]:
    """Rodapé com ENTRY e EXIT como x,y puros e a solução válida.

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário, ou None (sem comparação).

    Returns:
        As violações.
    """
    if labirinto.texto is None:
        return ["o labirinto veio de generate(), sem rodapé"]
    if len(labirinto.rodape) != 3:
        return [f"o rodapé tem {len(labirinto.rodape)} linhas, não 3"]
    violacoes: list[str] = []
    for linha, chave in zip(labirinto.rodape, ("ENTRY", "EXIT")):
        if coordenada(linha) is None:
            violacoes.append(f"a linha {linha!r} do rodapé não é x,y")
        elif chaves is not None and coordenada(linha) != coordenada(
            chaves.get(chave, "")
        ):
            violacoes.append(
                f"o rodapé tem {linha!r} e o config {chave}="
                f"{chaves.get(chave)}"
            )
    return violacoes + solucao_valida_e_mais_curta(labirinto, chaves)


def quarenta_e_dois_conforme_o_tamanho(
    labirinto: Labirinto, chaves: Chaves
) -> list[str]:
    """O "42" existe se cabe (D06, D07); senão não há célula F.

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        As violações.
    """
    return presenca_do_42(labirinto, bool(padrao_de(labirinto)))


def _com_config(verificacao: Verificacao) -> Verificacao:
    """Exige config antes de aplicar a verificação.

    Args:
        verificacao: Verificação que precisa do config.

    Returns:
        A verificação que falha sem config.
    """

    def exigindo(labirinto: Labirinto, chaves: Chaves) -> list[str]:
        """Aplica a verificação só com config.

        Args:
            labirinto: Labirinto conferido.
            chaves: Config do cenário.

        Returns:
            As violações.
        """
        if chaves is None:
            return ["o cenário não tem config"]
        return verificacao(labirinto, chaves)

    return exigindo


def _dimensoes(labirinto: Labirinto, chaves: Chaves) -> list[str]:
    """Dimensões iguais às do config.

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário.

    Returns:
        As violações.
    """
    assert chaves is not None
    return dimensoes_do_config(labirinto, chaves)


valido_conforme_o_config = _com_config(
    todas(
        _dimensoes,
        valores_de_0_a_15,
        borda_fechada,
        paredes_coerentes,
        entrada_e_saida_validas,
        quarenta_e_dois_conforme_o_tamanho,
        toda_celula_fora_do_42_alcancavel,
        sem_area_3x3,
        solucao_valida_e_mais_curta,
        modo_do_config,
    )
)


def _linhas_do_texto(labirinto: Labirinto) -> list[str] | str:
    """Linhas do arquivo de saída, separadas só por "\\n".

    Args:
        labirinto: Labirinto conferido.

    Returns:
        As linhas, ou a violação quando não veio de arquivo.
    """
    if labirinto.texto is None:
        return "o labirinto veio de generate(), sem arquivo de saída"
    return labirinto.texto.split("\n")


def _no_texto(
    labirinto: Labirinto, conferir: Callable[[list[str]], list[str]]
) -> list[str]:
    """Aplica uma conferência às linhas do arquivo.

    Args:
        labirinto: Labirinto conferido.
        conferir: Função que devolve as violações a partir das linhas.

    Returns:
        As violações.
    """
    linhas = _linhas_do_texto(labirinto)
    return [linhas] if isinstance(linhas, str) else conferir(linhas)


def linha_vazia_apos_a_grade(
    labirinto: Labirinto, chaves: Chaves
) -> list[str]:
    """A linha logo depois da última linha da grade é vazia.

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        A violação, se houver.
    """

    def conferir(linhas: list[str]) -> list[str]:
        """Confere a linha seguinte à grade.

        Args:
            linhas: Linhas do arquivo.

        Returns:
            A violação, se houver.
        """
        indice = labirinto.altura
        if indice >= len(linhas) or linhas[indice].strip():
            seguinte = linhas[indice] if indice < len(linhas) else None
            return [f"a linha {indice + 1} deveria ser vazia: {seguinte!r}"]
        return []

    return _no_texto(labirinto, conferir)


def tres_linhas_apos_a_vazia(
    labirinto: Labirinto, chaves: Chaves
) -> list[str]:
    """Depois da linha vazia há exatamente 3 linhas, nenhuma vazia.

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        A violação, se houver.
    """

    def conferir(linhas: list[str]) -> list[str]:
        """Conta as linhas do rodapé.

        Args:
            linhas: Linhas do arquivo.

        Returns:
            A violação, se houver.
        """
        resto = linhas[labirinto.altura + 1:]
        if resto and resto[-1] == "":
            resto = resto[:-1]
        if len(resto) != 3 or not all(resto):
            return [f"depois da linha vazia vieram {resto!r}"]
        return []

    return _no_texto(labirinto, conferir)


def termina_com_quebra(labirinto: Labirinto, chaves: Chaves) -> list[str]:
    """O arquivo termina com "\\n".

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        A violação, se houver.
    """
    return _no_texto(
        labirinto,
        lambda linhas: [] if linhas[-1] == "" else [
            f"a última linha {linhas[-1]!r} não termina com quebra de linha"
        ],
    )


def vazia_so_com_quebra(labirinto: Labirinto, chaves: Chaves) -> list[str]:
    """A linha vazia tem só o "\\n": nem espaço nem "\\r".

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        A violação, se houver.
    """

    def conferir(linhas: list[str]) -> list[str]:
        """Confere o conteúdo exato da linha vazia.

        Args:
            linhas: Linhas do arquivo.

        Returns:
            A violação, se houver.
        """
        indice = labirinto.altura
        if indice >= len(linhas) or linhas[indice] != "":
            seguinte = linhas[indice] if indice < len(linhas) else None
            return [
                f"a linha {indice + 1} deveria ser só a quebra de linha: "
                f"{seguinte!r}"
            ]
        return []

    return _no_texto(labirinto, conferir)


def sem_espaco_no_fim(labirinto: Labirinto, chaves: Chaves) -> list[str]:
    """Nenhuma linha do arquivo termina com espaço ou tabulação.

    Args:
        labirinto: Labirinto conferido.
        chaves: Config do cenário (não usado).

    Returns:
        Uma violação por linha.
    """
    return _no_texto(
        labirinto,
        lambda linhas: [
            f"a linha {numero} termina com espaço: {linha!r}"
            for numero, linha in enumerate(linhas, start=1)
            if linha != linha.rstrip(" \t")
        ],
    )


PROPRIEDADES: dict[str, Verificacao] = {
    "valores de 0 a 15": valores_de_0_a_15,
    "bits na convenção N=1, E=2, S=4, W=8": bits_na_convencao,
    "x é a coluna e y é a linha": x_coluna_y_linha,
    "entrada e saída válidas": entrada_e_saida_validas,
    "entrada diferente da saída": entrada_diferente_da_saida,
    "x de entrada e saída dentro da largura": x_dentro_da_largura,
    "y de entrada e saída dentro da altura": y_dentro_da_altura,
    "toda célula fora do 42 alcançável": toda_celula_fora_do_42_alcancavel,
    "borda fechada": borda_fechada,
    "paredes coerentes": paredes_coerentes,
    "vizinhas leste-oeste coerentes": vizinhas_leste_oeste,
    "vizinhas norte-sul coerentes": vizinhas_norte_sul,
    "inalcançáveis são as células do 42": inalcancaveis_sao_do_42,
    "células F em dois componentes 4-conexos": f_em_dois_componentes,
    "componente da esquerda com a forma do 4": forma_do_4,
    "componente da direita com a forma do 2": forma_do_2,
    "células F iguais ao padrão 42": f_iguais_ao_padrao,
    "nenhuma célula F fora do padrão": nenhuma_f_fora_do_padrao,
    "42 sem passagem aberta": sem_passagem_no_42,
    "glifos 3x5 com uma coluna livre entre os dígitos": glifos_3x5,
    "42 presente": lambda labirinto, chaves: presenca_do_42(labirinto, True),
    "42 ausente": lambda labirinto, chaves: presenca_do_42(labirinto, False),
    "42 com margem de corredor": margem_de_corredor,
    "42 fora dos cantos": cantos_fora_do_42,
    "centro livre do 42": centro_livre,
    "árvore geradora fora do 42": arvore_geradora,
    "caminho único entre entrada e saída": caminho_unico,
    "ramos fora da solução terminam em beco": ramos_terminam_em_beco,
    "solução atravessa só paredes abertas": (
        solucao_atravessa_so_paredes_abertas
    ),
    "solução não sai da grade": solucao_nao_sai_da_grade,
    "solução não entra no 42": solucao_nao_entra_no_42,
    "solução termina na saída": solucao_termina_na_saida,
    "solução mais curta": solucao_mais_curta,
    "solução sem célula repetida": solucao_sem_celula_repetida,
    "solução válida e mais curta": solucao_valida_e_mais_curta,
    "pelo menos 2 rotas independentes": rotas_minimas,
    "no máximo 2 becos reais": _becos_ate(MAXIMO_DE_BECOS),
    "zero becos reais": _becos_ate(0),
    "sem área aberta 3x3": sem_area_3x3,
    "blocos 2x2, 2x3 e 3x2 abertos aceitos": blocos_menores_aceitos,
    "modo igual ao PERFECT do config": modo_do_config,
    "rodapé com ENTRY, EXIT e caminho válido": rodape_valido,
    "labirinto válido conforme o config": valido_conforme_o_config,
    "uma linha vazia logo após a grade": linha_vazia_apos_a_grade,
    "exatamente 3 linhas após a linha vazia": tres_linhas_apos_a_vazia,
    "arquivo termina com quebra de linha": termina_com_quebra,
    "linha vazia contém só a quebra de linha": vazia_so_com_quebra,
    "nenhuma linha com espaço no fim": sem_espaco_no_fim,
}


def grade_retangular(labirinto: Labirinto) -> str | None:
    """Problema que impede validar a grade, se houver.

    Args:
        labirinto: Labirinto conferido.

    Returns:
        A mensagem, ou None quando a grade é retangular e não vazia.
    """
    if not labirinto.grade or not labirinto.grade[0]:
        return "a grade está vazia"
    larguras = {len(linha) for linha in labirinto.grade}
    if len(larguras) != 1:
        return f"as linhas da grade têm larguras {sorted(larguras)}"
    return None


def violacoes(
    labirinto: Labirinto, propriedade: str, chaves: Chaves
) -> list[str]:
    """Violações de uma propriedade de V72 num labirinto.

    Args:
        labirinto: Labirinto conferido.
        propriedade: Nome da lista fechada de V72.
        chaves: Config do cenário, ou None.

    Returns:
        As violações; vazio quando a propriedade vale.

    Raises:
        KeyError: Quando a propriedade não existe.
    """
    verificacao = PROPRIEDADES[propriedade]
    problema = grade_retangular(labirinto)
    if problema is not None:
        return [problema]
    return verificacao(labirinto, chaves)


def relatar(labirinto: Labirinto, verificacao: str) -> str:
    """Texto que o validador devolve numa verificação (V73).

    Args:
        labirinto: Labirinto conferido.
        verificacao: "coerência das paredes", "áreas abertas" ou
            "modo Pac-Man".

    Returns:
        O relato.

    Raises:
        KeyError: Quando a verificação não existe.
    """
    return RELATOS[verificacao](labirinto)


RELATOS: dict[str, Callable[[Labirinto], str]] = {
    "coerência das paredes": relato_de_coerencia,
    "áreas abertas": relato_de_areas,
    "modo Pac-Man": relato_de_pacman,
}


def contagem(labirinto: Labirinto, item: str) -> int:
    """Quantidade de um item de V74 no labirinto.

    Args:
        labirinto: Labirinto conferido.
        item: "células de valor F", "janelas 2x2 abertas", "células
            alcançáveis" ou "letras da solução".

    Returns:
        A contagem.

    Raises:
        KeyError: Quando o item não existe.
    """
    return CONTAGENS[item](labirinto)


CONTAGENS: dict[str, Callable[[Labirinto], int]] = {
    "células de valor F": lambda labirinto: len(celulas_f(labirinto)),
    "janelas 2x2 abertas": lambda labirinto: len(
        blocos_abertos(labirinto, 2, 2)
    ),
    "células alcançáveis": lambda labirinto: len(regiao(labirinto)),
    "letras da solução": lambda labirinto: len(labirinto.caminho or ""),
}


def paredes_em_bits(texto: str) -> int:
    """Converte "Norte, Leste e Sul" (ou "nenhuma") em bits.

    Args:
        texto: Lista de direções com vírgulas e "e".

    Returns:
        A soma dos bits das direções.

    Raises:
        ValueError: Quando um nome não é direção ou se repete.
    """
    if texto == "nenhuma":
        return 0
    bits = {nome: DIRECOES[letra] for letra, nome in NOMES.items()}
    nomes = re.split(r", | e ", texto)
    if len(set(nomes)) != len(nomes) or not set(nomes) <= set(bits):
        raise ValueError(
            f'paredes "{texto}" inválidas; use "nenhuma" ou direções '
            f"{', '.join(bits)} separadas por vírgula e \"e\""
        )
    return sum(bits[nome] for nome in nomes)


def bits_em_paredes(valor: int, fechadas: bool = True) -> str:
    """Escreve as paredes fechadas (ou abertas) da célula.

    Args:
        valor: Bits de 0 a 15.
        fechadas: True para as paredes de bit ligado.

    Returns:
        "nenhuma" ou os nomes na ordem N, E, S, W, como "Norte e Sul".
    """
    nomes = [
        NOMES[letra] for letra, bit in DIRECOES.items()
        if bool(valor & bit) == fechadas
    ]
    if not nomes:
        return "nenhuma"
    if len(nomes) == 1:
        return nomes[0]
    return f"{', '.join(nomes[:-1])} e {nomes[-1]}"


def intervalos(texto: str) -> set[int]:
    """Converte "6 a 8 e 10 a 12" em números.

    Args:
        texto: Intervalos "a a b" ou números soltos, com vírgulas e "e".

    Returns:
        Os números cobertos.

    Raises:
        ValueError: Quando um trecho não é número nem intervalo.
    """
    numeros: set[int] = set()
    for trecho in re.split(r", | e ", texto):
        casado = re.fullmatch(r"(\d+)(?: a (\d+))?", trecho)
        if casado is None:
            raise ValueError(
                f'intervalo "{trecho}" inválido em "{texto}"; use "6 a 8 e '
                '10 a 12"'
            )
        inicio = int(casado.group(1))
        fim = int(casado.group(2) or inicio)
        numeros.update(range(inicio, fim + 1))
    return numeros


def texto_do_arquivo(grade: list[str], entrada: str, saida: str) -> str:
    """Arquivo de saída de um labirinto de teste (V22).

    O caminho do rodapé é o da busca em largura, vazio quando a saída
    não é alcançável.

    Args:
        grade: Linhas hexadecimais da grade.
        entrada: Coordenada "x,y" da entrada.
        saida: Coordenada "x,y" da saída.

    Returns:
        A grade, a linha vazia e o rodapé, cada linha com "\\n".

    Raises:
        ValueError: Quando a grade não é hexadecimal retangular, ou uma
            coordenada não é x,y dentro da grade.
    """
    sem_rodape = ler_saida("".join(f"{linha}\n" for linha in grade))
    celulas: list[Celula] = []
    for texto in (entrada, saida):
        celula = coordenada(texto)
        if celula is None or not sem_rodape.dentro(celula):
            raise ValueError(f'coordenada "{texto}" fora da grade')
        celulas.append(celula)
    caminho = caminho_mais_curto(sem_rodape, celulas[0], celulas[1]) or ""
    linhas = [*grade, "", entrada, saida, caminho]
    return "".join(f"{linha}\n" for linha in linhas)
