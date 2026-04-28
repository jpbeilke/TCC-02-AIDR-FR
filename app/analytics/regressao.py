from pathlib import Path

import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

from app.db.repositories import buscar_eventos_producao
from app.services.data_service import preparar_dados_evento_producao


DIRETORIO_SAIDA_ANALYTICS = Path("output/analytics")


ALVOS_PERMITIDOS = ["quantidade_produzida", "produtividade"]


PREDITORES_POR_MODELO = {
    "quantidade_produzida": {
        "modelo_completo": [
            "qtd_batelada",
            "tempo_rodando_segundo",
            "taxa_producao",
            "oee",
            "produtividade",
        ],
        "modelo_sem_produtividade": [
            "qtd_batelada",
            "tempo_rodando_segundo",
            "taxa_producao",
            "oee",
        ],
        "modelo_sem_oee": [
            "qtd_batelada",
            "tempo_rodando_segundo",
            "taxa_producao",
            "produtividade",
        ],
        "modelo_essencial": [
            "qtd_batelada",
            "tempo_rodando_segundo",
            "taxa_producao",
        ],
    },
    "produtividade": {
        "modelo_completo": [
            "oee",
            "taxa_producao",
            "tempo_rodando_segundo",
            "qtd_batelada",
        ],
        "modelo_sem_oee": [
            "taxa_producao",
            "tempo_rodando_segundo",
            "qtd_batelada",
        ],
        "modelo_essencial": [
            "taxa_producao",
            "tempo_rodando_segundo",
        ],
    },
}


def _garantir_diretorio_saida() -> Path:
    DIRETORIO_SAIDA_ANALYTICS.mkdir(parents=True, exist_ok=True)
    return DIRETORIO_SAIDA_ANALYTICS


def _formatar_titulo(texto: str) -> None:
    print(f"\n{'=' * 20} {texto} {'=' * 20}")


