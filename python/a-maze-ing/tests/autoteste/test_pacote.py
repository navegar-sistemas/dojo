"""Testes dos virtualenvs, dos pacotes mazegen-* e dos arquivos de texto."""

import io
import tarfile
import zipfile
from collections.abc import Callable
from pathlib import Path

import pytest

from step_defs.pacote import (
    PROPRIEDADES,
    ambiente_do_virtualenv,
    arquivo_contem,
    metadado_do_pacote,
    pacote_confirma,
    secao_do_readme_contem,
    virtualenv_novo,
)
from step_defs.repositorio import git_ou_falha
from suporte.estado import Estado
from suporte.pacote import (
    abrir_pacote,
    nome_e_versao,
    secao_markdown,
    versao_do_pyproject,
)

Mudanca = Callable[[dict[str, bytes]], None]

WHEEL = "mazegen-1.0.0-py3-none-any.whl"
SDIST = "mazegen-1.0.0.tar.gz"
INFO = "mazegen-1.0.0.dist-info"
TOPO = "mazegen-1.0.0/"
INIT = '''"""Gera labirintos falsos.

Example:
    from mazegen import MazeGenerator
"""


class MazeGenerator:
    """Gerador."""
'''
GERADOR = '"""Fachada."""\n'
README = (
    "*Primeira linha.*\n\n# Projeto\n\n## Instructions\n\n```sh\n"
    "# make install\n```\n\nmake run\n\n### Detalhe\n\nfim\n\n"
    "## Resources\n\nhttps://exemplo\n"
)
LICENCA = "MIT License\n\nCopyright (c) 2026 alguem\n"
PYPROJECT = (
    '[build-system]\nrequires = ["setuptools>=77"]\n\n[project]\n'
    'name = "mazegen"\nversion = "1.0.0"  # fonte única\n\n'
    '[tool.outro]\nversion = "9"\n'
)


def metadados(nome: str = "mazegen", versao: str = "1.0.0") -> bytes:
    """METADATA ou PKG-INFO coerente com o projeto falso.

    Args:
        nome: Campo Name.
        versao: Campo Version.

    Returns:
        O texto em UTF-8, com o README como corpo.
    """
    return (
        f"Metadata-Version: 2.4\nName: {nome}\nVersion: {versao}\n"
        "License-Expression: MIT\nLicense-File: LICENSE.md\n\n" + README
    ).encode("utf-8")


def gravar_projeto(cwd: Path) -> None:
    """Grava o repositório falso: mazegen/, README, LICENSE e pyproject.

    Args:
        cwd: Pasta do cenário.
    """
    (cwd / "mazegen").mkdir()
    (cwd / "mazegen" / "__init__.py").write_text(INIT, encoding="utf-8")
    (cwd / "mazegen" / "generator.py").write_text(GERADOR, encoding="utf-8")
    (cwd / "README.md").write_text(README, encoding="utf-8")
    (cwd / "LICENSE.md").write_text(LICENCA, encoding="utf-8")
    (cwd / "pyproject.toml").write_text(PYPROJECT, encoding="utf-8")


def fontes(cwd: Path) -> dict[str, bytes]:
    """Arquivos do módulo no repositório falso.

    Args:
        cwd: Pasta do cenário.

    Returns:
        Caminho relativo para os bytes.
    """
    return {
        f"mazegen/{caminho.name}": caminho.read_bytes()
        for caminho in sorted((cwd / "mazegen").glob("*.py"))
    }


def membros_do_wheel(cwd: Path) -> dict[str, bytes]:
    """Arquivos de um wheel como o build produz, sem o RECORD.

    Args:
        cwd: Pasta do cenário.

    Returns:
        Caminho no wheel para os bytes.
    """
    membros = fontes(cwd)
    membros[f"{INFO}/licenses/LICENSE.md"] = LICENCA.encode("utf-8")
    membros[f"{INFO}/METADATA"] = metadados()
    membros[f"{INFO}/WHEEL"] = (
        b"Wheel-Version: 1.0\nGenerator: teste\nRoot-Is-Purelib: true\n"
        b"Tag: py3-none-any\n"
    )
    return membros


