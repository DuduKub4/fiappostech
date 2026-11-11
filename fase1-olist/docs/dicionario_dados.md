# Decisões de qualidade e definições

## Escopo
- Período: pedidos com compra entre 01/01/2017 e 31/08/2018. Em 2016 e a partir de set/2018 há volume residual (4 a 324 pedidos/mês).
- Apenas `order_status = delivered` com `order_delivered_customer_date` preenchida (96.470 de 99.441 pedidos antes do recorte de período).
- Excluídos: cancelados (625), indisponíveis (609), em trânsito/processamento (~1.700).

## Definições
- **Receita**: soma de `price` em `order_items`, por pedido (sem frete). Frete (`freight_value`) tratado à parte.
- **Prazo de entrega**: `order_delivered_customer_date − order_purchase_timestamp`, em dias.
- **Atraso**: `order_delivered_customer_date > order_estimated_delivery_date` (comparação por data/hora). Faixas de atraso arredondam frações de dia para cima.
- **Nota do pedido**: média de `review_score` por `order_id` (alguns pedidos têm mais de uma avaliação). 0,7% dos pedidos sem avaliação.
- **Cliente**: `customer_unique_id` (o `customer_id` muda a cada pedido). **Recompra**: cliente com 2+ pedidos entregues no período.
- **CEP**: lido como texto para preservar zeros à esquerda.
- **Pedidos por 100 mil habitantes**: pedidos entregues da UF no período ÷ população da UF em 2018 (IBGE) × 100.000.
- **Previsão de receita**: média da receita dos últimos 3 meses (jun–ago/2018); novembro multiplicado pelo fator Black Friday de 2017 (nov ÷ média de out e dez = 1,44). Faixa de ±7% = erro percentual médio (MAPE) do método no teste.

## Tipos de variáveis e escalas
| Variável | Tipo | Escala | Medida usada |
|---|---|---|---|
| `review_score` (nota 1–5) | qualitativa ordinal | ordinal | média por pedido e % de notas 1–2 (a média é uma simplificação usual para escalas de 5 pontos) |
| `customer_state` (UF) | qualitativa nominal | nominal | contagens e proporções |
| `order_status`, categoria do produto | qualitativa nominal | nominal | contagens e proporções |
| prazo de entrega (dias) | quantitativa contínua | razão | mediana (distribuição assimétrica), desvio-padrão e CV |
| `price`, `freight_value` (R$) | quantitativa contínua | razão | soma e média |
| itens por pedido, pedidos por cliente | quantitativa discreta | razão | contagens |

## Dados externos
- **População por UF (IBGE, 1º/07/2018)**: `data/external/populacao_uf_2018_ibge.csv`, transcrita do arquivo oficial do DOU. Validação: soma = 208.494.900 (total Brasil) e Região Norte = 18.182.253, como no documento.

## Validação da previsão
- Treino com jan/2017–abr/2018, teste com mai–ago/2018. MAPE: média dos últimos 3 meses 7,2%; ingênuo (último mês) 10,6%; Holt com tendência amortecida 27,2%; tendência linear 31,6%.
- Com apenas 20 meses não há como estimar sazonalidade anual completa; o efeito Black Friday vem de um único ano (2017).

## Limitações
- Recompra medida em janela curta (até 20 meses); clientes de 2018 têm pouco tempo para recomprar.
- Marketplace sem custos, margens ou take rate: "receita" é GMV, não receita da Olist.
- Avaliações são auto-selecionadas (amostra não probabilística: quem responde tende a estar muito satisfeito ou muito insatisfeito).
- A penetração por habitante não separa efeito de renda e efeito de entrega; parte da diferença do Nordeste pode vir de renda.
