"""Testes do validador da suíte e dos passos sobre labirinto e célula."""

import dataclasses
import re
from collections.abc import Callable
from pathlib import Path

import pytest

from step_defs.geracao import gerar_pelo_programa
from step_defs.labirinto import (
    ARQUIVO_DE_TESTE,
    alguma_alcancavel,
    bit_ligado,
    borda_com_parede,
    celula_com_paredes,
    celula_de_digito,
    celula_na_situacao,
    celula_tem_paredes,
    celulas_f_ocupam,
    confirma_presenca_do_42,
    confirmar,
    digito_da_celula,
    grade_tem_dimensoes,
    identico_ao_config_base,
    labirinto_de_teste_com_grade,
    labirinto_de_teste_modelo,
    linha_do_rodape,
    paredes_da_celula,
    todos_os_labirintos,
    validador_conta,
    validador_converte_a_celula,
    validador_le_o_labirinto,
    validador_relata,
)
from suporte.config import CONFIG_BASE, Config, chaves_das_linhas
from suporte.estado import PROJECT_DIR, Estado, Execucao
from suporte.labirinto import (
    DESLOCAMENTOS,
    DIRECOES,
    FECHADA,
    FIXTURES,
    GLIFOS_42,
    MODELOS,
    OPOSTAS,
    PROPRIEDADES,
    Celula,
    Chaves,
    Labirinto,
    becos_reais,
    bits_em_paredes,
    blocos_abertos,
    caminho_mais_curto,
    candidatas_do_centro,
    celulas_f,
    contagem,
    desenho_em_celulas,
    forma,
    grade_retangular,
    intervalos,
    ler_saida,
    padrao_42,
    paredes_em_bits,
    relatar,
    rotas_independentes,
    texto_do_arquivo,
    violacoes,
)

BASE = chaves_das_linhas(CONFIG_BASE)


def modelo(nome: str) -> Labirinto:
    """Lê um dos modelos de ``tests/fixtures/``.

    Args:
        nome: Nome da lista fechada de V23.

    Returns:
        O labirinto do arquivo.
    """
    caminho = FIXTURES / MODELOS[nome]
    with caminho.open(encoding="utf-8", newline="") as arquivo:
        return ler_saida(arquivo.read())


def grade(texto: str, entrada: str = "0,0", saida: str = "") -> Labirinto:
    """Labirinto de teste como o da V22.

    Args:
        texto: Linhas hexadecimais separadas por " / ".
        entrada: Coordenada "x,y" da entrada.
        saida: Coordenada "x,y" da saída; vazio é o canto inferior direito.

    Returns:
        O labirinto lido do arquivo montado.
    """
    linhas = texto.split(" / ")
    saida = saida or f"{len(linhas[0]) - 1},{len(linhas) - 1}"
    return ler_saida(texto_do_arquivo(linhas, entrada, saida))


def desenhado(
    largura: int,
    altura: int,
    fechadas: frozenset[Celula],
    entrada: Celula = (0, 0),
) -> Labirinto:
    """Grade toda aberta, salvo a borda e as células fechadas (valor F).

    Args:
        largura: Colunas.
        altura: Linhas.
        fechadas: Células F; as vizinhas fecham a parede para elas.
        entrada: Célula da entrada.

    Returns:
        O labirinto, com a solução da busca em largura até o canto
        inferior direito.
    """
    linhas: list[list[int]] = []
    for y in range(altura):
        linha: list[int] = []
        for x in range(largura):
            valor = FECHADA if (x, y) in fechadas else 0
            for letra, (dx, dy) in DESLOCAMENTOS.items():
                vizinha = (x + dx, y + dy)
                if (
                    not 0 <= vizinha[0] < largura
                    or not 0 <= vizinha[1] < altura
                    or vizinha in fechadas
                ):
                    valor |= DIRECOES[letra]
            linha.append(valor)
        linhas.append(linha)
    saida = (largura - 1, altura - 1)
    labirinto = Labirinto(linhas, entrada, saida, None)
    labirinto.caminho = caminho_mais_curto(labirinto, entrada, saida)
    return labirinto


def com_caminho(labirinto: Labirinto, caminho: str) -> Labirinto:
    """Cópia do labirinto com outra solução.

    Args:
        labirinto: Labirinto de origem.
        caminho: Letras da solução.

    Returns:
        A cópia.
    """
    return dataclasses.replace(labirinto, caminho=caminho)


def com_texto(labirinto: Labirinto, texto: str) -> Labirinto:
    """Cópia do labirinto com outro texto de arquivo.

    Args:
        labirinto: Labirinto de origem.
        texto: Conteúdo do arquivo.

    Returns:
        A cópia.
    """
    return dataclasses.replace(labirinto, texto=texto)


def com_valor(labirinto: Labirinto, celula: Celula, valor: int) -> Labirinto:
    """Cópia do labirinto com uma célula trocada.

    Args:
        labirinto: Labirinto de origem.
        celula: Célula (x, y).
        valor: Valor novo da célula.

    Returns:
        A cópia.
    """
    linhas = [list(linha) for linha in labirinto.grade]
    linhas[celula[1]][celula[0]] = valor
    return dataclasses.replace(labirinto, grade=linhas)


def com_chaves(**pares: str) -> dict[str, str]:
    """Config base com os pares trocados.

    Args:
        **pares: Chave e valor novos.

    Returns:
        As chaves.
    """
    return {**BASE, **pares}


EXEMPLO = modelo("exemplo do subject")
ANOTADO = modelo("exemplo do subject com o rodapé anotado")
PERFEITO = modelo("perfeito do config base")
UM_CICLO = modelo("perfeito do config base com uma parede interna aberta")
ABERTO_2X2 = grade("93 / c6")
ARVORE_2X2 = grade("93 / ee")
PACMAN_3X2 = grade("913 / c46")
ABERTO_3X3 = grade("913 / 802 / c46")
SOLTA = grade("97 / ef")
COM_42 = desenhado(9, 7, padrao_42(9, 7))
COM_42_GRANDE = desenhado(20, 15, padrao_42(20, 15))
TROCADO = desenho_em_celulas(
    tuple(f"{linha[4:]}.{linha[:3]}" for linha in GLIFOS_42), 1, 1
)
DESLOCADO = desenhado(9, 7, desenho_em_celulas(GLIFOS_42, 2, 1))
NO_CANTO = desenhado(9, 7, desenho_em_celulas(GLIFOS_42, 0, 0), (8, 6))
ABERTO_9X7 = desenhado(9, 7, frozenset())
ABERTO_8X7 = desenhado(8, 7, frozenset())
TEXTO_BOM = "93\nee\n\n0,0\n1,1\nES\n"

