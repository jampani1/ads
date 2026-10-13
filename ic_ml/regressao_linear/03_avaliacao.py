"""
03_avaliacao.py — Etapa 3: Avaliação do modelo e análise de resíduos
Atividade de IC: Capacity Planning com Regressão Linear Simples.

===============================================================================
MATEMÁTICA DA ETAPA — decomposição da variância
===============================================================================

Resíduo:  eᵢ = yᵢ − ŷᵢ   (o que sobra de cada dia depois da reta)

    SQT = Σ(yᵢ − ȳ)²      variação TOTAL      — o quanto y varia, ponto
    SQR = Σ(ŷᵢ − ȳ)²      variação EXPLICADA  — a parte que a reta reproduz
    SQE = Σ(yᵢ − ŷᵢ)²     variação RESIDUAL   — o que sobrou

e vale a identidade  SQT = SQR + SQE.

Ela não é óbvia. Escrevendo  yᵢ − ȳ = (ŷᵢ − ȳ) + (yᵢ − ŷᵢ)  e elevando ao
quadrado, aparece um termo cruzado  2·Σ(ŷᵢ − ȳ)·eᵢ . Ele é EXATAMENTE zero por
causa das equações normais da Etapa 2 (Σeᵢ = 0 e Σxᵢeᵢ = 0): como ŷᵢ − ȳ é
uma função linear de xᵢ, o termo cruzado é uma combinação de Σeᵢ e Σxᵢeᵢ.
Consequência: R² só tem essa leitura limpa PORQUE o ajuste foi por mínimos
quadrados. Num ajuste feito de outro jeito, R² pode até sair negativo.

Métricas:
    R²   = SQR/SQT = 1 − SQE/SQT      fração da variação de y explicada (sem unidade)
    RMSE = √(SQE / n)                 erro típico de um dia, EM GB
    s    = √(SQE / (n − 2))           erro padrão residual: divide por n−2 porque
                                      dois graus de liberdade foram gastos
                                      estimando β̂₀ e β̂₁ (mesma lógica do n−1 do
                                      desvio amostral). É o s que a Etapa 4 usa.

Em regressão SIMPLES (uma variável), R² = r², o quadrado da correlação de
Pearson. Deixa de valer com 2+ variáveis — e entender por quê é o começo da
regressão múltipla.

===============================================================================
"""

import importlib.util
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

# --- reaproveita a Etapa 2 (dados + funções), sem copiar código ---------------
AQUI = Path(__file__).parent
_spec = importlib.util.spec_from_file_location("ajuste", AQUI / "02_ajuste.py")
ajuste = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ajuste)          # o bloco __main__ do 02 NÃO roda aqui

x, y = ajuste.x, ajuste.y
n = len(x)
beta0, beta1 = ajuste.ajustar(x, y)
y_hat = ajuste.prever(x, beta0, beta1)
residuos = y - y_hat
y_barra = np.mean(y)
FIGURAS = ajuste.FIGURAS
LIMITE_GB = 5000


# ==============================================================================
# PARTE A — Decomposição e métricas (item 3.1 do enunciado)
# ==============================================================================
SQT = np.sum((y - y_barra) ** 2)
SQR = np.sum((y_hat - y_barra) ** 2)
SQE = np.sum(residuos ** 2)

R2 = 1 - SQE / SQT
RMSE = np.sqrt(SQE / n)
s_residual = np.sqrt(SQE / (n - 2))
MAE = np.mean(np.abs(residuos))

print("=== Etapa 3.1 — decomposição da variância ===")
print(f"SQT = {SQT:,.0f}")
print(f"SQR = {SQR:,.0f}")
print(f"SQE = {SQE:,.0f}")

# CHECKPOINT 5 — a identidade e as equações normais.
assert np.isclose(SQT, SQR + SQE, rtol=1e-9)
assert np.isclose(np.sum(residuos), 0, atol=1e-6)
print(f"\nCHECKPOINT 5 OK — SQT = SQR + SQE (erro relativo {abs(SQT - SQR - SQE) / SQT:.2e})")
print(f"                  Σeᵢ = {np.sum(residuos):.2e} ≈ 0")

