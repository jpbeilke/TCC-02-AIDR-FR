import argparse

from app.analytics.regressao_oee import (
    executar_regressao_oee,
    exibir_resultados_regressao_oee,
    salvar_resultados_regressao_oee,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Executa regressão linear múltipla com OEE como variável-alvo."
    )

    parser.add_argument(
        "--data-inicio",
        required=True,
        help="Data inicial no formato YYYY-MM-DD",
    )
    parser.add_argument(
        "--data-fim",
        required=True,
        help="Data final no formato YYYY-MM-DD",
    )
    parser.add_argument(
        "--cliente",
        required=True,
        help="ID do cliente (id_application_client)",
    )
    parser.add_argument(
        "--modelo",
        required=True,
        help="Modelo a ser testado.",
    )
    parser.add_argument(
        "--limite",
        type=int,
        default=None,
        help="Quantidade máxima de registros retornados pela consulta.",
    )
    parser.add_argument(
        "--sem-turno",
        action="store_true",
        help="Remove as variáveis dummy de turno da regressão.",
    )

    argumentos = parser.parse_args()

    resultado = executar_regressao_oee(
        data_inicio=argumentos.data_inicio,
        data_fim=argumentos.data_fim,
        id_application_client=argumentos.cliente,
        modelo=argumentos.modelo,
        limite=argumentos.limite,
        incluir_turno=not argumentos.sem_turno,
    )

    if resultado["modelo_estimado"] is None:
        print("Não foi possível ajustar o modelo com os filtros informados.")
        return

    exibir_resultados_regressao_oee(resultado)
    salvar_resultados_regressao_oee(resultado)

    print("\nArquivos salvos em: output/analytics/")


if __name__ == "__main__":
    main()