def membros_do_sdist(cwd: Path) -> dict[str, bytes]:
    """Arquivos de um sdist como o build produz.

    Args:
        cwd: Pasta do cenário.

    Returns:
        Caminho no sdist para os bytes.
    """
    membros = {TOPO + nome: dado for nome, dado in fontes(cwd).items()}
    for nome in ("README.md", "LICENSE.md", "pyproject.toml"):
        membros[TOPO + nome] = (cwd / nome).read_bytes()
    membros[TOPO + "PKG-INFO"] = metadados()
    membros[TOPO + "setup.cfg"] = b"[egg_info]\ntag_build =\n"
    membros[TOPO + "mazegen.egg-info/PKG-INFO"] = metadados()
    return membros


def gravar_wheel(caminho: Path, membros: dict[str, bytes]) -> None:
    """Grava o wheel com um RECORD que lista todos os arquivos.

    Args:
        caminho: Destino .whl.
        membros: Arquivos do wheel; um RECORD presente não é refeito.
    """
    registro = f"{INFO}/RECORD"
    if registro not in membros:
        linhas = [f"{nome},," for nome in [*membros, registro]]
        membros = {**membros, registro: "\n".join(linhas).encode("utf-8")}
    with zipfile.ZipFile(caminho, "w") as arquivo:
        for nome, dado in membros.items():
            arquivo.writestr(nome, dado)


def gravar_sdist(caminho: Path, membros: dict[str, bytes]) -> None:
    """Grava o sdist como .tar.gz.

    Args:
        caminho: Destino .tar.gz.
        membros: Arquivos do sdist.
    """
    with tarfile.open(caminho, "w:gz") as arquivo:
        for nome, dado in membros.items():
            info = tarfile.TarInfo(nome)
            info.size = len(dado)
            arquivo.addfile(info, io.BytesIO(dado))


def preparar_pacotes(
    cwd: Path,
    no_wheel: Mudanca | None = None,
    no_sdist: Mudanca | None = None,
    sdist: str = SDIST,
) -> None:
    """Grava o projeto falso e os dois pacotes, com uma mudança opcional.

    Args:
        cwd: Pasta do cenário.
        no_wheel: Mudança aplicada aos arquivos do wheel.
        no_sdist: Mudança aplicada aos arquivos do sdist.
        sdist: Nome do arquivo do sdist.
    """
    gravar_projeto(cwd)
    wheel = membros_do_wheel(cwd)
    if no_wheel is not None:
        no_wheel(wheel)
    gravar_wheel(cwd / WHEEL, wheel)
    membros = membros_do_sdist(cwd)
    if no_sdist is not None:
        no_sdist(membros)
    gravar_sdist(cwd / sdist, membros)


def test_abrir_pacote(cenario: Estado) -> None:
    """Wheel e sdist abrem com o arquivo de metadados certo.

    Args:
        cenario: Estado numa pasta temporária.
    """
    preparar_pacotes(cenario.cwd)
    wheel = abrir_pacote(cenario.cwd / WHEEL)
    sdist = abrir_pacote(cenario.cwd / SDIST)
    assert (wheel.wheel, wheel.info, wheel.raiz) == (
        True, f"{INFO}/METADATA", ""
    )
    assert (sdist.wheel, sdist.info, sdist.raiz) == (
        False, f"{TOPO}PKG-INFO", TOPO
    )
    assert wheel.metadados()["Name"] == "mazegen"
    assert wheel.fontes()[f"{INFO}/licenses/LICENSE.md"] == "LICENSE.md"
    assert f"{INFO}/METADATA" not in wheel.fontes()
    assert set(sdist.fontes().values()) == {
        "mazegen/__init__.py",
        "mazegen/generator.py",
        "README.md",
        "LICENSE.md",
        "pyproject.toml",
    }


def test_abrir_pacote_recusa(cenario: Estado) -> None:
    """Outra extensão, arquivo corrompido ou sem metadados são erro.

    Args:
        cenario: Estado numa pasta temporária.
    """
    (cenario.cwd / "mazegen-1.0.0.zip").write_bytes(b"")
    with pytest.raises(ValueError, match="não é .whl nem .tar.gz"):
        abrir_pacote(cenario.cwd / "mazegen-1.0.0.zip")
    (cenario.cwd / WHEEL).write_bytes(b"isto nao e zip")
    with pytest.raises(ValueError, match="não abre"):
        abrir_pacote(cenario.cwd / WHEEL)
    gravar_wheel(cenario.cwd / WHEEL, {"mazegen/__init__.py": b""})
    with pytest.raises(ValueError, match="metadados"):
        abrir_pacote(cenario.cwd / WHEEL)