Caso = tuple[str, Labirinto, Chaves]

BONS: list[Caso] = [
    ("valores de 0 a 15", PERFEITO, None),
    ("bits na convenção N=1, E=2, S=4, W=8", PERFEITO, None),
    ("x é a coluna e y é a linha", PERFEITO, BASE),
    ("entrada e saída válidas", PERFEITO, BASE),
    ("entrada diferente da saída", ARVORE_2X2, None),
    ("x de entrada e saída dentro da largura", ARVORE_2X2, None),
    ("y de entrada e saída dentro da altura", ARVORE_2X2, None),
    ("toda célula fora do 42 alcançável", PERFEITO, None),
    ("borda fechada", PERFEITO, None),
    ("paredes coerentes", grade("D7"), None),
    ("vizinhas leste-oeste coerentes", grade("D7"), None),
    ("vizinhas leste-oeste coerentes", grade("F / E"), None),
    ("vizinhas norte-sul coerentes", grade("B / E"), None),
    ("vizinhas norte-sul coerentes", grade("F7"), None),
    ("inalcançáveis são as células do 42", EXEMPLO, None),
    ("células F em dois componentes 4-conexos", EXEMPLO, None),
    ("componente da esquerda com a forma do 4", EXEMPLO, None),
    ("componente da direita com a forma do 2", EXEMPLO, None),
    ("células F iguais ao padrão 42", COM_42_GRANDE, None),
    ("células F iguais ao padrão 42", ABERTO_8X7, None),
    ("nenhuma célula F fora do padrão", COM_42, None),
    ("42 sem passagem aberta", COM_42, None),
    ("glifos 3x5 com uma coluna livre entre os dígitos", EXEMPLO, None),
    ("glifos 3x5 com uma coluna livre entre os dígitos", DESLOCADO, None),
    ("42 presente", COM_42, None),
    ("42 ausente", ABERTO_8X7, None),
    ("42 ausente", PACMAN_3X2, None),
    ("42 com margem de corredor", COM_42, None),
    ("42 fora dos cantos", COM_42, None),
    ("centro livre do 42", COM_42_GRANDE, None),
    ("árvore geradora fora do 42", PERFEITO, None),
    ("caminho único entre entrada e saída", PERFEITO, None),
    ("caminho único entre entrada e saída", ARVORE_2X2, None),
    ("ramos fora da solução terminam em beco", PERFEITO, None),
    ("solução atravessa só paredes abertas", PERFEITO, None),
    ("solução não sai da grade", PERFEITO, None),
    ("solução não entra no 42", COM_42, None),
    ("solução termina na saída", EXEMPLO, None),
    ("solução mais curta", EXEMPLO, None),
    ("solução sem célula repetida", EXEMPLO, None),
    ("solução válida e mais curta", EXEMPLO, None),
    ("solução válida e mais curta", PERFEITO, None),
    ("pelo menos 2 rotas independentes", PACMAN_3X2, None),
    ("no máximo 2 becos reais", EXEMPLO, None),
    ("no máximo 2 becos reais", ARVORE_2X2, None),
    ("zero becos reais", EXEMPLO, None),
    ("sem área aberta 3x3", PACMAN_3X2, None),
    ("sem área aberta 3x3", EXEMPLO, None),
    ("blocos 2x2, 2x3 e 3x2 abertos aceitos", ABERTO_2X2, None),
    ("blocos 2x2, 2x3 e 3x2 abertos aceitos", PACMAN_3X2, None),
    ("modo igual ao PERFECT do config", PERFEITO, BASE),
    ("modo igual ao PERFECT do config", EXEMPLO, com_chaves(PERFECT="false")),
    ("rodapé com ENTRY, EXIT e caminho válido", PERFEITO, BASE),
    ("rodapé com ENTRY, EXIT e caminho válido", EXEMPLO, None),
    ("labirinto válido conforme o config", PERFEITO, BASE),
    (
        "labirinto válido conforme o config",
        EXEMPLO,
        com_chaves(
            WIDTH="25", HEIGHT="20", ENTRY="1,1", PERFECT="False"
        ),
    ),
    ("uma linha vazia logo após a grade", ARVORE_2X2, None),
    ("exatamente 3 linhas após a linha vazia", ARVORE_2X2, None),
    ("arquivo termina com quebra de linha", ARVORE_2X2, None),
    ("linha vazia contém só a quebra de linha", ARVORE_2X2, None),
    ("nenhuma linha com espaço no fim", ARVORE_2X2, None),
]

