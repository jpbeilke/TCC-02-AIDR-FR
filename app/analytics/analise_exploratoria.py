from pathlib import Path

import pandas as pd

from app.db.repositories import buscar_eventos_producao
from app.services.data_service import preparar_dados_evento_producao


DIRETORIO_SAIDA_ANALYTICS = Path("output/analytics")


COLUNAS_ANALITICAS = [
    "quantidade_produzida",
    "oee",
    "produtividade",
    "qualidade",
    "taxa_producao",
    "tempo_rodando_segundo",
    "qtd_batelada",
]


def _garantir_diretorio_saida() -> Path:
    DIRETORIO_SAIDA_ANALYTICS.mkdir(parents=True, exist_ok=True)
    return DIRETORIO_SAIDA_ANALYTICS


def _formatar_titulo(texto: str) -> None:
    print(f"\n{'=' * 20} {texto} {'=' * 20}")


def _calcular_outliers_iqr(dados: pd.DataFrame, coluna: str) -> dict:
    """
    Calcula quantidade de outliers usando a regra do IQR.
    """
    serie = pd.to_numeric(dados[coluna], errors="coerce").dropna()

    if serie.empty:
        return {
            "coluna": coluna,
            "qtd_outliers": 0,
            "percentual_outliers": 0.0,
            "limite_inferior": None,
            "limite_superior": None,
        }

    q1 = serie.quantile(0.25)
    q3 = serie.quantile(0.75)
    iqr = q3 - q1

    limite_inferior = q1 - 1.5 * iqr
    limite_superior = q3 + 1.5 * iqr

    mascara_outlier = (serie < limite_inferior) | (serie > limite_superior)
    qtd_outliers = int(mascara_outlier.sum())
    percentual_outliers = round((qtd_outliers / len(serie)) * 100, 2)

    return {
        "coluna": coluna,
        "qtd_outliers": qtd_outliers,
        "percentual_outliers": percentual_outliers,
        "limite_inferior": round(float(limite_inferior), 4),
        "limite_superior": round(float(limite_superior), 4),
    }


def analisar_exploratoriamente(
    data_inicio: str,
    data_fim: str,
    id_application_client: str,
    limite: int | None = None,
) -> dict:
    """
    Executa a análise exploratória dos dados de produção.
    """
    dados_brutos = buscar_eventos_producao(
        data_inicio=data_inicio,
        data_fim=data_fim,
        id_application_client=id_application_client,
        limite=limite,
    )

    if dados_brutos.empty:
        return {
            "dados": dados_brutos,
            "resumo_por_turno": pd.DataFrame(),
            "correlacao": pd.DataFrame(),
            "outliers": pd.DataFrame(),
            "medias_por_turno": pd.DataFrame(),
        }

    dados = preparar_dados_evento_producao(dados_brutos)

    colunas_existentes = [coluna for coluna in COLUNAS_ANALITICAS if coluna in dados.columns]

    # Resumo estatístico por turno
    resumo_por_turno = (
        dados.groupby(["id_turno_estatico", "nome_turno"])[colunas_existentes]
        .agg(["mean", "median", "std", "min", "max"])
        .round(4)
    )

    # Para facilitar exportação e leitura
    resumo_por_turno_exportacao = resumo_por_turno.copy()
    resumo_por_turno_exportacao.columns = [
        f"{coluna}_{estatistica}" for coluna, estatistica in resumo_por_turno_exportacao.columns
    ]
    resumo_por_turno_exportacao = resumo_por_turno_exportacao.reset_index()

    # Médias por turno para leitura rápida
    medias_por_turno = (
        dados.groupby(["id_turno_estatico", "nome_turno"])[colunas_existentes]
        .mean()
        .round(4)
        .reset_index()
        .sort_values("id_turno_estatico")
        .reset_index(drop=True)
    )

    # Correlação entre métricas
    correlacao = dados[colunas_existentes].corr(numeric_only=True).round(4)

    # Outliers por coluna
    lista_outliers = [_calcular_outliers_iqr(dados, coluna) for coluna in colunas_existentes]
    outliers = pd.DataFrame(lista_outliers)

    return {
        "dados": dados,
        "resumo_por_turno": resumo_por_turno_exportacao,
        "correlacao": correlacao,
        "outliers": outliers,
        "medias_por_turno": medias_por_turno,
    }


def exibir_resultados_exploratorios(resultado: dict) -> None:
    """
    Exibe os principais resultados da análise exploratória no terminal.
    """
    if resultado["dados"].empty:
        print("Nenhum dado encontrado para o período e filtros informados.")
        return

    _formatar_titulo("MÉDIAS POR TURNO")
    print(resultado["medias_por_turno"].to_string(index=False))

    _formatar_titulo("CORRELAÇÃO ENTRE MÉTRICAS")
    print(resultado["correlacao"].to_string())

    _formatar_titulo("OUTLIERS POR MÉTRICA")
    print(resultado["outliers"].to_string(index=False))

    _formatar_titulo("RESUMO ESTATÍSTICO POR TURNO")
    print(resultado["resumo_por_turno"].to_string(index=False))


def salvar_resultados_exploratorios(resultado: dict) -> None:
    """
    Salva os resultados da análise exploratória em CSV.
    """
    diretorio_saida = _garantir_diretorio_saida()

    resultado["medias_por_turno"].to_csv(
        diretorio_saida / "eda_medias_por_turno.csv",
        index=False,
        encoding="utf-8-sig",
    )

    resultado["outliers"].to_csv(
        diretorio_saida / "eda_outliers.csv",
        index=False,
        encoding="utf-8-sig",
    )

    resultado["resumo_por_turno"].to_csv(
        diretorio_saida / "eda_resumo_por_turno.csv",
        index=False,
        encoding="utf-8-sig",
    )

    resultado["correlacao"].to_csv(
        diretorio_saida / "eda_correlacao.csv",
        encoding="utf-8-sig",
    )