@pytest.mark.parametrize(
    ("nome", "esperado"),
    [
        (WHEEL, ("mazegen", "1.0.0")),
        ("mazegen-2.1-1-py3-none-any.whl", ("mazegen", "2.1")),
        (SDIST, ("mazegen", "1.0.0")),
        ("mazegen.whl", None),
        ("mazegen-1.0.0.zip", None),
    ],
    ids=["wheel", "wheel-com-build", "sdist", "sem-versao", "zip"],
)
def test_nome_e_versao(nome: str, esperado: tuple[str, str] | None) -> None:
    """Nome e versão saem do nome do wheel e do sdist.

    Args:
        nome: Nome do arquivo.
        esperado: Nome e versão, ou None.
    """
    assert nome_e_versao(nome) == esperado


def test_versao_do_pyproject() -> None:
    """Só a version da tabela [project] conta."""
    assert versao_do_pyproject(PYPROJECT) == "1.0.0"
    assert versao_do_pyproject('[tool.x]\nversion = "9"\n') is None
    assert versao_do_pyproject('[project]\nname = "m"\n') is None


def test_secao_markdown() -> None:
    """A seção vai até o próximo título de nível igual ou mais alto."""
    instrucoes = secao_markdown(README, "Instructions")
    assert instrucoes is not None
    assert "# make install" in instrucoes and "fim" in instrucoes
    assert "https" not in instrucoes
    assert secao_markdown(README, "Resources") == "\nhttps://exemplo\n"
    projeto = secao_markdown(README, "Projeto")
    assert projeto is not None and "https" in projeto
    assert secao_markdown(README, "make install") is None
    assert secao_markdown(README, "Ausente") is None


def test_arquivo_contem(cenario: Estado) -> None:
    """Textos presentes e ausentes, com \\r preservado.

    Args:
        cenario: Estado numa pasta temporária.
    """
    (cenario.cwd / "a.txt").write_bytes(b"linha um\r\nlinha dois\n")
    arquivo_contem(cenario, "a.txt", "contém", ["um\r\n", "dois"])
    arquivo_contem(cenario, "a.txt", "não contém", ["três", "\t"])
    with pytest.raises(pytest.fail.Exception, match="não contém"):
        arquivo_contem(cenario, "a.txt", "contém", ["um", "três"])
    with pytest.raises(pytest.fail.Exception, match=r"contém \['\\r'\]"):
        arquivo_contem(cenario, "a.txt", "não contém", ["\r"])
    with pytest.raises(pytest.fail.Exception, match="não existe"):
        arquivo_contem(cenario, "b.txt", "contém", ["x"])


def test_secao_do_readme(cenario: Estado) -> None:
    """A seção do README contém os textos; seção ausente falha.

    Args:
        cenario: Estado numa pasta temporária.
    """
    gravar_projeto(cenario.cwd)
    secao_do_readme_contem(cenario, "Instructions", ["make install", "fim"])
    with pytest.raises(pytest.fail.Exception, match="não contém"):
        secao_do_readme_contem(cenario, "Instructions", ["https"])
    with pytest.raises(pytest.fail.Exception, match="título"):
        secao_do_readme_contem(cenario, "Description", ["x"])


def test_metadado_do_pacote(cenario: Estado) -> None:
    """Cada pacote do glob tem o campo com o valor; senão o passo falha.

    Args:
        cenario: Estado numa pasta temporária.
    """
    preparar_pacotes(cenario.cwd)
    metadado_do_pacote(cenario, "Name", "mazegen-*", "mazegen")
    metadado_do_pacote(cenario, "Version", "mazegen-*", "1.0.0")
    metadado_do_pacote(cenario, "License-Expression", "mazegen-*", "MIT")
    with pytest.raises(pytest.fail.Exception, match=WHEEL):
        metadado_do_pacote(cenario, "License-Expression", "mazegen-*", "BSD")
    with pytest.raises(pytest.fail.Exception, match="não existe"):
        metadado_do_pacote(cenario, "Author", "mazegen-*", "x")
    with pytest.raises(pytest.fail.Exception, match="nenhum arquivo"):
        metadado_do_pacote(cenario, "Name", "outro-*", "mazegen")


