"""
04_predicao.py — Etapa 4: Predição e decisão
Atividade de IC: Capacity Planning com Regressão Linear Simples.

===============================================================================
MATEMÁTICA DA ETAPA
===============================================================================

4.1 — O que o enunciado pede: inverter a reta.

    ŷ = β̂₀ + β̂₁·x = 5000    →    x* = (5000 − β̂₀) / β̂₁

  x* é o dia em que a MÉDIA prevista cruza 5000 GB. Mas o disco não enche na
  média: enche num dia concreto, com o ruído daquele dia. Metade dos dias fica
  acima da reta — o risco real começa bem antes de x*.

4.2 — Dois intervalos diferentes; a diferença é um "1" dentro da raiz:

    CONFIANÇA (onde está a MÉDIA de y no dia x₀):
        ŷ₀ ± t · s · √(     1/n + (x₀ − x̄)²/Sxx )

    PREDIÇÃO (onde estará UMA leitura no dia x₀):
        ŷ₀ ± t · s · √( 1 + 1/n + (x₀ − x̄)²/Sxx )

  Os três termos sob a raiz:
    1              variabilidade irredutível do dia. Não some nem com n → ∞.
                   Só existe na PREDIÇÃO — é ela que importa para a infra.
    1/n            incerteza sobre onde está a média. Com n = 10.000, nada.
    (x₀−x̄)²/Sxx    penalidade de EXTRAPOLAR: cresce com o quadrado da distância
                   ao centro dos dados. É o que faz as bandas abrirem em funil.

  O dia de risco: quando há 5% de chance de uma leitura passar de 5000 GB, ou
  seja, quando o percentil 95 da distribuição preditiva cruza o limite.
  Com n = 10.000, t ≈ z, e a conta vira:

        β̂₀ + β̂₁·x + z₀,₉₅ · s = 5000      (z₀,₉₅ ≈ 1,645)

  Capacity planning se faz no percentil, não na média: ninguém compra disco
  para o dia em que o uso, EM MÉDIA, estoura.

4.3 — A hipótese que ninguém escreve: extrapolar assume que a tendência
  linear continua valendo depois do dia 10.000. Isso é hipótese, não
  resultado. O modelo não sabe de expurgo de log, migração ou de um deploy que
  dobra o volume.

===============================================================================
"""

import importlib.util
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# --- reaproveita a Etapa 2 (dados + funções) ----------------------------------
AQUI = Path(__file__).parent
_spec = importlib.util.spec_from_file_location("ajuste", AQUI / "02_ajuste.py")
ajuste = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ajuste)

x, y = ajuste.x, ajuste.y
n = len(x)
beta0, beta1 = ajuste.ajustar(x, y)
residuos = y - ajuste.prever(x, beta0, beta1)
s_residual = np.sqrt(np.sum(residuos ** 2) / (n - 2))
x_barra = np.mean(x)
Sxx = ajuste.calcular_sxx(x)
FIGURAS = ajuste.FIGURAS
LIMITE_GB = 5000
ultimo_dia = int(x.max())


# ==============================================================================
# PARTE A — A resposta direta (item 4.1 do enunciado)
# ==============================================================================
x_estrela = (LIMITE_GB - beta0) / beta1
dias_restantes = x_estrela - ultimo_dia

print("=== Etapa 4.1 — a resposta algébrica ===")
print(f"Dia em que a TENDÊNCIA atinge {LIMITE_GB} GB:  x* = {x_estrela:,.1f}")
print(f"Último dia monitorado:                        {ultimo_dia:,}")
print(f"Dias restantes (resposta direta):             {dias_restantes:,.0f} dias "
      f"(≈ {dias_restantes / 30:.1f} meses)")

# CHECKPOINT 7 — comparar x* com o máximo observado.
acima = y > LIMITE_GB
print(f"\nCHECKPOINT 7 — máximo observado: {y.max():.2f} GB no dia {int(x[np.argmax(y)])}")
print(f"               dias da amostra já acima de {LIMITE_GB} GB: {acima.sum()} "
      f"(o primeiro no dia {int(x[acima].min())})")