RUINS: list[tuple[str, Labirinto, Chaves, str]] = [
    (
        "valores de 0 a 15",
        com_valor(ARVORE_2X2, (0, 0), 16),
        None,
        r"\(0,0\) vale 16",
    ),
    (
        "bits na convenção N=1, E=2, S=4, W=8",
        grade("83 / ee"),
        None,
        "Norte aberta",
    ),
    (
        "bits na convenção N=1, E=2, S=4, W=8",
        com_caminho(ARVORE_2X2, "SE"),
        None,
        "parede fechada",
    ),
    (
        "x é a coluna e y é a linha",
        PERFEITO,
        com_chaves(WIDTH="15", HEIGHT="20"),
        "WIDTH=15",
    ),
    (
        "x é a coluna e y é a linha",
        dataclasses.replace(PERFEITO, saida=(14, 19)),
        None,
        "y de 0 a 14",
    ),
    (
        "entrada e saída válidas",
        PERFEITO,
        com_chaves(ENTRY="1,1"),
        "ENTRY=1,1",
    ),
    (
        "entrada e saída válidas",
        SOLTA,
        None,
        r"saída \(1,1\) tem valor F",
    ),
    ("entrada e saída válidas", grade("F7", "0,0", "1,0"), None, "valor F"),
    (
        "entrada diferente da saída",
        grade("93 / ee", "0,0", "0,0"),
        None,
        "mesma célula",
    ),
    ("entrada diferente da saída", ANOTADO, None, "não tem entrada"),
    (
        "x de entrada e saída dentro da largura",
        dataclasses.replace(ARVORE_2X2, saida=(2, 0)),
        None,
        "x de 0 a 1",
    ),
    (
        "y de entrada e saída dentro da altura",
        dataclasses.replace(ARVORE_2X2, entrada=(0, 2)),
        None,
        "y de 0 a 1",
    ),
    (
        "toda célula fora do 42 alcançável",
        SOLTA,
        None,
        r"inalcançável\(is\): \(1,1\)",
    ),
    ("borda fechada", grade("83 / ee"), None, r"\(0,0\) .* Norte aberta"),
    (
        "paredes coerentes",
        grade("F7", "0,0", "1,0"),
        None,
        r"incoerente entre \(0,0\) e \(1,0\)",
    ),
    (
        "vizinhas leste-oeste coerentes",
        grade("F7", "0,0", "1,0"),
        None,
        r"\(0,0\) e \(1,0\)",
    ),
    (
        "vizinhas norte-sul coerentes",
        grade("F / E", "0,0", "0,1"),
        None,
        r"\(0,0\) e \(0,1\)",
    ),
    ("inalcançáveis são as células do 42", SOLTA, None, "fora do 42"),
    (
        "inalcançáveis são as células do 42",
        ABERTO_9X7,
        None,
        "células do 42 alcançáveis",
    ),
    ("células F em dois componentes 4-conexos", PACMAN_3X2, None, "0 comp"),
    (
        "componente da esquerda com a forma do 4",
        desenhado(9, 7, TROCADO),
        None,
        "forma do 4",
    ),
    (
        "componente da direita com a forma do 2",
        desenhado(9, 7, TROCADO),
        None,
        "forma do 2",
    ),
    ("células F iguais ao padrão 42", DESLOCADO, None, "fora do padrão"),
    ("células F iguais ao padrão 42", ABERTO_9X7, None, "sem valor F"),
    (
        "células F iguais ao padrão 42",
        dataclasses.replace(COM_42, padrao=frozenset({(1, 1)})),
        None,
        "pattern da classe",
    ),
    (
        "nenhuma célula F fora do padrão",
        desenhado(9, 7, padrao_42(9, 7) | {(0, 0)}, (1, 0)),
        None,
        r"fora do padrão: \(0,0\)",
    ),
    (
        "42 sem passagem aberta",
        com_valor(COM_42, (0, 1), 8),
        None,
        r"\(0,1\) abre a parede para a célula do 42 \(1,1\)",
    ),
    (
        "42 sem passagem aberta",
        com_valor(COM_42, (1, 1), 7),
        None,
        r"\(1,1\) vale 7",
    ),
    ("42 sem passagem aberta", PACMAN_3X2, None, "não tem células do 42"),
    (
        "glifos 3x5 com uma coluna livre entre os dígitos",
        desenhado(9, 7, TROCADO),
        None,
        "desenham",
    ),
    ("42 presente", PACMAN_3X2, None, "não cabe em 3x2"),
    ("42 presente", ABERTO_9X7, None, "desenham nada"),
    ("42 ausente", COM_42, None, "há células F"),
    (
        "42 ausente",
        dataclasses.replace(ABERTO_8X7, padrao=frozenset({(1, 1)})),
        None,
        "pattern da classe",
    ),
    ("42 com margem de corredor", NO_CANTO, None, "anel"),
    ("42 com margem de corredor", PACMAN_3X2, None, "não tem células F"),
    ("42 fora dos cantos", NO_CANTO, None, r"cantos no 42: \(0,0\)"),
    (
        "centro livre do 42",
        desenhado(20, 15, padrao_42(20, 15) | {(9, 7)}),
        None,
        "centro",
    ),
    ("árvore geradora fora do 42", UM_CICLO, None, "1 ciclo"),
    ("árvore geradora fora do 42", SOLTA, None, "inalcançável"),
    ("caminho único entre entrada e saída", ABERTO_2X2, None, "outra rota"),
    (
        "caminho único entre entrada e saída",
        grade("F7", "0,0", "1,0"),
        None,
        "não é alcançável",
    ),
    ("ramos fora da solução terminam em beco", EXEMPLO, None, "ligação"),
    (
        "ramos fora da solução terminam em beco",
        com_caminho(ARVORE_2X2, "SE"),
        None,
        "não é um percurso válido",
    ),
    (
        "solução atravessa só paredes abertas",
        com_caminho(ARVORE_2X2, "SE"),
        None,
        r"passo 2 \(E\) atravessa a parede fechada",
    ),
    (
        "solução atravessa só paredes abertas",
        com_caminho(ARVORE_2X2, "EXS"),
        None,
        "letra 2",
    ),
    (
        "solução atravessa só paredes abertas",
        dataclasses.replace(ARVORE_2X2, caminho=None),
        None,
        "não tem solução",
    ),
    (
        "solução não sai da grade",
        com_caminho(ARVORE_2X2, "N"),
        None,
        "sai da grade",
    ),
    (
        "solução não entra no 42",
        dataclasses.replace(COM_42, entrada=(0, 1), caminho="E"),
        None,
        r"passa no 42 em \(1,1\)",
    ),
    (
        "solução termina na saída",
        com_caminho(ARVORE_2X2, "E"),
        None,
        r"termina em \(1,0\)",
    ),
    (
        "solução termina na saída",
        com_caminho(ARVORE_2X2, "W"),
        None,
        "sai da grade",
    ),
    (
        "solução mais curta",
        com_caminho(PACMAN_3X2, "SEENS"),
        None,
        "5 passos; a busca em largura chega em 3",
    ),
    (
        "solução mais curta",
        grade("F7", "0,0", "1,0"),
        None,
        "não é alcançável",
    ),
    (
        "solução sem célula repetida",
        com_caminho(ABERTO_2X2, "EWES"),
        None,
        "repete",
    ),
    (
        "solução válida e mais curta",
        com_caminho(ABERTO_2X2, "EWES"),
        None,
        "repete",
    ),
    ("pelo menos 2 rotas independentes", UM_CICLO, None, "só 1 rota"),
    ("no máximo 2 becos reais", PERFEITO, None, "32 becos reais"),
    ("zero becos reais", ARVORE_2X2, None, "2 becos reais"),
    ("sem área aberta 3x3", ABERTO_3X3, None, r"canto em \(0,0\)"),
    (
        "blocos 2x2, 2x3 e 3x2 abertos aceitos",
        ARVORE_2X2,
        None,
        "nenhum bloco 2x2",
    ),
    (
        "blocos 2x2, 2x3 e 3x2 abertos aceitos",
        ABERTO_3X3,
        None,
        "recusado: área 3x3",
    ),
    (
        "modo igual ao PERFECT do config",
        PERFEITO,
        com_chaves(PERFECT="False"),
        "recusado: 0 rota",
    ),
    ("modo igual ao PERFECT do config", EXEMPLO, BASE, "ciclo"),
    ("modo igual ao PERFECT do config", PERFEITO, None, "não tem config"),
    (
        "modo igual ao PERFECT do config",
        PERFEITO,
        com_chaves(PERFECT="sim"),
        "não é booleano",
    ),
    (
        "rodapé com ENTRY, EXIT e caminho válido",
        ANOTADO,
        None,
        "não é x,y",
    ),
    (
        "rodapé com ENTRY, EXIT e caminho válido",
        PERFEITO,
        com_chaves(EXIT="18,14"),
        "EXIT=18,14",
    ),
    (
        "rodapé com ENTRY, EXIT e caminho válido",
        dataclasses.replace(ARVORE_2X2, rodape=["0,0", "1,1"]),
        None,
        "2 linhas",
    ),
    (
        "rodapé com ENTRY, EXIT e caminho válido",
        COM_42,
        None,
        "generate",
    ),
    (
        "labirinto válido conforme o config",
        PERFEITO,
        com_chaves(PERFECT="False"),
        "modo Pac-Man",
    ),
    (
        "labirinto válido conforme o config",
        PERFEITO,
        com_chaves(WIDTH="21"),
        "WIDTH=21, mas a grade tem 20",
    ),
    (
        "labirinto válido conforme o config",
        ABERTO_9X7,
        com_chaves(WIDTH="9", HEIGHT="7", EXIT="8,6"),
        "sem valor F",
    ),
    ("labirinto válido conforme o config", PERFEITO, None, "não tem config"),
    (
        "uma linha vazia logo após a grade",
        com_texto(ARVORE_2X2, "93\nee\n0,0\n1,1\nES\n"),
        None,
        "linha 3 deveria ser vazia",
    ),
    (
        "uma linha vazia logo após a grade",
        COM_42,
        None,
        "sem arquivo",
    ),
    (
        "exatamente 3 linhas após a linha vazia",
        com_texto(ARVORE_2X2, TEXTO_BOM + "extra\n"),
        None,
        "extra",
    ),
    (
        "exatamente 3 linhas após a linha vazia",
        com_texto(ARVORE_2X2, "93\nee\n\n0,0\n\nES\n"),
        None,
        "vieram",
    ),
    (
        "arquivo termina com quebra de linha",
        com_texto(ARVORE_2X2, TEXTO_BOM.rstrip("\n")),
        None,
        "'ES' não termina",
    ),
    (
        "linha vazia contém só a quebra de linha",
        com_texto(ARVORE_2X2, TEXTO_BOM.replace("\n\n", "\n\r\n")),
        None,
        r"'\\r'",
    ),
    (
        "linha vazia contém só a quebra de linha",
        com_texto(ARVORE_2X2, TEXTO_BOM.replace("\n\n", "\n \n")),
        None,
        "' '",
    ),
    (
        "nenhuma linha com espaço no fim",
        com_texto(ARVORE_2X2, TEXTO_BOM.replace("ES", "ES ")),
        None,
        "linha 6",
    ),
]


