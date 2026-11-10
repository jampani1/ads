"""
01_eda.py — Itens 1 a 4: compreender o problema, identificar a tarefa, conhecer e ver os dados
Atividade de IC: Classificação de entregas por Regressão Logística.

===============================================================================
MATEMÁTICA DA ETAPA — por que a reta não serve quando y é 0 ou 1
===============================================================================

Y só assume dois valores, então é uma variável de Bernoulli. A média de uma
Bernoulli é a própria probabilidade de sucesso:

    E[Y | x] = 1·P(Y=1 | x) + 0·P(Y=0 | x) = P(Y=1 | x) = p(x)

Ou seja: modelar a MÉDIA de y dado x, que é o que a regressão faz, aqui é modelar
uma PROBABILIDADE. Isso exige duas coisas que a reta não entrega:

  1. p(x) precisa ficar em [0, 1]. Uma reta com β₁ ≠ 0 é ilimitada: para x grande
     o bastante ela passa de 1, para x pequeno o bastante fica abaixo de 0.
  2. A variância de uma Bernoulli é p(1 − p): muda com x, é máxima em p = 0,5.
     O erro não tem variância constante nem é normal (só existem dois valores
     possíveis de resíduo para cada x), então a hipótese do modelo linear cai.

A saída é modelar uma quantidade que PODE ser ilimitada e voltar para [0, 1] no
fim. Essa quantidade é o logaritmo da chance (Etapa 2).

Tarefa (item 2): APRENDIZADO SUPERVISIONADO (cada pedido vem com o resultado
observado) de CLASSIFICAÇÃO BINÁRIA (a saída é uma de duas categorias). O nome
"regressão" vem de o modelo prever um número, a probabilidade; a classificação só
acontece depois, quando um limiar corta essa probabilidade.

===============================================================================
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

import comum
from comum import (COR_APOIO, COR_ATRASO, COR_CORRETA, COR_MODELO, FIGURAS, MARCA_ATRASO,
                   MARCA_CORRETA, br)

df = comum.carregar_dados()
x, y = df["x"].values, df["y"].values
n = len(df)
df["id"] = df["pedido"].str[-3:].astype(int)


# ==============================================================================
# Item 3 — integridade e variáveis
# ==============================================================================
assert df.shape == (42, 4)                                  # 3 colunas do CSV + id
assert df.isna().sum().sum() == 0                           # nenhum valor faltante
assert df["pedido"].is_unique                               # nenhum pedido repetido
assert set(df["id"]) == set(range(1, 43))                   # PED-001 a PED-042, sem buraco
assert set(df["y"]) == {0, 1}                               # alvo realmente binário
assert (df["x"] >= 0).all()                                 # antecedência não negativa

print("=== Item 3 — integridade ===")
print(f"{n} pedidos, sem faltantes nem repetidos; x em [{x.min()}, {x.max()}] horas")

n1, n0 = int(y.sum()), int(n - y.sum())
print("\n=== Item 3 — classes ===")
print(f"y = 1 (na data correta): {n1} ({n1 / n:.1%})")
print(f"y = 0 (com atraso)     : {n0} ({n0 / n:.1%})")

print("\n=== Item 3 — antecedência por classe ===")
print(df.groupby("y")["x"].describe().round(2).to_string())

# Separação perfeita faria a máxima verossimilhança não existir (β₁ iria a infinito).
# Basta um pedido de cada classe do lado "errado" para o ótimo ser finito.
max_atraso = x[y == 0].max()
min_correta = x[y == 1].min()
print("\n=== Item 3 — sobreposição das classes ===")
print(f"menor x de uma entrega correta: {min_correta}")
print(f"maior x de um atraso          : {max_atraso}")
assert min_correta < max_atraso
print(f"as classes se misturam em [{min_correta}, {max_atraso}]: não há separação perfeita")


# ==============================================================================
# Item 3 — o número do pedido não é um identificador neutro
# ==============================================================================
def melhor_corte(variavel, alvo):
    """Melhor regra 'variavel >= c prevê 1', testando todos os cortes possíveis."""
    v = np.sort(np.unique(variavel))
    cortes = np.r_[v[0] - 1, (v[:-1] + v[1:]) / 2, v[-1] + 1]
    acertos = [int(((variavel >= c).astype(int) == alvo).sum()) for c in cortes]
    i = int(np.argmax(acertos))
    return cortes[i], acertos[i]


rho_x = stats.spearmanr(df["id"], df["x"]).statistic
rho_y = stats.spearmanr(df["id"], df["y"]).statistic
corte_id, acertos_id = melhor_corte(df["id"].values, y)
corte_x, acertos_x = melhor_corte(x, y)

print("\n=== Item 3 — o número do pedido ===")
print(f"correlação de Spearman id × x: {rho_x:.3f}")
print(f"correlação de Spearman id × y: {rho_y:.3f}")
print(f"melhor corte em id: id ≥ {corte_id:.1f} acerta {acertos_id}/{n}")
print(f"melhor corte em x : x ≥ {corte_x:.3f} acerta {acertos_x}/{n}")
ordenado = df.sort_values("id")
sequencia = "".join(str(v) for v in ordenado["y"])
blocos = [len(b) for b in sequencia.replace("01", "0 1").replace("10", "1 0").split()]
print("y na ordem do pedido:", sequencia)
print("tamanho dos blocos  :", blocos)
print("→ o id acerta mais que a antecedência, e por isso mesmo fica fora do modelo: número de")
print("  pedido não explica atraso. Hipótese: a tabela foi montada em blocos e depois embaralhada.")


# ==============================================================================
# Item 4 — figuras
# ==============================================================================
# Figura 1: os dados por classe. O deslocamento vertical (jitter) só separa pontos
# próximos: ele não carrega informação, por isso a seed é fixa e o eixo y não tem escala.
rng = np.random.default_rng(42)
fig, ax = plt.subplots(figsize=(8, 3.6))
for classe, nome, cor, marca in [(1, "Na data correta", COR_CORRETA, MARCA_CORRETA),
                                 (0, "Com atraso", COR_ATRASO, MARCA_ATRASO)]:
    sel = y == classe
    faixa = classe + rng.uniform(-0.14, 0.14, sel.sum())
    ax.scatter(x[sel], faixa, s=64, color=cor, marker=marca, alpha=0.85,
               edgecolor="white", linewidth=0.8, label=f"{nome} (n = {sel.sum()})")
ax.set_yticks([0, 1], ["Atraso\n(y = 0)", "Correta\n(y = 1)"])
ax.set_ylim(-0.5, 1.5)
ax.set_xlabel("Antecedência do despacho (horas)")
ax.set_title("As classes se separam, mas se misturam no meio")
ax.grid(axis="y", visible=False)
fig.savefig(FIGURAS / "01_dados_por_classe.png")
plt.close(fig)

# Figura 2: taxa de entrega correta por faixa. É a primeira estimativa de p(x),
# feita sem modelo nenhum.
faixas = [0, 6, 12, 18, 24]
rotulos = ["0 a 6 h", "6 a 12 h", "12 a 18 h", "18 a 24 h"]
indice = np.digitize(x, faixas) - 1
contagem = np.array([(indice == i).sum() for i in range(4)])
corretas = np.array([y[indice == i].sum() for i in range(4)])
taxa = corretas / contagem
print("\n=== Item 4 — taxa de entrega correta por faixa ===")
for r, c, t, tx in zip(rotulos, corretas, contagem, taxa):
    print(f"{r:>10}: {c:2d}/{t:2d} = {tx:.1%}")

fig, ax = plt.subplots(figsize=(8, 4.2))
barras = ax.bar(rotulos, taxa, width=0.55, color=COR_CORRETA)
for barra, c, t, tx in zip(barras, corretas, contagem, taxa):
    ax.text(barra.get_x() + barra.get_width() / 2, tx + 0.025,
            f"{tx:.0%}\n{c} de {t}", ha="center", va="bottom", color=COR_MODELO, fontsize=12)
ax.set_ylim(0, 1.2)
ax.set_yticks(np.arange(0, 1.01, 0.25), ["0%", "25%", "50%", "75%", "100%"])
ax.set_ylabel("Entregas na data correta")
ax.set_xlabel("Antecedência do despacho")
ax.set_title("A taxa dá um salto perto de 12 horas")
ax.grid(axis="x", visible=False)
fig.savefig(FIGURAS / "01_taxa_por_faixa.png")
plt.close(fig)

# Figura 3: por que a reta não serve. Ajuste por mínimos quadrados em y = 0/1.
b1_reta = np.dot(x - x.mean(), y - y.mean()) / np.dot(x - x.mean(), x - x.mean())
b0_reta = y.mean() - b1_reta * x.mean()
print("\n=== Item 4 — a reta sobre y binário ===")
print(f"ŷ = {b0_reta:.4f} + {b1_reta:.4f}·x")
print(f"em x = 0  → {b0_reta:.3f}   (probabilidade negativa)")
print(f"em x = 24 → {b0_reta + 24 * b1_reta:.3f}   (probabilidade acima de 1)")

fig, ax = plt.subplots(figsize=(8, 4.6))
grade = np.array([0, 24])
ax.axhspan(1, 1.25, color="#f3e4dc", zorder=0)
ax.axhspan(-0.25, 0, color="#f3e4dc", zorder=0)
ax.scatter(x[y == 1], y[y == 1], s=56, color=COR_CORRETA, marker=MARCA_CORRETA, alpha=0.8,
           edgecolor="white", linewidth=0.8, label="Na data correta")
ax.scatter(x[y == 0], y[y == 0], s=56, color=COR_ATRASO, marker=MARCA_ATRASO, alpha=0.8,
           edgecolor="white", linewidth=0.8, label="Com atraso")
ax.plot(grade, b0_reta + b1_reta * grade, color=COR_MODELO, linewidth=2, label="Reta de mínimos quadrados")
ax.text(23.8, 1.17, "probabilidade acima de 1", ha="right", color=COR_APOIO, fontsize=12)
ax.text(0.3, -0.17, "probabilidade negativa", ha="left", color=COR_APOIO, fontsize=12)
ax.set_xlim(0, 24)
ax.set_ylim(-0.25, 1.25)
ax.yaxis.set_major_formatter(comum.virgula(1))
ax.set_xlabel("Antecedência do despacho (horas)")
ax.set_ylabel("y  /  reta")
ax.set_title("A reta escapa do intervalo [0, 1]")
ax.legend(loc="upper left", bbox_to_anchor=(0.01, 0.8), fontsize=12)
fig.savefig(FIGURAS / "01_reta_nao_serve.png")
plt.close(fig)

# Figura 4: o número do pedido contra a antecedência.
fig, ax = plt.subplots(figsize=(8, 4.4))
for classe, nome, cor, marca in [(1, "Na data correta", COR_CORRETA, MARCA_CORRETA),
                                 (0, "Com atraso", COR_ATRASO, MARCA_ATRASO)]:
    sel = df["y"] == classe
    ax.scatter(df.loc[sel, "id"], df.loc[sel, "x"], s=64, color=cor, marker=marca, alpha=0.9,
               edgecolor="white", linewidth=0.8, label=nome)
ax.axvline(corte_id, color=COR_APOIO, linewidth=1.5, linestyle="--")
ax.text(corte_id + 0.4, 0.6, f"corte em id: {acertos_id} de {n} acertos", color=COR_APOIO, fontsize=12)
ax.set_xlabel("Número do pedido (PED-001 a PED-042)")
ax.set_ylabel("Antecedência (horas)")
ax.set_title("O número do pedido carrega a resposta")
ax.legend(loc="upper left")
fig.savefig(FIGURAS / "01_id_vazamento.png")
plt.close(fig)

print(f"\nFiguras salvas em {FIGURAS.name}/")
