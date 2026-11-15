"""Testes da leitura da renderização no terminal."""

import pytest

from autoteste.desenho import (
    ANEL,
    ARQUIVO,
    AZUL,
    BRANCO,
    CAMINHO,
    CIANO,
    CINZA,
    GRAFITE,
    LARANJA,
    MAGENTA,
    TEXTO_DO_MENU,
    VERDE,
    VERMELHO,
    com_caminho,
    com_simbolo,
    com_texto,
    desenhar,
    grade,
    montar,
    saida,
    volta,
)
from suporte.labirinto import ler_saida
from suporte.render import (
    GLIFOS,
    Caractere,
    Cor,
    Posicao,
    Renderizacao,
    Tela,
    bracos,
    caminho_do_arquivo,
    caminho_marcado,
    cantos,
    conferir_rodizio,
    cor_das_paredes,
    desenho_do_caminho,
    dimensoes,
    direcoes,
    distancia,
    grade_desenhada,
    nome_da_cor,
    nomes_das_direcoes,
    paredes_desenhadas,
    paredes_na_tela,
    posicoes_da_cor,
    posicoes_de,
    problemas_de_sgr,
    problemas_do_formato,
    renderizacoes,
    seguida_do_menu,
    sequencias_que_nao_sao_sgr,
    tela,
    trocas_sem_mudanca,
    visiveis,
)


def bloco(desenho: Tela) -> Renderizacao:
    """Renderização só com as linhas desenhadas.

    Args:
        desenho: Caracteres e cores.

    Returns:
        O bloco, sem linhas depois dele.
    """
    return Renderizacao(desenhar(desenho).split("\n"), [])


def nao_espacos(desenho: Tela) -> set[Posicao]:
    """Posições do desenho cujo caractere não é espaço.

    Args:
        desenho: Caracteres e cores.

    Returns:
        As posições.
    """
    return {
        (linha, coluna)
        for linha, caracteres in enumerate(desenho)
        for coluna, caractere in enumerate(caracteres)
        if caractere.simbolo != " "
    }


def test_divide_a_saida_em_renderizacoes() -> None:
    """Cada exibição vira um bloco seguido do menu."""
    blocos = renderizacoes(saida(grade(), grade(LARANJA)), 2)
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


def test_sgr_como_maquina_de_estado() -> None:
    """38;2 troca o texto, 48;2 o fundo, e 0 ou vazio zeram os dois."""
    linha = (
        "\x1b[38;2;1;2;3;48;2;4;5;6mA\x1b[48;2;7;8;9mB\x1b[0mC"
        "\x1b[38;2;1;1;1mD\x1b[mE\x1b[0;48;2;0;0;0mF"
    )
    assert visiveis(linha) == [
        Caractere("A", (1, 2, 3), (4, 5, 6)),
        Caractere("B", (1, 2, 3), (7, 8, 9)),
        Caractere("C", None, None),
        Caractere("D", (1, 1, 1), None),
        Caractere("E", None, None),
        Caractere("F", None, (0, 0, 0)),
    ]


def test_tela_le_caracteres_e_cores() -> None:
    """Cada caractere vira uma posição com o texto e o fundo dele."""
    assert tela(bloco(grade())) == grade()


def test_tela_com_linhas_desiguais() -> None:
    """Linhas de tamanhos diferentes derrubam a leitura."""
    linhas = desenhar(grade()).split("\n")
    linhas[2] = linhas[2].replace("┫", "┫ ")
    with pytest.raises(ValueError, match="números diferentes"):
        tela(Renderizacao(linhas, []))


@pytest.mark.parametrize(
    ("linha", "problema"),
    [
        ("\x1b[31m ┃\x1b[0m", "'31' não é cor de 24 bits"),
        ("\x1b[1;38;2;1;2;3m ┃\x1b[0m", "'1' não é cor de 24 bits"),
        ("\x1b[2J\x1b[38;2;1;2;3m ┃\x1b[0m", "não é SGR"),
        ("\x1b[38;5;7m ┃\x1b[0m", "'38' sem 2;R;G;B"),
        ("\x1b[48;2;300;0;0m ┃\x1b[0m", "'48' sem 2;R;G;B"),
        ("\x1b[48;2;1;2m ┃\x1b[0m", "'48' sem 2;R;G;B"),
        ("\x1bc\x1b[38;2;1;2;3m ┃\x1b[0m", "ESC fora"),
    ],
    ids=["16 cores", "negrito", "limpa a tela", "256 cores",
         "canal acima de 255", "canal faltando", "ESC solto"],
)
def test_sequencia_que_nao_e_24_bits(linha: str, problema: str) -> None:
    """Só cores de texto e de fundo de 24 bits e o reset passam.

    Args:
        linha: Linha desenhada.
        problema: Trecho esperado no primeiro problema.
    """
    assert problema in problemas_de_sgr(linha)[0]