@pytest.mark.parametrize(
    ("propriedade", "labirinto", "chaves"),
    BONS,
    ids=[f"{caso[0]} {numero}" for numero, caso in enumerate(BONS)],
)
def test_propriedade_valida(
    propriedade: str, labirinto: Labirinto, chaves: Chaves
) -> None:
    """O labirinto bom não tem violação da propriedade.

    Args:
        propriedade: Nome da lista fechada de V72.
        labirinto: Labirinto que cumpre a propriedade.
        chaves: Config do caso, ou None.
    """
    assert violacoes(labirinto, propriedade, chaves) == []


@pytest.mark.parametrize(
    ("propriedade", "labirinto", "chaves", "trecho"),
    RUINS,
    ids=[f"{caso[0]} {numero}" for numero, caso in enumerate(RUINS)],
)
def test_propriedade_violada(
    propriedade: str,
    labirinto: Labirinto,
    chaves: Chaves,
    trecho: str,
) -> None:
    """O labirinto ruim tem uma violação que diz o que está errado.

    Args:
        propriedade: Nome da lista fechada de V72.
        labirinto: Labirinto que viola a propriedade.
        chaves: Config do caso, ou None.
        trecho: Expressão que alguma violação deve conter.
    """
    achadas = violacoes(labirinto, propriedade, chaves)
    assert any(re.search(trecho, achada) for achada in achadas), achadas


def test_toda_propriedade_tem_caso_bom_e_ruim() -> None:
    """Cada propriedade de V72 aparece entre os casos bons e os ruins."""
    assert {caso[0] for caso in BONS} == set(PROPRIEDADES)
    assert {caso[0] for caso in RUINS} == set(PROPRIEDADES)


def test_propriedade_inexistente() -> None:
    """Nome fora da lista fechada de V72 é KeyError."""
    with pytest.raises(KeyError):
        violacoes(PERFEITO, "inventada", None)


@pytest.mark.parametrize(
    ("linhas", "trecho"),
    [([], "vazia"), ([[1, 2], [3]], "larguras")],
    ids=["vazia", "irregular"],
)
def test_grade_que_nao_se_valida(linhas: list[list[int]], trecho: str) -> None:
    """Grade vazia ou irregular vira a única violação de qualquer propriedade.

    Args:
        linhas: Grade da classe.
        trecho: Texto que a violação contém.
    """
    labirinto = Labirinto(linhas, (0, 0), (0, 0), "")
    assert grade_retangular(labirinto) is not None
    achadas = violacoes(labirinto, "borda fechada", None)
    assert len(achadas) == 1 and trecho in achadas[0]


def test_padrao_42_da_d07() -> None:
    """O "42" fica em ((W-7)//2, (H-5)//2) e só existe a partir de 9x7."""
    assert padrao_42(8, 7) == frozenset()
    assert padrao_42(9, 6) == frozenset()
    assert len(padrao_42(9, 7)) == 18
    assert min(padrao_42(9, 7)) == (1, 1)
    assert padrao_42(25, 20) == celulas_f(EXEMPLO)
    assert forma(padrao_42(20, 15)) == GLIFOS_42
    assert {x for x, _ in padrao_42(20, 15)} == {6, 7, 8, 10, 11, 12}


