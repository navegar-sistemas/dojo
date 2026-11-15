"""Testes da leitura da renderização no terminal."""

import pytest

from autoteste.desenho import (
    AMARELO,
    ARQUIVO,
    AZUL,
    BRANCO,
    CIANO,
    TEXTO_DO_MENU,
    VERDE,
    desenhar,
    grade,
    saida,
)
from suporte.labirinto import ler_saida
from suporte.render import (
    Cor,
    Renderizacao,
    caminho_do_arquivo,
    caminho_marcado,
    conferir_rodizio,
    cor_das_paredes,
    dimensoes,
    direcoes,
    distancia,
    grade_desenhada,
    nome_da_cor,
    nomes_das_direcoes,
    paredes_desenhadas,
    posicoes_de,
    problemas_de_sgr,
    renderizacoes,
    seguida_do_menu,
    tela,
    visiveis,
)

# Labirinto 2x2 todo aberto: a BFS vai direto de (0,0) a (1,0), e o ciano
# dá a volta por baixo, com 3 passos.
ANEL = "93\nc6\n\n0,0\n1,0\nE\n"
VOLTA: list[list[Cor]] = [
    [BRANCO] * 5,
    [BRANCO, 45, None, 41, BRANCO],
    [BRANCO, CIANO, BRANCO, CIANO, BRANCO],
    [BRANCO, CIANO, CIANO, CIANO, BRANCO],
    [BRANCO] * 5,
]


def bloco(fundos: list[list[Cor]]) -> Renderizacao:
    """Renderização só com as linhas desenhadas.

    Args:
        fundos: Código de cada posição.

    Returns:
        O bloco, sem linhas depois dele.
    """
    return Renderizacao(desenhar(fundos).split("\n"), [])


def test_divide_a_saida_em_renderizacoes() -> None:
    """Cada exibição vira um bloco seguido do menu."""
    blocos = renderizacoes(saida(grade(), grade(AMARELO)), 2)
    assert [len(bloco.linhas) for bloco in blocos] == [5, 5]
    assert all(seguida_do_menu(bloco) for bloco in blocos)


def test_linhas_desenhadas_seguidas_viram_varios_blocos() -> None:
    """Dois desenhos sem nada entre eles são dois blocos; o resto é curto."""
    texto = desenhar(grade()) + "\n" + desenhar(grade()[:3]) + "\n"
    blocos = renderizacoes(texto, 2)
    assert [len(bloco.linhas) for bloco in blocos] == [5, 3]
    assert not seguida_do_menu(blocos[0])


def test_saida_sem_desenho() -> None:
    """Sem linha com ESC não há renderização."""
    assert renderizacoes(TEXTO_DO_MENU, 2) == []


@pytest.mark.parametrize(
    "seguinte",
    [
        [],
        TEXTO_DO_MENU.split("\n")[:5],
        ["=== Menu ===", *TEXTO_DO_MENU.split("\n")[1:]],
        ["", *TEXTO_DO_MENU.split("\n")],
    ],
    ids=["nada", "sem prompt", "outro título", "linha vazia antes"],
)
def test_sem_menu_logo_depois(seguinte: list[str]) -> None:
    """O menu da figura e o prompt vêm logo depois do desenho.

    Args:
        seguinte: Linhas depois do bloco.
    """
    assert not seguida_do_menu(Renderizacao(["x"], seguinte))


def test_fundo_padrao_e_reset_sao_sem_cor() -> None:
    """O 49 e o reset voltam ao fundo padrão; outros códigos ficam."""
    linha = "\x1b[47m \x1b[1;44m \x1b[49m \x1b[0m \x1b[100m \x1b[m "
    assert [fundo for _, fundo in visiveis(linha)] == [
        BRANCO, AZUL, None, None, 100, None,
    ]


def test_tela_le_os_fundos() -> None:
    """Cada par de caracteres vira uma posição com o fundo dela."""
    assert tela(bloco(grade())) == grade()