def test_linha_so_com_24_bits() -> None:
    """As sequências do desenho de exemplo não são problema."""
    for linha in desenhar(grade()).split("\n"):
        assert problemas_de_sgr(linha) == []


def test_formato_das_linhas_do_exemplo() -> None:
    """As linhas do exemplo seguem a forma da I02 e só trocam de par."""
    for linha in desenhar(grade()).split("\n"):
        assert problemas_do_formato(linha) == []
        assert trocas_sem_mudanca(linha) == []


PAR_UM = "\x1b[38;2;1;2;3;48;2;4;5;6m"
PAR_DOIS = "\x1b[38;2;9;9;9;48;2;4;5;6m"


@pytest.mark.parametrize(
    ("linha", "problema"),
    [
        ("", "não tem sequência"),
        (f" {PAR_UM}┃\x1b[0m", "não abre"),
        ("\x1b[38;2;1;2;3m\x1b[48;2;4;5;6m┃\x1b[0m", "não abre"),
        (f"{PAR_UM}┃\x1b[0m┃", "não termina com o reset"),
        (f"{PAR_UM}┃", "não termina com o reset"),
        (f"{PAR_UM}┃\x1b[0m{PAR_UM}┃\x1b[0m", "no meio da linha"),
    ],
    ids=["vazia", "caractere antes", "texto e fundo separados",
         "caractere depois do reset", "sem reset", "reset no meio"],
)
def test_formato_fora_da_i02(linha: str, problema: str) -> None:
    """Sequência que não abre a linha ou reset fora do fim são problema.

    Args:
        linha: Linha desenhada.
        problema: Trecho esperado no primeiro problema.
    """
    assert problema in problemas_do_formato(linha)[0]


@pytest.mark.parametrize(
    ("linha", "problemas"),
    [
        (f"{PAR_UM}┃{PAR_DOIS}━\x1b[0m", 0),
        (f"{PAR_UM}┃{PAR_UM}━\x1b[0m", 1),
        (f"{PAR_UM}{PAR_DOIS}━\x1b[0m", 1),
        (f"{PAR_UM}┃{PAR_UM}━{PAR_UM}━\x1b[0m", 2),
    ],
    ids=["troca", "repete o par", "sem caractere", "repete duas vezes"],
)
def test_trocas_sem_mudanca(linha: str, problemas: int) -> None:
    """Só a sequência que muda o par do caractere seguinte é aceita.

    Args:
        linha: Linha desenhada.
        problemas: Número de sequências sobrando.
    """
    assert len(trocas_sem_mudanca(linha)) == problemas


def test_sequencias_que_nao_sao_sgr() -> None:
    """ESC c, ESC 7, CSI de controle e ESC solto contam; SGR não."""
    texto = f"{PAR_UM}x\x1b[0m\x1bc\x1b[2J\x1b7\x1b[2J\x1b"
    assert sequencias_que_nao_sao_sgr(texto) == [
        "\x1bc", "\x1b[2J", "\x1b7", "\x1b",
    ]


@pytest.mark.parametrize(
    "desenho",
    [
        montar((" " * 12,) * 3, GRAFITE, {}),
        montar((" " * 13,) * 4, GRAFITE, {}),
        montar((" ",), GRAFITE, {}),
        [],
    ],
    ids=["colunas fora de 4m + 1", "linhas pares", "um caractere", "vazio"],
)
def test_dimensoes_sem_grade(desenho: Tela) -> None:
    """Uma grade precisa de 2n + 1 linhas de 4m + 1 caracteres.

    Args:
        desenho: Caracteres e cores.
    """
    with pytest.raises(ValueError, match="2n \\+ 1 linhas de 4m \\+ 1"):
        dimensoes(desenho)