# Se a reta só chega a 5000 GB daqui a 861 dias, como 9 dias JÁ passaram?
# Porque quem passou foi o ruído, não a reta. É o sinal de que a resposta
# direta é insuficiente — e o motivo da Parte B.


# ==============================================================================
# PARTE B — Intervalo de confiança × intervalo de predição (item 4.2)
# ==============================================================================
def intervalos(x0, confianca=0.95):
    """Retorna (ŷ₀, meia-largura do IC da média, meia-largura do IP de um dia)."""
    x0 = np.asarray(x0, dtype=float)
    y0 = beta0 + beta1 * x0
    t_crit = stats.t.ppf(1 - (1 - confianca) / 2, df=n - 2)
    nucleo = 1.0 / n + (x0 - x_barra) ** 2 / Sxx
    return y0, t_crit * s_residual * np.sqrt(nucleo), t_crit * s_residual * np.sqrt(1 + nucleo)


termo_media = 1.0 / n
termo_extrap = (x_estrela - x_barra) ** 2 / Sxx
print(f"\n=== Etapa 4.2 — os termos sob a raiz, em x₀ = x* = {x_estrela:,.0f} ===")
print(f"  1                 = 1.000000")
print(f"  1/n               = {termo_media:.6f}")
print(f"  (x₀ − x̄)²/Sxx     = {termo_extrap:.6f}")
print(f"→ a variabilidade do dia é {100 / (1 + termo_media + termo_extrap):.1f}% do total sob a raiz")

_, ic, ip = intervalos(x_estrela)
print(f"\nEm x*:  IC 95% da média = ±{ic:,.2f} GB")
print(f"        IP 95% de um dia = ±{ip:,.2f} GB   ({ip / ic:,.0f}× mais largo)")
# Leitura: sabemos MUITO bem onde a média estará (±10 GB); não sabemos onde
# um dia específico estará (±447 GB) — 44 vezes mais largo. A extrapolação de
# 861 dias pesa pouco (termo 0,0004) porque x* fica perto do fim de uma série
# longa: 99,9% da incerteza sob a raiz é o "1", a variabilidade do dia.


# ==============================================================================
# PARTE C — O dia em que o RISCO se torna relevante
# ==============================================================================
z95 = stats.norm.ppf(0.95)
x_risco = (LIMITE_GB - z95 * s_residual - beta0) / beta1


def prob_estouro(x0):
    """P(uma leitura no dia x0 passar de 5000 GB), pela normal dos resíduos."""
    y0 = beta0 + beta1 * np.asarray(x0, dtype=float)
    return 1 - stats.norm.cdf((LIMITE_GB - y0) / s_residual)


print("\n=== As duas respostas ===")
print(f"Dia em que a TENDÊNCIA atinge {LIMITE_GB} GB     : {x_estrela:,.0f}")
print(f"Dia em que o PERCENTIL 95 atinge {LIMITE_GB} GB  : {x_risco:,.0f}")
print(f"Diferença                                  : {x_estrela - x_risco:,.0f} dias")
print(f"\nP(estouro) no último dia observado         : {100 * prob_estouro(ultimo_dia):.2f}%")
print(f"Margem real a partir do dia {ultimo_dia}          : {x_risco - ultimo_dia:,.0f} dias")

# Validação contra a própria amostra: o modelo prevê bem a taxa de estouro?
ultimos = x > 9500
taxa_obs = np.mean(y[ultimos] > LIMITE_GB)
taxa_prev = np.mean(prob_estouro(x[ultimos]))
print(f"\nValidação (dias 9.501–10.000):")
print(f"  taxa observada de estouro : {100 * taxa_obs:.2f}%")
print(f"  taxa prevista pelo modelo : {100 * taxa_prev:.2f}%")
# Previsto ≈ observado: o modelo normal com desvio s não só descreve a média,
# descreve também a CAUDA — que é exatamente o que a decisão usa.


# ==============================================================================
# PARTE D — Visualização da extrapolação com as duas bandas
# ==============================================================================
x_fut = np.linspace(1, x_estrela * 1.05, 600)
y_fut, erro_ic, erro_ip = intervalos(x_fut)

