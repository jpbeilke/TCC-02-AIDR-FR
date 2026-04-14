# TCC 02 - Relatório de Turnos

## Descrição
Projeto desenvolvido para gerar relatórios automatizados de turnos de funcionários, utilizando processamento de dados com agentes inteligentes.

## Objetivo
Automatizar a geração de relatórios mensais com métricas, ranking de funcionários e análise de turnos trabalhados.

## Estrutura do Projeto

```
tcc02-relatorio-turnos/
├── app/                 # Código principal da aplicação
│   ├── db/             # Módulo de banco de dados
│   ├── models/         # Modelos de dados
│   ├── services/       # Serviços de negócio
│   ├── agents/         # Agentes de processamento
│   ├── utils/          # Utilitários
│   └── templates/      # Templates HTML/CSS
├── config/             # Arquivos de configuração
├── output/             # Relatórios gerados
├── tests/              # Testes unitários
└── requirements.txt    # Dependências
```

## Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd tcc02-relatorio-turnos
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
```

## Uso

Execute a aplicação:
```bash
python run.py
```

## Testes

Execute os testes unitários:
```bash
python -m pytest tests/
```

## Funcionalidades

- ✅ Coleta de dados de turnos
- ✅ Cálculo de métricas
- ✅ Geração de ranking
- ✅ Exportação em PDF
- ✅ Processamento com agentes inteligentes

## Dependências Principais

- Flask: Framework web
- Pandas: Processamento de dados
- CrewAI: Orquestração de agentes
- ReportLab: Geração de PDF
- Jinja2: Templates

## Autores

- [Seu Nome]

## Licença

MIT License

## Data de Criação

Abril de 2026
