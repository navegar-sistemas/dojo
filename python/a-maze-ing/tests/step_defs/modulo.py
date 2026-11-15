"""Passos que usam a classe MazeGenerator do módulo mazegen."""

import ast
import importlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

import pytest
from pytest_bdd import given, parsers, then, when

from suporte.config import chaves_das_linhas
from suporte.estado import TIMEOUT, Estado, Execucao
from suporte.labirinto import FECHADA, Labirinto
from suporte.modulo import (
    CLASSE,
    INVALIDOS,
    MODULO,
    argumentos,
    avaliar,
    classe_de_erro,
    classe_geradora,
    dimensoes,
    exemplo_da_docstring,
    extremos,
    labirinto_do_gerador,
    parametros_do_config,
)
from suporte.tipos import TIPOS

EXCECOES = ("MazeError",)
EXCECAO = "MazeError"
SOLUCAO = re.compile(r"[NESW]+")

# Roda no python3 do cenário, que pode ser o de um virtualenv com o pacote
# instalado: o import em processo veria o mazegen de ../project.
EXPORTADOS = """
import inspect, json, mazegen
nomes = getattr(mazegen, "__all__", None)
classes = {}
for nome in nomes or []:
    valor = getattr(mazegen, nome, None)
    if inspect.isclass(valor):
        classes[nome] = {
            "excecao": issubclass(valor, BaseException),
            "gera": callable(getattr(valor, "generate", None)),
        }
print(json.dumps({"all": None if nomes is None else list(nomes),
                  "classes": classes}))
"""


def conferir_expressao(expressao: str) -> dict[str, object]:
    """Argumentos da expressão, ou falha dizendo o que se aceita.

    Args:
        expressao: Texto do passo.

    Returns:
        Nome do parâmetro para valor.
    """
    try:
        return argumentos(expressao)
    except ValueError as erro:
        pytest.fail(
            f'"{expressao}": {erro}; a expressão é só {CLASSE}(...) com '
            "literais, na assinatura da I09"
        )


def valores_do_gerador(estado: Estado) -> dict[str, object]:
    """Argumentos com que o gerador do cenário foi criado.

    Args:
        estado: Estado do cenário.

    Returns:
        Os da expressão (V26, V44) ou, sem ela, os do config atual.
    """
    if estado.expressao is not None:
        return conferir_expressao(estado.expressao)
    if estado.config is None:
        pytest.fail("o gerador do cenário não veio de expressão nem de config")
    try:
        return parametros_do_config(chaves_das_linhas(estado.config.linhas))
    except (KeyError, ValueError) as erro:
        pytest.fail(f"o config não serve à classe geradora: {erro!r}")


def gerador_do_cenario(estado: Estado) -> Any:
    """O gerador criado por um passo anterior.

    Args:
        estado: Estado do cenário.

    Returns:
        A instância de MazeGenerator.
    """
    if estado.gerador is None:
        pytest.fail(f"nenhum {CLASSE} foi criado antes deste passo")
    return estado.gerador


def nova_instancia(estado: Estado) -> Any:
    """Cria de novo o gerador, com os mesmos argumentos.

    Args:
        estado: Estado do cenário.

    Returns:
        A instância nova, sem ``generate()``.
    """
    if estado.expressao is not None:
        return construir(estado.expressao)
    return classe_geradora()(**valores_do_gerador(estado))


def construir(expressao: str) -> Any:
    """Avalia a expressão e falha se o construtor levantar exceção.

    Args:
        expressao: Chamada a MazeGenerator com literais.

    Returns:
        A instância criada.
    """
    conferir_expressao(expressao)
    try:
        return avaliar(expressao)
    except Exception as erro:
        pytest.fail(f"{expressao} levantou {type(erro).__name__}: {erro}")