@pytest.mark.parametrize(
    ("linhas", "mensagem"),
    [
        (["\x1b[47m   \x1b[0m"], "número ímpar"),
        (["\x1b[47m \x1b[43m \x1b[0m"], "dois fundos"),
        (["\x1b[47m    \x1b[0m", "\x1b[47m  \x1b[0m"], "números diferentes"),
    ],
    ids=["caractere ímpar", "posição com dois fundos", "linhas desiguais"],
)
def test_tela_com_defeito(linhas: list[str], mensagem: str) -> None:
    """Posições mal formadas derrubam a leitura.

    Args:
        linhas: Linhas desenhadas.
        mensagem: Trecho esperado no erro.
    """
    with pytest.raises(ValueError, match=mensagem):
        tela(Renderizacao(linhas, []))


@pytest.mark.parametrize(
    ("linha", "problema"),
    [
        ("\x1b[31m  \x1b[0m", "'31'"),
        ("\x1b[2J\x1b[47m  \x1b[0m", "não é SGR"),
        ("\x1b[48;5;7m  \x1b[0m", "'48'"),
        ("\x1bc\x1b[47m  \x1b[0m", "ESC fora"),
    ],
    ids=["frente", "limpa a tela", "256 cores", "ESC solto"],
)
def test_sequencia_que_nao_e_fundo(linha: str, problema: str) -> None:
    """Só fundos, o 49 e o reset passam.

    Args:
        linha: Linha desenhada.
        problema: Trecho esperado no primeiro problema.
    """
    assert problema in problemas_de_sgr(linha)[0]


def test_linha_so_com_fundos() -> None:
    """Fundos, 49 e reset não são problema."""
    assert problemas_de_sgr(desenhar(grade()).split("\n")[1]) == []


@pytest.mark.parametrize(
    "fundos",
    [[[BRANCO] * 4] * 3, [[BRANCO] * 3] * 2, [[BRANCO]]],
    ids=["colunas pares", "linhas pares", "uma posição"],
)
def test_dimensoes_sem_grade(fundos: list[list[Cor]]) -> None:
    """Uma grade precisa de 2n + 1 linhas e colunas.

    Args:
        fundos: Grade de fundos.
    """
    with pytest.raises(ValueError, match="2n \\+ 1"):
        dimensoes(fundos)


def test_grade_desenhada_igual_ao_arquivo() -> None:
    """As paredes na cor do canto viram os bits do arquivo."""
    desenho = grade(VERDE)
    assert dimensoes(desenho) == (3, 2)
    assert cor_das_paredes(desenho) == VERDE
    assert grade_desenhada(desenho) == ler_saida(ARQUIVO).grade
    assert paredes_desenhadas(desenho, (1, 1)) == {"S", "W"}


@pytest.mark.parametrize(
    ("nome", "esperadas"),
    [
        ("entrada", {(1, 1)}),
        ("saída", {(1, 5)}),
        ("células do caminho", {(1, 3)}),
        ("passagens do caminho", {(1, 2), (1, 4)}),
        ("células do 42", {(3, 1)}),
    ],
    ids=["entrada", "saída", "células", "passagens", "42"],
)
def test_posicoes_dos_elementos(
    nome: str, esperadas: set[tuple[int, int]]
) -> None:
    """Cada elemento ocupa as posições dadas pelo arquivo.

    Args:
        nome: Elemento.
        esperadas: Posições (linha, coluna).
    """
    assert posicoes_de(ler_saida(ARQUIVO), nome) == esperadas


def test_paredes_sao_os_cantos_e_as_fechadas() -> None:
    """As paredes do exemplo são todas as posições brancas do desenho."""
    desenho = grade()
    brancas = {
        (linha, coluna)
        for linha, fundos in enumerate(desenho)
        for coluna, fundo in enumerate(fundos)
        if fundo == BRANCO
    }
    assert posicoes_de(ler_saida(ARQUIVO), "paredes") == brancas


