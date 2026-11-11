"""Passos que preparam o repositório de entrega (project/)."""

from dataclasses import dataclass

import pytest
from pytest_bdd import given, parsers

from conftest import PROJECT_DIR, TIPOS, Estado, Execucao


@dataclass
class Instalacao:
    """Resultado do ``make install``, feito uma vez por sessão de testes."""

    execucao: Execucao | None = None

    def garantir(self) -> Execucao:
        """Roda ``make install`` na primeira chamada e reaproveita depois.

        Returns:
            A execução do ``make install``.
        """
        if self.execucao is None:
            self.execucao = Estado().executar("make install")
        return self.execucao


@pytest.fixture(scope="session")
def instalacao() -> Instalacao:
    """Instalação compartilhada por todos os cenários da sessão."""
    return Instalacao()


@given(parsers.parse('o repositório no estado "{nome:Q}"', extra_types=TIPOS))
def repositorio_no_estado(
    estado: Estado, instalacao: Instalacao, nome: str
) -> None:
    """V02: prepara o repositório no estado pedido.

    Args:
        estado: Estado do cenário.
        instalacao: Instalação da sessão.
        nome: "atual" ou "instalado"; os demais estados ainda não existem.
    """
    estado.cwd = PROJECT_DIR
    if nome == "atual":
        return
    if nome == "instalado":
        execucao = instalacao.garantir()
        if execucao.codigo != 0:
            pytest.fail(
                f"'{execucao.comando}' terminou com código {execucao.codigo}"
                f"\n{execucao.saida_padrao}{execucao.saida_erro}"
            )
        estado.caminhos_extras = [PROJECT_DIR / ".venv" / "bin"]
        return
    pytest.fail(f'estado "{nome}" ainda não implementado (V02 no README)')