def gerar(gerador: Any, valores: dict[str, object]) -> Labirinto:
    """Chama ``generate()`` e monta o labirinto da classe.

    Args:
        gerador: Instância de MazeGenerator.
        valores: Argumentos do construtor, para a entrada e a saída.

    Returns:
        O labirinto com ``grid``, ``solution`` e ``pattern``.
    """
    try:
        gerador.generate()
    except Exception as erro:
        pytest.fail(f"generate() levantou {type(erro).__name__}: {erro}")
    try:
        entrada, saida = extremos(valores)
    except ValueError as erro:
        pytest.fail(str(erro))
    return labirinto_do_gerador(gerador, entrada, saida)


@given(parsers.parse('o gerador "{expressao:Q}"', extra_types=TIPOS))
def o_gerador(estado: Estado, expressao: str) -> None:
    """Cria o gerador avaliando a expressão e guarda o texto.

    Args:
        estado: Estado do cenário.
        expressao: Chamada a MazeGenerator com literais.
    """
    estado.gerador = construir(expressao)
    estado.expressao = expressao


@when("o gerador gera o labirinto")
def gerador_gera(estado: Estado) -> None:
    """Chama ``generate()`` e guarda o labirinto lido de grid e solution.

    Args:
        estado: Estado do cenário.
    """
    gerador = gerador_do_cenario(estado)
    estado.labirintos.append(gerar(gerador, valores_do_gerador(estado)))


@when(
    parsers.parse("eu gero o labirinto com {n:d} instâncias novas do gerador")
)
def gero_com_instancias(estado: Estado, n: int) -> None:
    """Avalia a expressão n vezes, gera com cada instância e troca a lista.

    Args:
        estado: Estado do cenário.
        n: Número de instâncias.
    """
    if estado.expressao is None:
        pytest.fail("este passo precisa de um 'o gerador \"...\"' antes")
    valores = conferir_expressao(estado.expressao)
    execucoes: list[Execucao] = []
    for _ in range(n):
        labirinto = gerar(construir(estado.expressao), valores)
        execucoes.append(
            Execucao(estado.expressao, 0, "", "", labirinto=labirinto)
        )
        estado.labirintos.append(labirinto)
    estado.execucoes = execucoes


@when(parsers.parse('eu tento criar o gerador "{expressao:Q}"',
                    extra_types=TIPOS))
def tento_criar(estado: Estado, expressao: str) -> None:
    """Avalia a expressão e guarda a exceção do construtor, se houver.

    Args:
        estado: Estado do cenário.
        expressao: Chamada a MazeGenerator com literais.
    """
    conferir_expressao(expressao)
    estado.expressao = expressao
    estado.gerador = None
    estado.excecao = None
    try:
        estado.gerador = avaliar(expressao)
    except Exception as erro:
        estado.excecao = erro


def excecao_do_cenario(estado: Estado) -> Exception:
    """A exceção que o construtor levantou em V44.

    Args:
        estado: Estado do cenário.

    Returns:
        A exceção guardada.
    """
    if estado.excecao is None:
        pytest.fail(f"o construtor de {estado.expressao} não levantou exceção")
    return estado.excecao


@then(parsers.parse('o construtor levanta "{excecao:Q}"', extra_types=TIPOS))
def construtor_levanta(estado: Estado, excecao: str) -> None:
    """Confere o tipo da exceção guardada.

    Args:
        estado: Estado do cenário.
        excecao: Nome da exceção pública do módulo.
    """
    if excecao not in EXCECOES:
        pytest.fail(
            f'exceção "{excecao}" não existe; as válidas são: '
            f"{', '.join(EXCECOES)}"
        )
    levantada = excecao_do_cenario(estado)
    if not isinstance(levantada, classe_de_erro()):
        pytest.fail(
            f"{estado.expressao} levantou {type(levantada).__name__}: "
            f"{levantada}, não {excecao}"
        )


@then(parsers.parse("a mensagem da exceção cita {trechos:L}",
                    extra_types=TIPOS))
