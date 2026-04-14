"""
Utilitários para manipulação de datas
"""

from datetime import datetime, timedelta

def formatar_data(data: str, formato: str = "%d/%m/%Y") -> str:
    """Formata uma data"""
    return datetime.strptime(data, "%Y-%m-%d").strftime(formato)

def obter_data_atual() -> str:
    """Retorna a data atual"""
    return datetime.now().strftime("%Y-%m-%d")

def adicionar_dias(data: str, dias: int) -> str:
    """Adiciona dias à uma data"""
    data_obj = datetime.strptime(data, "%Y-%m-%d")
    nova_data = data_obj + timedelta(days=dias)
    return nova_data.strftime("%Y-%m-%d")
