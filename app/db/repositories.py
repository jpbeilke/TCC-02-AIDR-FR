import pandas as pd

from app.db.connection import obter_conexao
from app.db.queries import montar_consulta_evento_producao


def buscar_eventos_producao(
    data_inicio: str,
    data_fim: str,
    id_application_client: str,
    ids_turno: list[int] | None = None,
    limite: int | None = None,
) -> pd.DataFrame:
    """
    Busca registros da tabela evento_producao dentro do período informado.
    """
    if ids_turno is None:
        ids_turno = [3, 4, 5]

    consulta = montar_consulta_evento_producao(
        ids_turno=ids_turno,
        limite=limite,
    )

    parametros = [*ids_turno, id_application_client, data_inicio, data_fim]

    with obter_conexao() as conexao:
        dados = pd.read_sql_query(
            sql=consulta,
            con=conexao,
            params=parametros,
        )

    return dados