def test_grade_desenhada_igual_ao_arquivo() -> None:
    """Os caracteres de parede viram os bits do arquivo."""
    desenho = grade(VERDE)
    assert dimensoes(desenho) == (3, 2)
    assert cor_das_paredes(desenho) == VERDE
    assert grade_desenhada(desenho) == ler_saida(ARQUIVO).grade
    assert grade_desenhada(grade(caminho=False)) == ler_saida(ARQUIVO).grade
    assert paredes_desenhadas(desenho, (1, 1)) == {"S", "W"}


def test_parede_desenhada_em_parte() -> None:
    """Uma parede horizontal com só parte dos ━ derruba a leitura."""
    desenho = com_simbolo(grade(), [(4, 6)], " ")
    with pytest.raises(ValueError, match="Sul da célula \\(1, 1\\).*só em"):
        paredes_desenhadas(desenho, (1, 1))


def test_cantos_pelos_bracos_das_paredes() -> None:
    """Os braços das paredes desenhadas dão o caractere de cada canto."""
    desenho = grade()
    fechadas = paredes_na_tela(desenho)
    assert (1, 4) not in fechadas
    assert {(2, 1), (3, 4)} <= fechadas
    for linha, coluna in cantos(3, 2):
        simbolo = desenho[linha][coluna].simbolo
        assert GLIFOS[bracos(fechadas, (linha, coluna))] == simbolo


@pytest.mark.parametrize(
    ("nome", "esperadas"),
    [
        ("entrada", {(1, 1), (1, 2), (1, 3)}),
        ("saída", {(1, 9), (1, 10), (1, 11)}),
        ("células do caminho", {(1, 6)}),
        ("passagens do caminho",
         {(1, 3), (1, 4), (1, 5), (1, 7), (1, 8), (1, 9)}),
        ("42", {(3, 1), (3, 2), (3, 3)}),
    ],
    ids=["entrada", "saída", "células", "passagens", "42"],
)
def test_posicoes_dos_elementos(nome: str, esperadas: set[Posicao]) -> None:
    """Cada elemento ocupa as posições dadas pelo arquivo.

    Args:
        nome: Elemento.
        esperadas: Posições (linha, coluna).
    """
    assert posicoes_de(ler_saida(ARQUIVO), nome) == esperadas


def test_paredes_sao_os_caracteres_de_parede() -> None:
    """As paredes do exemplo são todos os caracteres que não são espaço."""
    paredes = posicoes_de(ler_saida(ARQUIVO), "paredes")
    assert paredes == nao_espacos(grade(caminho=False))


def test_42_com_paredes_internas() -> None:
    """Num bloco 2x2 de células F, as paredes entre elas são do 42.

    O canto do meio fica fora: o desenho do 42 não tem bloco 2x2, e a I02
    só pinta as paredes entre duas células F.
    """
    posicoes = posicoes_de(ler_saida("ff\nff\n\n0,0\n1,0\nE\n"), "42")
    interiores = {
        (linha, coluna) for linha in (1, 3) for coluna in (1, 2, 3, 5, 6, 7)
    }
    internas = {(1, 4), (3, 4)} | {
        (2, coluna) for coluna in (1, 2, 3, 5, 6, 7)
    }
    assert posicoes == interiores | internas


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


def test_desenho_do_caminho() -> None:
    """O caminho do arquivo vira os caracteres ciano da I02."""
    celulas = caminho_do_arquivo(ler_saida(ARQUIVO))
    assert desenho_do_caminho(celulas) == CAMINHO


def test_caminho_marcado() -> None:
    """O ciano do exemplo é a corrente entrada, (1,0), saída."""
    assert caminho_marcado(grade(), (0, 0), (2, 0)) == [
        (0, 0), (1, 0), (2, 0),
    ]


def test_caminho_marcado_pela_volta() -> None:
    """Um caminho mais longo que o mais curto ainda é lido."""
    assert caminho_marcado(volta(), (0, 0), (1, 0)) == [
        (0, 0), (0, 1), (1, 1), (1, 0),
    ]


