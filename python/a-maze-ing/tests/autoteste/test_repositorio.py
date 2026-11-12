"""Testes dos passos que preparam e conferem o repositório de entrega."""

from pathlib import Path

import pytest

from step_defs.repositorio import (
    CONTEUDOS,
    REMOTO,
    Instalacao,
    arquivo_na_raiz,
    caminho_na_situacao,
    caminho_preparado,
    config_de,
    git_ou_falha,
    repositorio_no_estado,
    situacao_de_erro,
)
from suporte.config import CONFIG_BASE, Config
from suporte.estado import PROJECT_DIR, Estado


@pytest.fixture
def repositorio(cenario: Estado, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Repositório git temporário no lugar de project/.

    Tem ``a_maze_ing.py`` e ``.gitignore`` versionados, ``rascunho.txt``
    fora do git e ``maze.txt`` ignorado.

    Args:
        cenario: Estado numa pasta temporária.
        monkeypatch: Aponta o projeto dos passos para o repositório.

    Returns:
        A raiz do repositório, que também é o ``cwd`` do cenário.
    """
    raiz = cenario.cwd / "origem"
    raiz.mkdir()
    (raiz / "a_maze_ing.py").write_text("print(1)\n", encoding="utf-8")
    (raiz / ".gitignore").write_text("maze.txt\n", encoding="utf-8")
    git_ou_falha(["init", "-q"], raiz)
    git_ou_falha(["add", "-A"], raiz)
    git_ou_falha(["commit", "-q", "-m", "inicial"], raiz)
    (raiz / "rascunho.txt").write_text("fora do git\n", encoding="utf-8")
    (raiz / "maze.txt").write_text("9\n", encoding="utf-8")
    monkeypatch.setattr("step_defs.repositorio.PROJECT_DIR", raiz)
    cenario.cwd = raiz
    return raiz


def test_estado_atual_roda_em_project(cenario: Estado, tmp_path: Path) -> None:
    """O estado "atual" aponta o cenário para a pasta do projeto.

    Args:
        cenario: Estado numa pasta temporária.
        tmp_path: Pasta temporária do teste.
    """
    repositorio_no_estado(cenario, Instalacao(), tmp_path, "atual")
    assert cenario.cwd == PROJECT_DIR
    assert cenario.caminhos_extras == []


def test_estado_desconhecido_falha(cenario: Estado, tmp_path: Path) -> None:
    """Estado que os passos não conhecem derruba o cenário.

    Args:
        cenario: Estado numa pasta temporária.
        tmp_path: Pasta temporária do teste.
    """
    with pytest.raises(pytest.fail.Exception, match="espelho"):
        repositorio_no_estado(cenario, Instalacao(), tmp_path, "espelho")


def test_clone_limpo_so_tem_o_que_esta_no_git(
    cenario: Estado, repositorio: Path, tmp_path: Path
) -> None:
    """O clone recebe os arquivos versionados e um git próprio, limpo.

    Args:
        cenario: Estado numa pasta temporária.
        repositorio: Repositório temporário no lugar de project/.
        tmp_path: Pasta temporária do teste.
    """
    repositorio_no_estado(cenario, Instalacao(), tmp_path, "clone limpo")
    clone = tmp_path / "clone"
    assert cenario.cwd == clone
    assert cenario.caminhos_extras == [clone / ".venv" / "bin"]
    assert sorted(item.name for item in clone.iterdir()) == [
        ".git",
        ".gitignore",
        "a_maze_ing.py",
    ]
    assert git_ou_falha(["status", "--porcelain"], clone) == ""
    assert git_ou_falha(["rev-parse", "--show-toplevel"], clone).strip() == (
        str(clone.resolve())
    )


def test_arquivo_na_raiz_aceita_glob(cenario: Estado) -> None:
    """O arquivo é procurado por caminho ou por glob no repositório.

    Args:
        cenario: Estado numa pasta temporária.
    """
    (cenario.cwd / "mazegen-1.0.0.tar.gz").write_text("", encoding="utf-8")
    arquivo_na_raiz(cenario, "mazegen-*")
    with pytest.raises(pytest.fail.Exception, match="não existe"):
        arquivo_na_raiz(cenario, "Makefile")


@pytest.mark.parametrize("tipo", sorted(CONTEUDOS))
def test_caminho_preparado_com_conteudo(cenario: Estado, tipo: str) -> None:
    """Cada tipo grava o seu conteúdo e desliga a gravação do config.

    Args:
        cenario: Estado numa pasta temporária.
        tipo: Tipo de arquivo preparado.
    """
    alvo = cenario.cwd / "sub" / "cfg.txt"
    caminho_preparado(cenario, "sub/cfg.txt", tipo)
    assert alvo in cenario.sem_gravacao
    if tipo == "sem permissão de leitura":
        assert alvo.stat().st_mode & 0o777 == 0
    else:
        assert alvo.read_bytes() == CONTEUDOS[tipo]()


@pytest.mark.parametrize(
    "tipo",
    [
        "bytes binários aleatórios",
        "só WÍDTH=20 e HEÍGHT=15, com acento",
        "não UTF-8",
    ],
)
def test_conteudo_que_o_nome_promete(tipo: str) -> None:
    """Os aleatórios e o latin-1 não são UTF-8; o config acentuado é.

    Args:
        tipo: Tipo de arquivo preparado.
    """
    conteudo = CONTEUDOS[tipo]()
    if tipo == "só WÍDTH=20 e HEÍGHT=15, com acento":
        assert conteudo.decode("utf-8") == "WÍDTH=20\nHEÍGHT=15\n"
        return
    with pytest.raises(UnicodeDecodeError):
        conteudo.decode("utf-8")
    if tipo == "não UTF-8":
        assert "WIDTH=20" in conteudo.decode("latin-1").splitlines()


def test_caminho_preparado_inexistente_guarda_o_original(
    cenario: Estado,
) -> None:
    """O arquivo some durante o cenário e volta no fim.

    Args:
        cenario: Estado numa pasta temporária.
    """
    alvo = cenario.cwd / "maze.txt"
    alvo.write_text("original", encoding="utf-8")
    caminho_preparado(cenario, "maze.txt", "inexistente")
    assert not alvo.exists()
    cenario.restaurar()
    assert alvo.read_text(encoding="utf-8") == "original"


def test_caminho_preparado_como_diretorio(cenario: Estado) -> None:
    """A pasta é criada com os pais e tudo o que foi criado some no fim.

    Args:
        cenario: Estado numa pasta temporária.
    """
    caminho_preparado(cenario, "build/lib/mazegen", "diretório")
    assert (cenario.cwd / "build" / "lib" / "mazegen").is_dir()
    cenario.restaurar()
    assert not (cenario.cwd / "build").exists()


def test_diretorio_que_ja_existia_fica(cenario: Estado) -> None:
    """Preparar como diretório uma pasta existente não a apaga no fim.

    Args:
        cenario: Estado numa pasta temporária.
    """
    (cenario.cwd / "mazegen").mkdir()
    caminho_preparado(cenario, "mazegen", "diretório")
    cenario.restaurar()
    assert (cenario.cwd / "mazegen").is_dir()


def test_caminho_preparado_tipo_desconhecido(cenario: Estado) -> None:
    """Tipo que os passos não conhecem derruba o cenário sem criar nada.

    Args:
        cenario: Estado numa pasta temporária.
    """
    with pytest.raises(pytest.fail.Exception, match="não implementado"):
        caminho_preparado(cenario, "cfg.txt", "link simbólico")
    assert list(cenario.cwd.iterdir()) == []


def test_config_base_e_do_repositorio(cenario: Estado) -> None:
    """O config vem da lista base ou do config.txt da pasta do cenário.

    Args:
        cenario: Estado numa pasta temporária.
    """
    config_de(cenario, "base")
    base = cenario.config
    assert base == Config(CONFIG_BASE)
    assert base is not None and base.linhas is not CONFIG_BASE
    with pytest.raises(pytest.fail.Exception, match="config.txt"):
        config_de(cenario, "do repositório")
    (cenario.cwd / "config.txt").write_text(
        "# largura\nWIDTH=20\n", encoding="utf-8"
    )
    config_de(cenario, "do repositório")
    assert cenario.config == Config(["# largura", "WIDTH=20"])


@pytest.mark.parametrize(
    ("situacao", "linha"),
    [
        ("valor inválido", "WIDTH=abc"),
        ("parâmetros impossíveis", "EXIT=0,0"),
        (
            "OUTPUT_FILE num diretório inexistente",
            "OUTPUT_FILE=diretorio_inexistente/maze.txt",
        ),
    ],
)
def test_situacao_de_erro_muda_o_config(
    cenario: Estado, situacao: str, linha: str
) -> None:
    """A situação troca a linha da chave no config do cenário.

    Args:
        cenario: Estado numa pasta temporária.
        situacao: Situação de erro pedida pelo passo.
        linha: Linha que o config passa a ter.
    """
    cenario.config = Config(list(CONFIG_BASE))
    situacao_de_erro(cenario, situacao)
    assert linha in cenario.config.linhas
    assert len(cenario.config.linhas) == len(CONFIG_BASE)


def test_situacao_chave_obrigatoria_ausente(cenario: Estado) -> None:
    """A situação tira a linha de WIDTH do config.

    Args:
        cenario: Estado numa pasta temporária.
    """
    cenario.config = Config(list(CONFIG_BASE))
    situacao_de_erro(cenario, "chave obrigatória ausente")
    assert cenario.config.linhas == CONFIG_BASE[1:]


def test_situacoes_do_arquivo_preparam_o_destino(cenario: Estado) -> None:
    """Arquivo inexistente e sem leitura agem no destino do config.

    Args:
        cenario: Estado numa pasta temporária.
    """
    cenario.config = Config(list(CONFIG_BASE))
    destino = cenario.cwd / "cfg.txt"
    situacao_de_erro(cenario, "arquivo de configuração inexistente")
    cenario.gravar_config()
    assert not destino.exists()
    situacao_de_erro(
        cenario, "arquivo de configuração sem permissão de leitura"
    )
    assert destino.stat().st_mode & 0o777 == 0


def test_situacao_de_erro_invalida(cenario: Estado) -> None:
    """Sem config ou com situação desconhecida o passo falha.

    Args:
        cenario: Estado numa pasta temporária.
    """
    with pytest.raises(pytest.fail.Exception, match="config antes"):
        situacao_de_erro(cenario, "valor inválido")
    cenario.config = Config(list(CONFIG_BASE))
    with pytest.raises(pytest.fail.Exception, match="não existe"):
        situacao_de_erro(cenario, "disco cheio")


def test_caminho_existe_e_nao_esta_vazio(cenario: Estado) -> None:
    """Existência e conteúdo aceitam arquivo, pasta e glob.

    Args:
        cenario: Estado numa pasta temporária.
    """
    (cenario.cwd / "vazio.txt").write_text("", encoding="utf-8")
    (cenario.cwd / "pasta").mkdir()
    (cenario.cwd / "cheio.txt").write_text("x", encoding="utf-8")
    caminho_na_situacao(cenario, "vazio.txt", "existe")
    caminho_na_situacao(cenario, "pasta/", "existe")
    caminho_na_situacao(cenario, "*.py", "não existe")
    caminho_na_situacao(cenario, "cheio.*", "não está vazio")
    for caminho, situacao in [
        ("ausente.txt", "existe"),
        ("cheio.txt", "não existe"),
        ("vazio.txt", "não está vazio"),
        ("pasta", "não está vazio"),
        ("ausente.txt", "não está vazio"),
    ]:
        with pytest.raises(pytest.fail.Exception):
            caminho_na_situacao(cenario, caminho, situacao)


def test_caminho_no_git(cenario: Estado, repositorio: Path) -> None:
    """Versionado e ignorado são perguntados ao git do repositório.

    Args:
        cenario: Estado numa pasta temporária.
        repositorio: Repositório temporário no lugar de project/.
    """
    caminho_na_situacao(cenario, "a_maze_ing.py", "está versionado no git")
    caminho_na_situacao(cenario, "maze.txt", "é ignorado pelo git")
    caminho_na_situacao(cenario, "rascunho.txt", "não é ignorado pelo git")
    for caminho, situacao in [
        ("rascunho.txt", "está versionado no git"),
        ("rascunho.txt", "é ignorado pelo git"),
        ("maze.txt", "não é ignorado pelo git"),
    ]:
        with pytest.raises(pytest.fail.Exception):
            caminho_na_situacao(cenario, caminho, situacao)
    assert cenario.cwd == repositorio


def test_clone_limpo_usa_o_commit(
    cenario: Estado, repositorio: Path, tmp_path: Path
) -> None:
    """Mudança não commitada num arquivo versionado não entra no clone.

    Args:
        cenario: Estado numa pasta temporária.
        repositorio: Repositório temporário no lugar de project/.
        tmp_path: Pasta temporária do teste.
    """
    (repositorio / "a_maze_ing.py").write_text("print(2)\n", encoding="utf-8")
    repositorio_no_estado(cenario, Instalacao(), tmp_path, "clone limpo")
    assert (cenario.cwd / "a_maze_ing.py").read_text(
        encoding="utf-8"
    ) == "print(1)\n"


def modelo_que_ignora(pasta: Path) -> Path:
    """Modelo de git init cujo info/exclude ignora rascunho.txt.

    Args:
        pasta: Pasta onde o modelo é criado.

    Returns:
        A pasta do modelo.
    """
    modelo = pasta / "modelo"
    (modelo / "info").mkdir(parents=True)
    (modelo / "info" / "exclude").write_text(
        "rascunho.txt\n", encoding="utf-8"
    )
    return modelo


@pytest.mark.parametrize(
    "variavel", ["GIT_CONFIG_GLOBAL", "GIT_CONFIG_SYSTEM", "GIT_TEMPLATE_DIR"]
)
def test_git_da_suite_ignora_a_configuracao_de_quem_roda(
    cenario: Estado,
    repositorio: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    variavel: str,
) -> None:
    """Um modelo de git init vindo da máquina não esconde arquivos no clone.

    Args:
        cenario: Estado numa pasta temporária.
        repositorio: Repositório temporário no lugar de project/.
        tmp_path: Pasta temporária do teste.
        monkeypatch: Define a variável de ambiente do git.
        variavel: Variável que traz o modelo para o git.
    """
    modelo = modelo_que_ignora(tmp_path)
    if variavel == "GIT_TEMPLATE_DIR":
        monkeypatch.setenv(variavel, str(modelo))
    else:
        configuracao = tmp_path / "gitconfig"
        configuracao.write_text(
            f"[init]\n\ttemplateDir = {modelo}\n", encoding="utf-8"
        )
        monkeypatch.setenv(variavel, str(configuracao))
    repositorio_no_estado(cenario, Instalacao(), tmp_path, "clone limpo")
    caminho_na_situacao(cenario, "rascunho.txt", "não é ignorado pelo git")


def test_clone_do_remoto_sem_a_variavel(
    cenario: Estado, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Sem AMAZEING_REMOTE o cenário é pulado dizendo qual variável falta.

    Args:
        cenario: Estado numa pasta temporária.
        tmp_path: Pasta temporária do teste.
        monkeypatch: Remove a variável do ambiente.
    """
    monkeypatch.delenv(REMOTO, raising=False)
    with pytest.raises(pytest.skip.Exception, match=REMOTO):
        repositorio_no_estado(
            cenario, Instalacao(), tmp_path, "clone do remoto"
        )


def test_clone_do_remoto_clona_a_url(
    cenario: Estado,
    repositorio: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Com AMAZEING_REMOTE o cenário roda num clone dessa URL.

    Args:
        cenario: Estado numa pasta temporária.
        repositorio: Repositório que faz o papel do remoto.
        tmp_path: Pasta temporária do teste.
        monkeypatch: Define a variável no ambiente.
    """
    monkeypatch.setenv(REMOTO, repositorio.as_uri())
    repositorio_no_estado(cenario, Instalacao(), tmp_path, "clone do remoto")
    clone = tmp_path / "remoto"
    assert cenario.cwd == clone
    assert cenario.caminhos_extras == [clone / ".venv" / "bin"]
    assert sorted(item.name for item in clone.iterdir()) == [
        ".git",
        ".gitignore",
        "a_maze_ing.py",
    ]


def test_diretorio_preparado_nao_e_protegido_de_novo(cenario: Estado) -> None:
    """A pasta preparada como OUTPUT_FILE continua lá quando o programa roda.

    Args:
        cenario: Estado numa pasta temporária.
    """
    (cenario.cwd / "cfg.txt").write_text(
        "OUTPUT_FILE=pasta\n", encoding="utf-8"
    )
    (cenario.cwd / "a_maze_ing.py").write_text(
        'import os\nprint(os.path.isdir("pasta"))\n', encoding="utf-8"
    )
    caminho_preparado(cenario, "pasta", "diretório")
    execucao = cenario.executar("python3 a_maze_ing.py cfg.txt")
    assert execucao.saida_padrao == "True\n"
    cenario.restaurar()
    assert not (cenario.cwd / "pasta").exists()


def test_diretorio_existente_fica_vazio_e_volta(cenario: Estado) -> None:
    """A pasta que existia é reservada, fica vazia e volta inteira no fim.

    Args:
        cenario: Estado numa pasta temporária.
    """
    pasta = cenario.cwd / "mazegen"
    pasta.mkdir()
    (pasta / "gerador.py").write_text("", encoding="utf-8")
    caminho_preparado(cenario, "mazegen", "diretório")
    assert cenario.reservado(pasta)
    assert pasta in cenario.sem_gravacao
    assert list(pasta.iterdir()) == []
    cenario.restaurar()
    assert (pasta / "gerador.py").is_file()


def test_diretorio_pai_criado(cenario: Estado) -> None:
    """Só a pasta pai passa a existir; o caminho fica reservado e ausente.

    Args:
        cenario: Estado numa pasta temporária.
    """
    caminho_preparado(cenario, "saida/labirinto.txt", "diretório pai criado")
    alvo = cenario.cwd / "saida" / "labirinto.txt"
    assert alvo.parent.is_dir()
    assert not alvo.exists()
    assert cenario.reservado(alvo)
    assert alvo in cenario.sem_gravacao


def test_diretorio_sem_permissao_de_escrita(cenario: Estado) -> None:
    """A pasta existe, recusa arquivos novos e some no fim.

    Args:
        cenario: Estado numa pasta temporária.
    """
    caminho_preparado(
        cenario, "trancado", "diretório sem permissão de escrita"
    )
    alvo = cenario.cwd / "trancado"
    assert alvo.stat().st_mode & 0o777 == 0o500
    with pytest.raises(PermissionError):
        (alvo / "maze.txt").write_text("9\n", encoding="utf-8")
    cenario.restaurar()
    assert not alvo.exists()


PASTA_DO_PROGRAMA = "pasta com a_maze_ing.py, amazeing/ e config.txt"


def test_pasta_com_o_programa(cenario: Estado) -> None:
    """A pasta recebe a cópia dos três itens, sem __pycache__.

    Args:
        cenario: Estado numa pasta temporária.
    """
    (cenario.cwd / "a_maze_ing.py").write_text("print(1)\n", encoding="utf-8")
    (cenario.cwd / "config.txt").write_text("WIDTH=20\n", encoding="utf-8")
    (cenario.cwd / "amazeing" / "__pycache__").mkdir(parents=True)
    (cenario.cwd / "amazeing" / "ui.py").write_text("", encoding="utf-8")
    caminho_preparado(cenario, "teste", PASTA_DO_PROGRAMA)
    copia = cenario.cwd / "teste"
    assert sorted(item.name for item in copia.iterdir()) == [
        "a_maze_ing.py",
        "amazeing",
        "config.txt",
    ]
    assert [item.name for item in (copia / "amazeing").iterdir()] == ["ui.py"]
    assert (copia / "config.txt").read_text(encoding="utf-8") == "WIDTH=20\n"
    cenario.restaurar()
    assert not copia.exists()


def test_pasta_com_o_programa_sem_a_origem(cenario: Estado) -> None:
    """Item que falta na raiz derruba o passo sem criar nada.

    Args:
        cenario: Estado numa pasta temporária.
    """
    (cenario.cwd / "a_maze_ing.py").write_text("", encoding="utf-8")
    with pytest.raises(pytest.fail.Exception, match="amazeing, config.txt"):
        caminho_preparado(cenario, "teste", PASTA_DO_PROGRAMA)
    assert [item.name for item in cenario.cwd.iterdir()] == ["a_maze_ing.py"]


@pytest.mark.parametrize(
    "tipo", ["sem permissão de leitura", "diretório sem permissão de escrita"]
)
def test_tipo_que_depende_de_permissao_pula_como_root(
    cenario: Estado, monkeypatch: pytest.MonkeyPatch, tipo: str
) -> None:
    """Como root o chmod não barra nada: o cenário é pulado com o motivo.

    Args:
        cenario: Estado numa pasta temporária.
        monkeypatch: Finge que o processo roda como root.
        tipo: Tipo que depende de permissão.
    """
    monkeypatch.setattr("step_defs.repositorio.os.geteuid", lambda: 0)
    with pytest.raises(pytest.skip.Exception, match="root"):
        caminho_preparado(cenario, "sub/alvo", tipo)
    assert list(cenario.cwd.iterdir()) == []


def test_pastas_pai_criadas_somem_no_fim(cenario: Estado) -> None:
    """Config, arquivos e pastas preparados em subpastas não deixam rastro.

    Args:
        cenario: Estado numa pasta temporária.
    """
    cenario.config = Config(["WIDTH=20"], "configs/grande.txt")
    cenario.gravar_config()
    caminho_preparado(cenario, "sub/cfg.txt", "vazio")
    caminho_preparado(cenario, "a/b/c", "diretório")
    caminho_preparado(cenario, "saida/fundo/maze.txt", "diretório pai criado")
    caminho_preparado(
        cenario, "x/trancado", "diretório sem permissão de escrita"
    )
    caminho_preparado(cenario, "y/fechado.txt", "sem permissão de leitura")
    cenario.restaurar()
    assert list(cenario.cwd.iterdir()) == []