SEM_REDE = [
    propriedade for propriedade in PROPRIEDADES
    if propriedade not in (
        "instala e importa MazeGenerator num virtualenv novo",
        "nada do build ignorado pelo git",
    )
]


@pytest.mark.parametrize("propriedade", SEM_REDE)
def test_propriedade_aceita(cenario: Estado, propriedade: str) -> None:
    """Pacotes coerentes com o repositório passam em cada propriedade.

    Args:
        cenario: Estado numa pasta temporária.
        propriedade: Propriedade de V66.
    """
    preparar_pacotes(cenario.cwd)
    pacote_confirma(cenario, cenario.cwd, "mazegen-*", propriedade)


def tirar(nome: str) -> Mudanca:
    """Mudança que remove um arquivo do pacote.

    Args:
        nome: Caminho dentro do pacote.

    Returns:
        A mudança.
    """
    def mudar(membros: dict[str, bytes]) -> None:
        """Remove o arquivo.

        Args:
            membros: Arquivos do pacote.
        """
        del membros[nome]

    return mudar


def trocar(nome: str, dado: bytes) -> Mudanca:
    """Mudança que troca o conteúdo de um arquivo do pacote.

    Args:
        nome: Caminho dentro do pacote.
        dado: Conteúdo novo.

    Returns:
        A mudança.
    """
    def mudar(membros: dict[str, bytes]) -> None:
        """Troca o conteúdo.

        Args:
            membros: Arquivos do pacote.
        """
        membros[nome] = dado

    return mudar


def mover_topo(membros: dict[str, bytes]) -> None:
    """Põe os arquivos do sdist sob outra pasta de topo.

    Args:
        membros: Arquivos do sdist.
    """
    for nome in list(membros):
        membros["outro-1.0.0/" + nome[len(TOPO):]] = membros.pop(nome)


RECUSAS: list[tuple[str, Mudanca | None, Mudanca | None, str, str]] = [
    (
        "contém o código do módulo",
        tirar("mazegen/generator.py"), None, "falta mazegen/generator.py",
        "sem-modulo",
    ),
    (
        "contém o código do módulo",
        None, trocar(TOPO + "mazegen/generator.py", b"x = 1\n"), "difere",
        "modulo-diferente",
    ),
    (
        "contém o código do módulo",
        trocar("mazegen/velho.py", b""), None, "não existe no repositório",
        "modulo-a-mais",
    ),
    (
        "contém a docstring de mazegen/__init__.py",
        trocar("mazegen/__init__.py", b'"""Outra."""\n'), None,
        "outra docstring", "docstring-diferente",
    ),
    (
        "contém a docstring de mazegen/__init__.py",
        None, tirar(TOPO + "mazegen/__init__.py"), "não existe",
        "sem-init",
    ),
    (
        "README como descrição longa",
        trocar(f"{INFO}/METADATA", metadados()[:-5]), None, "linha",
        "readme-cortado",
    ),
    (
        "formato produzido por python -m build",
        tirar(f"{INFO}/WHEEL"), None, "falta", "sem-wheel",
    ),
    (
        "formato produzido por python -m build",
        trocar(f"{INFO}/RECORD", b"mazegen/__init__.py,,\n"), None,
        "RECORD", "record-incompleto",
    ),
    (
        "formato produzido por python -m build",
        trocar(f"{INFO}/WHEEL", b"Generator: teste\n"), None,
        "sem Wheel-Version", "wheel-sem-versao",
    ),
    (
        "formato produzido por python -m build",
        None, mover_topo, "pasta de topo", "sdist-outro-topo",
    ),
    (
        "formato produzido por python -m build",
        trocar(f"{INFO}/METADATA", metadados(nome="outro")), None,
        "Name é outro", "nome-diferente",
    ),
    (
        "versão igual à do pyproject.toml",
        trocar(f"{INFO}/METADATA", metadados(versao="2.0")), None,
        r"Version é \['2.0'\]", "versao-dos-metadados",
    ),
    (
        "LICENSE.md incluído",
        tirar(f"{INFO}/licenses/LICENSE.md"), None, "não leva",
        "sem-licenca",
    ),
    (
        "LICENSE.md incluído",
        None, trocar(TOPO + "LICENSE.md", b"BSD\n"), "difere",
        "licenca-diferente",
    ),
    (
        "LICENSE.md incluído",
        trocar(f"{INFO}/METADATA", metadados().replace(
            b"License-File: LICENSE.md\n", b""
        )), None, "License-File", "sem-license-file",
    ),
]