@pytest.mark.parametrize(
    ("desenho", "mensagem"),
    [
        (com_texto(grade(), 2, 4, CIANO), "canto"),
        (com_caminho(grade(), {(2, 1): "━"}), "fora do meio"),
        (com_caminho(grade(), {(2, 6): "┃"}), "liga a célula \\(1, 1\\)"),
        (com_caminho(grade(), {(3, 10): "╹"}), "0 passagens ciano"),
        (grade(caminho=False), "centro da entrada"),
        (com_simbolo(grade(), [(1, 6)], "╋"), "pedem '━'"),
        (com_simbolo(grade(), [(1, 4)], "┃"), "não '━'"),
        (com_texto(grade(), 1, 4, GRAFITE), "2 dos 3"),
        (com_texto(grade(), 1, 10, GRAFITE), "centro da saída"),
    ],
    ids=["canto", "parede fora do meio", "passagem solta", "célula solta",
         "sem caminho", "centro com braço errado", "passagem com caractere "
         "errado", "passagem incompleta", "saída sem ciano"],
)
def test_caminho_marcado_com_defeito(desenho: Tela, mensagem: str) -> None:
    """O ciano que não forma a corrente derruba a leitura.

    Args:
        desenho: Caracteres e cores.
        mensagem: Trecho esperado no erro.
    """
    with pytest.raises(ValueError, match=mensagem):
        caminho_marcado(desenho, (0, 0), (2, 0))


def test_anel_ciano_fora_da_corrente() -> None:
    """Um anel ciano separado da corrente entre entrada e saída não passa."""
    desenho = com_caminho(
        montar((" " * 13,) * 5, GRAFITE, {}),
        {
            (1, 2): "╻", (2, 2): "┃", (3, 2): "╹",
            (1, 6): "┏", (1, 7): "━", (1, 8): "━", (1, 9): "━",
            (1, 10): "┓", (2, 6): "┃", (2, 10): "┃", (3, 6): "┗",
            (3, 7): "━", (3, 8): "━", (3, 9): "━", (3, 10): "┛",
        },
    )
    with pytest.raises(ValueError, match="fora da corrente"):
        caminho_marcado(desenho, (0, 0), (0, 1))


def test_cor_aparece_no_fundo_e_no_texto_que_nao_e_espaco() -> None:
    """O texto dos espaços não conta; o fundo conta em todo caractere."""
    desenho = grade()
    assert posicoes_da_cor(desenho, GRAFITE) == nao_espacos(
        grade(caminho=False)
    ) - set(CAMINHO)
    assert posicoes_da_cor(desenho, CIANO) == set(CAMINHO)
    assert posicoes_da_cor(desenho, CINZA) == {(3, 1), (3, 2), (3, 3)}
    assert len(posicoes_da_cor(desenho, BRANCO)) == 5 * 13 - 9


def test_distancia() -> None:
    """A busca em largura usa só as passagens abertas dos dois lados."""
    assert distancia(ler_saida(ANEL), (0, 0), (1, 0)) == 1
    assert distancia(ler_saida(ARQUIVO), (0, 0), (2, 1)) == 3
    with pytest.raises(ValueError, match="não é alcançável"):
        distancia(ler_saida(ARQUIVO), (0, 0), (0, 1))


@pytest.mark.parametrize(
    ("cores", "acoes"),
    [
        ([GRAFITE, LARANJA], ["3"]),
        ([GRAFITE, LARANJA, VERDE, AZUL, GRAFITE], ["3", "3", "3", "3"]),
        ([GRAFITE, GRAFITE, LARANJA, LARANJA], ["2", "3", "9", "1", "4"]),
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
        ([LARANJA, VERDE], ["3"], "renderização 0"),
        ([GRAFITE, VERDE], ["3"], "esperado laranja"),
        ([GRAFITE, LARANJA], ["1"], "nenhuma opção 3"),
        ([GRAFITE], ["3"], "1 renderizações"),
        ([GRAFITE, LARANJA, LARANJA], ["3", "3"], "renderização 2"),
    ],
    ids=["começa fora do grafite", "pula cor", "sem 3", "falta renderização",
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
    [
        (None, "sem cor"),
        (CIANO, "ciano"),
        (MAGENTA, "magenta"),
        (VERMELHO, "vermelho"),
        ((1, 2, 3), "RGB 1,2,3"),
    ],
    ids=["sem cor", "ciano", "magenta", "vermelho", "fora da lista"],
)
def test_nome_da_cor(cor: Cor, nome: str) -> None:
    """Cores da I21 têm nome; as outras aparecem pelo RGB.

    Args:
        cor: RGB ou None.
        nome: Nome esperado.
    """
    assert nome_da_cor(cor) == nome
