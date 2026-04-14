from pathlib import Path

import pandas as pd

from app.utils.json_loader import carregar_json


CAMINHO_REGRAS_RANKING = Path("config/report_rules.json")


def calcular_ranking_turnos(resumo_turnos: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula a pontuação de cada turno com base nas regras do JSON.
    """
    if resumo_turnos.empty:
        return resumo_turnos.copy()

    regras = carregar_json(CAMINHO_REGRAS_RANKING)
    pesos = regras.get("weights", {})
    direcoes = regras.get("direction", {})

    ranking = resumo_turnos.copy()
    ranking["pontuacao_total"] = 0.0

    for coluna, peso in pesos.items():
        if coluna not in ranking.columns:
            continue

        serie = pd.to_numeric(ranking[coluna], errors="coerce")
        valor_minimo = serie.min()
        valor_maximo = serie.max()

        if pd.isna(valor_minimo) or pd.isna(valor_maximo):
            notas = pd.Series(0.0, index=ranking.index)
        elif valor_maximo == valor_minimo:
            notas = pd.Series(1.0, index=ranking.index)
        else:
            direcao = direcoes.get(coluna, "higher")

            if direcao == "higher":
                notas = (serie - valor_minimo) / (valor_maximo - valor_minimo)
            else:
                notas = (valor_maximo - serie) / (valor_maximo - valor_minimo)

        nome_coluna_nota = f"nota_{coluna}"
        ranking[nome_coluna_nota] = notas.fillna(0.0)
        ranking["pontuacao_total"] += ranking[nome_coluna_nota] * float(peso)

    ranking["pontuacao_total"] = ranking["pontuacao_total"].round(4)

    ranking = ranking.sort_values(
        by="pontuacao_total",
        ascending=False,
    ).reset_index(drop=True)

    return ranking


def identificar_melhor_e_pior_turno(resumo_turnos: pd.DataFrame) -> dict:
    """
    Identifica o melhor e o pior turno com base no ranking.
    """
    ranking = calcular_ranking_turnos(resumo_turnos)

    if ranking.empty:
        return {
            "melhor_turno": None,
            "pior_turno": None,
            "ranking": ranking,
        }

    melhor_turno = ranking.iloc[0]["nome_turno"]
    pior_turno = ranking.iloc[-1]["nome_turno"]

    return {
        "melhor_turno": melhor_turno,
        "pior_turno": pior_turno,
        "ranking": ranking,
    }