@pytest.mark.parametrize(
    ("propriedade", "no_wheel", "no_sdist", "motivo"),
    [caso[:4] for caso in RECUSAS],
    ids=[caso[4] for caso in RECUSAS],
)
def test_propriedade_recusa(
    cenario: Estado,
    propriedade: str,
    no_wheel: Mudanca | None,
    no_sdist: Mudanca | None,
    motivo: str,
) -> None:
    """Um pacote que diverge do repositório ou do build falha.

    Args:
        cenario: Estado numa pasta temporária.
        propriedade: Propriedade de V66.
        no_wheel: Mudança no wheel.
        no_sdist: Mudança no sdist.
        motivo: Trecho esperado na mensagem.
    """
    preparar_pacotes(cenario.cwd, no_wheel, no_sdist)
    with pytest.raises(pytest.fail.Exception, match=motivo):
        pacote_confirma(cenario, cenario.cwd, "mazegen-*", propriedade)


def test_versao_nos_nomes(cenario: Estado) -> None:
    """Versões diferentes no nome dos arquivos falham.

    Args:
        cenario: Estado numa pasta temporária.
    """
    preparar_pacotes(cenario.cwd, sdist="mazegen-1.0.1.tar.gz")
    with pytest.raises(pytest.fail.Exception, match="versões diferentes"):
        pacote_confirma(
            cenario, cenario.cwd, "mazegen-*",
            "mesma versão no nome dos arquivos",
        )
    with pytest.raises(pytest.fail.Exception, match="o nome declara 1.0.1"):
        pacote_confirma(
            cenario, cenario.cwd, "mazegen-*",
            "versão igual à do pyproject.toml",
        )


def test_versao_sem_pyproject(cenario: Estado) -> None:
    """Sem version em [project] a propriedade falha citando o arquivo.

    Args:
        cenario: Estado numa pasta temporária.
    """
    preparar_pacotes(cenario.cwd)
    (cenario.cwd / "pyproject.toml").write_text(
        '[project]\nname = "mazegen"\n', encoding="utf-8"
    )
    with pytest.raises(pytest.fail.Exception, match="não declara version"):
        pacote_confirma(
            cenario, cenario.cwd, "mazegen-*",
            "versão igual à do pyproject.toml",
        )


def test_propriedade_desconhecida(cenario: Estado) -> None:
    """Propriedade fora da lista é recusada com a lista das válidas.

    Args:
        cenario: Estado numa pasta temporária.
    """
    with pytest.raises(pytest.fail.Exception, match="as válidas são"):
        pacote_confirma(cenario, cenario.cwd, "mazegen-*", "pesa pouco")


def versionar(cwd: Path, ignorar: str, adicionados: list[str]) -> None:
    """Cria um repositório git com o .gitignore e os arquivos dados.

    Args:
        cwd: Pasta do cenário.
        ignorar: Conteúdo do .gitignore.
        adicionados: Caminhos passados ao git add.
    """
    (cwd / ".gitignore").write_text(ignorar, encoding="utf-8")
    git_ou_falha(["init", "-q"], cwd)
    git_ou_falha(["add", ".gitignore", *adicionados], cwd)
    git_ou_falha(["commit", "-q", "-m", "teste"], cwd)


TUDO = ["mazegen", "README.md", "LICENSE.md", "pyproject.toml", WHEEL, SDIST]


