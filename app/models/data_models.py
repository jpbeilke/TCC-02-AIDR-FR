"""
Modelos de dados
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class Turno:
    id: str
    data: str
    turno: str
    funcionario: str
    horas: float
    observacoes: Optional[str] = None
