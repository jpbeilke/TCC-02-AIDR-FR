"""
Modelos de relatório
"""

from dataclasses import dataclass, field
from typing import List, Any

@dataclass
class Relatorio:
    titulo: str
    data_geracao: str
    metricas: dict = field(default_factory=dict)
    dados: List[Any] = field(default_factory=list)
    ranking: List[dict] = field(default_factory=list)
