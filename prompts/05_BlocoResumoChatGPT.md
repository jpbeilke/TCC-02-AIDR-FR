Cenário da aplicação:
Estou analisando dados operacionais de uma fábrica de ração com o objetivo de entender fatores associados ao OEE e, a partir disso, gerar interpretações e sugestões prescritivas com apoio de IA. Os dados são reais, anonimizados, e foram extraídos de um SQL Server. Os registros foram consolidados por turno, e os turnos estáticos são:
- Turno 1 = referência
- turno_4 = diferença do Turno 2 em relação ao Turno 1
- turno_5 = diferença do Turno 3 em relação ao Turno 1

Modelo utilizado:
Regressão linear com OEE como variável-alvo.
Modelo escolhido: modelo_sem_quantidade.
Período analisado: 1 ano.
Quantidade de observações: 317121.

Métricas do modelo:
- R²: 0,273545
- R² ajustado: 0,273536

Coeficientes:
- const: 17,671728
- qtd_batelada: 0,313652
- taxa_producao: 5,211792
- turno_4: -2,287845
- turno_5: 5,380093

Significância estatística:
- Todas as variáveis do modelo tiveram p-valor 0,0, ou seja, apareceram como estatisticamente significativas.

VIF:
- taxa_producao: 2,1220
- turno_4: 1,5186
- qtd_batelada: 1,4398
- turno_5: 1,2068

Principais leituras iniciais:
- taxa_producao tem associação positiva forte com o OEE
- qtd_batelada também tem associação positiva com o OEE
- turno_4 indica associação negativa em relação ao Turno 1
- turno_5 indica associação positiva em relação ao Turno 1
- o modelo é interpretável e estável, com VIFs baixos
- o poder explicativo é moderado, então o OEE também depende de outros fatores não incluídos neste modelo
- a regressão indica associação e não causalidade