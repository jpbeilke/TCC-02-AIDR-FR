from app.models.report_models import RelatorioTurnos, ResultadoTurno


def montar_relatorio_turnos(
    resumo_turnos,
    ranking,
    data_inicio: str,
    data_fim: str,
    id_application_client: str,
    melhor_turno: str | None,
    pior_turno: str | None,
) -> RelatorioTurnos:
    """
    Constrói um objeto estruturado de relatório a partir do resumo e do ranking.
    """
    mapa_pontuacao = {}

    if not ranking.empty:
        for _, linha in ranking.iterrows():
            mapa_pontuacao[linha["nome_turno"]] = float(linha["pontuacao_total"])

    resultados = []

    for _, linha in resumo_turnos.iterrows():
        resultados.append(
            ResultadoTurno(
                id_turno_estatico=int(linha["id_turno_estatico"]),
                nome_turno=str(linha["nome_turno"]),
                total_registros=int(linha["total_registros"]),
                quantidade_total_produzida=float(linha["quantidade_total_produzida"]),
                qtd_batelada_total=float(linha["qtd_batelada_total"]),
                oee_medio=float(linha["oee_medio"]),
                produtividade_media=float(linha["produtividade_media"]),
                qualidade_media=float(linha["qualidade_media"]),
                taxa_producao_media=float(linha["taxa_producao_media"]),
                tempo_rodando_medio_seg=float(linha["tempo_rodando_medio_seg"]),
                pontuacao_total=mapa_pontuacao.get(str(linha["nome_turno"])),
            )
        )

    return RelatorioTurnos(
        data_inicio=data_inicio,
        data_fim=data_fim,
        id_application_client=id_application_client,
        melhor_turno=melhor_turno,
        pior_turno=pior_turno,
        resultados_por_turno=resultados,
    )