print(f"\nR²   = {R2:.6f}")
print(f"RMSE = {RMSE:.2f} GB")
print(f"s    = {s_residual:.2f} GB   (divisor n−2)")
print(f"MAE  = {MAE:.2f} GB")

# CHECKPOINT 6 — R² = r² em regressão simples.
r_pearson = np.corrcoef(x, y)[0, 1]
assert np.isclose(r_pearson ** 2, R2)
print(f"\nCHECKPOINT 6 OK — r = {r_pearson:.6f},  r² = {r_pearson ** 2:.6f} = R²")

# Conferência cruzada com sklearn.metrics, quando disponível.
try:
    from sklearn.metrics import mean_squared_error, r2_score
    assert np.isclose(R2, r2_score(y, y_hat))
    assert np.isclose(RMSE, np.sqrt(mean_squared_error(y, y_hat)))
    print("R² e RMSE idênticos aos de sklearn.metrics.")
except ImportError:
    print("(sklearn.metrics indisponível nesta máquina — conferência cruzada pulada)")


# ==============================================================================
# PARTE B — R² alto E erro grande ao mesmo tempo? (item 3.2 do enunciado)
# ==============================================================================
# O R² compara o erro do modelo com o de um modelo "burro" que chuta sempre ȳ.
# Quantificando essa comparação implícita:
erro_trivial = np.sqrt(np.mean((y - y_barra) ** 2))

tabela = pd.DataFrame({
    "Modelo trivial (ŷ = ȳ)": [0.0, erro_trivial, np.mean(np.abs(y - y_barra))],
    "Regressão linear":       [R2, RMSE, MAE],
}, index=["R²", "RMSE (GB)", "MAE (GB)"])
print("\n=== Etapa 3.2 — o que o R² está comparando ===")
print(tabela.round(4).to_string())
print(f"\nO modelo reduz o erro típico de {erro_trivial:.0f} GB para {RMSE:.0f} GB "
      f"({100 * (1 - RMSE / erro_trivial):.1f}% de redução).")

# RESPOSTA À PERGUNTA 3.2:
#   Não há contradição. R² = 0,97 e RMSE = 228 GB respondem perguntas
#   diferentes.
#   - R² é uma RAZÃO sem unidade: "quanto da variação de y a reta explica".
#     Como y sobe de ~130 a ~4600 GB ao longo da série, a variação total é
#     enorme (o modelo trivial erra 1.315 GB em média) — e a reta captura 97%
#     dela.
#   - RMSE está em GB: "quanto um dia típico se afasta da reta". Os 3% que
#     sobram de uma variação enorme ainda são ±228 GB.
#   A leitura ERRADA, a evitar no relatório: "o modelo erra 3% das vezes" ou
#   "margem de erro de 3%". 1 − R² é fração da VARIÂNCIA, não probabilidade nem
#   percentual de erro. A tradução operacional é o RMSE: "a leitura de um dia
#   se afasta da tendência em tipicamente ± 228 GB". Isso é acionável.


# ==============================================================================
# PARTE C — Análise de resíduos (item 3.3 do enunciado, e o que ele não pede)
# ==============================================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 9))
fig.suptitle("Diagnóstico de resíduos", fontsize=13)

# (a) resíduo vs. dia: procura-se faixa de largura constante centrada em zero.
ax = axes[0, 0]
ax.scatter(x, residuos, s=2, alpha=0.10)
ax.axhline(0, color="red", lw=1.2)
ax.axhline(2 * s_residual, color="orange", lw=1, ls="--", label="±2s")
ax.axhline(-2 * s_residual, color="orange", lw=1, ls="--")
ax.set_xlabel("dia"); ax.set_ylabel("resíduo (GB)")
ax.set_title("(a) resíduo vs. dia")
ax.legend(loc="lower right", fontsize=8)

# (b) histograma: a hipótese de normalidade que a Etapa 4 vai usar.
ax = axes[0, 1]
ax.hist(residuos, bins=60, density=True, alpha=0.75, edgecolor="white", linewidth=0.3)
grade = np.linspace(residuos.min(), residuos.max(), 400)
ax.plot(grade, stats.norm.pdf(grade, residuos.mean(), residuos.std()),
        color="red", lw=1.5, label="normal ajustada")