def mensagem_cita(estado: Estado, trechos: list[str]) -> None:
    """Confere que ``str(excecao)`` contém cada trecho.

    Args:
        estado: Estado do cenário.
        trechos: Textos que a mensagem precisa conter.
    """
    mensagem = str(excecao_do_cenario(estado))
    faltando = [trecho for trecho in trechos if trecho not in mensagem]
    if faltando:
        pytest.fail(f"a mensagem {mensagem!r} não cita {faltando}")


def problemas_da_grade(grade: object, largura: int, altura: int) -> list[str]:
    """Diferenças entre ``grid`` e o formato da I09.

    Args:
        grade: Valor do atributo ``grid``.
        largura: ``width`` do construtor.
        altura: ``height`` do construtor.

    Returns:
        Uma linha por problema; vazia quando ``grid`` tem ``altura``
        listas de ``largura`` inteiros de 0 a 15.
    """
    if not isinstance(grade, list):
        return [f"grid é {type(grade).__name__}, não list"]
    if len(grade) != altura:
        return [f"grid tem {len(grade)} linhas, não {altura}"]
    problemas: list[str] = []
    for y, linha in enumerate(grade):
        if not isinstance(linha, list) or len(linha) != largura:
            problemas.append(f"grid[{y}] não é uma lista de {largura} itens")
            continue
        problemas += [
            f"grid[{y}][{x}] = {valor!r} não é um inteiro de 0 a {FECHADA}"
            for x, valor in enumerate(linha)
            if type(valor) is not int or not 0 <= valor <= FECHADA
        ]
    return problemas


def conferir_grade_publica(estado: Estado) -> list[str]:
    """Problemas do ``grid`` público do gerador do cenário.

    Args:
        estado: Estado do cenário.

    Returns:
        Uma linha por problema.
    """
    gerador = gerador_do_cenario(estado)
    if not hasattr(gerador, "grid"):
        return [f"{CLASSE} não tem o atributo grid"]
    try:
        largura, altura = dimensoes(valores_do_gerador(estado))
    except ValueError as erro:
        pytest.fail(str(erro))
    return problemas_da_grade(gerador.grid, largura, altura)


def problemas_da_solucao(gerador: Any) -> list[str]:
    """Diferenças entre ``solution`` e o formato da I09.

    Args:
        gerador: Instância já gerada.

    Returns:
        Vazia quando ``solution`` é um texto não vazio de N, E, S e W.
    """
    if not hasattr(gerador, "solution"):
        return [f"{CLASSE} não tem o atributo solution"]
    solucao = gerador.solution
    if not isinstance(solucao, str) or not SOLUCAO.fullmatch(solucao):
        return [f"solution = {solucao!r} não é um texto de N, E, S e W"]
    return []


def falhar_se_houver(problemas: list[str], regra: str) -> None:
    """Falha o teste listando os problemas encontrados.

    Args:
        problemas: Uma linha por problema.
        regra: O que se esperava, para o título da mensagem.
    """
    if problemas:
        lista = "\n".join(f"  {item}" for item in problemas)
        pytest.fail(f"{regra}:\n{lista}")


def diferenca_de_grades(esperada: list[list[int]], achada: object) -> str:
    """Descreve a primeira diferença entre duas grades.

    Args:
        esperada: Grade de referência.
        achada: Grade conferida.

    Returns:
        Vazio quando são iguais; senão a primeira célula diferente.
    """
    if achada == esperada:
        return ""
    if not isinstance(achada, list) or len(achada) != len(esperada):
        return f"formatos diferentes: {achada!r}"
    for y, (linha, outra) in enumerate(zip(esperada, achada)):
        if linha != outra:
            for x, valor in enumerate(linha):
                if not isinstance(outra, list) or x >= len(outra):
                    return f"linha {y} diferente: {outra!r}"
                if outra[x] != valor:
                    return f"célula ({x}, {y}): {valor} e {outra[x]}"
            return f"linha {y} diferente: {outra!r}"
    return "grades diferentes"