@pytest.mark.parametrize(
    ("arquivo", "nome", "mensagem"),
    [
        (ARQUIVO, "corredor", "não existe"),
        ("d17\nfc7\n\n0,0\n", "saída", "entrada e a saída"),
        ("d17\nfc7\n\n0,0\n2,0\n\n", "células do caminho", "caminho"),
    ],
    ids=["elemento inválido", "sem saída", "sem caminho"],
)
def test_elemento_sem_dados(arquivo: str, nome: str, mensagem: str) -> None:
    """Elemento fora da lista ou rodapé incompleto derrubam a leitura.

    Args:
        arquivo: Conteúdo do arquivo de saída.
        nome: Elemento pedido.
        mensagem: Trecho esperado no erro.
    """
    with pytest.raises(ValueError, match=mensagem):
        posicoes_de(ler_saida(arquivo), nome)


def test_caminho_do_arquivo() -> None:
    """As letras do rodapé levam da entrada à saída."""
    assert caminho_do_arquivo(ler_saida(ARQUIVO)) == [(0, 0), (1, 0), (2, 0)]


@pytest.mark.parametrize(
    ("caminho", "mensagem"),
    [("EX", "'X'"), ("N", "fora da grade")],
    ids=["letra inválida", "sai da grade"],
)
def test_caminho_do_arquivo_invalido(caminho: str, mensagem: str) -> None:
    """Letra fora de N, E, S, W ou passo para fora da grade.

    Args:
        caminho: Linha 3 do rodapé.
        mensagem: Trecho esperado no erro.
    """
    labirinto = ler_saida(f"d17\nfc7\n\n0,0\n2,0\n{caminho}\n")
    with pytest.raises(ValueError, match=mensagem):
        caminho_do_arquivo(labirinto)


def test_caminho_marcado() -> None:
    """O ciano do exemplo é a corrente entrada, (1,0), saída."""
    assert caminho_marcado(grade(), (0, 0), (2, 0)) == [
        (0, 0), (1, 0), (2, 0),
    ]


def test_caminho_marcado_pela_volta() -> None:
    """Um caminho mais longo que o mais curto ainda é lido."""
    assert caminho_marcado(VOLTA, (0, 0), (1, 0)) == [
        (0, 0), (0, 1), (1, 1), (1, 0),
    ]


def com_ciano(linha: int, coluna: int) -> list[list[Cor]]:
    """O desenho de exemplo com uma posição a mais em ciano.

    Args:
        linha: Linha da posição.
        coluna: Coluna da posição.

    Returns:
        A grade de fundos.
    """
    desenho = grade()
    desenho[linha][coluna] = CIANO
    return desenho


@pytest.mark.parametrize(
    ("desenho", "mensagem"),
    [
        (com_ciano(2, 2), "canto"),
        (com_ciano(2, 3), "liga a célula"),
        (com_ciano(3, 5), "fora da corrente|passagens ciano"),
        (grade(caminho=False), "0 passagens ciano"),
    ],
    ids=["canto", "passagem solta", "célula solta", "sem caminho"],
)
def test_caminho_marcado_com_defeito(
    desenho: list[list[Cor]], mensagem: str
) -> None:
    """O ciano que não forma a corrente derruba a leitura.

    Args:
        desenho: Grade de fundos.
        mensagem: Trecho esperado no erro.
    """
    with pytest.raises(ValueError, match=mensagem):
        caminho_marcado(desenho, (0, 0), (2, 0))


def test_anel_ciano_fora_da_corrente() -> None:
    """Um anel ciano separado da corrente entre entrada e saída não passa."""
    desenho: list[list[Cor]] = [
        [BRANCO] * 7,
        [BRANCO, 45, BRANCO, CIANO, CIANO, CIANO, BRANCO],
        [BRANCO, CIANO, BRANCO, CIANO, BRANCO, CIANO, BRANCO],
        [BRANCO, 41, BRANCO, CIANO, CIANO, CIANO, BRANCO],
        [BRANCO] * 7,
    ]
    with pytest.raises(ValueError, match="fora da corrente"):
        caminho_marcado(desenho, (0, 0), (0, 1))


