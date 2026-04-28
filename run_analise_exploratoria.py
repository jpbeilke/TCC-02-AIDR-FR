import argparse

from app.analytics.analise_exploratoria import (
    analisar_exploratoriamente,
    exibir_resultados_exploratorios,
    salvar_resultados_exploratorios,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Executa a análise exploratória dos dados do projeto."
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

    resultado = analisar_exploratoriamente(
        data_inicio=argumentos.data_inicio,
        data_fim=argumentos.data_fim,
        id_application_client=argumentos.cliente,
        limite=argumentos.limite,
    )

    if resultado["dados"].empty:
        print("Nenhum dado encontrado para o período e filtros informados.")
        return

    exibir_resultados_exploratorios(resultado)
    salvar_resultados_exploratorios(resultado)

    print("\nArquivos salvos em: output/analytics/")


if __name__ == "__main__":
    main()