def test_exemplo_do_subject() -> None:
    """Os números do exemplo do subject conferem com o enunciado."""
    assert (EXEMPLO.largura, EXEMPLO.altura) == (25, 20)
    assert EXEMPLO.entrada == (1, 1) and EXEMPLO.saida == (19, 14)
    assert contagem(EXEMPLO, "células de valor F") == 18
    assert contagem(EXEMPLO, "janelas 2x2 abertas") == 35
    assert contagem(EXEMPLO, "células alcançáveis") == 482
    assert contagem(EXEMPLO, "letras da solução") == 33
    assert blocos_abertos(EXEMPLO, 3, 3) == []
    assert becos_reais(EXEMPLO) == []
    assert ANOTADO.grade == EXEMPLO.grade and ANOTADO.entrada is None


def test_modelos_perfeitos() -> None:
    """O perfeito do config base não tem ciclo; a variante tem um só."""
    assert (PERFEITO.largura, PERFEITO.altura) == (20, 15)
    assert rotas_independentes(PERFEITO) == 0
    assert rotas_independentes(UM_CICLO) == 1
    diferentes = [
        celula for celula in PERFEITO.celulas()
        if PERFEITO.valor(celula) != UM_CICLO.valor(celula)
    ]
    assert diferentes == [(0, 0), (0, 1)]
    assert violacoes(UM_CICLO, "paredes coerentes", None) == []
    assert violacoes(UM_CICLO, "solução válida e mais curta", None) == []


def test_caminho_mais_curto_na_ordem_n_e_s_w() -> None:
    """A busca em largura prefere N, E, S, W e devolve None sem rota."""
    assert caminho_mais_curto(ABERTO_2X2, (0, 0), (1, 1)) == "ES"
    assert caminho_mais_curto(ABERTO_2X2, (1, 1), (0, 0)) == "NW"
    assert caminho_mais_curto(ABERTO_2X2, (0, 0), (0, 0)) == ""
    assert caminho_mais_curto(grade("F7"), (0, 0), (1, 0)) is None


def test_becos_reais_ignoram_o_42_e_a_borda() -> None:
    """Beco cercado só pelo "42" e pela borda não é real (D09)."""
    assert becos_reais(ARVORE_2X2) == [(0, 1), (1, 1)]
    cercado = desenhado(3, 2, frozenset({(1, 0), (1, 1), (2, 1)}))
    assert becos_reais(cercado) == []


@pytest.mark.parametrize(
    ("largura", "altura", "centro"),
    [
        (21, 15, {(10, 7)}),
        (20, 15, {(9, 7), (10, 7)}),
        (21, 14, {(10, 6), (10, 7)}),
        (20, 14, {(9, 6), (10, 6), (9, 7), (10, 7)}),
    ],
    ids=["ímpar", "largura par", "altura par", "par"],
)
def test_candidatas_do_centro(
    largura: int, altura: int, centro: set[Celula]
) -> None:
    """O centro segue a D08, como o _centre_candidates do analyzer.

    Args:
        largura: Colunas.
        altura: Linhas.
        centro: Células esperadas.
    """
    assert candidatas_do_centro(largura, altura) == centro


@pytest.mark.parametrize(
    ("labirinto", "verificacao", "esperado"),
    [
        (grade("F7", "0,0", "1,0"), "coerência das paredes",
         "incoerente entre (0,0) e (1,0)"),
        (grade("D7", "0,0", "1,0"), "coerência das paredes", "coerente"),
        (grade("F / E", "0,0", "0,1"), "coerência das paredes",
         "incoerente entre (0,0) e (0,1)"),
        (grade("B / E", "0,0", "0,1"), "coerência das paredes", "coerente"),
        (grade("FF / FF"), "coerência das paredes", "coerente"),
        (grade("F3 / ff", "0,0", "1,0"), "coerência das paredes",
         "incoerente entre (0,0) e (1,0); incoerente entre (1,0) e (1,1)"),
        (ABERTO_2X2, "áreas abertas", "aceito"),
        (grade("93 / 82 / c6"), "áreas abertas", "aceito"),
        (PACMAN_3X2, "áreas abertas", "aceito"),
        (ABERTO_3X3, "áreas abertas", "recusado: área 3x3"),
        (PERFEITO, "modo Pac-Man", "recusado: 0 rota(s) independente(s)"),
        (UM_CICLO, "modo Pac-Man", "recusado: 1 rota(s) independente(s)"),
        (PACMAN_3X2, "modo Pac-Man", "aceito"),
        (EXEMPLO, "modo Pac-Man", "aceito"),
        (grade("913 / 802 / eee"), "modo Pac-Man",
         "recusado: 3 beco(s) real(is)"),
        (desenhado(5, 3, frozenset({(2, 1)})), "modo Pac-Man",
         "recusado: canto ou centro fechado em (2,1)"),
        (desenhado(6, 4, frozenset()), "áreas abertas",
         "recusado: área 3x3"),
    ],
    ids=[
        "F7", "D7", "F/E", "B/E", "fechada", "dois pares", "2x2", "2x3",
        "3x2", "3x3", "perfeito", "um ciclo", "pacman", "exemplo",
        "becos", "centro", "6x4",
    ],
)
def test_relatos(
    labirinto: Labirinto, verificacao: str, esperado: str
) -> None:
    """Os relatos de V73 têm o texto da lista fechada.

    Args:
        labirinto: Labirinto conferido.
        verificacao: Nome da verificação.
        esperado: Relato esperado.
    """
    assert relatar(labirinto, verificacao) == esperado


def test_relato_pacman_com_celulas_soltas() -> None:
    """Com rotas, becos, cantos e centro bons, as células soltas recusam."""
    soltas = {(2, 1), (3, 1)}
    labirinto = desenhado(6, 4, frozenset())
    for x, y in soltas:
        for letra, (dx, dy) in DESLOCAMENTOS.items():
            vizinha = (x + dx, y + dy)
            if vizinha not in soltas:
                labirinto.grade[y][x] |= DIRECOES[letra]
                oposta = DIRECOES[OPOSTAS[letra]]
                labirinto.grade[vizinha[1]][vizinha[0]] |= oposta
    assert relatar(labirinto, "modo Pac-Man") == (
        "recusado: 2 célula(s) inalcançável(is)"
    )


