"""Gráficos da apresentação executiva, na paleta do deck.

Usa as mesmas definições do notebook (pedidos entregues, jan/2017–ago/2018).
Rodar a partir de fase1-olist/:  python reports/graficos_deck.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter

BASE = Path(__file__).resolve().parents[1]
RAW, EXT = BASE / "data/raw", BASE / "data/external"
OUT = BASE / "reports/figuras/deck"
OUT.mkdir(parents=True, exist_ok=True)

# Paleta do deck
CLARO, ESCURO = "#F5F3EC", "#14233A"
MARINHO, LARANJA, LARANJA_ESC = "#14233A", "#B8500A", "#F4A460"
CINZA, CINZA_ESC = "#B9C2CC", "#3E5370"
TEXTO, TEXTO_ESC = "#4A5563", "#C9D3E0"
NE = ["MA", "PI", "CE", "RN", "PB", "PE", "AL", "SE", "BA"]

plt.rcParams.update({
    "font.family": "Inter", "font.size": 18, "axes.spines.top": False,
    "axes.spines.right": False, "axes.spines.left": False,
    "axes.titlesize": 18, "xtick.major.size": 0, "ytick.major.size": 0,
})
br = lambda v, d=0: f"{v:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
MESES = "jan fev mar abr mai jun jul ago set out nov dez".split()


def figura(w, h, fundo=CLARO, texto=TEXTO):
    fig, ax = plt.subplots(figsize=(w / 100, h / 100), dpi=100)
    fig.patch.set_facecolor(fundo); ax.set_facecolor(fundo)
    ax.tick_params(colors=texto); ax.spines["bottom"].set_color(texto)
    for lbl in (ax.xaxis.label, ax.yaxis.label):
        lbl.set_color(texto)
    return fig, ax


def salvar(fig, nome):
    fig.savefig(OUT / nome, dpi=200, bbox_inches="tight", pad_inches=0.15,
                facecolor=fig.get_facecolor())
    plt.close(fig)


# ---------- dados (mesmas definições do notebook) ----------
dt = ["order_purchase_timestamp", "order_delivered_customer_date", "order_estimated_delivery_date"]
orders = pd.read_csv(RAW / "olist_orders_dataset.csv", parse_dates=dt)
items = pd.read_csv(RAW / "olist_order_items_dataset.csv")
reviews = pd.read_csv(RAW / "olist_order_reviews_dataset.csv")
cust = pd.read_csv(RAW / "olist_customers_dataset.csv", dtype={"customer_zip_code_prefix": str})
prods = pd.read_csv(RAW / "olist_products_dataset.csv")
pop = pd.read_csv(EXT / "populacao_uf_2018_ibge.csv")

df = orders[(orders.order_status == "delivered") & orders.order_delivered_customer_date.notna()]
df = df[(df.order_purchase_timestamp >= "2017-01-01") & (df.order_purchase_timestamp < "2018-09-01")].copy()
df = df.join(items.groupby("order_id").price.sum().rename("receita"), on="order_id")
df = df.join(reviews.groupby("order_id").review_score.mean().rename("nota"), on="order_id")
df = df.merge(cust, on="customer_id")
df["atrasou"] = df.order_delivered_customer_date > df.order_estimated_delivery_date
df["dias_atraso"] = np.ceil((df.order_delivered_customer_date - df.order_estimated_delivery_date).dt.total_seconds() / 86400)

# ---------- 1. Receita mensal ----------
s = df.set_index("order_purchase_timestamp").receita.resample("MS").sum()
rot = [f"{MESES[d.month-1]}/{str(d.year)[2:]}" for d in s.index]
media18 = s["2018"].mean()
fig, ax = figura(1664, 500)
x = np.arange(len(s))
ax.plot(x, s / 1e3, color=MARINHO, lw=4, marker="o", ms=8)
i18 = list(s.index).index(pd.Timestamp("2018-01-01"))
ax.hlines(media18 / 1e3, i18, len(s) - 1, colors=LARANJA, linestyles="--", lw=2.5)
ax.text((i18 + len(s) - 1) / 2, 680, f"média 2018: R$ {br(media18/1e3)} mil", color=LARANJA, ha="center", fontsize=18, fontweight="bold")
ipk = list(s.index).index(pd.Timestamp("2017-11-01"))
ax.annotate(f"Black Friday\nR$ {br(s.iloc[ipk]/1e3)} mil", (ipk, s.iloc[ipk] / 1e3), xytext=(ipk - 3.2, s.iloc[ipk] / 1e3 - 60),
            color=MARINHO, fontsize=17, fontweight="bold", arrowprops=dict(arrowstyle="-", color=MARINHO, lw=1.5))
ax.set_xticks(x[::2]); ax.set_xticklabels(rot[::2])
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"R$ {br(v)} mil"))
ax.grid(axis="y", color="#E2DED3", lw=1); ax.set_ylim(0, 1100)
salvar(fig, "d1_receita.png")

# ---------- 2. Previsão ----------
base = s.iloc[-3:].mean()
fator = s["2017-11-01"] / s[["2017-10-01", "2017-12-01"]].mean()
prev = pd.Series([base, base, base * fator, base], index=pd.date_range("2018-09-01", periods=4, freq="MS"))
fig, ax = figura(1000, 560)
xs = np.arange(len(s)); xp = np.arange(len(s) - 1, len(s) + 4)
ax.plot(xs, s / 1e3, color=MARINHO, lw=4)
yp = np.r_[s.iloc[-1], prev.values] / 1e3
ax.plot(xp, yp, color=LARANJA, lw=4, ls="--", marker="o", ms=8)
ax.fill_between(xp[1:], yp[1:] * 0.93, yp[1:] * 1.07, color=LARANJA, alpha=.18, lw=0)
ax.text(len(s) + 1.6, base * fator / 1e3 + 55, f"nov/18: R$ {br(base*fator/1e6, 2)} mi", color=LARANJA, ha="center", fontsize=17, fontweight="bold")
ax.text(len(s) + 1.5, 560, "previsto", color=LARANJA, ha="center", fontsize=17)
ax.text(5, 700, "realizado", color=MARINHO, fontsize=17)
todos = rot + [f"{MESES[d.month-1]}/18" for d in prev.index]
ax.set_xticks(np.arange(0, len(todos), 4)); ax.set_xticklabels(todos[::4])
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"R$ {br(v)} mil"))
ax.grid(axis="y", color="#E2DED3", lw=1); ax.set_ylim(0, 1400)
salvar(fig, "d2_previsao.png")

# ---------- 3. Categorias ----------
nomes = {"beleza_saude": "Beleza e saúde", "relogios_presentes": "Relógios e presentes", "cama_mesa_banho": "Cama, mesa e banho",
         "esporte_lazer": "Esporte e lazer", "informatica_acessorios": "Informática", "moveis_decoracao": "Móveis e decoração",
         "utilidades_domesticas": "Utilidades domésticas", "cool_stuff": "Cool stuff", "automotivo": "Automotivo",
         "ferramentas_jardim": "Ferramentas e jardim"}
cat = items[items.order_id.isin(df.order_id)].merge(prods[["product_id", "product_category_name"]], on="product_id")
cs = cat.groupby("product_category_name").price.sum().sort_values(ascending=False)
top = (cs.head(10) / cs.sum())[::-1]
fig, ax = figura(1000, 600)
ax.barh([nomes[c] for c in top.index], top * 100, color=[MARINHO if v >= top.iloc[-3] else CINZA for v in top], height=.68)
for i, v in enumerate(top):
    ax.text(v * 100 + .2, i, f"{br(v*100, 1)}%", va="center", color=TEXTO, fontsize=17)
ax.set_xticks([]); ax.spines["bottom"].set_visible(False)
salvar(fig, "d3_categorias.png")

# ---------- 4. Penetração (IBGE) ----------
pen = df.groupby("customer_state").order_id.size().rename("pedidos").to_frame().join(pop.set_index("uf"))
pen["p100k"] = pen.pedidos / pen.populacao_2018 * 1e5
pen = pen.sort_values("p100k")
media_br = len(df) / pop.populacao_2018.sum() * 1e5
fig, ax = figura(960, 700)
ax.barh(pen.index, pen.p100k, color=[LARANJA if u in NE else CINZA for u in pen.index], height=.72)
ax.axvline(media_br, color=MARINHO, ls="--", lw=2)
ax.text(media_br + 1.5, 1.2, f"média Brasil: {br(media_br)}", color=MARINHO, fontsize=17, fontweight="bold")
ax.text(pen.p100k.max(), 4.5, "Nordeste", color=LARANJA, ha="right", fontsize=18, fontweight="bold")
ax.tick_params(axis="y", labelsize=12, pad=2); ax.set_ylim(-.7, len(pen) - .3); ax.set_xlabel("pedidos por 100 mil habitantes", fontsize=16)
salvar(fig, "d4_penetracao.png")

# ---------- 5. Atraso por UF (slide escuro) ----------
uf = df.groupby("customer_state").agg(n=("order_id", "size"), atraso=("atrasou", "mean"))
uf = uf[uf.n >= 300].sort_values("atraso", ascending=False)
fig, ax = figura(1664, 470, fundo=ESCURO, texto=TEXTO_ESC)
cores = [LARANJA_ESC if v > .10 else CINZA_ESC for v in uf.atraso]
ax.bar(uf.index, uf.atraso * 100, color=cores, width=.7)
ax.axhline(10, color=TEXTO_ESC, ls="--", lw=1.5)
ax.text(len(uf) - .5, 10.6, "10%", color=TEXTO_ESC, ha="right", fontsize=17)
for i, v in enumerate(uf.atraso):
    if v > .10:
        ax.text(i, v * 100 + .5, f"{br(v*100)}%", ha="center", color=LARANJA_ESC, fontsize=16, fontweight="bold")
ax.set_yticks([]); ax.tick_params(axis="x", labelsize=17)
salvar(fig, "d5_atraso_uf.png")

# ---------- 6. Nota por faixa de atraso ----------
g = df.dropna(subset=["nota"]).copy()
g["faixa"] = pd.cut(g.dias_atraso, [-999, 0, 3, 7, 15, 999], labels=["No prazo", "1–3 dias", "4–7 dias", "8–15 dias", "+15 dias"])
t = g.groupby("faixa", observed=True).nota.mean()
fig, ax = figura(1000, 560)
ax.bar(t.index.astype(str), t.values, color=[MARINHO] + [LARANJA] * 4, width=.62)
for i, v in enumerate(t.values):
    ax.text(i, v + .08, br(v, 1), ha="center", color=MARINHO if i == 0 else LARANJA, fontsize=24, fontweight="bold")
ax.set_ylim(0, 5); ax.set_yticks([]); ax.tick_params(axis="x", labelsize=18)
ax.set_xlabel("atraso em relação à data prometida", fontsize=16)
salvar(fig, "d6_nota_atraso.png")

print("média 2018", round(media18), "| pico nov/17", round(s["2017-11-01"]), "| base", round(base), "| nov/18", round(base * fator))
print("top10 categorias", round(top.sum() * 100, 1), "% |", "Brasil p100k", round(media_br, 1))
print("atraso UFs >10%:", list(uf[uf.atraso > .10].index))
print("notas por faixa:", t.round(2).to_dict())