ax.set_xlabel("resíduo (GB)"); ax.set_ylabel("densidade")
ax.set_title("(b) distribuição dos resíduos")
ax.legend(fontsize=8)

# (c) Q-Q plot: normalidade com mais rigor que o histograma, sobretudo nas caudas.
ax = axes[1, 0]
stats.probplot(residuos, dist="norm", plot=ax)
ax.set_title("(c) Q-Q plot (normalidade)")
ax.get_lines()[0].set_markersize(2)
ax.get_lines()[0].set_alpha(0.3)

# (d) média móvel do resíduo: revela curvatura sistemática que o scatter esconde.
janela = 200
media_movel = pd.Series(residuos).rolling(janela, center=True).mean()
ax = axes[1, 1]
ax.plot(x, media_movel, lw=1.2)
ax.axhline(0, color="red", lw=1.2)
ax.set_xlabel("dia"); ax.set_ylabel(f"resíduo médio (janela={janela})")
ax.set_title("(d) média móvel do resíduo — detecta curvatura")

fig.tight_layout()
fig.savefig(FIGURAS / "03_diagnostico_residuos.png", dpi=150)

print("\n=== Etapa 3.3 — resíduos ===")
print(f"média              : {residuos.mean():.2e} GB  (zero por construção)")
print(f"desvio (ddof=2)    : {residuos.std(ddof=2):.2f} GB")
print(f"assimetria (skew)  : {stats.skew(residuos):.4f}   (0 = simétrica)")
print(f"curtose (excesso)  : {stats.kurtosis(residuos):.4f}   (0 = normal)")
for ini, fim in [(0, 3333), (3333, 6666), (6666, n)]:
    print(f"desvio dos resíduos, dias {ini + 1:>5}–{fim:<5}: {residuos[ini:fim].std():.1f} GB")

# LEITURA DO DIAGNÓSTICO:
#   (a) Faixa de largura constante em torno de zero do início ao fim —
#       HOMOCEDASTICIDADE. O desvio por terço da série (222 / 230 / 231 GB)
#       confirma em número. A reta descendente no canto inferior esquerdo é a
#       CENSURA da Etapa 1: para os dias travados em 10 GB, e = 10 − ŷ, que é
#       uma reta de inclinação −β₁.
#   (b)(c) Distribuição simétrica (skew 0,02), colada na normal (curtose 0,03);
#       no Q-Q os pontos seguem a diagonal inteira — só meia dúzia de pontos
#       extremos, nas duas pontas, se afasta dela.
#   (d) A média móvel oscila em torno de zero sem tendência: NÃO há curvatura
#       sistemática — a relação é de fato uma reta (a Parte E confirma).
#       As ondas de até ±45 GB parecem padrão no olho, mas não são: a Parte F
#       mede e mostra que é exatamente a amplitude de ruído independente.
#   Conclusão: as hipóteses do modelo se sustentam. Isso dá à Etapa 4 o direito
#   de usar s e a distribuição normal para falar de RISCO.


# ==============================================================================
# PARTE D — A reta ajustada sobre os dados (item 3.3 do enunciado)
# ==============================================================================
fig, axes = plt.subplots(1, 2, figsize=(15, 5.5))

# Versão 1: dados com transparência + reta + banda de ±2s
ax = axes[0]
ax.scatter(x, y, s=2, alpha=0.10, label="observações")
ax.plot(x, y_hat, color="red", lw=2, label=f"ŷ = {beta0:.1f} + {beta1:.4f}·x")
ax.fill_between(x, y_hat - 2 * s_residual, y_hat + 2 * s_residual,
                color="red", alpha=0.18, label="±2s (~95% das observações)")
ax.axhline(LIMITE_GB, color="black", ls=":", lw=1.5, label=f"limite {LIMITE_GB} GB")
ax.set_xlabel("dia"); ax.set_ylabel("uso_disco_gb (GB)")
ax.set_title("Reta ajustada sobre os dados")
ax.legend(fontsize=8, loc="upper left")