@pytest.mark.parametrize(
    ("texto", "bits"),
    [
        ("nenhuma", 0),
        ("Norte", 1),
        ("Norte e Leste", 3),
        ("Norte, Leste e Sul", 7),
        ("Norte, Leste, Sul e Oeste", 15),
        ("Sul e Oeste", 12),
    ],
    ids=["nenhuma", "N", "NE", "NES", "todas", "SW"],
)
def test_paredes_e_bits(texto: str, bits: int) -> None:
    """Paredes viram bits e os bits voltam ao mesmo texto.

    Args:
        texto: Paredes como escritas no passo.
        bits: Valor esperado.
    """
    assert paredes_em_bits(texto) == bits
    assert bits_em_paredes(bits) == texto


@pytest.mark.parametrize(
    "texto",
    ["", "Norte e Norte", "Cima", "norte"],
    ids=["vazio", "repetida", "inexistente", "minúscula"],
)
def test_paredes_invalidas(texto: str) -> None:
    """Direção fora da lista ou repetida é ValueError.

    Args:
        texto: Paredes inválidas.
    """
    with pytest.raises(ValueError, match="inválidas"):
        paredes_em_bits(texto)


def test_paredes_abertas() -> None:
    """As paredes abertas são as de bit desligado."""
    assert bits_em_paredes(3, fechadas=False) == "Sul e Oeste"
    assert bits_em_paredes(15, fechadas=False) == "nenhuma"


@pytest.mark.parametrize(
    ("texto", "numeros"),
    [
        ("6 a 8 e 10 a 12", {6, 7, 8, 10, 11, 12}),
        ("5 a 9", {5, 6, 7, 8, 9}),
        ("3", {3}),
        ("1, 3 e 5 a 6", {1, 3, 5, 6}),
    ],
    ids=["dois", "um", "número", "misto"],
)
def test_intervalos(texto: str, numeros: set[int]) -> None:
    """Intervalos "a a b" e números soltos viram o conjunto coberto.

    Args:
        texto: Intervalos como escritos no passo.
        numeros: Conjunto esperado.
    """
    assert intervalos(texto) == numeros


@pytest.mark.parametrize("texto", ["", "6 até 8", "a a b"])
def test_intervalos_invalidos(texto: str) -> None:
    """Trecho que não é número nem intervalo é ValueError.

    Args:
        texto: Intervalos inválidos.
    """
    with pytest.raises(ValueError, match="inválido"):
        intervalos(texto)


def test_texto_do_arquivo() -> None:
    """O arquivo de teste tem grade, linha vazia e rodapé com a BFS."""
    assert texto_do_arquivo(["93", "ee"], "0,0", "1,1") == TEXTO_BOM
    assert texto_do_arquivo(["F7"], "0,0", "1,0") == "F7\n\n0,0\n1,0\n\n"


@pytest.mark.parametrize(
    ("linhas", "entrada", "saida"),
    [
        (["9g"], "0,0", "1,0"),
        (["93", "e"], "0,0", "1,0"),
        (["93"], "0,0", "2,0"),
        (["93"], "0, 0", "1,0"),
    ],
    ids=["não hex", "irregular", "fora", "com espaço"],
)
def test_texto_do_arquivo_invalido(
    linhas: list[str], entrada: str, saida: str
) -> None:
    """Grade ou coordenada inválida é ValueError.

    Args:
        linhas: Linhas da grade.
        entrada: Coordenada da entrada.
        saida: Coordenada da saída.
    """
    with pytest.raises(ValueError):
        texto_do_arquivo(linhas, entrada, saida)


def test_ler_saida_tolera_crlf_e_guarda_o_texto() -> None:
    """Com CRLF a grade e o rodapé se leem e o texto guarda o "\\r"."""
    texto = TEXTO_BOM.replace("\n", "\r\n")
    labirinto = ler_saida(texto)
    assert labirinto.grade == ARVORE_2X2.grade
    assert labirinto.rodape == ["0,0", "1,1", "ES"]
    assert labirinto.texto == texto
    assert violacoes(
        labirinto, "linha vazia contém só a quebra de linha", None
    )


def test_ler_saida_de_preserva_o_retorno_de_carro(tmp_path: Path) -> None:
    """O arquivo de saída é lido sem converter "\\r\\n".

    Args:
        tmp_path: Pasta temporária do teste.
    """
    arquivo = tmp_path / "maze.txt"
    arquivo.write_bytes(b"93\r\nee\r\n\r\n0,0\r\n1,1\r\nES\r\n")
    assert Estado.ler_saida_de(arquivo) == arquivo.read_bytes().decode()


def gravado(cenario: Estado) -> Labirinto:
    """Último labirinto registrado, que deve ter arquivo no cenário.

    Args:
        cenario: Estado numa pasta temporária.

    Returns:
        O labirinto.
    """
    labirinto = cenario.labirintos[-1]
    assert labirinto.arquivo == cenario.cwd / ARQUIVO_DE_TESTE
    assert labirinto.texto is not None
    assert labirinto.arquivo.read_bytes() == labirinto.texto.encode()
    return labirinto


def test_labirinto_de_teste_com_grade(cenario: Estado) -> None:
    """V22 grava a grade com o rodapé da BFS e registra o labirinto.

    Args:
        cenario: Estado numa pasta temporária.
    """
    labirinto_de_teste_com_grade(cenario, "93 / ee", "0,0", "1,1")
    assert gravado(cenario).texto == TEXTO_BOM
    labirinto_de_teste_com_grade(cenario, "F / E", "0,0", "0,1")
    assert gravado(cenario).caminho == ""
    assert len(cenario.labirintos) == 2
    cenario.restaurar()
    assert not (cenario.cwd / ARQUIVO_DE_TESTE).exists()


@pytest.mark.parametrize(
    ("texto", "entrada", "saida"),
    [("9x", "0,0", "1,0"), ("93", "0,0", "5,0"), ("93", "a", "1,0")],
    ids=["não hex", "fora", "não x,y"],
)
def test_labirinto_de_teste_invalido(
    cenario: Estado, texto: str, entrada: str, saida: str
) -> None:
    """V22 falha dizendo qual grade não serve.

    Args:
        cenario: Estado numa pasta temporária.
        texto: Grade do passo.
        entrada: Entrada do passo.
        saida: Saída do passo.
    """
    with pytest.raises(pytest.fail.Exception, match="não serve"):
        labirinto_de_teste_com_grade(cenario, texto, entrada, saida)


