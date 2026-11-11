# Tech Challenge Fase 1 — Olist: crescimento, entrega e satisfação

Relatório analítico para investidores com o *Brazilian E-Commerce Public Dataset by Olist* (≈100 mil pedidos, 2016–2018).

## Tese
A Olist cresceu rápido até 2017, mas estagnou em 2018. O atraso na entrega derruba a satisfação do cliente, e quase ninguém volta a comprar.

## Principais resultados (jan/2017–ago/2018, pedidos entregues)
| Indicador | Valor |
|---|---|
| Receita (itens) | R$ 13,2 mi · 96,2 mil pedidos · ticket médio R$ 137 |
| Crescimento | receita mensal ~R$ 0,9 mi desde jan/2018, sem tendência de alta; pico em nov/2017 (Black Friday) |
| Concentração | top 10 categorias = 63% da receita; top 10% dos vendedores = 67% |
| Atraso | 8,1% dos pedidos chegam após a data estimada; mediana de entrega 10 dias |
| Custo do atraso | nota média 4,30 (no prazo) vs 2,57 (atrasado); 54% das notas 1–2 vs 9% |
| Atraso por região | AL 24%, MA 20%, PI 16%, CE e SE 15%, BA 14%, RJ 13,5% vs SP 5,9% e PR 5,0%; 13 UFs acima de 10% |
| Retenção | só 3,0% dos clientes recompram |
| Achado contraintuitivo | recompra quase não muda com o atraso (3,0% no prazo vs 2,4% atrasado) nem com a nota (3,0% nota 4–5 vs 2,8% nota 1–2) |
| Previsibilidade da entrega | prazo com média 12,5 e mediana 10,2 dias (assimetria 3,85: usamos a mediana); desvio-padrão por UF de 6,7 dias (SP) a 16,8 (SE), correlação de 0,67 com a taxa de atraso |
| Penetração (IBGE) | 46 pedidos por 100 mil habitantes no Brasil; SP 89, Nordeste 16 (MA 10); os 9 estados do Nordeste estão entre as 13 UFs com atraso acima de 10% |
| Cenário Nordeste | na média do Brasil, seriam ~17 mil pedidos e R$ 2,8 mi a mais no período |
| Previsão set–dez/2018 | ~R$ 854 mil/mês, R$ 1,23 mi em nov (Black Friday, fator 1,44); 2018 fecha em ~R$ 11,0 mi. Método validado em mai–ago/2018: média dos últimos 3 meses (erro 7%) vs modelos de tendência (27–32%) |

**Leitura:** o crescimento estagnou, e o maior espaço para crescer (o Nordeste) é onde a entrega mais atrasa e varia. O atraso machuca a reputação (nota), mas o problema de retenção é estrutural, não só logístico. Corrigir a logística protege a marca e abre o Nordeste; aumentar a recompra exige outras alavancas (CRM, cupons, mix de produtos recorrentes).

## Dados externos
- `data/external/populacao_uf_2018_ibge.csv`: estimativas da população residente por UF em 1º/07/2018, publicadas pelo IBGE no DOU ([arquivo oficial](https://ftp.ibge.gov.br/Estimativas_de_Populacao/Estimativas_2018/estimativa_dou_2018_20181019.pdf)). A soma das UFs confere com o total do Brasil (208.494.900); o notebook valida isso ao carregar.

## Como reproduzir
```bash
pip install -r requirements.txt
python -c "import kagglehub,shutil; shutil.copytree(kagglehub.dataset_download('olistbr/brazilian-ecommerce'),'data/raw',dirs_exist_ok=True)"
jupyter nbconvert --to notebook --execute --inplace notebooks/analise_olist.ipynb
```

## Estrutura
```
notebooks/analise_olist.ipynb   análise completa (limpeza → métricas → gráficos)
reports/figuras/                gráficos exportados
docs/dicionario_dados.md        decisões de qualidade, tipos de variáveis e definições de métricas
docs/roteiro_video.md           roteiro do vídeo executivo (~3,8 min)
data/raw/                       CSVs da Olist (não versionados)
data/external/                  dados externos (IBGE), versionados
```