fig, axes = plt.subplots(1, 2, figsize=(15, 5.8))
for ax, (ini, fim, titulo) in zip(axes, [
    (1, x_estrela * 1.05, "Série completa + extrapolação"),
    (9000, x_estrela * 1.02, "Zoom na região de decisão"),
]):
    visivel = (x_fut >= ini) & (x_fut <= fim)
    obs = (x >= ini) & (x <= fim)
    ax.scatter(x[obs], y[obs], s=3, alpha=0.12, label="observações")
    ax.plot(x_fut[visivel], y_fut[visivel], color="red", lw=2, label="reta ajustada")
    ax.fill_between(x_fut[visivel], (y_fut - erro_ip)[visivel], (y_fut + erro_ip)[visivel],
                    color="red", alpha=0.13, label="intervalo de PREDIÇÃO 95%")
    ax.fill_between(x_fut[visivel], (y_fut - erro_ic)[visivel], (y_fut + erro_ic)[visivel],
                    color="darkred", alpha=0.45, label="intervalo de CONFIANÇA 95%")
    ax.axhline(LIMITE_GB, color="black", ls=":", lw=1.6, label=f"limite {LIMITE_GB} GB")
    ax.axvline(ultimo_dia, color="gray", ls="--", lw=1, label="fim dos dados")
    ax.axvline(x_risco, color="darkorange", lw=1.6, label=f"risco 5% (dia {x_risco:,.0f})")
    ax.axvline(x_estrela, color="purple", lw=1.6, label=f"tendência (dia {x_estrela:,.0f})")
    ax.set_xlabel("dia"); ax.set_ylabel("uso_disco_gb (GB)")
    ax.set_title(titulo)
axes[1].set_ylim(4000, 5600)
axes[0].legend(fontsize=7.5, loc="upper left")
fig.tight_layout()
fig.savefig(FIGURAS / "04_extrapolacao_bandas.png", dpi=150)


# ==============================================================================
# PARTE E — Resumo e recomendação (item 4.3 do enunciado)
# ==============================================================================
print("\n=== Resumo ===")
resumo = [
    ("Equação ajustada", f"ŷ = {beta0:.2f} + {beta1:.6f}·x"),
    ("Taxa de crescimento", f"{beta1:.4f} GB/dia ({beta1 * 30:.1f} GB/mês · {beta1 * 365:.0f} GB/ano)"),
    ("Erro típico diário (s)", f"{s_residual:.1f} GB"),
    ("Ocupação prevista no último dia", f"{beta0 + beta1 * ultimo_dia:,.1f} GB"),
    ("Dia em que a TENDÊNCIA atinge 5.000 GB", f"{x_estrela:,.0f}  ({dias_restantes:,.0f} dias de margem)"),
    ("Dia em que o RISCO (5%) atinge 5.000 GB", f"{x_risco:,.0f}  ({x_risco - ultimo_dia:,.0f} dias de margem)"),
    ("Dias da amostra já acima de 5.000 GB", f"{int(acima.sum())}"),
]
for rotulo, valor in resumo:
    print(f"  {rotulo:<42} {valor}")

# RECOMENDAÇÃO TÉCNICA:
#   1. A resposta direta ("861 dias") descreve a ocupação MÉDIA e superestima a
#      margem em mais de 30 vezes. A margem operacional real é de ~26 dias: é
#      quando passa a haver 5% de chance de uma leitura diária estourar o
#      limite — e 9 dias da amostra já estouraram.
#   2. Ação imediata: tratar como capacidade crítica AGORA. Com 26 dias de
#      margem, o prazo de compra/provisionamento de hardware provavelmente já
#      é maior que a margem.
#   3. Duas alavancas matematicamente diferentes:
#        - mudar o TETO (disco maior / migração): sobe a linha horizontal de
#          5.000 GB; a reta continua igual.
#        - mudar a INCLINAÇÃO (política de retenção / expurgo de logs): reduz
#          β̂₁ = 13,5 GB/mês; a reta fica mais deitada e todas as datas andam.
#      A primeira compra tempo uma vez; a segunda compra tempo continuamente.
#   4. Hipótese declarada: a projeção assume que a tendência linear continua
#      depois do dia 10.000. Reavaliar o modelo periodicamente com os dados
#      novos.

plt.show()
