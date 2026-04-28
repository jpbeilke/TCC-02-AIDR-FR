from pathlib import Path

import pandas as pd

from app.db.repositories import buscar_eventos_producao


DIRETORIO_SAIDA_ANALYTICS = Path("output/analytics")


def _garantir_diretorio_saida() -> Path:
    """
    Garante que o diretório de saída da análise exista.
    """
    DIRETORIO_SAIDA_ANALYTICS.mkdir(parents=True, exist_ok=True)
    return DIRETORIO_SAIDA_ANALYTICS


def _formatar_titulo(texto: str) -> None:
    print(f"\n{'=' * 20} {texto} {'=' * 20}")


def analisar_entendimento_dados(
    data_inicio: str,
    data_fim: str,
    id_application_client: str,
    limite: int | None = None,
) -> dict:
    """
    Executa uma análise inicial de entendimento da base de dados.
    """
    dados = buscar_eventos_producao(
        data_inicio=data_inicio,
        data_fim=data_fim,
        id_application_client=id_application_client,
        limite=limite,
    )

    if dados.empty:
        return {
            "dados": dados,
            "tipos_colunas": pd.DataFrame(),
            "nulos_por_coluna": pd.DataFrame(),
            "duplicados": 0,
            "resumo_numerico": pd.DataFrame(),
            "distribuicao_turnos": pd.DataFrame(),
            "intervalo_datas": {},
        }

    dados_analise = dados.copy()
    dados_analise["data_evento"] = pd.to_datetime(
        dados_analise["data_evento"],
        errors="coerce",
    )

    tipos_colunas = pd.DataFrame(
        {
            "coluna": dados_analise.columns,
            "tipo": [str(tipo) for tipo in dados_analise.dtypes],
        }
    )

    nulos_por_coluna = (
        dados_analise.isnull()
        .sum()
        .reset_index()
        .rename(columns={"index": "coluna", 0: "quantidade_nulos"})
    )
    nulos_por_coluna["percentual_nulos"] = (
        nulos_por_coluna["quantidade_nulos"] / len(dados_analise) * 100
    ).round(2)

    quantidade_duplicados = int(dados_analise.duplicated().sum())

    colunas_numericas = dados_analise.select_dtypes(include=["number"]).columns.tolist()

    if colunas_numericas:
        resumo_numerico = (
            dados_analise[colunas_numericas]
            .describe()
            .transpose()
            .reset_index()
            .rename(columns={"index": "coluna"})
        )
        resumo_numerico = resumo_numerico.round(4)
    else:
        resumo_numerico = pd.DataFrame()

    if "id_turno_estatico" in dados_analise.columns:
        distribuicao_turnos = (
            dados_analise.groupby("id_turno_estatico")
            .size()
            .reset_index(name="quantidade_registros")
            .sort_values("id_turno_estatico")
            .reset_index(drop=True)
        )
    else:
        distribuicao_turnos = pd.DataFrame()

    intervalo_datas = {
        "data_minima": (
            dados_analise["data_evento"].min().strftime("%Y-%m-%d %H:%M:%S")
            if dados_analise["data_evento"].notna().any()
            else None
        ),
        "data_maxima": (
            dados_analise["data_evento"].max().strftime("%Y-%m-%d %H:%M:%S")
            if dados_analise["data_evento"].notna().any()
            else None
        ),
    }

    return {
        "dados": dados_analise,
        "tipos_colunas": tipos_colunas,
        "nulos_por_coluna": nulos_por_coluna,
        "duplicados": quantidade_duplicados,
        "resumo_numerico": resumo_numerico,
        "distribuicao_turnos": distribuicao_turnos,
        "intervalo_datas": intervalo_datas,
    }


def exibir_resultados_entendimento(resultado: dict) -> None:
    """
    Exibe os resultados da análise no terminal.
    """
    dados = resultado["dados"]

    _formatar_titulo("VISÃO GERAL")
    print(f"Quantidade de linhas: {len(dados)}")
    print(f"Quantidade de colunas: {len(dados.columns)}")

    _formatar_titulo("COLUNAS")
    print(", ".join(dados.columns.tolist()))

    _formatar_titulo("TIPOS DAS COLUNAS")
    print(resultado["tipos_colunas"].to_string(index=False))

    _formatar_titulo("VALORES NULOS")
    print(resultado["nulos_por_coluna"].to_string(index=False))

    _formatar_titulo("DUPLICADOS")
    print(f"Quantidade de linhas duplicadas: {resultado['duplicados']}")

    _formatar_titulo("INTERVALO DE DATAS")
    print(f"Data mínima: {resultado['intervalo_datas']['data_minima']}")
    print(f"Data máxima: {resultado['intervalo_datas']['data_maxima']}")

    _formatar_titulo("DISTRIBUIÇÃO POR TURNO")
    if resultado["distribuicao_turnos"].empty:
        print("Não foi possível identificar a distribuição por turno.")
    else:
        print(resultado["distribuicao_turnos"].to_string(index=False))

    _formatar_titulo("ESTATÍSTICAS NUMÉRICAS")
    if resultado["resumo_numerico"].empty:
        print("Não há colunas numéricas para resumir.")
    else:
        print(resultado["resumo_numerico"].to_string(index=False))


def salvar_resultados_entendimento(resultado: dict) -> None:
    """
    Salva os principais resultados da análise em arquivos CSV.
    """
    diretorio_saida = _garantir_diretorio_saida()

    resultado["tipos_colunas"].to_csv(
        diretorio_saida / "tipos_colunas.csv",
        index=False,
        encoding="utf-8-sig",
    )

    resultado["nulos_por_coluna"].to_csv(
        diretorio_saida / "nulos_por_coluna.csv",
        index=False,
        encoding="utf-8-sig",
    )

    if not resultado["resumo_numerico"].empty:
        resultado["resumo_numerico"].to_csv(
            diretorio_saida / "resumo_numerico.csv",
            index=False,
            encoding="utf-8-sig",
        )

    if not resultado["distribuicao_turnos"].empty:
        resultado["distribuicao_turnos"].to_csv(
            diretorio_saida / "distribuicao_turnos.csv",
            index=False,
            encoding="utf-8-sig",
        )

    resultado["dados"].head(200).to_csv(
        diretorio_saida / "amostra_dados.csv",
        index=False,
        encoding="utf-8-sig",
    )