@pytest.mark.parametrize(
    ("ignorar", "adicionados", "motivo"),
    [
        ("*.whl\n", [nome for nome in TUDO if nome != WHEEL],
         f"{WHEEL} é ignorado"),
        ("", [nome for nome in TUDO if nome != "LICENSE.md"],
         "LICENSE.md não está versionado"),
    ],
    ids=["pacote-ignorado", "licenca-fora-do-git"],
)
def test_nada_ignorado(
    cenario: Estado, ignorar: str, adicionados: list[str], motivo: str
) -> None:
    """Tudo versionado passa; ignorado ou fora do git falha.

    Args:
        cenario: Estado numa pasta temporária.
        ignorar: Conteúdo do .gitignore do caso ruim.
        adicionados: Caminhos versionados no caso ruim.
        motivo: Trecho esperado na mensagem.
    """
    propriedade = "nada do build ignorado pelo git"
    preparar_pacotes(cenario.cwd)
    versionar(cenario.cwd, "", TUDO)
    pacote_confirma(cenario, cenario.cwd, "mazegen-*", propriedade)
    ruim = cenario.cwd / "ruim"
    ruim.mkdir()
    cenario.cwd = ruim
    preparar_pacotes(ruim)
    versionar(ruim, ignorar, adicionados)
    with pytest.raises(pytest.fail.Exception, match=motivo):
        pacote_confirma(cenario, ruim, "mazegen-*", propriedade)


def test_instala_e_importa(cenario: Estado, tmp_path: Path) -> None:
    """O wheel com MazeGenerator instala e importa; sem a classe, falha.

    Args:
        cenario: Estado numa pasta temporária.
        tmp_path: Pasta temporária para os virtualenvs.
    """
    propriedade = "instala e importa MazeGenerator num virtualenv novo"
    preparar_pacotes(cenario.cwd)
    pacote_confirma(cenario, tmp_path / "bom", WHEEL, propriedade)
    ruim = cenario.cwd / "ruim"
    ruim.mkdir()
    preparar_pacotes(
        ruim, trocar("mazegen/__init__.py", b'"""Sem a classe."""\n')
    )
    cenario.cwd = ruim
    with pytest.raises(pytest.fail.Exception, match="ImportError"):
        pacote_confirma(cenario, tmp_path / "ruim-venv", WHEEL, propriedade)


def test_virtualenv_novo(cenario: Estado, tmp_path: Path) -> None:
    """Os comandos rodam no virtualenv, na pasta do cenário.

    Args:
        cenario: Estado numa pasta temporária.
        tmp_path: Pasta temporária do cenário.
    """
    virtualenv_novo(
        cenario, tmp_path, "v",
        ["python -c 'import sys; print(sys.prefix)' > prefixo.txt"],
    )
    venv = cenario.venvs["v"]
    prefixo = (cenario.cwd / "prefixo.txt").read_text(encoding="utf-8")
    assert Path(prefixo.strip()).resolve() == venv.resolve()
    assert not cenario.resultados
    with pytest.raises(pytest.fail.Exception, match="já foi criado"):
        virtualenv_novo(cenario, tmp_path, "v", ["true"])


def test_virtualenv_com_comando_que_falha(
    cenario: Estado, tmp_path: Path
) -> None:
    """Comando com código diferente de 0 derruba o passo.

    Args:
        cenario: Estado numa pasta temporária.
        tmp_path: Pasta temporária do cenário.
    """
    with pytest.raises(pytest.fail.Exception, match="código 3"):
        virtualenv_novo(cenario, tmp_path, "v", ["true", "exit 3"])
    assert "v" not in cenario.venvs


def test_ambiente_do_virtualenv(cenario: Estado, tmp_path: Path) -> None:
    """Os próximos comandos usam o PATH do virtualenv e a pasta pedida.

    Args:
        cenario: Estado numa pasta temporária.
        tmp_path: Pasta temporária do cenário.
    """
    virtualenv_novo(cenario, tmp_path, "v", ["mkdir sub"])
    with pytest.raises(pytest.fail.Exception, match="os criados são: v"):
        ambiente_do_virtualenv(cenario, "outro", ".")
    with pytest.raises(pytest.fail.Exception, match="não existe"):
        ambiente_do_virtualenv(cenario, "v", "nada")
    raiz = cenario.cwd
    ambiente_do_virtualenv(cenario, "v", "sub")
    assert cenario.cwd == raiz / "sub"
    execucao = cenario.executar("python -c 'import sys; print(sys.prefix)'")
    assert Path(execucao.saida_padrao.strip()).resolve() == (
        cenario.venvs["v"].resolve()
    )
    with pytest.raises(pytest.fail.Exception, match="já é um virtualenv"):
        ambiente_do_virtualenv(cenario, "v", ".")