def test_distancia() -> None:
    """A busca em largura usa só as passagens abertas dos dois lados."""
    assert distancia(ler_saida(ANEL), (0, 0), (1, 0)) == 1
    assert distancia(ler_saida(ARQUIVO), (0, 0), (2, 1)) == 3
    with pytest.raises(ValueError, match="não é alcançável"):
        distancia(ler_saida(ARQUIVO), (0, 0), (0, 1))


@pytest.mark.parametrize(
    ("cores", "acoes"),
    [
        ([BRANCO, AMARELO], ["3"]),
        ([BRANCO, AMARELO, VERDE, AZUL, BRANCO], ["3", "3", "3", "3"]),
        ([BRANCO, BRANCO, AMARELO, AMARELO], ["2", "3", "9", "1", "4"]),
    ],
    ids=["um passo", "volta completa", "ações que não trocam"],
)
def test_rodizio(cores: list[Cor], acoes: list[str]) -> None:
    """Só a opção 3 avança a cor; inválidas e a 4 não desenham.

    Args:
        cores: Cor das paredes de cada renderização.
        acoes: Linhas enviadas ao menu.
    """
    conferir_rodizio(cores, acoes)


@pytest.mark.parametrize(
    ("cores", "acoes", "mensagem"),
    [
        ([AMARELO, VERDE], ["3"], "renderização 0"),
        ([BRANCO, VERDE], ["3"], "esperado amarelo"),
        ([BRANCO, AMARELO], ["1"], "nenhuma opção 3"),
        ([BRANCO], ["3"], "1 renderizações"),
        ([BRANCO, AMARELO, AMARELO], ["3", "3"], "renderização 2"),
    ],
    ids=["começa fora do branco", "pula cor", "sem 3", "falta renderização",
         "não avança"],
)
def test_rodizio_errado(
    cores: list[Cor], acoes: list[str], mensagem: str
) -> None:
    """Fora da ordem da I04 ou com renderizações a menos, falha.

    Args:
        cores: Cor das paredes de cada renderização.
        acoes: Linhas enviadas ao menu.
        mensagem: Trecho esperado no erro.
    """
    with pytest.raises(ValueError, match=mensagem):
        conferir_rodizio(cores, acoes)


@pytest.mark.parametrize(
    ("texto", "letras"),
    [
        ("nenhuma", set()),
        ("Norte", {"N"}),
        ("Norte e Sul", {"N", "S"}),
        ("Norte, Leste, Sul e Oeste", {"N", "E", "S", "W"}),
    ],
    ids=["nenhuma", "uma", "duas", "quatro"],
)
def test_direcoes(texto: str, letras: set[str]) -> None:
    """As paredes do passo viram letras, e de volta.

    Args:
        texto: Paredes como no passo.
        letras: Direções esperadas.
    """
    assert direcoes(texto) == letras
    assert direcoes(nomes_das_direcoes(letras).replace(", ", " e ")) == letras


@pytest.mark.parametrize(
    "texto", ["norte", "Norte e", "Nordeste"], ids=["caixa", "vazio", "outra"]
)
def test_direcao_invalida(texto: str) -> None:
    """Nome fora de Norte, Leste, Sul e Oeste derruba a leitura.

    Args:
        texto: Paredes como no passo.
    """
    with pytest.raises(ValueError, match="não existe"):
        direcoes(texto)


@pytest.mark.parametrize(
    ("cor", "nome"),
    [(None, "sem cor"), (CIANO, "ciano"), (31, "SGR 31")],
    ids=["padrão", "da lista", "fora da lista"],
)
def test_nome_da_cor(cor: Cor, nome: str) -> None:
    """Cores da I21 têm nome; as outras aparecem pelo código.

    Args:
        cor: Código SGR ou None.
        nome: Nome esperado.
    """
    assert nome_da_cor(cor) == nome