def _calcular_vif(base_preditores: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula VIF para os preditores do modelo.
    """
    if base_preditores.empty:
        return pd.DataFrame(columns=["variavel", "vif"])

    resultados = []
    for indice, coluna in enumerate(base_preditores.columns):
        vif = variance_inflation_factor(base_preditores.values, indice)
        resultados.append(
            {
                "variavel": coluna,
                "vif": round(float(vif), 4),
            }
        )

    return (
        pd.DataFrame(resultados)
        .sort_values("vif", ascending=False)
        .reset_index(drop=True)
    )


def _remover_colunas_constantes(dados: pd.DataFrame) -> pd.DataFrame:
    """
    Remove colunas com apenas um valor único.
    """
    colunas_validas = [
        coluna for coluna in dados.columns
        if dados[coluna].nunique(dropna=True) > 1
    ]
    return dados[colunas_validas].copy()


def _obter_preditores(alvo: str, modelo: str) -> list[str]:
    if alvo not in PREDITORES_POR_MODELO:
        raise ValueError(f"Alvo inválido: {alvo}")

    modelos_disponiveis = PREDITORES_POR_MODELO[alvo]

    if modelo not in modelos_disponiveis:
        raise ValueError(
            f"Modelo inválido para alvo '{alvo}'. "
            f"Use um destes: {list(modelos_disponiveis.keys())}"
        )

    return modelos_disponiveis[modelo]


def preparar_base_regressao(
    data_inicio: str,
    data_fim: str,
    id_application_client: str,
    alvo: str,
    modelo: str,
    limite: int | None = None,
    incluir_turno: bool = True,
) -> tuple[pd.DataFrame, pd.Series, pd.DataFrame]:
    """
    Busca e prepara a base para regressão.
    """
    if alvo not in ALVOS_PERMITIDOS:
        raise ValueError(f"Alvo inválido. Use um destes: {ALVOS_PERMITIDOS}")

    preditores = _obter_preditores(alvo, modelo)

    dados_brutos = buscar_eventos_producao(
        data_inicio=data_inicio,
        data_fim=data_fim,
        id_application_client=id_application_client,
        limite=limite,
    )

    if dados_brutos.empty:
        return pd.DataFrame(), pd.Series(dtype="float64"), pd.DataFrame()

    dados = preparar_dados_evento_producao(dados_brutos)

    colunas_necessarias = [alvo] + preditores
    if incluir_turno and "id_turno_estatico" in dados.columns:
        colunas_necessarias.append("id_turno_estatico")

    base = dados[colunas_necessarias].copy()

    for coluna in base.columns:
        base[coluna] = pd.to_numeric(base[coluna], errors="coerce")

    base = base.dropna().reset_index(drop=True)

    if incluir_turno and "id_turno_estatico" in base.columns:
        dummies_turno = pd.get_dummies(
            base["id_turno_estatico"],
            prefix="turno",
            drop_first=True,
            dtype=int,
        )
        base = pd.concat([base.drop(columns=["id_turno_estatico"]), dummies_turno], axis=1)

    y = base[alvo].copy()
    x = base.drop(columns=[alvo]).copy()

    x = _remover_colunas_constantes(x)

    return x, y, base


def executar_regressao(
    data_inicio: str,
    data_fim: str,
    id_application_client: str,
    alvo: str,
    modelo: str,
    limite: int | None = None,
    incluir_turno: bool = True,
) -> dict:
    """
    Executa a regressão linear múltipla.
    """
    x, y, base_modelo = preparar_base_regressao(
        data_inicio=data_inicio,
        data_fim=data_fim,
        id_application_client=id_application_client,
        alvo=alvo,
        modelo=modelo,
        limite=limite,
        incluir_turno=incluir_turno,
    )

    if x.empty or y.empty:
        return {
            "x": x,
            "y": y,
            "base_modelo": base_modelo,
            "modelo_estimado": None,
            "coeficientes": pd.DataFrame(),
            "vif": pd.DataFrame(),
            "metricas_modelo": {},
        }

    x_com_constante = sm.add_constant(x, has_constant="add")
    modelo_estimado = sm.OLS(y, x_com_constante).fit()

    coeficientes = pd.DataFrame(
        {
            "variavel": modelo_estimado.params.index,
            "coeficiente": modelo_estimado.params.values,
            "erro_padrao": modelo_estimado.bse.values,
            "estatistica_t": modelo_estimado.tvalues.values,
            "p_valor": modelo_estimado.pvalues.values,
        }
    ).round(6)

    vif = _calcular_vif(x)

    metricas_modelo = {
        "alvo": alvo,
        "modelo": modelo,
        "quantidade_observacoes": int(modelo_estimado.nobs),
        "r2": round(float(modelo_estimado.rsquared), 6),
        "r2_ajustado": round(float(modelo_estimado.rsquared_adj), 6),
        "aic": round(float(modelo_estimado.aic), 6),
        "bic": round(float(modelo_estimado.bic), 6),
    }

    return {
        "x": x,
        "y": y,
        "base_modelo": base_modelo,
        "modelo_estimado": modelo_estimado,
        "coeficientes": coeficientes,
        "vif": vif,
        "metricas_modelo": metricas_modelo,
    }


def exibir_resultados_regressao(resultado: dict) -> None:
    """
    Exibe os resultados principais da regressão no terminal.
    """
    if resultado["modelo_estimado"] is None:
        print("Não foi possível ajustar o modelo de regressão com os dados informados.")
        return

    metricas = resultado["metricas_modelo"]

    _formatar_titulo("MÉTRICAS DO MODELO")
    print(f"Variável alvo: {metricas['alvo']}")
    print(f"Modelo testado: {metricas['modelo']}")
    print(f"Quantidade de observações: {metricas['quantidade_observacoes']}")
    print(f"R²: {metricas['r2']}")
    print(f"R² ajustado: {metricas['r2_ajustado']}")
    print(f"AIC: {metricas['aic']}")
    print(f"BIC: {metricas['bic']}")

    _formatar_titulo("COEFICIENTES")
    print(resultado["coeficientes"].to_string(index=False))

    _formatar_titulo("VIF")
    if resultado["vif"].empty:
        print("Não foi possível calcular VIF.")
    else:
        print(resultado["vif"].to_string(index=False))


def salvar_resultados_regressao(resultado: dict) -> None:
    """
    Salva os resultados da regressão em CSV e TXT.
    """
    if resultado["modelo_estimado"] is None:
        return

    diretorio_saida = _garantir_diretorio_saida()
    alvo = resultado["metricas_modelo"]["alvo"]
    modelo = resultado["metricas_modelo"]["modelo"]

    resultado["coeficientes"].to_csv(
        diretorio_saida / f"regressao_coeficientes_{alvo}_{modelo}.csv",
        index=False,
        encoding="utf-8-sig",
    )

    resultado["vif"].to_csv(
        diretorio_saida / f"regressao_vif_{alvo}_{modelo}.csv",
        index=False,
        encoding="utf-8-sig",
    )

    pd.DataFrame([resultado["metricas_modelo"]]).to_csv(
        diretorio_saida / f"regressao_metricas_{alvo}_{modelo}.csv",
        index=False,
        encoding="utf-8-sig",
    )

    resumo_textual = resultado["modelo_estimado"].summary().as_text()
    with open(
        diretorio_saida / f"regressao_resumo_{alvo}_{modelo}.txt",
        "w",
        encoding="utf-8",
    ) as arquivo:
        arquivo.write(resumo_textual)