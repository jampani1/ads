"""
03_classificacao.py — Itens 6 e 7: limiar, curva logística e matriz de confusão
Atividade de IC: Classificação de entregas por Regressão Logística.

===============================================================================
MATEMÁTICA DA ETAPA — limiar, inversão e por que o ótimo é uma faixa
===============================================================================

A regressão devolve uma probabilidade. Classificar exige uma regra:

    ŷ = 1  se  p(x) ≥ t        ŷ = 0  caso contrário

ACURÁCIA É UMA ESCADA. Ela é uma contagem de acertos, então só muda quando t cruza a
probabilidade de algum pedido. Entre dois pedidos vizinhos nada muda. Consequências:

  1. Não adianta derivar: a função é constante por trechos, com derivada zero ou
     inexistente. Aqui não se otimiza, se ENUMERA.
  2. Com n pedidos existem no máximo n + 1 classificações diferentes. Testar os
     candidatos t = pᵢ cobre TODAS elas. Uma grade (0,01; 0,02; ...) não cobre: se
     o degrau ótimo for mais estreito que o passo, ela passa por cima dele.
  3. O máximo é sempre um INTERVALO de limiares, nunca um número. Qualquer t dentro
     dele dá a mesma classificação. Adotamos o ponto médio como convenção.

INVERSÃO DA LOGÍSTICA. A sigmoide é estritamente crescente quando β₁ > 0, logo tem
inversa. Para achar o x em que p(x) = t:

    t = 1 / (1 + e^(−Z))
    1/t − 1 = e^(−Z)
    Z = ln(t / (1 − t))                       ← o logit, de novo
    β₀ + β₁x* = ln(t / (1 − t))

    x* = ( ln(t / (1 − t)) − β₀ ) / β₁

Como p(x) é crescente, "p(x) ≥ t" e "x ≥ x*" são a MESMA regra. O modelo inteiro
vira uma linha de corte em horas. Com uma única variável, a fronteira de decisão de
uma regressão logística é sempre um ponto.

MATRIZ DE CONFUSÃO. Classe positiva = entrega na data correta (y = 1):

                      previsto 0     previsto 1
    observado 0          VN             FP
    observado 1          FN             VP

FP aqui é prometer no prazo o pedido que vai atrasar. FN é dar como atrasado o que
chegaria certo.

===============================================================================
"""

import matplotlib.pyplot as plt
import numpy as np

import comum
from comum import (COR_APOIO, COR_ATRASO, COR_CORRETA, COR_GRADE, COR_MODELO, FIGURAS,
                   MARCA_ATRASO, MARCA_CORRETA, br)

ajuste = comum.carregar_modulo("02_ajuste.py")
df, x, y = ajuste.df, ajuste.x, ajuste.y
n = len(y)


def classificar(p, t):
    """ŷ = 1 se p ≥ t."""
    return (p >= t).astype(int)


def varrer_limiares(p, y):
    """
    Enumera todas as classificações possíveis.

    Devolve (candidatos, acertos): candidatos são os pᵢ ordenados, mais um valor acima
    de 1 (a regra "ninguém é 1"). O candidato pᵢ representa o intervalo (pᵢ₋₁, pᵢ].
    """
    candidatos = np.r_[np.sort(np.unique(p)), 1.0 + 1e-9]
    acertos = np.array([(classificar(p, t) == y).sum() for t in candidatos])
    return candidatos, acertos


def faixa_otima(p, y):
    """Devolve (limite inferior aberto, limite superior fechado, acertos) do melhor degrau."""
    candidatos, acertos = varrer_limiares(p, y)
    i = int(np.argmax(acertos))
    assert (acertos == acertos[i]).sum() == 1, "mais de um degrau empatado: rever a convenção"
    inferior = candidatos[i - 1] if i > 0 else 0.0
    return inferior, candidatos[i], int(acertos[i])


def logit(t):
    """ln(t / (1 − t))."""
    return np.log(t / (1 - t))


def inverter(t, beta):
    """x* tal que p(x*) = t."""
    return (logit(t) - beta[0]) / beta[1]


def matriz_confusao(y, y_hat):
    """Devolve VN, FP, FN, VP."""
    vn = int(((y == 0) & (y_hat == 0)).sum())
    fp = int(((y == 0) & (y_hat == 1)).sum())
    fn = int(((y == 1) & (y_hat == 0)).sum())
    vp = int(((y == 1) & (y_hat == 1)).sum())
    return vn, fp, fn, vp


