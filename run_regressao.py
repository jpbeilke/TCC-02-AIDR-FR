import argparse

from app.analytics.regressao import (
    executar_regressao,
    exibir_resultados_regressao,
    salvar_resultados_regressao,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Executa regressão linear múltipla para análise dos dados."
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
        "--alvo",
        required=True,
        choices=["quantidade_produzida", "produtividade"],
        help="Variável alvo da regressão.",
    )
    parser.add_argument(
        "--modelo",
        required=True,
        help="Nome do modelo a ser testado.",
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

    resultado = executar_regressao(
        data_inicio=argumentos.data_inicio,
        data_fim=argumentos.data_fim,
        id_application_client=argumentos.cliente,
        alvo=argumentos.alvo,
        modelo=argumentos.modelo,
        limite=argumentos.limite,
        incluir_turno=not argumentos.sem_turno,
    )

    if resultado["modelo_estimado"] is None:
        print("Não foi possível ajustar o modelo com os filtros informados.")
        return

    exibir_resultados_regressao(resultado)
    salvar_resultados_regressao(resultado)

    print("\nArquivos salvos em: output/analytics/")


if __name__ == "__main__":
    main()