@then('o módulo mazegen confirma "uma única classe pública de geração"')
def uma_unica_classe(estado: Estado) -> None:
    """``__all__`` exporta só MazeGenerator e MazeError (D19, I11).

    Roda no python3 e na pasta do cenário, para conferir o mazegen que o
    ambiente importa (o do virtualenv, quando V05 trocou o ambiente).

    Args:
        estado: Estado do cenário.
    """
    processo = subprocess.run(
        ["python3", "-c", EXPORTADOS],
        cwd=estado.cwd,
        env=estado.ambiente(),
        capture_output=True,
        text=True,
        timeout=TIMEOUT,
    )
    if processo.returncode != 0:
        pytest.fail(
            f"import {MODULO} em {estado.cwd} terminou com código "
            f"{processo.returncode}\n{processo.stderr}"
        )
    dados = json.loads(processo.stdout)
    exportados = dados["all"]
    if exportados is None:
        pytest.fail(f"{MODULO} não define __all__")
    problemas: list[str] = []
    if sorted(exportados) != sorted([CLASSE, EXCECAO]):
        problemas.append(f"__all__ é {exportados}")
    classes: dict[str, dict[str, bool]] = dados["classes"]
    geradoras = [
        nome for nome, classe in classes.items()
        if classe["gera"] and not classe["excecao"]
    ]
    if geradoras != [CLASSE]:
        problemas.append(f"classes exportadas com generate(): {geradoras}")
    if not classes.get(EXCECAO, {}).get("excecao"):
        problemas.append(f"{EXCECAO} não é uma classe de exceção exportada")
    falhar_se_houver(
        problemas,
        f"{MODULO} deveria exportar só {CLASSE} e a exceção {EXCECAO}",
    )


@then('o módulo mazegen confirma "grid e solution preenchidos após generate"')
def grid_e_solution_preenchidos(estado: Estado) -> None:
    """Depois de ``generate()``, grid e solution seguem a I09.

    Args:
        estado: Estado do cenário.
    """
    problemas = conferir_grade_publica(estado)
    problemas += problemas_da_solucao(gerador_do_cenario(estado))
    falhar_se_houver(problemas, "grid e solution deveriam estar preenchidos")


@then('o módulo mazegen confirma "solution pública e documentada"')
def solution_documentada(estado: Estado) -> None:
    """``solution`` é um atributo público e a documentação do módulo o cita.

    Args:
        estado: Estado do cenário.
    """
    problemas = problemas_da_solucao(gerador_do_cenario(estado))
    documentacao = importlib.import_module(MODULO).__doc__ or ""
    if not re.search(r"\bsolution\b", documentacao):
        problemas.append(f"a docstring de {MODULO} não cita solution")
    falhar_se_houver(problemas, "solution deveria ser pública e documentada")


@then('o módulo mazegen confirma "grid público com as paredes de cada célula"')
def grid_publico(estado: Estado) -> None:
    """``grid`` tem um inteiro de paredes por célula (I09).

    Args:
        estado: Estado do cenário.
    """
    falhar_se_houver(
        conferir_grade_publica(estado),
        "grid deveria ter as paredes de cada célula",
    )


@then('o módulo mazegen confirma "mesmos parâmetros geram a mesma grade"')
def mesmos_parametros(estado: Estado) -> None:
    """Uma instância nova, com os mesmos argumentos, gera a mesma grade.

    Args:
        estado: Estado do cenário.
    """
    atual = gerador_do_cenario(estado).grid
    if not atual:
        pytest.fail("o gerador do cenário ainda não gerou o labirinto")
    nova = nova_instancia(estado)
    gerar(nova, valores_do_gerador(estado))
    diferenca = diferenca_de_grades(atual, nova.grid)
    if diferenca:
        pytest.fail(f"uma instância nova gerou outra grade: {diferenca}")


