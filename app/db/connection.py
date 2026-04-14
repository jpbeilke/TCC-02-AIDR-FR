import os
from pathlib import Path

import pyodbc
from dotenv import load_dotenv

from app.utils.json_loader import carregar_json


CAMINHO_CONFIG_BANCO = Path("config/db.json")


def obter_string_conexao() -> str:
    """
    Lê o config/db.json, identifica qual conexão deve ser usada
    e expande variáveis do arquivo .env.
    """
    load_dotenv()

    configuracao = carregar_json(CAMINHO_CONFIG_BANCO)

    nome_banco_configurado = configuracao.get("Database")
    conexoes = configuracao.get("ConnectionStrings", {})

    if not nome_banco_configurado:
        raise ValueError("O campo 'Database' não foi definido no config/db.json.")

    if nome_banco_configurado not in conexoes:
        raise ValueError(
            f"A conexão '{nome_banco_configurado}' não foi encontrada em 'ConnectionStrings'."
        )

    string_conexao = conexoes[nome_banco_configurado]

    # Expande variáveis como ${SQL_SERVER}, ${SQL_DATABASE}, etc.
    string_conexao_expandida = os.path.expandvars(string_conexao)

    return string_conexao_expandida


def obter_conexao() -> pyodbc.Connection:
    """
    Abre e devolve uma conexão ativa com o SQL Server.
    """
    string_conexao = obter_string_conexao()
    return pyodbc.connect(string_conexao, timeout=30)


def testar_conexao() -> bool:
    """
    Testa a conexão executando um SELECT simples.
    """
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT 1")
        resultado = cursor.fetchone()

    return bool(resultado and resultado[0] == 1)