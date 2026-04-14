from app.db.connection import testar_conexao
from app.db.repository import buscar_eventos_producao
from app.services.data_service import (
    gerar_resumo_por_turno,
    preparar_dados_evento_producao,
)
from app.services.ranking_service import identificar_melhor_e_pior_turno


def executar_aplicacao(
    data_inicio: str,
    data_fim: str,
    limite: int | None = None,
) -> dict:
    """
    Executa o fluxo principal da primeira versão do projeto.
    """
    conexao_valida = testar_conexao()

    if not conexao_valida:
        raise ConnectionError("Não foi possível validar a conexão com o SQL Server.")

    dados_brutos = buscar_eventos_producao(
        data_inicio=data_inicio,
        data_fim=data_fim,
        limite=limite,
    )

    dados_preparados = preparar_dados_evento_producao(dados_brutos)
    resumo_turnos = gerar_resumo_por_turno(dados_preparados)
    resultado_ranking = identificar_melhor_e_pior_turno(resumo_turnos)

    return {
        "dados_brutos": dados_brutos,
        "dados_preparados": dados_preparados,
        "resumo_turnos": resumo_turnos,
        "ranking": resultado_ranking["ranking"],
        "melhor_turno": resultado_ranking["melhor_turno"],
        "pior_turno": resultado_ranking["pior_turno"],
    }