@then('o módulo mazegen confirma "grade igual à do arquivo de saída"')
def grade_igual_ao_arquivo(estado: Estado) -> None:
    """O ``grid`` do gerador é a grade do OUTPUT_FILE da última execução.

    Args:
        estado: Estado do cenário.
    """
    grade = gerador_do_cenario(estado).grid
    execucao = estado.resultado
    if execucao.labirinto is None:
        pytest.fail(f"'{execucao.comando}' não gravou um labirinto legível")
    diferenca = diferenca_de_grades(execucao.labirinto.grade, grade)
    if diferenca:
        pytest.fail(
            f"o grid difere do arquivo de {execucao.comando!r}: {diferenca}"
        )


def chamada(caso: dict[str, object]) -> str:
    """Texto da chamada ao construtor com os argumentos do caso.

    Args:
        caso: Argumentos por nome.

    Returns:
        ``MazeGenerator(width=20, ...)``.
    """
    pares = ", ".join(f"{nome}={valor!r}" for nome, valor in caso.items())
    return f"{CLASSE}({pares})"


@then('o módulo mazegen confirma "só MazeError escapa do construtor"')
def so_maze_error(estado: Estado) -> None:
    """Valores e tipos inválidos levantam MazeError, e nada além dela.

    Confere a expressão do cenário, se houver, e os casos de INVALIDOS.

    Args:
        estado: Estado do cenário.
    """
    classe = classe_geradora()
    erro = classe_de_erro()
    casos = [(chamada(caso), caso) for caso in INVALIDOS]
    if estado.expressao is not None:
        casos.insert(
            0, (estado.expressao, conferir_expressao(estado.expressao))
        )
    problemas: list[str] = []
    for texto, caso in casos:
        try:
            classe(**caso)
        except erro:
            continue
        except Exception as outra:
            problemas.append(
                f"{texto} levantou {type(outra).__name__}: {outra}"
            )
            continue
        problemas.append(f"{texto} não levantou exceção")
    falhar_se_houver(
        problemas, f"o construtor deveria levantar só {EXCECAO}"
    )


def arquivo_do_modulo(estado: Estado, modulo: str) -> Path:
    """Arquivo-fonte de um módulo do repositório.

    Args:
        estado: Estado do cenário.
        modulo: Nome do módulo, com pontos.

    Returns:
        ``<pasta>/__init__.py`` para pacote ou ``<nome>.py``.
    """
    base = estado.cwd.joinpath(*modulo.split("."))
    fonte = base / "__init__.py" if base.is_dir() else base.with_suffix(".py")
    if not fonte.is_file():
        pytest.fail(f'o módulo "{modulo}" não existe em {estado.cwd}')
    return fonte


@given(
    parsers.parse(
        'o exemplo de uso da docstring de "{modulo:Q}" salvo em "{arquivo:Q}"',
        extra_types=TIPOS,
    )
)
def exemplo_salvo(estado: Estado, modulo: str, arquivo: str) -> None:
    """Grava o código da seção Example: da docstring do módulo (I22).

    O arquivo e as pastas pai criadas somem no fim do cenário.

    Args:
        estado: Estado do cenário.
        modulo: Nome do módulo, como "mazegen".
        arquivo: Destino relativo à raiz do repositório.
    """
    fonte = arquivo_do_modulo(estado, modulo)
    docstring = ast.get_docstring(
        ast.parse(fonte.read_text(encoding="utf-8"))
    )
    if not docstring:
        pytest.fail(f"{fonte} não tem docstring de módulo")
    try:
        codigo = exemplo_da_docstring(docstring)
    except ValueError as erro:
        pytest.fail(f"{fonte}: {erro}")
    destino = estado.cwd / arquivo
    estado.criar_pastas(destino.parent)
    estado.proteger(destino)
    destino.write_text(codigo, encoding="utf-8")
