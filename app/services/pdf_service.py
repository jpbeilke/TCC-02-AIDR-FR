from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from app.models.report_models import RelatorioTurnos
from app.utils.json_loader import carregar_json


CAMINHO_CONFIG_BANCO = Path("config/db.json")


def _formatar_numero(valor: float | int | None, casas_decimais: int = 2) -> str:
    """
    Formata números para exibição no relatório.
    """
    if valor is None:
        return "-"

    if isinstance(valor, int):
        return str(valor)

    return f"{valor:,.{casas_decimais}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _obter_diretorio_saida() -> Path:
    """
    Lê o diretório de saída do PDF a partir do db.json.
    """
    configuracao = carregar_json(CAMINHO_CONFIG_BANCO)
    relatorios = configuracao.get("Reports", {})
    caminho_saida = relatorios.get("OutputPath", "output/reports/")

    diretorio = Path(caminho_saida)
    diretorio.mkdir(parents=True, exist_ok=True)

    return diretorio


def _montar_nome_arquivo(relatorio: RelatorioTurnos) -> str:
    """
    Gera um nome de arquivo padronizado para o PDF.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"relatorio_turnos_{relatorio.data_inicio}_{relatorio.data_fim}_{timestamp}.pdf"


def _gerar_resumo_textual(relatorio: RelatorioTurnos) -> list[str]:
    """
    Gera textos simples de resumo a partir do objeto estruturado do relatório.
    """
    resultados = relatorio.resultados_por_turno

    if not resultados:
        return ["Não foram encontrados dados para o período analisado."]

    turno_maior_volume = max(resultados, key=lambda x: x.quantidade_total_produzida)
    turno_maior_produtividade = max(resultados, key=lambda x: x.produtividade_media)
    turno_maior_oee = max(resultados, key=lambda x: x.oee_medio)

    textos = [
        (
            f"No período analisado, o melhor desempenho geral foi atribuído ao "
            f"{relatorio.melhor_turno}, enquanto o menor desempenho geral foi observado no "
            f"{relatorio.pior_turno}."
        ),
        (
            f"O maior volume total produzido foi registrado no {turno_maior_volume.nome_turno}, "
            f"com {_formatar_numero(turno_maior_volume.quantidade_total_produzida)} unidades produzidas."
        ),
        (
            f"A maior produtividade média foi observada no {turno_maior_produtividade.nome_turno}, "
            f"com {_formatar_numero(turno_maior_produtividade.produtividade_media)}."
        ),
        (
            f"O maior OEE médio foi identificado no {turno_maior_oee.nome_turno}, "
            f"com {_formatar_numero(turno_maior_oee.oee_medio)}."
        ),
    ]

    return textos


def gerar_pdf_relatorio(relatorio: RelatorioTurnos, caminho_arquivo: str | None = None) -> str:
    """
    Gera um PDF simples com os resultados consolidados por turno.
    """
    diretorio_saida = _obter_diretorio_saida()

    if caminho_arquivo is None:
        caminho_pdf = diretorio_saida / _montar_nome_arquivo(relatorio)
    else:
        caminho_pdf = Path(caminho_arquivo)

    documento = SimpleDocTemplate(
        str(caminho_pdf),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    estilos = getSampleStyleSheet()

    estilo_titulo = estilos["Title"]
    estilo_subtitulo = estilos["Heading2"]
    estilo_texto = estilos["BodyText"]

    estilo_texto.spaceAfter = 10
    estilo_texto.leading = 16

    estilo_texto_negrito = ParagraphStyle(
        name="TextoNegrito",
        parent=estilo_texto,
        fontName="Helvetica-Bold",
    )

    elementos = []

    elementos.append(Paragraph("Relatório Comparativo de Produção por Turno", estilo_titulo))
    elementos.append(Spacer(1, 0.5 * cm))

    elementos.append(Paragraph("Informações Gerais", estilo_subtitulo))
    elementos.append(
        Paragraph(
            f"<b>Período analisado:</b> {relatorio.data_inicio} a {relatorio.data_fim}",
            estilo_texto,
        )
    )
    elementos.append(
        Paragraph(
            f"<b>Cliente:</b> {relatorio.id_application_client}",
            estilo_texto,
        )
    )
    elementos.append(
        Paragraph(
            f"<b>Melhor turno:</b> {relatorio.melhor_turno or '-'}",
            estilo_texto,
        )
    )
    elementos.append(
        Paragraph(
            f"<b>Pior turno:</b> {relatorio.pior_turno or '-'}",
            estilo_texto,
        )
    )

    elementos.append(Spacer(1, 0.3 * cm))
    elementos.append(Paragraph("Resumo Executivo", estilo_subtitulo))

    for texto in _gerar_resumo_textual(relatorio):
        elementos.append(Paragraph(texto, estilo_texto))

    elementos.append(Spacer(1, 0.3 * cm))
    elementos.append(Paragraph("Tabela Comparativa dos Turnos", estilo_subtitulo))

    cabecalho_tabela = [
        "Turno",
        "Registros",
        "Qtd. Produzida",
        "Bateladas",
        "OEE Médio",
        "Produtividade",
        "Qualidade",
        "Taxa Produção",
        "Tempo Médio (s)",
        "Pontuação",
    ]

    linhas_tabela = [cabecalho_tabela]

    for resultado in relatorio.resultados_por_turno:
        linhas_tabela.append(
            [
                resultado.nome_turno,
                _formatar_numero(resultado.total_registros, 0),
                _formatar_numero(resultado.quantidade_total_produzida),
                _formatar_numero(resultado.qtd_batelada_total),
                _formatar_numero(resultado.oee_medio),
                _formatar_numero(resultado.produtividade_media),
                _formatar_numero(resultado.qualidade_media),
                _formatar_numero(resultado.taxa_producao_media),
                _formatar_numero(resultado.tempo_rodando_medio_seg),
                _formatar_numero(resultado.pontuacao_total),
            ]
        )

    tabela = Table(linhas_tabela, repeatRows=1)

    tabela.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9E2F3")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7F7F7")]),
            ]
        )
    )

    elementos.append(tabela)
    elementos.append(Spacer(1, 0.5 * cm))

    data_geracao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elementos.append(Paragraph(f"Relatório gerado em: {data_geracao}", estilo_texto_negrito))

    documento.build(elementos)

    return str(caminho_pdf)