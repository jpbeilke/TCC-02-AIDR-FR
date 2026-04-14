from typing import Iterable


def montar_consulta_evento_producao(
    ids_turno: Iterable[int],
    limite: int | None = None,
) -> str:
    """
    Monta a consulta principal da tabela evento_producao.
    """
    ids_turno = list(ids_turno)

    if not ids_turno:
        raise ValueError("É necessário informar ao menos um id de turno.")

    clausula_top = f"TOP {int(limite)} " if limite else ""
    marcadores_turno = ", ".join("?" for _ in ids_turno)

    consulta = f"""
        SELECT {clausula_top}
            ep.id_evento_producao,
            ep.data_evento,
            ep.quantidade_produzida,
            ep.id_evento_turno,
            ep.oee,
            ep.produtividade,
            ep.qualidade,
            ep.taxa_producao,
            ep.tempo_rodando_segundo,
            ep.qtd_batelada,
            et.id_evento_turno_atual,
            et.id_application_client,
            et.id_turno AS id_turno_estatico,
            et.data_inicio,
            et.data_fim
        FROM paas.evento_producao ep
        INNER JOIN paas.evento_turnos et
            ON ep.id_evento_turno = et.id_evento_turno_atual
        WHERE et.id_turno IN ({marcadores_turno})
          AND et.id_application_client = ?
          AND ep.data_evento >= ?
          AND ep.data_evento <= ?
        ORDER BY ep.data_evento
    """

    return consulta