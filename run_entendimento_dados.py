import argparse

from app.analytics.entendimento_dados import (
    analisar_entendimento_dados,
    exibir_resultados_entendimento,
    salvar_resultados_entendimento,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Executa a etapa de entendimento dos dados do projeto."
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
        "--limite",
        type=int,
        default=None,
        help="Quantidade máxima de registros retornados pela consulta.",
    )

    argumentos = parser.parse_args()

    resultado = analisar_entendimento_dados(
        data_inicio=argumentos.data_inicio,
        data_fim=argumentos.data_fim,
        id_application_client=argumentos.cliente,
        limite=argumentos.limite,
    )

    if resultado["dados"].empty:
        print("Nenhum dado encontrado para o período e filtros informados.")
        return

    exibir_resultados_entendimento(resultado)
    salvar_resultados_entendimento(resultado)

    print("\nArquivos salvos em: output/analytics/")


if __name__ == "__main__":
    main()