"""
Modelos de requisição
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class RelatorioRequest:
    data_inicio: str
    data_fim: str
    filtros: Optional[dict] = None