# Resultado usado também pela Etapa 8
beta, _ = ajuste.ajustar_newton(x, y)
p = ajuste.prever_p(x, beta)
t_inf, t_sup, acertos_max = faixa_otima(p, y)
LIMIAR = (t_inf + t_sup) / 2               # convenção: ponto médio do degrau ótimo
X_CORTE = inverter(LIMIAR, beta)
y_hat = classificar(p, LIMIAR)


if __name__ == "__main__":
    print("=== Item 6 — varredura de limiares ===")
    candidatos, acertos = varrer_limiares(p, y)
    print(f"{len(candidatos)} classificações possíveis para {n} pedidos")
    print(f"acertos em t = 0,5 : {(classificar(p, 0.5) == y).sum()}/{n}")
    print(f"melhor resultado   : {acertos_max}/{n} = {acertos_max / n:.4f}")
    print(f"degrau ótimo       : t ∈ ({t_inf:.4f}, {t_sup:.4f}]   largura {t_sup - t_inf:.4f}")

    print("\n=== Item 6 — a grade passa por cima do degrau? ===")
    for passo in [0.1, 0.05, 0.01, 0.005, 0.001]:
        grade = np.round(np.arange(0, 1 + passo / 2, passo), 6)
        a = np.array([(classificar(p, t) == y).sum() for t in grade])
        print(f"passo {passo:<6}: melhor {a.max()}/{n}")

    print("\n=== Item 6 — limiar adotado e inversão ===")
    print(f"t* = ponto médio do degrau = {LIMIAR:.4f}")
    print(f"logit(t*) = {logit(LIMIAR):.4f}")
    print(f"x* = (logit(t*) − β₀)/β₁ = {X_CORTE:.3f} h")
    x_inf, x_sup = inverter(t_inf, beta), inverter(t_sup, beta)
    print(f"o degrau em horas: x* ∈ ({x_inf:.3f}, {x_sup:.3f}]")
    assert np.isclose(ajuste.prever_p(X_CORTE, beta), LIMIAR)     # ida e volta
    assert np.array_equal(y_hat, (x >= X_CORTE).astype(int))      # p ≥ t  ⇔  x ≥ x*
    print("conferido: p(x*) = t*  e  'p ≥ t*' classifica igual a 'x ≥ x*'")

    x_05 = inverter(0.5, beta)
    mudou = classificar(p, 0.5) != y_hat
    print(f"\nem t = 0,5 o corte seria x = {x_05:.3f} h; muda só o pedido:")
    print(df.assign(p=p.round(4))[mudou].to_string(index=False))

    # --- item 7 -------------------------------------------------------------------
    vn, fp, fn, vp = matriz_confusao(y, y_hat)
    assert vn + fp + fn + vp == n
    print("\n=== Item 7 — matriz de confusão ===")
    print(f"{'':>14}{'previsto 0':>12}{'previsto 1':>12}")
    print(f"{'observado 0':>14}{vn:>12}{fp:>12}")
    print(f"{'observado 1':>14}{fn:>12}{vp:>12}")
    try:
        from sklearn.metrics import confusion_matrix
        assert confusion_matrix(y, y_hat).tolist() == [[vn, fp], [fn, vp]]
        print("conferida com sklearn.metrics.confusion_matrix")
    except ImportError:
        print("scikit-learn indisponível: conferência pulada")

    print("\nOs erros:")
    erros = df.assign(p=p.round(3), previsto=y_hat)[y_hat != y].sort_values("x")
    print(erros.to_string(index=False))

    # --- figura: curva logística ---------------------------------------------------
    grade = np.linspace(0, 24, 400)
    fig, ax = plt.subplots(figsize=(8, 5))
    for classe, nome, cor, marca in [(1, "Na data correta", COR_CORRETA, MARCA_CORRETA),
                                     (0, "Com atraso", COR_ATRASO, MARCA_ATRASO)]:
        sel = y == classe
        ax.scatter(x[sel], y[sel], s=60, color=cor, marker=marca, alpha=0.8,
                   edgecolor="white", linewidth=0.8, label=nome, zorder=3)
    ax.plot(grade, ajuste.prever_p(grade, beta), color=COR_MODELO, linewidth=2.2, label="p(x) ajustada")
    ax.axhline(LIMIAR, color=COR_APOIO, linewidth=1.2, linestyle=":")
    ax.axvline(X_CORTE, color=COR_APOIO, linewidth=1.5, linestyle="--")
    ax.annotate(f"t* = {br(LIMIAR, 3)}\nx* = {br(X_CORTE)} h",
                xy=(X_CORTE, LIMIAR), xytext=(14.2, 0.26), color=COR_MODELO, fontsize=13,
                arrowprops=dict(arrowstyle="-", color=COR_APOIO))
    ax.set_xlim(0, 24)
    ax.set_ylim(-0.06, 1.06)
    ax.yaxis.set_major_formatter(comum.virgula(1))
    ax.set_xlabel("Antecedência do despacho (horas)")
    ax.set_ylabel("Probabilidade de entrega correta")
    ax.set_title("Função logística ajustada e limiar ótimo")
    ax.legend(loc="center left", bbox_to_anchor=(0.0, 0.72))
    fig.savefig(FIGURAS / "03_curva_logistica.png")
    plt.close(fig)

    # --- figura: acurácia por limiar ------------------------------------------------
    ts = np.linspace(0, 1, 4001)
    acc = np.array([(classificar(p, t) == y).mean() for t in ts])
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(8, 7.4), gridspec_kw={"hspace": 0.42})
    a1.step(ts, acc, where="post", color=COR_MODELO, linewidth=2)
    a1.axhline(y.mean(), color=COR_APOIO, linewidth=1.2, linestyle=":")
    a1.text(0.015, y.mean() - 0.018, "sempre prever 'correta'", ha="left", va="top",
            color=COR_APOIO, fontsize=12)
    a1.axvspan(0.4, 0.56, color=COR_GRADE, zorder=0)
    a1.set_title("A acurácia é uma escada")
    a1.set_xlabel("Limiar t")
    a1.set_ylabel("Acurácia")
    a1.set_xlim(0, 1)
    a1.xaxis.set_major_formatter(comum.virgula(1))
    a1.yaxis.set_major_formatter(comum.virgula(2))

    zoom = (ts >= 0.40) & (ts <= 0.56)
    a2.step(ts[zoom], acc[zoom] * n, where="post", color=COR_MODELO, linewidth=2)
    grade01 = np.round(np.arange(0.40, 0.561, 0.01), 2)
    a2.scatter(grade01, [(classificar(p, t) == y).sum() for t in grade01], s=52, color=COR_ATRASO,
               marker=MARCA_ATRASO, zorder=4, label="Grade de 0,01 em 0,01")
    a2.axvspan(t_inf, t_sup, color=COR_CORRETA, alpha=0.3, zorder=0)
    a2.scatter([LIMIAR], [acertos_max], s=170, marker="*", color=COR_CORRETA, zorder=5,
               label=f"Limiar adotado ({acertos_max} acertos)")
    a2.set_title("De perto: a grade não enxerga o degrau")
    a2.set_xlabel("Limiar t")
    a2.set_ylabel("Acertos (de 42)")
    a2.set_ylim(acertos_max - 5.5, acertos_max + 1)
    a2.xaxis.set_major_formatter(comum.virgula(2))
    a2.legend(loc="lower left")
    fig.savefig(FIGURAS / "03_acuracia_por_limiar.png")
    plt.close(fig)

    # --- figura: matriz de confusão -------------------------------------------------
    M = np.array([[vn, fp], [fn, vp]])
    rotulos = [["VN", "FP"], ["FN", "VP"]]
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.imshow(M, cmap="Blues", vmin=0, vmax=M.max() * 1.6)
    for i in range(2):
        for j in range(2):
            ax.text(j, i - 0.08, str(M[i, j]), ha="center", va="center", fontsize=30,
                    fontweight="bold", color=COR_MODELO)
            ax.text(j, i + 0.24, rotulos[i][j], ha="center", va="center", fontsize=13, color=COR_MODELO)
    ax.set_xticks([0, 1], ["Atraso", "Correta"])
    ax.set_yticks([0, 1], ["Atraso", "Correta"])
    ax.set_xlabel("Previsto")
    ax.set_ylabel("Observado")
    ax.grid(False)
    ax.tick_params(length=0)
    for lado in ax.spines.values():
        lado.set_visible(False)
    ax.set_title(f"Matriz de confusão em t* = {br(LIMIAR, 3)}")
    fig.savefig(FIGURAS / "03_matriz_confusao.png")
    plt.close(fig)

    print(f"\nFiguras salvas em {FIGURAS.name}/")