# Versão 2: hexbin + reta — a mesma reta sobre a densidade medida
ax = axes[1]
hb = ax.hexbin(x, y, gridsize=45, cmap="Blues", mincnt=1)
fig.colorbar(hb, ax=ax, label="pontos por célula")
ax.plot(x, y_hat, color="red", lw=2)
ax.axhline(LIMITE_GB, color="black", ls=":", lw=1.5)
ax.set_xlabel("dia"); ax.set_ylabel("uso_disco_gb (GB)")
ax.set_title("A mesma reta sobre a densidade (hexbin)")

fig.tight_layout()
fig.savefig(FIGURAS / "03_reta_ajustada.png", dpi=150)


# ==============================================================================
# PARTE E — Linear × polinomial (o bloco da trilha pede a comparação)
# ==============================================================================
# R² ajustado penaliza parâmetros extras: só sobe se o termo novo pagar o custo.
def r2_ajustado(r2, n_obs, n_params):
    return 1 - (1 - r2) * (n_obs - 1) / (n_obs - n_params - 1)


linhas = []
for grau in (1, 2, 3):
    pred = np.polyval(np.polyfit(x, y, grau), x)
    sqe_g = np.sum((y - pred) ** 2)
    r2_g = 1 - sqe_g / SQT
    linhas.append({
        "Grau": grau,
        "Parâmetros": grau + 1,
        "R²": r2_g,
        "R² ajustado": r2_ajustado(r2_g, n, grau),
        "RMSE (GB)": np.sqrt(sqe_g / n),
    })
comp_poli = pd.DataFrame(linhas).set_index("Grau")
print("\n=== Linear × polinomial ===")
print(comp_poli.round(6).to_string())
ganho = comp_poli.loc[2, "R² ajustado"] - comp_poli.loc[1, "R² ajustado"]
print(f"\nGanho de R² ajustado do grau 1 para o 2: {ganho:+.2e}")
# Ganho desprezível → o modelo LINEAR é o adequado (parcimônia): o termo
# quadrático não captura nada que a reta já não capture. Bate com a média
# móvel sem curvatura da Parte C (d).


# ==============================================================================
# PARTE F — Autocorrelação dos resíduos (Durbin-Watson)
# ==============================================================================
# Série temporal costuma ter dias correlacionados: um dia acima da reta tende a
# vir seguido de outro acima. Se fosse o caso aqui, os n = 10.000 dias valeriam
# menos de 10.000 informações independentes, e os intervalos da Etapa 4
# sairiam OTIMISTAS (estreitos demais). A versão publicada do notebook deixou
# isso como "limitação assumida, não testada". Testando:
#
#   DW = Σ(eᵢ − eᵢ₋₁)² / Σeᵢ²   ≈ 2(1 − ρ₁)
#
#   DW ≈ 2  → sem autocorrelação     DW < 2 → positiva     DW > 2 → negativa
dw = np.sum(np.diff(residuos) ** 2) / np.sum(residuos ** 2)
rho1 = np.corrcoef(residuos[:-1], residuos[1:])[0, 1]

# Segunda forma de ver: se os resíduos são independentes, a média de 200 dias
# tem desvio s/√200. Com autocorrelação positiva, oscilaria bem mais que isso.
desvio_mm = media_movel.dropna().std()
desvio_mm_indep = residuos.std() / np.sqrt(janela)

print("\n=== Autocorrelação dos resíduos ===")
print(f"Durbin-Watson                 = {dw:.3f}   (2 = nenhuma autocorrelação)")
print(f"correlação entre dias vizinhos = {rho1:+.4f}")
print(f"desvio da média móvel: observado {desvio_mm:.2f} GB × "
      f"esperado se independentes {desvio_mm_indep:.2f} GB")

# RESULTADO: DW = 2,03 e ρ₁ = −0,014 — não há autocorrelação. A média móvel
# oscila exatamente o que ruído independente oscilaria (16,09 × 16,10 GB).
# A limitação que estava declarada como aberta fica TESTADA e DESCARTADA: os
# intervalos da Etapa 4 não são otimistas por esse motivo.
# (Lição de método: as ondas do painel (d) pareciam padrão no olho. Só o número
# separou "parece" de "é".)

plt.show()
