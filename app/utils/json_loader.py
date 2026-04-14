import json
from pathlib import Path
from typing import Any


def carregar_json(caminho_arquivo: str | Path) -> dict[str, Any]:
    """
    Carrega um arquivo JSON e devolve seu conteúdo como dicionário.
    """
    caminho = Path(caminho_arquivo)

    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo JSON não encontrado: {caminho}")

    with caminho.open("r", encoding="utf-8") as arquivo:
        return json.load(arquivo)