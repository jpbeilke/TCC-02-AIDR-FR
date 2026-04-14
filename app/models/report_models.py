from dataclasses import dataclass
from typing import Any


@dataclass
class ResultadoTurno:
    id_turno_estatico: int
    nome_turno: str
    total_registros: int
    quantidade_total_produzida: float
    qtd_batelada_total: float
    oee_medio: float
    produtividade_media: float
    qualidade_media: float
    taxa_producao_media: float
    tempo_rodando_medio_seg: float
    pontuacao_total: float | None = None


@dataclass
class RelatorioTurnos:
    data_inicio: str
    data_fim: str
    id_application_client: str
    melhor_turno: str | None
    pior_turno: str | None
    resultados_por_turno: list[ResultadoTurno]

    def para_dict(self) -> dict[str, Any]:
        return {
            "data_inicio": self.data_inicio,
            "data_fim": self.data_fim,
            "id_application_client": self.id_application_client,
            "melhor_turno": self.melhor_turno,
            "pior_turno": self.pior_turno,
            "resultados_por_turno": [
                resultado.__dict__ for resultado in self.resultados_por_turno
            ],
        }