@pytest.mark.parametrize("nome", list(MODELOS))
def test_labirinto_de_teste_modelo(cenario: Estado, nome: str) -> None:
    """V23 grava cada modelo como arquivo do cenário, byte a byte.

    Args:
        cenario: Estado numa pasta temporária.
        nome: Modelo da lista fechada.
    """
    labirinto_de_teste_modelo(cenario, nome)
    assert gravado(cenario).arquivo is not None
    assert (cenario.cwd / ARQUIVO_DE_TESTE).read_bytes() == (
        FIXTURES / MODELOS[nome]
    ).read_bytes()


def test_labirinto_de_teste_modelo_inexistente(cenario: Estado) -> None:
    """Modelo fora da lista falha citando os válidos.

    Args:
        cenario: Estado numa pasta temporária.
    """
    with pytest.raises(pytest.fail.Exception, match="exemplo do subject"):
        labirinto_de_teste_modelo(cenario, "outro")


@pytest.mark.parametrize(
    ("digito", "valor"),
    [("0", 0), ("3", 3), ("A", 10), ("f", 15)],
    ids=["0", "3", "A", "f"],
)
def test_celula_de_digito(cenario: Estado, digito: str, valor: int) -> None:
    """V24 guarda o valor do dígito, em qualquer caixa.

    Args:
        cenario: Estado numa pasta temporária.
        digito: Dígito do passo.
        valor: Valor esperado.
    """
    celula_de_digito(cenario, digito)
    assert cenario.celula == valor
    validador_converte_a_celula(cenario)


@pytest.mark.parametrize("digito", ["", "g", "10", "-1"])
def test_celula_de_digito_invalido(cenario: Estado, digito: str) -> None:
    """V24 recusa o que não é um único dígito hexadecimal.

    Args:
        cenario: Estado numa pasta temporária.
        digito: Texto inválido.
    """
    with pytest.raises(pytest.fail.Exception, match="hexadecimal"):
        celula_de_digito(cenario, digito)


def test_celula_com_paredes(cenario: Estado) -> None:
    """V25 guarda os bits das paredes e recusa direção inválida.

    Args:
        cenario: Estado numa pasta temporária.
    """
    celula_com_paredes(cenario, "Sul e Oeste")
    assert cenario.celula == 12
    with pytest.raises(pytest.fail.Exception, match="inválidas"):
        celula_com_paredes(cenario, "Cima")


def test_converter_sem_celula(cenario: Estado) -> None:
    """V40 sem célula dada falha.

    Args:
        cenario: Estado numa pasta temporária.
    """
    with pytest.raises(pytest.fail.Exception, match="nenhuma célula"):
        validador_converte_a_celula(cenario)
    cenario.celula = 16
    with pytest.raises(pytest.fail.Exception, match="fora de 0 a 15"):
        validador_converte_a_celula(cenario)


def test_passos_sobre_a_celula(cenario: Estado) -> None:
    """V79 a V82 conferem o dígito, as paredes, a contagem e o bit.

    Args:
        cenario: Estado numa pasta temporária.
    """
    cenario.celula = 10
    digito_da_celula(cenario, "A")
    digito_da_celula(cenario, "a")
    paredes_da_celula(cenario, "fechadas", "Leste e Oeste")
    paredes_da_celula(cenario, "abertas", "Norte e Sul")
    celula_tem_paredes(cenario, 2)
    bit_ligado(cenario, 1)
    bit_ligado(cenario, 3)
    falhas: list[Callable[[], None]] = [
        lambda: digito_da_celula(cenario, "b"),
        lambda: paredes_da_celula(cenario, "fechadas", "Norte e Sul"),
        lambda: paredes_da_celula(cenario, "abertas", "nenhuma"),
        lambda: paredes_da_celula(cenario, "fechadas", "Cima"),
        lambda: celula_tem_paredes(cenario, 3),
        lambda: bit_ligado(cenario, 0),
        lambda: bit_ligado(cenario, 4),
    ]
    for falha in falhas:
        with pytest.raises(pytest.fail.Exception):
            falha()


def test_sem_labirinto(cenario: Estado) -> None:
    """Os passos sobre labirinto falham quando nenhum foi produzido.

    Args:
        cenario: Estado numa pasta temporária.
    """
    with pytest.raises(pytest.fail.Exception, match="nenhum labirinto"):
        todos_os_labirintos(cenario)
    with pytest.raises(pytest.fail.Exception, match="nenhum labirinto"):
        validador_le_o_labirinto(cenario)
    with pytest.raises(pytest.fail.Exception, match="nenhum labirinto"):
        confirmar(cenario, "borda fechada")


def test_le_o_labirinto_com_saida_ilegivel(cenario: Estado) -> None:
    """V39 conta por que o arquivo da última execução não se lê.

    Args:
        cenario: Estado numa pasta temporária.
    """
    cenario.resultados.append(
        Execucao("comando", 1, "", "", conteudo_saida="93\nxx\n")
    )
    with pytest.raises(pytest.fail.Exception, match="não é hexadecimal"):
        validador_le_o_labirinto(cenario)


def test_le_o_labirinto_das_execucoes(cenario: Estado) -> None:
    """Labirintos só das execuções repetidas também valem.

    Args:
        cenario: Estado numa pasta temporária.
    """
    cenario.execucoes.append(
        Execucao("comando", 0, "", "", labirinto=PERFEITO)
    )
    cenario.labirintos.append(PERFEITO)
    cenario.execucoes.append(
        Execucao("comando", 0, "", "", labirinto=EXEMPLO)
    )
    validador_le_o_labirinto(cenario)
    assert todos_os_labirintos(cenario) == [PERFEITO, EXEMPLO]


def test_le_o_labirinto_da_sessao(cenario: Estado) -> None:
    """Numa sessão, V39 relê o OUTPUT_FILE do config da sessão.

    Args:
        cenario: Estado numa pasta temporária.
    """
    (cenario.cwd / "cfg.txt").write_text("OUTPUT_FILE=maze.txt\n")
    cenario.abrir_sessao("python3 a_maze_ing.py cfg.txt")
    saida = cenario.cwd / "maze.txt"
    with pytest.raises(pytest.fail.Exception, match="legível"):
        validador_le_o_labirinto(cenario)
    saida.write_text("93\nxx\n")
    with pytest.raises(pytest.fail.Exception, match="não se lê"):
        validador_le_o_labirinto(cenario)
    saida.write_text(TEXTO_BOM)
    validador_le_o_labirinto(cenario)
    assert cenario.labirintos[-1].arquivo == saida
    assert cenario.labirintos[-1].grade == ARVORE_2X2.grade


