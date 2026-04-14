from pathlib import Path

import pandas as pd

from app.utils.json_loader import carregar_json


CAMINHO_TURNOS = Path("config/turnos.json")


def preparar_dados_evento_producao(dados_brutos: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza tipos, mapeia nomes dos turnos e prepara os dados para análise.
    """
    if dados_brutos.empty:
        return dados_brutos.copy()

    dados = dados_brutos.copy()

    dados["data_evento"] = pd.to_datetime(dados["data_evento"], errors="coerce")

    colunas_numericas = [
        "quantidade_produzida",
        "oee",
        "produtividade",
        "qualidade",
        "taxa_producao",
        "tempo_rodando_segundo",
        "qtd_batelada",
    ]

    for coluna in colunas_numericas:
        if coluna in dados.columns:
            dados[coluna] = pd.to_numeric(dados[coluna], errors="coerce")

    mapeamento_turnos = {
        int(chave): valor
        for chave, valor in carregar_json(CAMINHO_TURNOS).items()
    }

    dados["nome_turno"] = (
        dados["id_evento_turno"]
        .map(mapeamento_turnos)
        .fillna(dados["id_evento_turno"].astype(str))
    )

    return dados


def gerar_resumo_por_turno(dados: pd.DataFrame) -> pd.DataFrame:
    """
    Consolida os indicadores por turno.
    """
    if dados.empty:
        return pd.DataFrame()

    resumo = (
        dados.groupby(["id_evento_turno", "nome_turno"], dropna=False)
        .agg(
            total_registros=("id_evento_producao", "count"),
            quantidade_total_produzida=("quantidade_produzida", "sum"),
            qtd_batelada_total=("qtd_batelada", "sum"),
            oee_medio=("oee", "mean"),
            produtividade_media=("produtividade", "mean"),
            qualidade_media=("qualidade", "mean"),
            taxa_producao_media=("taxa_producao", "mean"),
            tempo_rodando_medio_seg=("tempo_rodando_segundo", "mean"),
        )
        .reset_index()
        .sort_values("id_evento_turno")
        .reset_index(drop=True)
    )

    colunas_para_arredondar = [
        "quantidade_total_produzida",
        "qtd_batelada_total",
        "oee_medio",
        "produtividade_media",
        "qualidade_media",
        "taxa_producao_media",
        "tempo_rodando_medio_seg",
    ]

    for coluna in colunas_para_arredondar:
        if coluna in resumo.columns:
            resumo[coluna] = resumo[coluna].round(2)

    return resumo