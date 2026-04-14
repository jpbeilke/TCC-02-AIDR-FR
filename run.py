import argparse

from app.main import executar_aplicacao


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Gera resumo inicial por turno a partir da tabela evento_producao."
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

    resultado = executar_aplicacao(
        data_inicio=argumentos.data_inicio,
        data_fim=argumentos.data_fim,
        id_application_client=argumentos.cliente,
        limite=argumentos.limite,
    )

    print("\n=== RESUMO POR TURNO ===")
    if resultado["resumo_turnos"].empty:
        print("Nenhum dado encontrado para o período e filtros informados.")
        return

    print(resultado["resumo_turnos"].to_string(index=False))

    print("\n=== RANKING DOS TURNOS ===")
    if resultado["ranking"].empty:
        print("Não foi possível calcular o ranking dos turnos.")
    else:
        print(resultado["ranking"][["nome_turno", "pontuacao_total"]].to_string(index=False))

    print(f"\nMelhor turno: {resultado['melhor_turno']}")
    print(f"Pior turno: {resultado['pior_turno']}")


if __name__ == "__main__":
    main()