def test_confirmar(cenario: Estado) -> None:
    """V72 confere todos os labirintos e cita o que falhou e onde.

    Args:
        cenario: Estado numa pasta temporária.
    """
    cenario.labirintos.extend([PERFEITO, EXEMPLO])
    confirmar(cenario, "borda fechada")
    confirma_presenca_do_42(cenario, "presente")
    with pytest.raises(
        pytest.fail.Exception, match=r"labirinto 2 de 2 \(25x20\)"
    ):
        confirmar(cenario, "árvore geradora fora do 42")
    with pytest.raises(pytest.fail.Exception, match="as válidas são"):
        confirmar(cenario, "inventada")
    with pytest.raises(pytest.fail.Exception, match="há células F"):
        confirma_presenca_do_42(cenario, "ausente")


def test_confirmar_usa_o_config(cenario: Estado) -> None:
    """As propriedades que dependem do config leem o config do cenário.

    Args:
        cenario: Estado numa pasta temporária.
    """
    cenario.labirintos.append(PERFEITO)
    with pytest.raises(pytest.fail.Exception, match="não tem config"):
        confirmar(cenario, "labirinto válido conforme o config")
    cenario.config = Config(list(CONFIG_BASE))
    confirmar(cenario, "labirinto válido conforme o config")
    cenario.config.definir("PERFECT", "False")
    with pytest.raises(pytest.fail.Exception, match="modo Pac-Man"):
        confirmar(cenario, "modo igual ao PERFECT do config")


def test_passos_sobre_o_labirinto(cenario: Estado) -> None:
    """V68, V69, V73 a V78 aceitam o certo e recusam o errado.

    Args:
        cenario: Estado numa pasta temporária.
    """
    cenario.labirintos.append(EXEMPLO)
    grade_tem_dimensoes(cenario, 25, 20)
    linha_do_rodape(cenario, 1, "1,1")
    linha_do_rodape(cenario, 3, "ESEENEEESSSEESESSESESSSSEEEEEESES")
    validador_relata(cenario, "aceito", "áreas abertas")
    validador_relata(cenario, "coerente", "coerência das paredes")
    validador_conta(cenario, 18, "células de valor F")
    celula_na_situacao(cenario, "0,0", "não tem valor F")
    celula_na_situacao(cenario, "0,0", "é alcançável a partir da entrada")
    celula_na_situacao(cenario, "0,5", "tem as paredes externas fechadas")
    alguma_alcancavel(cenario, ["9,7", "12,10"])
    borda_com_parede(cenario, "primeira linha", "Norte")
    borda_com_parede(cenario, "última coluna", "Leste")
    celulas_f_ocupam(cenario, "9 a 11 e 13 a 15", "7 a 11")
    falhas: list[tuple[Callable[[], None], str]] = [
        (lambda: grade_tem_dimensoes(cenario, 20, 25), "25 colunas"),
        (lambda: linha_do_rodape(cenario, 1, "0,0"), "'1,1'"),
        (lambda: linha_do_rodape(cenario, 4, "x"), "não a 4"),
        (lambda: validador_relata(cenario, "x", "áreas abertas"), "aceito"),
        (lambda: validador_relata(cenario, "x", "outra"), "válidas"),
        (lambda: validador_conta(cenario, 17, "células de valor F"), "18"),
        (lambda: validador_conta(cenario, 1, "outro"), "válidos"),
        (
            lambda: celula_na_situacao(cenario, "9,7", "não tem valor F"),
            r"\(9,7\) tem valor F",
        ),
        (
            lambda: celula_na_situacao(
                cenario, "9,7", "é alcançável a partir da entrada"
            ),
            "não é alcançável",
        ),
        (
            lambda: celula_na_situacao(
                cenario, "5,5", "tem as paredes externas fechadas"
            ),
            "não fica na borda",
        ),
        (
            lambda: celula_na_situacao(cenario, "30,0", "não tem valor F"),
            "fora da grade",
        ),
        (lambda: celula_na_situacao(cenario, "x", "não tem valor F"), "x,y"),
        (lambda: celula_na_situacao(cenario, "0,0", "outra"), "válidas"),
        (lambda: alguma_alcancavel(cenario, ["9,7", "13,7"]), "nenhuma"),
        (lambda: borda_com_parede(cenario, "meio", "Norte"), "válidas"),
        (
            lambda: borda_com_parede(cenario, "primeira linha", "Cima"),
            "válidas",
        ),
        (
            lambda: borda_com_parede(cenario, "primeira linha", "Sul"),
            "Sul aberta",
        ),
        (
            lambda: celulas_f_ocupam(cenario, "6 a 8", "7 a 11"),
            "colunas",
        ),
        (lambda: celulas_f_ocupam(cenario, "x", "7 a 11"), "inválido"),
    ]
    for falha, trecho in falhas:
        with pytest.raises(pytest.fail.Exception, match=trecho):
            falha()


def test_rodape_de_labirinto_da_classe(cenario: Estado) -> None:
    """V69 sobre labirinto de generate() falha: ele não tem rodapé.

    Args:
        cenario: Estado numa pasta temporária.
    """
    cenario.labirintos.append(COM_42)
    with pytest.raises(pytest.fail.Exception, match="sem rodapé"):
        linha_do_rodape(cenario, 1, "0,0")


def test_identico_ao_config_base(estado: Estado) -> None:
    """V70 compara os bytes com a geração do config base.

    Roda o programa de ../project, como os cenários.

    Args:
        estado: Estado novo, com cwd em project/.
    """
    assert estado.cwd == PROJECT_DIR
    estado.config = Config(["# comentário", *CONFIG_BASE])
    gerar_pelo_programa(estado)
    identico_ao_config_base(estado)
    estado.config = Config(list(CONFIG_BASE))
    estado.config.definir("SEED", "7")
    gerar_pelo_programa(estado)
    with pytest.raises(pytest.fail.Exception, match="difere"):
        identico_ao_config_base(estado)


def test_identico_sem_arquivo(cenario: Estado) -> None:
    """V70 sem labirinto vindo de arquivo falha.

    Args:
        cenario: Estado numa pasta temporária.
    """
    cenario.labirintos.append(COM_42)
    with pytest.raises(pytest.fail.Exception, match="arquivo de saída"):
        identico_ao_config_base(cenario)
